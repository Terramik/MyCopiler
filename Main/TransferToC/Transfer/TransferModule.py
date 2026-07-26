from .Simple import *
from .TransferExpression import transfer_expression
from .TransferGlobal import transfer_global


__all__ = ('transfer_modules',)


def write_exports(module: Module, f: TextIO, data: DataContainer):
    for exp in module.export_:
        if isinstance(exp.thing, TokenOperatorVariableDefinition):
            f.write(
                f'extern {data.type_to_name[exp.thing.type]} {exp.thing.name};\n'
            )


def write_import(module: Module, f: TextIO, data: DataContainer, dest_path: Path):
    for mod in module.imported_modules:
        if mod.is_std:
            # просто имя .h
            f.write(
                f'#include "{mod.transfer_path.as_posix()}_our.h"\n'
            )
        else:
            # считаем относительность

            # path_to = mod.transfer_path.relative_to(module.transfer_path.parent, walk_up=True)
            f.write(
                f'#include "{(mod.path_h.relative_to(module.path_h.parent, walk_up=True)).as_posix()}"\n'
            )


def transfer_module(module: Module, dest_path: Path, data: DataContainer):
    if module.is_std:
        return

    # print(dest_path)

    module.path_c.parent.mkdir(exist_ok=True, parents=True)
    module.path_h.parent.mkdir(exist_ok=True, parents=True)
    depth = len(module.relative_path.parents) - 1

    # .c
    with open(module.path_c, 'w') as f_c:
        # берём .h модуля из соседней ветви
        f_c.write(f'''
#include "{module.path_h.relative_to(module.path_c.parent, walk_up=True).as_posix()}"
''')
        # собственно сам код
        transfer_global(module, f_c, data)

    # .h
    with open(module.path_h, 'w') as f_h:
        i = abs(hash(module.path_h))
        # берём base
        f_h.write(f'''
#ifndef FILE_{i}_H
#define FILE_{i}_H
#include "{'../' * depth}project_base.h"

''')
        # импорты для нашего .с
        write_import(module, f_h, data, dest_path)
        # экспорты
        write_exports(module, f_h, data)
        # есть штука для инициализации переменных, добавим её
        if module.global_variables_initializer is not None:
            f_h.write(f'void {module.global_variables_initializer}();')

        # ВРЕМЯ ДЛЯ КОСТЫЛЕЙ (нужно добавить main сюда)
        if module.is_main:
            is_main_in_here = False
            for exp in module.export_:
                if isinstance(exp.thing, TokenOperatorVariableDefinition):
                    if exp.thing.name == 'not_very_main':
                        is_main_in_here = True
                        break
            if not is_main_in_here:
                main = module.scope.find_function_in_cur_scope('not_very_main')
                assert main is not None
                f_h.write(f'extern {data.type_to_name[main.var.type]} not_very_main;\n')

        # конец
        f_h.write('''
#endif
''')


def transfer_modules(module: list[Module], dest_path: Path, data: DataContainer):
    module = module[:]
    while module:
        mod = module.pop()
        module.extend(mod.imported_modules)
        transfer_module(mod, dest_path, data)

