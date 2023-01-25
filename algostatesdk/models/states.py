from dataclasses import dataclass
from enum import Enum
from typing import List, Literal, Optional


@dataclass
class Value:
    bytes: str
    type: int
    uint: int


@dataclass
class State:
    key: str
    value: Value


class AttributeType(Enum):
    INT = "int"
    STR = "str"
    ADDR = "addr"
    BYTES = "bytes"


@dataclass
class AttributeSchema:
    type: Literal[AttributeType.INT, AttributeType.STR, AttributeType.ADDR, AttributeType.BYTES]
    size: int
    offset: int
    name: str


class StateType(Enum):
    LOCAL = "local"
    GLOBAL = "global"
    BOX = "box"


@dataclass
class StateSchema:
    attrs: List[AttributeSchema]
    type: Literal[StateType.GLOBAL, StateType.LOCAL, StateType.BOX]
    key: Optional[str | int] = None
    address: Optional[str] = None
    key_byte_length: Optional[int] = None
