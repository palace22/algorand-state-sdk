import json

from algosdk.v2client.algod import AlgodClient
from dacite import from_dict

from algostatesdk.models.asset import AssetInfo


class Asset:
    @staticmethod
    def info(algod_client: AlgodClient, asset_id: int) -> AssetInfo:
        res = json.dumps(algod_client.asset_info(asset_id)).replace("-", "_")  # TODO
        return from_dict(AssetInfo, json.loads(res))
