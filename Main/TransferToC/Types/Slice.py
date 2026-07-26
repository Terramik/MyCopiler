from .Simple import *


def transfer_slice(file: TextIO, data: DataContainer, t: Type):
    dims = t.dimensions

    least_type_name = data.type_to_name[t.without_one_modifier()]

    if t == types.str:
        bigger_type_name = 'str_t'
    else:
        bigger_type_name = get_unique_name(data.all_names,
                                           f'{least_type_name}s{dims}')

    # указатель и все размерности
    file.write(
        'typedef struct {'
            # старт всего среза
            f'{least_type_name}* start;'
            # размерности
            f'{
                ''.join(
                    f'size_t _{i};'
                    for i in range(dims)
                )
            }'
            # если больше 2-х измерений, то берём произведение всех 
            # измерений до последнего не включительно (для оптимизации)
            f'{
                '' if dims <= 2 else 'size_t stride;'
            }'
        '}' f'{bigger_type_name};\n'
    )

    data.type_to_name[t] = bigger_type_name


def transfer_slice_index(file: TextIO, data: DataContainer, t: Type):
    dims = t.dimensions

    lesser_type_name = data.type_to_name[t.without_one_dimension()]
    bigger_type_name = data.type_to_name[t]
    # функция для индексации
    indexing_func = get_unique_name(data.all_names, f'{bigger_type_name}i')

    # если dims это 1, то это фактически просто массив, так что только проверим индекс
    if dims == 1:
        # просто проверяем
        file.write(
            f'static inline size_t {indexing_func} ('
                f'{bigger_type_name} slise, size_t i, char* position'
            ') {'
                'if ( i >= slise._0 )'
                '{'
                    'printf('
                        r'"Index %zu out of slise range %zu on %s\n", i, slise._0, position'
                    ');'
                    'abort();'
                '}'
                'return i;'
            '}\n'
        )
    # dims - это не 1, так что результат - это иной срез, и всё сложнее
    else:
        # генерируем новый срез
        file.write(
            # объявление
            f'static inline {lesser_type_name} {indexing_func} ('
                f'{bigger_type_name} slise, size_t i, char* position'
            ') {'
            
                # проверка границы
                f'if ( i >= slise._{dims - 1} )'
                '{'
                    'printf('
                        rf'"Index %zu out of slise range %zu on %s\n", i, slise._{dims - 1}, position'
                    ');'
                    'abort();'
                '}'
            
                # делаем новый срез
                f'return ({lesser_type_name})' '{'
                    # двигаем старт
                    f'{
                        # есть stride, пользуемся им
                        'slise.start + slise.stride * i,'
                        if dims > 2 else
                        # stride нет, пользуемся последним индексом (размерность тут только 2)
                        'slise.start + slise._0 * i,'
                    }'
                    # размерности
                    f'{
                        ','.join(
                            f'slise._{i}' for i in range(dims - 1)
                        )
                    }'
                    # stride(если нужен)
                    f'{
                        # запятая стоит тут, т.к. этот аргумент может не существовать
                        f', slise.stride / slise._{dims - 2}'
                        if dims > 2 else
                        ''
                    }'
                '};'
            
            '}\n'
        )

    data.type_to_indexing_func[t] = indexing_func


def transfer_slice_slice(file: TextIO, data: DataContainer, slice_data: TransferSlicingData):
    operand_type = slice_data.arg_type
    result_type = slice_data.res_type
    indexes_num = slice_data.pos_start_num
    dims_num = slice_data.dims_num
    elem_type = operand_type.without_one_modifier()

    lengths = []
    # развернём, так как _0 в срезе - это последняя на изменение размерность, а _n - первая
    for i in range(indexes_num - 1, -1, -1):
        lengths.append(
            f'slice->_{i}'
        )

    f_name = get_unique_name(data.all_names,
                             f'{data.type_to_name[operand_type]}s{indexes_num}_{dims_num}')

    file.write(
        f'static inline {data.type_to_name[result_type]} {f_name}('
            # указатель на массив
            f'{data.type_to_name[operand_type]}* slice, '
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
            # все ли индексы в пределах размерностей срез
            f'{
                ''.join(
                    f'if (i_{i} >= {lengths[i]})' '{'
                        'printf('
                            rf'"Index %zu out of slice range %zu in {i + 1} index of slice creation on %s\n",'
                            f'i_{i}, {lengths[i]}, position'
                        ');'
                        'abort();'
                    '}'
                    for i in range(indexes_num)
                )
            }'
            # максимально допустимый
            'size_t max_total_size = ' f'{
                '*'.join(
                    f'({lengths[i]} - i_{i})'
                    for i in range(indexes_num)
                )
            };'
            # нужный
            'size_t total_size = ' f'{
                ' * '.join(
                    f'd_{i}'
                    for i in range(dims_num)
                )
            };'
            # сама проверка
            'if ( total_size > max_total_size ) '
                '{'
                'printf('
                    rf'"Size of slice %zu out of allowed sliced slise size %zu on %s\n", '
                    'total_size, max_total_size, position'
                ');'
                'abort();'
            '}'
        # ===== Срез =====
            # считаем сдвиг
            'size_t shift = i_0;'
            f'size_t stride = {lengths[0]};'
            f'{
                ''.join(
                    f'shift += i_{i} * stride;'
                    f'stride *= {lengths[i]};'
                    for i in range(1, indexes_num)
                )
            }'
            # сам срез
            f'return ({data.type_to_name[result_type]})' '{'
                'slice->start + shift, '
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







