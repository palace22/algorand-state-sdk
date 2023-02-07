from dataclasses import dataclass
from typing import  Optional


@dataclass
class AssetParams:
    creator: str
    decimals: int
    default_frozen: bool
    name: str
    name_b64: str
    reserve: str
    total: int
    unit_name: str
    unit_name_b64: str
    url: str
    url_b64: str
    freeze: Optional[str]=None
    manager: Optional[str]=None
    clawback: Optional[str]=None


@dataclass
class AssetInfo:
    index: int
    params: AssetParams
