from .Utils import *
from ..Types import *
from ..Simple import *
from .CollectAllNames import collect_all_names
from ..Transfer.TransferExpression import transfer_expression
from ..Types.Simple import TransferSlicingData
from ....Definitions import TypesShortener as types
from pathlib import Path
from typing import TextIO
import pickle


__all__ = ('retransfer_str_modules',)


def transfer_f(f_h: TextIO, f_c: TextIO, func: ControlFunctionDefinition, realisation: dict[str, str], data: DataContainer, initializers: list[str]):

    func.global_name = get_unique_name(data.all_names, f'{func.name}g')
    f_type = func.var.type

    f_h.write(
        f'extern {data.type_func_to_enclosure_struct[f_type]} {func.name};\n' # просто внешняя переменная
    )

    # переменная, её функция и присвоение
    f_c.write(f'''
{data.type_func_to_enclosure_struct[f_type]} {func.name};   
{data.type_func_to_result_type[f_type]} {func.global_name}({
    f'{', '.join(
        f'{transfer_expression(var, data)}'
        for var in func.parameters
    )}'
    f'{
        ',' if func.parameters else ''
    }'
    f'void* _par'
}){{
    {realisation[func.name]}
}}
{data.type_func_to_enclosure_struct[f_type]} {func.name} = ({data.type_func_to_enclosure_struct[f_type]}){{{func.global_name}, NULL}};

''')


def transfer_exp(f_h: TextIO, f_c: TextIO, exp: ControlExpression, realisation: dict[str, str], data: DataContainer, initializers: list[str]):
    assert isinstance(exp.first, TokenOperatorVariableDefinition)
    var = exp.first

    f_h.write(f'extern {data.type_to_name[var.type]} {var.name};\n')

    f_c.write(f'{data.type_to_name[var.type]} {var.name};\n')

    initializers.append(f'{var.name} = {realisation[var.name]};\n')


def transfer_cls_f(f_h: TextIO, f_c: TextIO, cls_name: str, func: ControlFunctionDefinition, realisation: dict[str, str], data: DataContainer, initializers: list[str]):

    func.global_name = get_unique_name(data.all_names, f'{func.name}g')
    f_type = func.var.type

    # просто сама функция
    f_c.write(f'''
    {data.type_func_to_result_type[f_type]} {func.global_name}({
    f'{', '.join(
        f'{transfer_expression(var, data)}'
        for var in func.parameters
    )}'
    f'{
    ',' if func.parameters else ''
    }'
    f'void* _par'
    }){{
        {realisation[(cls_name, func.name)]}
    }}'''
    )


def transfer_cls(f_h: TextIO, f_c: TextIO, cls: ControlClass, realisation: dict[str, str], data: DataContainer, initializers: list[str]):

    f_h.write(f'extern {data.type_to_name[cls.class_var.type]} {cls.name};\n')

    def t(thing: ControlFunctionDefinition | ControlExpression | ControlABC) -> str:
        if isinstance(thing, ControlFunctionDefinition):
            return f'.{thing.name} = {thing.global_name}'
        elif isinstance(thing, ControlExpression):
            assert isinstance(thing.first, TokenOperatorVariableDefinition)
            var = thing.first

            return f'.{var.name} = {realisation[var.name]}'
        else:
            raise ValueError()

    f_c.write(f'{data.type_to_name[cls.class_var.type]} {cls.name};\n')

    initializers.append(f'''
    {cls.name} = ({data.type_to_name[cls.class_var.type]}){{
        {','.join(
            t(thing) 
            for thing in cls.rest.block_parts
        )}
    }};\n
    ''')


def write_module(name: str, mod: Module, path: Path, data: DataContainer):
    realization = std_realization[name]
    initializers: list[str] = []

    with open((path / 'include' / f'{name}_our').with_suffix('.h'), 'w') as f_h:
        with open((path / 'src' / f'{name}_our').with_suffix('.c'), 'w') as f_c:
            f_h.write(f'''
#ifndef {name.upper()}_OUR_H
#define {name.upper()}_OUR_H

#include "base.h"

void vars_initializer_{name}();
            
''')

            def initializers_final(module: Module, file: TextIO, data: DataContainer, initializers: list[str]):
                # у глобальных переменных(и классов, и т.д.) есть штуки для инициализации,
                # создадим специальную функцию чтобы их собственно применить
                if initializers:
                    module.global_variables_initializer = get_unique_name(data.all_names, 'vars_initializer')


            f_c.write('''
#include "../include/base.h"
''')
            f_c.write(std_headers[name])

            for thing in mod.code.block_parts:
                if isinstance(thing, ControlFunctionDefinition):
                    transfer_f(f_h, f_c, thing, realization, data, initializers)
                elif isinstance(thing, ControlExpression):
                    transfer_exp(f_h, f_c, thing, realization, data, initializers)
                elif isinstance(thing, ControlClass):
                    for r in thing.rest.block_parts:
                        if isinstance(r, ControlFunctionDefinition):
                            transfer_cls_f(f_h, f_c, thing.name, r, realization, data, initializers)
                    transfer_cls(f_h, f_c, thing, realization, data, initializers)
                else:
                    raise ValueError('')

            # и инициализатор
            f_c.write(
                f'void vars_initializer_{name}()''{'
                    f'{
                        ''.join(initializers)
                    }'
                '}'
            )

            f_h.write('''
#endif
''')


def retransfer_str_modules():
    all_std_modules = [m for m in std_modules.values()]
    data = DataContainer()
    all_types = collect_all_types(all_std_modules)

    # добавим базовый типы
    data.type_to_name = {
        types.bool: 'bool',
        types.int8: 'int8_t',
        types.int16: 'int16_t',
        types.int32: 'int32_t',
        types.int64: 'int64_t',
        types.uint8: 'uint8_t',
        types.uint16: 'uint16_t',
        types.uint32: 'uint32_t',
        types.uint64: 'uint64_t',
        types.float32: 'float',
        types.float64: 'double',
    }
    # строка и прочее
    all_types.update((
        types.str,
        types.bool,
        types.int8,
        types.int16,
        types.int32,
        types.int64,
        types.uint8,
        types.uint16,
        types.uint32,
        types.uint64,
        types.float32,
        types.float64,
    ))

    all_slices = collect_slicing_functions(all_std_modules)
    collect_all_names(all_std_modules, data) # соберём все имена

    file_path = Path(__file__).parent / 'realization'

    with open(file_path / 'include/base.h', 'w') as f:
        f.write('''
#ifndef PROJECT_BASE_H
#define PROJECT_BASE_H

#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

''')

        transfer_all_types(f, all_types, data)
        f.write( # функция для генерации наших строк(срезов) из обычных
            f'static inline {data.type_to_name[types.str]} c_str_to_slise(char* str, size_t len)' '{'
                f'return ({data.type_to_name[types.str]})' '{'
                    f'({data.type_to_name[types.char]}*)str, len'
                '};'
            '}'
        )
        make_slicing_functions(f, data, all_slices)

        f.write('''
        
#endif

''')
    for name, std in std_modules.items():
        write_module(name, std, file_path, data)

    with open(file_path / '../pickle_things/all_types.pkl', 'wb') as f:
        pickle.dump(all_types,  f)
    with open(file_path / '../pickle_things/all_slices.pkl', 'wb') as f:
        pickle.dump(all_slices, f)
    with open(file_path / '../pickle_things/data.pkl', 'wb') as f:
        pickle.dump(data, f)

# retransfer_str_modules()