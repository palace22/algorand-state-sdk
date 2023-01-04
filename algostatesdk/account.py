import json

from algosdk.v2client.algod import AlgodClient
from dacite import from_dict

from algostatesdk.models.asset import AccountAssetInfo


class Account:
    def __init__(self, algod_client: AlgodClient):
        self.algod_client = algod_client

    def raw_asset_balance(self, address: str, asset_id: int) -> int:
        from pprint import pprint

        res = json.dumps(self.algod_client.account_asset_info(address, asset_id)).replace("-", "_")  # TODO
        acc_asset_holding = from_dict(AccountAssetInfo, json.loads(res))
        return acc_asset_holding.asset_holding.amount

    def asset_balance(self, address: str, asset_id: int) -> float:
        decimals = self.algod_client.asset_info(asset_id)["params"]["decimals"]
        raw_balance = self.raw_asset_balance(address, asset_id)
        return raw_balance / 10**decimals
