from .Simple import *
from .Types.Simple import IteratorModule
from .STDModules import get_path_to_std_lib, get_path_to_std_header
import subprocess


__all__ = ('compile_',)


class ItModule(IteratorModule):
    """
    Должен собрать все импользуемые std модули
    """
    def __init__(self):
        self.all_std: set[str] = set()
        self.all_paths: list[str] = []

    def on_module(self, module: Module):
        if module.is_std:
            self.all_std.add(module.transfer_path.name)
        else:
            self.all_paths.append(
                module.path_c.as_posix()
            )
        super().on_module(module)


def compile_(modules: list[Module], for_c_path: Path, result_path: Path, compiler: str):
    """
    Компилирует штуку
    """
    it_module = ItModule()
    it_module.many_modules(modules)

    result = subprocess.run(
        [
            compiler, f'-I{get_path_to_std_header()}', '-O2',
            (for_c_path / 'src/main.c').as_posix(), get_path_to_std_lib(),
            *(p for p in it_module.all_paths),
            '-o',
            result_path.as_posix(),
            '-mconsole'
        ], capture_output=True, text=True
    )

    if result.returncode != 0:
        raise ValueError(f'Критическая ошибка при компиляции: \n{result.stderr}')

