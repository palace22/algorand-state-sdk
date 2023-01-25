import json
from typing import List

from algosdk.v2client.algod import AlgodClient
from dacite import from_dict

from algostatesdk import exceptions
from algostatesdk.models.app import *
from algostatesdk.models.states import State, Value


class App:
    @staticmethod
    def info(algod_client: AlgodClient, app_id: int) -> Application:
        res = json.dumps(algod_client.application_info(app_id)).replace("-", "_")  # TODO
        return from_dict(Application, json.loads(res))

    @staticmethod
    def global_states(algod_client: AlgodClient, app_id: int) -> List[State]:
        return App.info(algod_client, app_id).params.global_state

    @staticmethod
    def local_states(algod_client: AlgodClient, address: str, app_id: int) -> List[State]:
        try:
            res = json.dumps(algod_client.account_application_info(address, app_id)).replace("-", "_")  # TODO
            return from_dict(ApplicationLocalState, json.loads(res)).app_local_state.key_value
        except:
            raise exceptions.NoLocalStatesFound(app_id, address)

    @staticmethod
    def get_byte_key(key: str | int, key_byte_length: int = 8):
        return bytes(key, "utf-8") if type(key) == str else key.to_bytes(key_byte_length, "big")

    @staticmethod
    def get_box_state(
        algod_client: AlgodClient, app_id: int, key: str | int | bytes, key_byte_length: int = None
    ) -> State:
        byte_key = key if type(key) is bytes else App.get_byte_key(key, key_byte_length)
        try:
            box = algod_client.application_box_by_name(app_id, byte_key)
        except:
            raise exceptions.NoBoxFound(app_id, key)
        return State(box["name"], Value(box["value"], 1, 0))
