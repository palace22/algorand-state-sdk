from dataclasses import dataclass
from typing import List
from algostatesdk.models.states import State
from typing import Optional


@dataclass
class Params:
    approval_program: str
    clear_state_program: str
    creator: str
    extra_program_pages: Optional[int]
    global_state: List[State]


@dataclass
class Application:
    id: int
    params: Params


@dataclass
class AppLocalStateParam:
    id: int
    key_value: List[State]


@dataclass
class ApplicationLocalState:
    app_local_state: AppLocalStateParam
