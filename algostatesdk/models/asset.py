from dataclasses import dataclass
from typing import Optional


@dataclass
class AssetParams:
    creator: str
    decimals: int
    default_frozen: bool
    reserve: str
    total: int
    name: Optional[str] = None
    name_b64: Optional[str] = None
    unit_name: Optional[str] = None
    unit_name_b64: Optional[str] = None
    url: Optional[str] = None
    url_b64: Optional[str] = None
    freeze: Optional[str] = None
    manager: Optional[str] = None
    clawback: Optional[str] = None


@dataclass
class AssetInfo:
    index: int
    params: AssetParams
