from dataclasses import dataclass


@dataclass
class AssetHolding:
    amount: int
    asset_id: int
    is_frozen: bool


@dataclass
class AccountAssetInfo:
    asset_holding: AssetHolding
    round: int
