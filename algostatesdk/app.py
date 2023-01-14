import base64
import json
from typing import List

from algosdk.encoding import encode_address
from algosdk.v2client.algod import AlgodClient
from dacite import from_dict

from algostatesdk import exceptions
from algostatesdk.models.app import *
from algostatesdk.models.states import State, StateSchema, Value, StateType, AttributeType


class App:
    def __init__(self, algod_client: AlgodClient):
        self.algod_client = algod_client

    def get_app(self, app_id: int) -> Application:
        res = json.dumps(self.algod_client.application_info(app_id)).replace("-", "_")  # TODO
        return from_dict(Application, json.loads(res))

    def get_global_states(self, app_id: int) -> List[State]:
        return self.get_app(app_id).params.global_state

    def get_local_states(self, address: str, app_id: int) -> List[State]:
        try:
            res = json.dumps(self.algod_client.account_application_info(address, app_id)).replace("-", "_")  # TODO
            return from_dict(ApplicationLocalState, json.loads(res)).app_local_state.key_value
        except:
            raise exceptions.NoLocalStatesFound(app_id, address)

    def get_byte_key(self, key: str | int, key_byte_length: int = 8):
        return bytes(key, "utf-8") if type(key) == str else key.to_bytes(key_byte_length, "big")

    def get_box_state(self, app_id: int, key: str | int | bytes, key_byte_length: int = None) -> State:
        byte_key = key if type(key) is bytes else self.get_byte_key(key, key_byte_length)
        try:
            box = self.algod_client.application_box_by_name(app_id, byte_key)
        except:
            raise exceptions.NoBoxFound(app_id, key)
        return State(box["name"], Value(box["value"], 1, 0))

    def get_state(
        self, app_id: int, key: str | int | bytes, state_type: str, address: str = None, key_byte_length: int = None
    ) -> State:
        byte_key = key if type(key) is bytes else self.get_byte_key(key, key_byte_length)

        match state_type:
            case StateType.BOX:
                return self.get_box_state(app_id, byte_key)
            case StateType.GLOBAL:
                states = self.get_global_states(app_id)
            case StateType.LOCAL:
                states = self.get_local_states(address, app_id)

        state = next(filter(lambda state: base64.b64decode(state.key) == byte_key, states), None)

        if state:
            return state
        if state_type == StateType.GLOBAL:
            raise exceptions.NoGlobalStateMatch(app_id, str(byte_key))
        raise exceptions.NoLocalStateMatch(str(byte_key), app_id, address)

    def extract_state_bytes(self, state: State, offset: int = None, size: int = None) -> bytes:
        value_bytes = base64.b64decode(state.value.bytes)
        return value_bytes if offset is None else value_bytes[offset : offset + size]

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
        key_byte_length: int = 1,
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
        key_byte_length: int = 1,
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
        key_byte_length: int = 1,
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
        key_byte_length: int = 1,
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
