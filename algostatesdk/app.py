import base64
import json
from typing import List

from algosdk.encoding import encode_address
from algosdk.v2client.algod import AlgodClient
from dacite import from_dict

from algostatesdk import exceptions
from algostatesdk.models.app import *
from algostatesdk.models.states import State, StateCustom, Value


class App:
    def __init__(self, algod_client: AlgodClient):
        self.algod_client = algod_client

    def get_app(self, app_id: int) -> Application:
        res = json.dumps(self.algod_client.application_info(app_id)).replace("-", "_")  # TODO
        return from_dict(Application, json.loads(res))

    def get_app_local_state(self, address: str, app_id: int) -> ApplicationLocalState:
        try:
            res = json.dumps(self.algod_client.account_application_info(address, app_id)).replace("-", "_")  # TODO
            return from_dict(ApplicationLocalState, json.loads(res))
        except:
            raise exceptions.NoLocalStatesFound(app_id, address)

    def get_global_states(self, app_id: int) -> List[State]:
        return self.get_app(app_id).params.global_state

    def get_local_states(self, address: str, app_id: int) -> List[State]:
        return self.get_app_local_state(address, app_id).app_local_state.key_value

    def get_state(
        self,
        app_id: int,
        key: str | int,
        address: str = None,
        states: List[State] = None,
        key_byte_length: int = 1,
        is_box: bool = False,
    ) -> State:
        byte_key = bytes(key, "utf-8") if type(key) == str else key.to_bytes(key_byte_length, "big")
        if is_box:
            box = self.algod_client.application_box_by_name(app_id, byte_key)
            return State(box["name"], Value(box["value"], 0, 0))
        states = (
            states if states else self.get_local_states(address, app_id) if address else self.get_global_states(app_id)
        )
        state = next(filter(lambda gs: base64.b64decode(gs.key) == byte_key, states), None)
        if not state:
            raise exceptions.NoLocalStateMatch(key, app_id, address)
        return state

    def extract_state_bytes_value(
        self,
        app_id: int,
        key: str | int,
        address: str = None,
        state: State = None,
        key_byte_length: int = 1,
    ):
        state = state if state is not None else self.get_state(app_id, key, address, state, key_byte_length)
        return base64.b64decode(state.value.bytes)

    def get_state_bytes_value(
        self,
        app_id: int,
        key: str | int,
        size: int = None,
        offset: int = 0,
        address: str = None,
        state: State = None,
        key_byte_length: int = 1,
    ) -> bytes:
        gs_value_bytes = self.extract_state_bytes_value(app_id, key, address, state, key_byte_length)
        value = state.value.uint if not size else gs_value_bytes[offset : offset + size]
        return value

    def get_state_int_value(
        self,
        app_id: int,
        key: str | int,
        size: int = None,
        offset: int = 0,
        address: str = None,
        state: State = None,
        key_byte_length: int = 1,
    ) -> int:
        gs_value_bytes = self.extract_state_bytes_value(app_id, key, address, state, key_byte_length)
        state = self.get_state(app_id, key, address, state, key_byte_length) if not state else state
        value = state.value.uint if not size else int.from_bytes(gs_value_bytes[offset : offset + size], "big")
        return value

    def get_state_str_value(
        self,
        app_id: int,
        key: str | int,
        size: int = None,
        offset: int = 0,
        address: str = None,
        state: State = None,
        key_byte_length: int = 1,
    ) -> str:
        gs_value_bytes = self.extract_state_bytes_value(app_id, key, address, state, key_byte_length)
        value = gs_value_bytes if not size else gs_value_bytes[offset : offset + size]
        return value.decode("utf-8")

    def get_state_addr_value(
        self,
        app_id: int,
        key: str | int,
        offset: int = None,
        address: str = None,
        state: State = None,
        key_byte_length: int = 1,
    ) -> str:
        gs_value_bytes = self.extract_state_bytes_value(app_id, key, address, state, key_byte_length)
        value = gs_value_bytes if not offset else gs_value_bytes[offset : offset + 32]
        return encode_address(value)

    def get_state_custom(self, app_id: int, state_custom: StateCustom) -> dict:
        is_box = state_custom.is_box if hasattr(state_custom, "is_box") else None
        state, key, obj_custom = (
            self.get_state(app_id, state_custom.key, state_custom.address, None, state_custom.key_byte_length, is_box),
            state_custom.key,
            {},
        )
        for attr in state_custom.attrs:
            match attr.type:
                case "str":
                    obj_custom[attr.name] = self.get_state_str_value(
                        app_id, key, attr.size, attr.offset, state_custom.address, state
                    )
                case "int":
                    obj_custom[attr.name] = self.get_state_int_value(
                        app_id, key, attr.size, attr.offset, state_custom.address, state
                    )
                case "bytes":
                    obj_custom[attr.name] = self.get_state_bytes_value(
                        app_id, key, attr.size, attr.offset, state_custom.address, state
                    )
                case "addr":
                    obj_custom[attr.name] = self.get_state_addr_value(
                        app_id, key, attr.offset, state_custom.address, state
                    )
        return obj_custom
