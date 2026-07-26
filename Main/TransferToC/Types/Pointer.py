from .Simple import *


def transfer_pointer(file: TextIO, data: DataContainer, t: Type):
    lesser_type_name = data.type_to_name[t.without_one_modifier()]
    bigger_type_name = get_unique_name(data.all_names,
                                       f'{lesser_type_name}p')

    # просто указатель
    file.write(
        f'typedef {lesser_type_name}* {bigger_type_name};'
    )

    data.type_to_name[t] = bigger_type_name


def transfer_pointer_slice(file: TextIO, data: DataContainer, slice_data: TransferSlicingData):
    assert slice_data.pos_start_num == 1
    operand_type = slice_data.arg_type
    result_type = slice_data.res_type
    dims_num = slice_data.dims_num

    f_name = get_unique_name(data.all_names,
                             f'{data.type_to_name[operand_type]}s1_{dims_num}')

    file.write(
        f'static inline {data.type_to_name[result_type]} {f_name}('
            # операнд
            f'{data.type_to_name[operand_type]} pointer, '
            # индекс(только 1)
            f'size_t i_0, '
            # измерения
            f'{
                ', '.join(
                    f'size_t d_{i}'
                    for i in range(dims_num)
                )
            }, '
            'char* position'
        ') {'
            # проверок никаких не будет
            # сам срез
            f'return ({data.type_to_name[result_type]})' '{'
                # указатель со смещением
                'pointer + i_0, '
                # размерности
                f'{
                    ', '.join( 
                        f'd_{i}' for i in range(dims_num)
                    )
                }'
                # stride
                f'{
                    '' if dims_num <= 2 else 
                    f',{
                        '*'.join(
                            f'd_{i}' for i in range(dims_num - 1)
                    )}'
                }'
            '};'
        # конец
        '}\n'
    )

    data.type_to_slicing_func[(result_type, operand_type)] = f_name

