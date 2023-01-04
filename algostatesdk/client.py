from algosdk.v2client.algod import AlgodClient

from algostatesdk.account import Account
from algostatesdk.app import App


class AlgoStateClient:
    def __init__(self, algod_token, algod_address, headers=None):
        self.algod_client = AlgodClient(algod_token, algod_address, headers)
        self.account: Account = Account(self.algod_client)
        self.app: App = App(self.algod_client)
