from .Simple import *
from ..Types.Simple import IteratorControl
from .TransferExpression import transfer_expression
from .TransferControls import transfer_control


class ItCont(IteratorControl):
    def __init__(self, all: list):
        self.all = all

    def on_func_def(self, func_def: ControlFunctionDefinition):
        super().on_func_def(func_def)
        self.all.append(func_def)


def transfer_func(file: TextIO, func: ControlFunctionDefinition, data: DataContainer):
    """
    Переводит локальную функцию. Также добавляет замыкание для использования внешних переменных.
    """
    func_type = func.var.type

    # собираем все внешние переменные
    unique_outer_vars = []
    for var in func.outer_variables_inner:
        if var not in unique_outer_vars:
            unique_outer_vars.append(var)
    for var in func.outer_variables:
        if var not in unique_outer_vars:
            unique_outer_vars.append(var)
    func.outer_variables_all = unique_outer_vars

    # внешние переменные есть, сделаем структуру для замыкания
    if unique_outer_vars:
        env_name = get_unique_name(data.all_names,
                                   f'{func.name}env')

        # структура тут, т.к. она локальная для функции в это файле, и выходить наружу не должна.
        file.write(
            'typedef struct {'
                f'{
                    ''.join(
                        f'{data.type_to_name[var.type]}* {var.name};'
                        for var in unique_outer_vars
                    )
                }'
            '}' f'{env_name};\n'
        )

        func.enclosure_struct_name = env_name

    func.global_name = get_unique_name(data.all_names,
                                       f'{func.name}g')

    # делаем объявление функции
    file.write(
        f'{data.type_func_to_result_type[func_type]} {func.global_name}('
            f'{
                # обычные параметры
                f'{
                    ','.join(
                        transfer_expression(par, data)
                        for par in func.parameters
                    )
                }'
                # запятая, если есть обычные
                f'{
                    ',' if func.parameters else ''
                }' 
                # указатель на окружение(внешние переменные)
                'void* _env' 
            }' 
        ')'
    )
    if unique_outer_vars or func.is_class_init:
        file.write('{')
        # если есть замыкание, то получаем его
        if unique_outer_vars:
            file.write(f'{env_name}* env = ({env_name}*)_env;')
        # создадим пустую структуры-экземпляр
        if func.is_class_init:
            file.write(
                # мы делаем так, т.к. это - __init__ и его результат - именно то что нужно
                f'{data.type_to_name[func.var.type.simple.results[0]]} {func.is_class_init} = '
                f'({data.type_to_name[func.var.type.simple.results[0]]})' '{};' # создаём пустую структуру
            )

    # и её код блока
    transfer_control(func.code_block, file, data)

    if unique_outer_vars or func.is_class_init:
        file.write(
            '}'
        )


def transfer_local_functions(file: TextIO, thing: ControlFunctionDefinition | ControlClass, data: DataContainer):
    """
    Генерирует локальные функции для глобальной функции или класса.
    """
    it_control = ItCont([])
    if isinstance(thing, ControlFunctionDefinition):
        it_control(thing.code_block)
    else:
        it_control(thing.rest)
    local_funcs = it_control.all

    for local in local_funcs:
        transfer_func(file, local, data)





