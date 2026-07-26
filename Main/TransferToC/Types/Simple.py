from typing import TextIO
from ....Definitions.TreeInterface import *
from ....Definitions.Scopes import *
from ....Definitions.Tokens import *
from ..Simple import get_unique_name, DataContainer
from ....Definitions.Modules import Module
from pathlib import Path


@dataclass(slots=True, frozen=True)
class TransferSlicingData:
    """
    Нужно для получения данных о том, какие функции для срезов генерировать
    """
    res_type: Type
    arg_type: Type
    pos_start_num: int
    dims_num: int
