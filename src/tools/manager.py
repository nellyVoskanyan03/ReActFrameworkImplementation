from enum import Enum
from enum import auto
from typing import Callable


class ToolName(Enum):
    wikipedia = auto()
    google = auto()
    none = auto()

    def __str__(self) -> str:
        return self.name


class Tool:

    def __init__(self, name: ToolName, func: Callable[[str], str]):
        self.name = name
        self.func = func
