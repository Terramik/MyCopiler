import uuid
from .Utils import Module, IteratorModule
from .Utils import *


__all__ = ('rename_modules',)


all_forbidden_words = {
    # для трансляции
    'base', 'project_base', 'main',
    # std
    'io_our', 'mem_our', 'time_our', 'math_our', 'rand_our', 'testing_our',
}


class ItModule(IteratorModule):
    def __init__(self, forbidden_names: set[str]):
        self.forbidden_names = forbidden_names

    def on_module(self, module: Module):
        if not module.is_std and module.path_to_file.stem in self.forbidden_names:
            new_name = module.path_to_file.stem + uuid.uuid4().hex + module.path_to_file.suffix
            new_path = module.path_to_file.parent / new_name
            module.transfer_path = new_path
        else:
            module.transfer_path = module.path_to_file
        super().on_module(module)


def rename_modules(modules: Module | list[Module], data: DataContainer):
    """
    Переименовывает модули, чтобы они не трогали уникальные имена
    """
    it_module = ItModule(all_forbidden_words)
    it_module.many_modules(modules)
