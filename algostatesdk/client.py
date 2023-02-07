import base64

from algosdk.encoding import encode_address
from algosdk.v2client.algod import AlgodClient

from algostatesdk import exceptions
from algostatesdk.app import App
from algostatesdk.models.states import AttributeType, State, StateSchema, StateType


class AlgoStateClient:
    def __init__(self, algod_client: AlgodClient):
        self.algod_client = algod_client

    def get_state(
        self, app_id: int, key: str | int | bytes, state_type: str, address: str = None, key_byte_length: int = None
    ) -> State:
        byte_key = key if type(key) is bytes else App.get_byte_key(key, key_byte_length)
        match state_type:
            case StateType.BOX:
                return App.get_box_state(self.algod_client, app_id, byte_key)
            case StateType.GLOBAL:
                states = App.global_states(self.algod_client, app_id)
            case StateType.LOCAL:
                states = App.local_states(self.algod_client, address, app_id)
            case _:
                raise exceptions.WrongStateType(state_type)

        state = next(filter(lambda state: base64.b64decode(state.key) == byte_key, states), None)

        if state:
            return state
        if state_type == StateType.GLOBAL:
            raise exceptions.NoGlobalStateMatch(app_id, str(byte_key))
        raise exceptions.NoLocalStateMatch(str(byte_key), app_id, address)

    def extract_state_bytes(self, state: State, offset: int = None, size: int = None) -> bytes:
        value_bytes = base64.b64decode(state.value.bytes)
        return value_bytes if offset is None else value_bytes[offset : offset + size if size else None]

    def extract_state_int(self, state: State, offset: int = None, size: int = None) -> int:
        if state.value.type == 2:
            return state.value.uint
        value_bytes = base64.b64decode(state.value.bytes)
        return (
            int.from_bytes(value_bytes, "big")
            if offset is None
            else int.from_bytes(value_bytes[offset : offset + size], "big")
        )

    def extract_state_str(self, state: State, offset: int = None, size: int = None) -> str:
        value_bytes = base64.b64decode(state.value.bytes)
        value_bytes = value_bytes if offset is None else value_bytes[offset : offset + size]
        return value_bytes.decode("utf-8")

    def extract_state_addr(self, state: State, offset: int = None) -> str:
        value_bytes = base64.b64decode(state.value.bytes)
        value_bytes = value_bytes if offset is None else value_bytes[offset : offset + 32]
        return encode_address(value_bytes)

    def get_state_bytes_value(
        self,
        app_id: int,
        key: str | int,
        state_type: str,
        size: int = None,
        offset: int = None,
        address: str = None,
        key_byte_length: int = 8,
    ) -> bytes:
        state = self.get_state(app_id, key, state_type, address, key_byte_length)
        return self.extract_state_bytes(state, offset, size)

    def get_state_int_value(
        self,
        app_id: int,
        key: str | int,
        state_type: str,
        size: int = None,
        offset: int = None,
        address: str = None,
        key_byte_length: int = 8,
    ) -> int:
        state = self.get_state(app_id, key, state_type, address, key_byte_length)
        return self.extract_state_int(state, offset, size)

    def get_state_str_value(
        self,
        app_id: int,
        key: str | int,
        state_type: str,
        size: int = None,
        offset: int = None,
        address: str = None,
        key_byte_length: int = 8,
    ) -> str:
        state = self.get_state(app_id, key, state_type, address, key_byte_length)
        return self.extract_state_str(state, offset, size)

    def get_state_addr_value(
        self,
        app_id: int,
        key: str | int,
        state_type: str,
        offset: int = None,
        address: str = None,
        key_byte_length: int = 8,
    ) -> str:
        state = self.get_state(app_id, key, state_type, address, key_byte_length)
        return self.extract_state_addr(state, offset)

    def get_state_custom(self, app_id: int, sc: StateSchema) -> dict:
        state = self.get_state(app_id, sc.key, sc.type, sc.address, sc.key_byte_length)
        state_custom = {}
        for attr in sc.attrs:
            match attr.type:
                case AttributeType.STR:
                    state_custom[attr.name] = self.extract_state_str(state, attr.offset, attr.size)
                case AttributeType.INT:
                    state_custom[attr.name] = self.extract_state_int(state, attr.offset, attr.size)
                case AttributeType.BYTES:
                    state_custom[attr.name] = self.extract_state_bytes(state, attr.offset, attr.size)
                case AttributeType.ADDR:
                    state_custom[attr.name] = self.extract_state_addr(state, attr.offset)
                case _:
                    raise exceptions.WrongAttributeType(attr)
        return state_custom
