from .Simple import *


def transfer_array(file: TextIO, data: DataContainer, t: Type):
    length = t.length

    lesser_type_name = data.type_to_name[t.without_one_modifier()]
    bigger_type_name = get_unique_name(data.all_names,
                                       f'{lesser_type_name}a{length}')

    # массив в структуре
    file.write(
        'typedef struct {'
            f'{lesser_type_name} arr[{length}];'
        '}' f'{bigger_type_name};\n'
    )

    data.type_to_name[t] = bigger_type_name


def transfer_array_index(file: TextIO, data: DataContainer, t: Type):
    length = t.length
    bigger_type_name = data.type_to_name[t]

    # делаем функцию для проверки выхода за границы
    indexing_func = get_unique_name(data.all_names, f'{bigger_type_name}i')
    file.write(
        f'static inline size_t {indexing_func} ('
            'size_t i, char* position'
        ') {'
            f'if ( i >= {length} )'
            '{'
                'printf('
                    rf'"Index %zu out of array range {length} on %s\n", i, position'
                ');'
                'abort();'
            '}'
            'return i;'
        '}\n'
    )

    data.type_to_indexing_func[t] = indexing_func


def transfer_array_slice(file: TextIO, data: DataContainer, slice_data: TransferSlicingData):
    operand_type = slice_data.arg_type
    result_type = slice_data.res_type
    indexes_num = slice_data.pos_start_num
    dims_num = slice_data.dims_num

    array_lengths = []
    elem_type = operand_type
    while elem_type.is_mod_array:
        array_lengths.append(elem_type.length)
        elem_type = elem_type.without_one_modifier()

    f_name = get_unique_name(data.all_names,
                             f'{data.type_to_name[operand_type]}s{indexes_num}_{dims_num}')

    file.write(
        f'static inline {data.type_to_name[result_type]} {f_name}('
            # указатель на массив
            f'{data.type_to_name[operand_type]}* array, '
            # индексы
            f'{
                ', '.join(
                    f'size_t i_{i}'
                    for i in range(indexes_num)
                )
            }, '
            # измерения
            f'{
                ', '.join(
                    f'size_t d_{i}'
                    for i in range(dims_num)
                )
            }, '
            'char* position'
        ') {'
        # ===== Проверки ===== 
            # сначала проверим, все ли индексы в пределах массива
            f'{
                ''.join(
                    f'if ( i_{i} >= {array_lengths[i]} )' '{'
                        'printf('
                            rf'"Index %zu out of array range {array_lengths[i]} in {i + 1}' 
                            rf'index of slice creation on %s\n", i_{i}, position'
                        ');'
                        'abort();'
                    '}'
                    for i in range(indexes_num)
                )
            }'
            # теперь, проверим, не выходит ли новая размерность из-за предела массива
            # оставшийся после индексации максимально допустимый размер
            'size_t max_total_size = ' f'{
                ' * '.join(
                    f'({array_lengths[i]} - i_{i})'
                    for i in range(indexes_num)
                )
            };'
            # количество элементов, что есть
            'size_t total_size = ' f'{
                '*'.join(
                    f'd_{i}'
                    for i in range(dims_num)
                )
            };'
            # сама проверка
            f'if (total_size > max_total_size)' '{'
                'printf('
                    r'"Size of slice %zu out of allowed sliced array size %zu on %s\n", '
                    'total_size, max_total_size, position'
                ');'
                'abort();'
            '}'
        # ===== Срез =====
            f'return ({data.type_to_name[result_type]})' '{'
                # старт, просто берём адрес нужного элемента
                f'&(array->{
                        '.'.join(
                            f'arr[i_{i}]'
                            for i in range(indexes_num)
                        )
                    }'
                '), '
                # размерности
                f'{
                    ', '.join(
                        f'd_{i}'
                        for i in range(dims_num)
                )}'
                # stride
                f'{
                    '' if dims_num <= 2 else 
                    f', total_size / d_{dims_num - 1}'
                }'
            '};'
        # конец
        '}\n'
    )

    data.type_to_slicing_func[(result_type, operand_type)] = f_name
