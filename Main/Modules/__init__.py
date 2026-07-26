from .Utils import *
from .ProcessModule import get_module, process_module
from pathlib import Path
from ...Definitions.Tokens import zero_origin


__all__ = ('make_modules',)


def make_modules(
        enter_point: Path
) -> Module:
    main_module = get_module(enter_point, zero_origin)
    main_module.type = Module.Types.Main
    process_module(main_module, {})
    return main_module


