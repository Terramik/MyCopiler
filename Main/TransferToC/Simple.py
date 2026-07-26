from ...Definitions.Scopes import *
from ...Definitions.Tokens import *
from ...Definitions.Enums import *
from ...Definitions.Modules import *
from uuid import uuid4
from dataclasses import field
from pathlib import Path
from typing import TextIO


@dataclass(slots=True)
class DataContainer:
    modules: list[Module] = field(default_factory=lambda: [])
    type_to_name: dict[Type, str] = field(default_factory=lambda: {})
    type_to_indexing_func: dict[Type, str] = field(default_factory=lambda: {})
    type_to_slicing_func: dict[tuple[Type, Type], str] = field(default_factory=lambda: {})
    type_func_to_result_type: dict[Type, str] = field(default_factory=lambda: {})
    type_func_to_enclosure_struct: dict[Type, str] = field(default_factory=lambda: {})
    all_names: set[str] = field(default_factory=lambda: set())


def get_unique_name(all_names: set[str], name: str) -> str:
    if name in all_names:
        clean_name = name
        while name in all_names:
            name = f'{clean_name}_{uuid4().hex}'
    all_names.add(name)
    return name
