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
    key: str | int
    key_byte_length: Optional[int]
    is_box: Optional[bool]
    address: str
    attrs: List[AttributeCustom]
