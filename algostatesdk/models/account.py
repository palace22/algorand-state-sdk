from dataclasses import dataclass
from typing import List

from algostatesdk.models.states import State


@dataclass
class AssetHolding:
    amount: int
    asset_id: int
    is_frozen: bool


@dataclass
class AccountAssetInfo:
    asset_holding: AssetHolding
    round: int


@dataclass
class Schema:
    num_byte_slice: int
    num_uint: int


@dataclass
class AccountAppLocalState:
    id: int
    key_value: List[State]
    schema: Schema


@dataclass
class AccountInfo:
    address: str
    amount: int
    amount_without_pending_rewards: int
    apps_local_state: List[AccountAppLocalState]
    apps_total_schema: Schema
    assets: List[AssetHolding]
    created_apps: List  # TODO
    created_assets: List  # TODO
    min_balance: int
    pending_rewards: int
    reward_base: int
    rewards: int
    round: int
    status: str
    total_apps_opted_in: int
    total_assets_opted_in: int
    total_created_apps: int
    total_created_assets: int
