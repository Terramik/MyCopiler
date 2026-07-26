from ....Definitions.TreeInterface import *
from ....Definitions.Scopes import *
from ....Definitions.Tokens import *
from ....Definitions.Modules import *
from ..Simple import *
from uuid import uuid4


def get_unique_name(all_names: set[str], name: str) -> str:
    if name in all_names:
        clean_name = name
        while name in all_names:
            name = f'{clean_name}_{uuid4().hex}'
    all_names.add(name)
    return name

