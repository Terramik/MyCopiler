from .Simple import *


def transfer_func(file: TextIO, data: DataContainer, t: Type):
    func = t.simple
    assert isinstance(func, Type.SimpleTypeFunc)


    # смертельно оригинальное имя
    name = (
        '_ft'
        f'{
            'void' if not func.arguments else
            f'{'_'.join(
                data.type_to_name[s][:10] 
                for s in func.arguments
            )}' 
        }'
        '__'
        f'{
            'void' if not func.results else
            f'{'_'.join(
                data.type_to_name[s][:10] 
                for s in func.results
            )}'
        }'
        f'ft_'
    )

    # берём тип-результат
    if len(func.results) > 1:
        # создадим структуру, содержащею все возвращаемые значения функции (если есть)
        result_type_name = get_unique_name(data.all_names,
                                    f'{name}resst')
        file.write(
            'typedef struct {'
                f'{
                    ''.join(
                        f'{data.type_to_name[_t]} _{i};'
                        for i, _t in enumerate(func.results)
                    )
                }'
            '}' f'{result_type_name};\n'
        )

    elif len(func.results) == 1:
        # результат - просто 1 результат функции
        result_type_name = data.type_to_name[func.results[0]]
    else:
        # результат - ничего
        result_type_name = 'void'

    # теперь сам тип-функции
    type_name = get_unique_name(data.all_names,
                                f'{name}fp')

    file.write(
        f'typedef {result_type_name} (*{type_name})('
            f'{','.join(
                data.type_to_name[_t]
                for _t in func.arguments
            )}'
            f'{
                ', ' if func.arguments else ''
            }'
            'void*' # указатель на окружение для мини-замыканий
        ');\n'
    )

    enclosure_name = get_unique_name(data.all_names,
                                     f'{name}_env')

    file.write(
        'typedef struct {'
            f'{type_name} func;' # функция
            'void* env;' # окружение
        '}' f'{enclosure_name};\n'
    )

    data.type_func_to_result_type[t] = result_type_name
    data.type_func_to_enclosure_struct[t] = enclosure_name
    data.type_to_name[t] = type_name
