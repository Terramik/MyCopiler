from typing import TextIO
from .Types import *
from .Transforms import *
from .Transfer import *
from .STDModules import *
from .MakeMain import make_main
from .Compile import compile_
from .Types.Simple import IteratorModule

from ...Definitions.Scopes import *
from ...Definitions.Tokens import *
from ...Definitions.STDModules import *
from .Simple import *


__all__ = ('transfer',)


class CaclPaths(IteratorModule):
    def __init__(self, common: Path, dest_path: Path):
        self.common = common
        self.dest_path = dest_path

    def on_module(self, module: Module):
        if not module.is_std:
            module.relative_path = module.transfer_path.relative_to(self.common, walk_up=True)
            module.path_c = (self.dest_path / 'src' / module.relative_path).with_suffix('.c')
            module.path_h = (self.dest_path / 'include' / module.relative_path).with_suffix('.h')
        super().on_module(module)


class GetAllPaths(IteratorModule):
    def __init__(self):
        self.paths = []

    def on_module(self, module: Module):
        if not module.is_std:
            self.paths.append(module.transfer_path)
        super().on_module(module)


def set_paths(module: list[Module], dest_path: Path):
    paths = GetAllPaths()
    paths.many_modules(module)
    paths = paths.paths
    common = paths[0].parent
    while not all(p.is_relative_to(common) for p in paths):
        common = common.parent
    CaclPaths(common, dest_path).many_modules(module)


def transfer(module: Module | list[Module], result_path: Path, compiler: str):
    if isinstance(module, Module):
        module = [module]

    done_types, done_slices, data = load_std_data()

    # собираем все штуки и исключаем те, что уже есть
    all_types = collect_all_types(module)
    all_types = all_types - done_types
    all_slices = collect_slicing_functions(module)
    all_slices = all_slices - done_slices

    # избавляемся от коллизий в модулях
    rename_modules(module, data)
    rename_and_collect(module, data)

    # делаем базовую штуку для всего проекта
    base_path = result_path / 'include/project_base.h'
    base_path.parent.mkdir(exist_ok=True, parents=True)
    with open(base_path, 'w') as f:
        i = abs(hash(module[0].transfer_path))
        f.write(f'''
#ifndef PROJ_{i}_BASE_H
#define PROJ_{i}_BASE_H
#include "base.h"
''')

        transfer_all_types(f, all_types, data)
        make_slicing_functions(f, data, all_slices)
        change_funcs_types(data)

        f.write('''
#endif
''')

    # получаем относительные пути для трансляции
    set_paths(module, result_path)

    # обрабатываем модули
    connect_imports(module, data)
    decompose_multiple_assignment_expressions(module, data)
    move_all_vdef_to_beginning(module, data)
    turn_all_enums_to_constants(module, data)

    # транслируем
    transfer_modules(module, result_path, data)

    # и теперь main
    make_main(module, result_path)
    # и всё
    compile_(module, result_path, compiler)


