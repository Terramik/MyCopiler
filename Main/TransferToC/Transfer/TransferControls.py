from .Simple import *
from .TransferExpression import transfer_expression
from io import StringIO


__all__ = ('transfer_control',)


@singledispatch
def transfer_control(node: ControlABC, file: TextIO, data: DataContainer):
    raise NotImplementedError('Что-то пошло не так')


@transfer_control.register(ControlFunctionDefinition)
def _(node: ControlFunctionDefinition, file: TextIO, data: DataContainer):
    # так как это вызывается только в других функциях, и все функции уже
    # объявлены, пы просто скопируем их в переменную - указатель.

    # есть внешние перменные, делаем полноценное замыкание
    if node.outer_variables_all:
        temp_var_name = get_unique_name(data.all_names,
                                        f'{node.enclosure_struct_name}_ex')
        file.write(
            # делаем замыкание
            f'{node.enclosure_struct_name} {temp_var_name} = '
            f'({node.enclosure_struct_name})' '{'
                f'{
                    ''.join(
                        f'&({transfer_expression(
                            TokenVariableAccess(
                                '', zero_origin, False, var
                            ), 
                            data)})'
                        for var in node.outer_variables_all
                    )
                }'
            '};'
            # и теперь сама функция
            f'{data.type_func_to_enclosure_struct[node.var.type]} {node.var.name} = '
            f'({data.type_func_to_enclosure_struct[node.var.type]})' '{' f'{node.global_name}, &{temp_var_name} ' '};'
        )
    # замыкания нет, просто функция и null
    else:
        file.write(
            f'{data.type_func_to_enclosure_struct[node.var.type]} {node.var.name} = '
            f'({data.type_func_to_enclosure_struct[node.var.type]})' '{' f'{node.global_name}' ', NULL};'
        )


@transfer_control.register(ControlExpression)
def _(node: ControlExpression, file: TextIO, data: DataContainer):
    file.write(transfer_expression(node.first, data))
    file.write(f';\n')


@transfer_control.register(ControlReturn)
def _(node: ControlReturn, file: TextIO, data: DataContainer):
    if len(node.results) == 0:
        file.write('return;\n')
    elif len(node.results) == 1:
        file.write(f'return {
            transfer_expression(node.results[0], data)
        };\n')
    else:
        file.write(
            f'return (struct {data.type_func_to_result_type[node.func.var.type]})'
            '{'
                f'{
                    ','.join(
                        transfer_expression(r, data) 
                        for r in node.results
                    )
                }'
            '};\n'
        )


@transfer_control.register(ControlCycleControl)
def _(node: ControlCycleControl, file: TextIO, data: DataContainer):
    match node.type:
        case CycleControlTypes.break_:
            file.write('break;\n')
        case CycleControlTypes.continue_:
            file.write('continue;\n')


@transfer_control.register(ControlIf)
def _(node: ControlIf, file: TextIO, data: DataContainer):
    file.write(
        f'if ({transfer_expression(node.condition, data)})'
    )
    transfer_control(node.block_if, file, data)
    file.write('else')
    transfer_control(node.block_else, file, data)


@transfer_control.register(ControlWhile)
def _(node: ControlWhile, file: TextIO, data: DataContainer):
    file.write(f'while ({transfer_expression(node.condition, data)})')
    transfer_control(node.code_block, file, data)


@transfer_control.register(ControlCodeBlock)
def _(node: ControlCodeBlock, file: TextIO, data: DataContainer):
    file.write('{')
    for control in node.block_parts:
        transfer_control(control, file, data)
    file.write('}')


@transfer_control.register(ControlMassAssignment)
def _(node: ControlMassAssignment, file: TextIO, data: DataContainer):
    # вложенный блок кода
    file.write('{')

    # этап 1 - вычислить значения справа
    for i, p in enumerate(node.processed):
        if len(p.wvalues) == 1:
            # одно значение - просто значение
            file.write(
                f'{data.type_to_name[p.rvalue.res_type]} _{i}' 
                '=' 
                f'{transfer_expression(p.rvalue, data)};\n'
            )
        else:
            # много - это структура функции
            assert isinstance(p.rvalue, TokenOperatorFunctionCall)
            file.write(
                f'{data.type_func_to_result_type[p.rvalue.func.res_type]} _{i}'
                '='
                f'{transfer_expression(p.rvalue, data)};\n')

    # этап 2 - присвоить

    for i, p in enumerate(node.processed):
        if len(p.wvalues) == 1:
            # одно - просто присваиваем
            file.write(
                f'{transfer_expression(p.wvalues[0], data)}' 
                '='
                # каст если надо
                f'{
                    f'_{i}' 
                    if p.t_need[0] is None else
                    f'{
                        f'({data.type_to_name[p.t_need[0]]})'
                        f'(_{i})'
                    }'
                }'
                ';\n'
            )

        else:
            # много - распаковываем
            for ii, w, t in (
                (i, p.wvalues[i], p.t_need[i]) for i in range(len(p.wvalues))
            ):
                file.write(
                    f'{transfer_expression(w, data)}'
                    f'='
                    f'{
                        f'_{i}._{ii}'
                        if t is None else
                        f'{
                            f'({data.type_to_name[t]})'
                            f'(_{i}._{ii});'
                        }'
                    }'
                    ';\n'
                )
    file.write('}')


@transfer_control.register(ControlClass)
def _(node: ControlClass, file: TextIO, data: DataContainer):
    # проделаем туже штуку, что и при трансляции глобального класса
    code = StringIO()
    transfer_control(node.rest, code, data)
    code = code.getvalue()[:-1]

    file.write(
        # сам класс
        f'{data.type_to_name[node.class_var.type]} {node.name} = ({data.type_to_name[node.class_var.type]})' '{};'
        # код
        f'{code}'
            # присваиваем
            f'{''.join(
                f'{node.name}.{var.name} = {var.name};'
                for var in node.class_field
            )}'
        '}'
    )

# с этими ничего делать не надо
@transfer_control.register(ControlTypedef)
def _(node: ControlTypedef, file: TextIO, data: DataContainer): pass
@transfer_control.register(ControlImport)
def _(node: ControlImport, file: TextIO, data: DataContainer): pass
@transfer_control.register(ControlExport)
def _(node: ControlExport, file: TextIO, data: DataContainer): pass
@transfer_control.register(ControlEnum)
def _(node: ControlEnum, file: TextIO, data: DataContainer): pass



