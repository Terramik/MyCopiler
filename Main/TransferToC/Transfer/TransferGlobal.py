from .Simple import *
from .TransferLocalFunctions import transfer_local_functions
from .TransferExpression import transfer_expression
from .TransferControls import transfer_control
from io import StringIO


__all__ = ('transfer_global',)



def initializers_final(module: Module, file: TextIO, data: DataContainer, initializers: list[str]):
    # у глобальных переменных(и классов, и т.д.) есть штуки для инициализации,
    # создадим специальную функцию чтобы их собственно применить
    if initializers:
        module.global_variables_initializer = get_unique_name(data.all_names, 'vars_initializer')
        file.write(
            f'void {module.global_variables_initializer}()''{'
                f'{
                    ''.join(initializers)
                }'
            '}'
            )

def on_expression(module: Module, exp: ControlExpression, file: TextIO, data: DataContainer, initializers: list[str]):
    # добавляем только объявления переменных(т.к. с нашими преобразованиями
    # сначала идут они, а потом полные выражения, но уже с обращениями)
    if isinstance(exp.first, TokenOperatorVariableDefinition):
        file.write(f'{transfer_expression(exp.first, data)};\n')
    # это уже обращения с инициализациями, мы добавим этот код в специальной функции к main
    else:
        initializers.append(
            f'{transfer_expression(exp.first, data)};\n'
        )


def on_function(func: ControlFunctionDefinition, file: TextIO, data: DataContainer):
    # добавляем локальные функции
    transfer_local_functions(file, func, data)

    func.global_name = get_unique_name(data.all_names,
                                       f'{func.name}g')

    file.write(
        # глобальная переменная-указатель на функцию
        f'{data.type_func_to_enclosure_struct[func.var.type]} {func.name};'
        # сама функций
        f'{data.type_func_to_result_type[func.var.type]} {func.global_name}('
            f'{
                # аргументы
                f'{
                    ', '.join(
                        transfer_expression(par, data)
                        for par in func.parameters
                    )
                }'
                # окружение
                f'{
                    ', ' if func.parameters else ''
                }'
                f'void* _par'
            }'
        ')'
    )
    # её блок кода
    transfer_control(func.code_block, file, data)
    # и делаем замыкание
    file.write(
        f'{data.type_func_to_enclosure_struct[func.var.type]} {func.name} = ('
            f'{data.type_func_to_enclosure_struct[func.var.type]}'
        '){'
            f'{func.global_name}, NULL'
        '};'
    )


def on_class(cls: ControlClass, file: TextIO, data: DataContainer, initializers: list[str]):
    # в самом коде просто объявление переменной класса

    file.write(
        f'{data.type_to_name[cls.class_var.type]} {cls.name} = '
        f'({data.type_to_name[cls.class_var.type]})' '{};'
    )

    # добавим локальных штук
    transfer_local_functions(file, cls, data)

    # а вот в инициализацию присвоим всё что нужно
    res = StringIO()

    # пишем код блока, чтобы инициализировать все нужные переменные
    transfer_control(cls.rest, res, data)
    res = res.getvalue()[:-1]  # чтобы убрать последний "}"

    initializers.append(
        f'{res}'
        # теперь, присвоим классу все полученные переменные
            f'{''.join(
                f'{cls.name}.{var.name} = {var.name};' # переменной класса переменную из блока кода
                for var in cls.class_field
            )}'
        # и конец
        '}'
    )


def transfer_global(module: Module, f: TextIO, data: DataContainer):
    initializers = []
    for thing in module.code.block_parts:
        if isinstance(thing, ControlExpression):
            on_expression(module, thing, f, data, initializers)
        elif isinstance(thing, ControlFunctionDefinition):
            on_function(thing, f, data)
        elif isinstance(thing, ControlClass):
            on_class(thing, f, data, initializers)

    initializers_final(module, f, data, initializers)
