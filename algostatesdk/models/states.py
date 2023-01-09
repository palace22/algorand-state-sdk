from dataclasses import dataclass
from typing import Literal, List, Optional


@dataclass
class Value:
    bytes: str
    type: int
    uint: int


@dataclass
class State:
    key: str
    value: Value


@dataclass
class AttributeCustom:
    type: Literal["int", "str", "addr", "bytes"]
    size: int
    offset: int
    name: str


@dataclass
class StateCustom:
    attrs: List[AttributeCustom]
    key: Optional[str | int] = None
    address: Optional[str] = None
    key_byte_length: Optional[int] = None
    is_box: Optional[bool] = None
