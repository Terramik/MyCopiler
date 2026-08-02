from .Utils import *
from .ProcessModule import get_module, process_module
from pathlib import Path
from ...Definitions.Tokens import zero_origin
from ...Definitions.Exceptions import SemanticError, OurSyntaxError


__all__ = ('make_modules', 'analyze_module')


def make_modules(
        enter_point: Path
) -> Module:
    main_module = get_module(enter_point, zero_origin)
    main_module.type = Module.Types.Main
    process_module(main_module, {})
    return main_module


def analyze_module(path: Path, processed_modules: dict[Path, Module]) -> tuple[bool, SemanticError | OurSyntaxError | None]:
    """
    Нужна для ls и анализа модулей вне полной компиляции. Также перехватит ошибку.
    """
    if path in processed_modules:
        del processed_modules[path]
    try:
        module = get_module(path, zero_origin)
        module.type = Module.Types.Usual
        process_module(module, processed_modules, True)
        processed_modules[path] = module
    except SemanticError as err:
        return True, err
    except OurSyntaxError as err:
        return True, err
    return False, None
