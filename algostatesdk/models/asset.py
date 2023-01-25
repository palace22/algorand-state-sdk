from dataclasses import dataclass


@dataclass
class AssetParams:
    creator: str
    decimals: int
    default_frozen: bool
    freeze: str
    manager: str
    name: str
    name_b64: str
    reserve: str
    total: int
    unit_name: str
    unit_name_b64: str
    url: str
    url_b64: str


@dataclass
class AssetInfo:
    index: int
    params: AssetParams
