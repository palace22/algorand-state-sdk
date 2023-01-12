from dataclasses import dataclass
from typing import Literal, List, Optional
from enum import Enum


@dataclass
class Value:
    bytes: str
    type: int
    uint: int


@dataclass
class State:
    key: str
    value: Value


class AttributeCustomType(Enum):
    INT = "int"
    STR = "str"
    ADDR = "addr"
    BYTES = "bytes"


@dataclass
class AttributeCustom:
    type: Literal[AttributeCustomType.INT, AttributeCustomType.STR, AttributeCustomType.ADDR, AttributeCustomType.BYTES]
    size: int
    offset: int
    name: str


class StateCustomType(Enum):
    LOCAL = "local"
    GLOBAL = "global"
    BOX = "box"


@dataclass
class StateCustom:
    attrs: List[AttributeCustom]
    type: Literal[StateCustomType.GLOBAL, StateCustomType.LOCAL, StateCustomType.BOX]
    key: Optional[str | int] = None
    address: Optional[str] = None
    key_byte_length: Optional[int] = None
