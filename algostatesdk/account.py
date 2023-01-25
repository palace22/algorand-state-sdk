import json

from algosdk.v2client.algod import AlgodClient
from dacite import from_dict

from algostatesdk.asset import Asset
from algostatesdk.models.account import AccountAssetInfo, AccountInfo


class Account:
    @staticmethod
    def info(algod_client: AlgodClient, address: str) -> AccountInfo:
        res = json.dumps(algod_client.account_info(address)).replace("-", "_")  # TODO
        return from_dict(AccountInfo, json.loads(res))

    @staticmethod
    def asset_info(algod_client: AlgodClient, address: str, asset_id: int) -> AccountAssetInfo:
        res = json.dumps(algod_client.account_asset_info(address, asset_id)).replace("-", "_")  # TODO
        return from_dict(AccountAssetInfo, json.loads(res))

    @staticmethod
    def raw_asset_balance(algod_client: AlgodClient, address: str, asset_id: int) -> int:
        return Account.asset_info(algod_client, address, asset_id).asset_holding.amount

    @staticmethod
    def asset_balance(algod_client: AlgodClient, address: str, asset_id: int) -> float:
        decimals = Asset.info(algod_client, asset_id).params.decimals
        raw_balance = Account.raw_asset_balance(algod_client, address, asset_id)
        return raw_balance / 10**decimals

    @staticmethod
    def min_balance(algod_client: AlgodClient, address: str):
        return Account.info(algod_client, address).min_balance
