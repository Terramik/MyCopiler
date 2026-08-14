from .Utils import *
from .ProcessModule import get_module, process_module
from pathlib import Path
from ...Definitions.Tokens import zero_origin
from ...Definitions.Exceptions import SemanticError, OurSyntaxError
from ...Definitions.TreeInterface import IteratorModule


__all__ = ('make_modules', 'analyze_module')


class ItMod(IteratorModule):
    def __init__(self):
        self.processed = set()
        self.errors = []

    def on_module(self, module: Module):
        if module.path_to_file in self.processed:
            return
        self.processed.add(module.path_to_file)
        self.errors.extend(module.errors)
        super().on_module(module)



def make_modules(
        enter_point: Path
) -> tuple[Module, list[SemanticError | OurSyntaxError]]:

    main_module = get_module(enter_point, zero_origin)
    main_module.type = Module.Types.Main
    process_module(main_module, {})

    it = ItMod()
    it.many_modules(main_module)
    return main_module, it.errors


def analyze_module(path: Path, processed_modules: dict[Path, Module]) -> Module:
    """
    Нужна для ls и анализа модулей вне полной компиляции.
    """
    if path in processed_modules:
        del processed_modules[path]

    module = get_module(path, zero_origin)
    module.type = Module.Types.Usual
    process_module(module, processed_modules, True)
    processed_modules[path] = module
    return module
