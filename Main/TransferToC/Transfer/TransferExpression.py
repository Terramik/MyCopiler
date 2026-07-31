from .Simple import *
import re


__all__ = ('transfer_expression',)


@singledispatch
def transfer_expression(node: TokenOperatorWvalueABC | TokenOperatorRvalueABC, data: DataContainer) -> str:
    raise NotImplementedError('Что-то пошло не так')


@transfer_expression.register(TokenOperatorVariableDefinition)
def _(node: TokenOperatorVariableDefinition | TokenOperatorRvalueABC, data: DataContainer) -> str:
    return f'{data.type_to_name[node.res_type.full_type]} {node.name}'


@transfer_expression.register(TokenVariableAccess)
def _(node: TokenVariableAccess, data: DataContainer) -> str:
    if node.is_nonlocal:
        return f'(*env->{node.var_def.name})'
    return node.var_def.name


@transfer_expression.register(TokenLiteral)
def _(node: TokenLiteral, data: DataContainer) -> str:
    if node.type == node.Types.Str:
        return f'c_str_to_slise("{node.value}", {
            len(node.value) - 
            # убираем лишние символы escape-последовательностей, т.к. они 1 символ.
            len(re.findall(r'\\[n|t|\\|"]', node.value)) - 
            3 * len(re.findall(r'\\\d{3}', node.value))
        })'
    else:
        return node.value


@transfer_expression.register(TokenOperatorAssignment)
def _(node: TokenOperatorAssignment, data: DataContainer) -> str:
    return f'({transfer_expression(node.left, data)})=({transfer_expression(node.right, data)})'


@transfer_expression.register(TokenOperatorFunctionCall)
def _(node: TokenOperatorFunctionCall, data: DataContainer) -> str:
    f = transfer_expression(node.func, data)
    return (
        f'(({f}).func)' # функция замыкания
        '('
            # обычные аргументы
            f'{
                ','.join(
                    transfer_expression(exp, data) 
                    for exp in node.arguments
                )
            }'
            # запятая, если есть обычные
            f'{
                ',' if node.arguments else ''
            }' 
            f'({f}).env' # замыкание замыкания
        ')'
    )


@transfer_expression.register(TokenOperatorBinary)
def _(node: TokenOperatorBinary, data: DataContainer) -> str:
    symbol: str
    match node.type:
        case TokenOperatorBinaryTypes.ArfmAdd: symbol = '+'
        case TokenOperatorBinaryTypes.ArfmSub: symbol = '-'
        case TokenOperatorBinaryTypes.ArfmMul: symbol = '*'
        case TokenOperatorBinaryTypes.ArfmDiv: symbol = '/'
        case TokenOperatorBinaryTypes.ArfmMod: symbol = '%'
        case TokenOperatorBinaryTypes.BitShiftLeft: symbol = '<<'
        case TokenOperatorBinaryTypes.BitShiftRight: symbol = '>>'
        case TokenOperatorBinaryTypes.BitAnd: symbol = '&'
        case TokenOperatorBinaryTypes.BitXor: symbol = '^'
        case TokenOperatorBinaryTypes.BitOr: symbol = '|'
        case TokenOperatorBinaryTypes.ComprEq: symbol = '=='
        case TokenOperatorBinaryTypes.ComprNEq: symbol = '!='
        case TokenOperatorBinaryTypes.ComprLess: symbol = '<'
        case TokenOperatorBinaryTypes.ComprLessOrEq: symbol = '<='
        case TokenOperatorBinaryTypes.ComprMore: symbol = '>'
        case TokenOperatorBinaryTypes.ComprMoreOrEq: symbol = '>='
        case TokenOperatorBinaryTypes.LogAnd: symbol = '&&'
        case TokenOperatorBinaryTypes.LogOr: symbol = '||'
        case _: raise ValueError('ЧТо-то пошло не так')
    return f'({transfer_expression(node.left, data)}){symbol}({transfer_expression(node.right, data)})'


@transfer_expression.register(TokenOperatorPrefix)
def _(node: TokenOperatorPrefix, data: DataContainer) -> str:
    symbol: str
    match node.type:
        case TokenOperatorPrefixTypes.ArfmUnMin: symbol = '-'
        case TokenOperatorPrefixTypes.BitNot: symbol = f'~'
        case TokenOperatorPrefixTypes.LogNot: symbol = '!'
        case _: raise ValueError('ЧТо-то пошло не так')
    return f'{symbol}({transfer_expression(node.operand, data)})'


@transfer_expression.register(TokenOperatorPostfix)
def _(node: TokenOperatorPostfix, data: DataContainer) -> str:
    raise ValueError('ЧТо-то пошло не так')


@transfer_expression.register(TokenOperatorCast)
def _(node: TokenOperatorCast, data: DataContainer) -> str:
    if node.cast_type.is_mod_array:
        # считаем, во что приобразовывать элемент и размерности массива
        least_cast_to = node.cast_type
        dims = []
        while least_cast_to.is_mod_array:
            dims.append(least_cast_to.length)
            least_cast_to = least_cast_to.without_one_modifier()
        dims = dims[::-1]
        # преобразовалка
        def rec(_dims, _indexes, _operand) -> str:
            if not _dims:
                return (
                    f'{_operand}'
                    f'{
                        ''.join(
                            f'.arr[{i}]'
                            for i in _indexes
                        )
                    }'
                )
            n = _dims.pop()
            return (
                '{'
                f'{
                    ','.join(
                        rec(_dims[:], [i, *_indexes], _operand)
                        for i in range(n)
                    )
                }'
                '}'
            )

        operand = transfer_expression(node.operand, data)
        return f'({data.type_to_name[node.cast_type]}){rec(dims, [], operand)}'
    elif node.operand.res_type.is_mod_slize and node.cast_type.is_mod_pointer:
        return f'({data.type_to_name[node.cast_type]})(({transfer_expression(node.operand, data)}).start)'
    else:
        return f'({data.type_to_name[node.cast_type]})({transfer_expression(node.operand, data)})'


@transfer_expression.register(TokenOperatorSizeof)
def _(node: TokenOperatorSizeof, data: DataContainer) -> str:
    return f'sizeof({data.type_to_name[node.type]})'


@transfer_expression.register(TokenOperatorLenof)
def _(node: TokenOperatorLenof, data: DataContainer) -> str:
    if node.operand.res_type.is_mod_array:
        return f'{node.operand.res_type.length}'
        # raise ValueError('Все леноф от массивов должны были быть свёрнуты ранее')
    else:
        dims = node.operand.res_type.dimensions
        # структура среза, первая размерность
        return f'({transfer_expression(node.operand, data)})._{dims-1}'


@transfer_expression.register(TokenOperatorIndex)
def _(node: TokenOperatorIndex, data: DataContainer) -> str:
    operand_type = node.operand.res_type
    if operand_type.is_mod_array:
        return (
            # поле структуры - сам массив
            f'{transfer_expression(node.operand, data)}.arr['
                # функция для проверки индекса
                f'{data.type_to_indexing_func[operand_type]}('
                    # индекс                        
                    f'{transfer_expression(node.index, data)}, '
                    # позиция для указания ошибки уже в нашем коде
                    f'"{node.origin}"'
            ')]'
        )
    else:
        if operand_type.dimensions == 1:
            # тоже индексация
            return (
                # используем указатель
                f'{transfer_expression(node.operand, data)}.start['
                    # функция для проверки индекса(уже со срезом)
                    f'{data.type_to_indexing_func[operand_type]}('
                        # срез         
                        f'{transfer_expression(node.operand, data)}, '
                        # индекс и позиция
                        f'{transfer_expression(node.index, data)}, '
                        f'"{node.origin}"'
                ')]'
            )
        else:
            return (
                # делаем новый срез функцией
                f'{data.type_to_indexing_func[operand_type]}('
                    f'{transfer_expression(node.operand, data)}, '
                    f'{transfer_expression(node.index, data)}, '
                    f'"{node.origin}"'
                ')'
            )


@transfer_expression.register(TokenOperatorSlize)
def _(node: TokenOperatorSlize, data: DataContainer) -> str:
    return (
        # имя
        f'{data.type_to_slicing_func[(node.res_type, node.operand.res_type)]}('
            # операнд
            f'{
                # просто указатель, если это указатель
                f'{transfer_expression(node.operand, data)},'
                if node.operand.res_type.is_mod_pointer else
                # или указатель на структуру, если это не указатель
                f'&({transfer_expression(node.operand, data)}),' 
            }'
            # указатель на операнд
            
            # идексы
            f'{
                ','.join(
                    transfer_expression(index, data)
                    for index in node.position_start
                )
            }'
            ','
            # измерения
            f'{
                ','.join(
                    transfer_expression(dim, data)
                    for dim in node.result_dimensions
                )
            }'
            ','
            # позиция
            f'"{node.origin}"'
        ')'
    )


@transfer_expression.register(TokenOperatorArrayCreation)
def _(node: TokenOperatorArrayCreation, data: DataContainer) -> str:
    return (
        # создаём структуру-массив на месте
        f'({data.type_to_name[node.res_type]}){{'
            f'{{{
                ','.join(
                    transfer_expression(opr, data)
                    for opr in node.operands
                )
            }}}'
        '}'
    )


@transfer_expression.register(TokenOperatorReferencing)
def _(node: TokenOperatorReferencing, data: DataContainer) -> str:
    return f'&({transfer_expression(node.operand, data)})'


@transfer_expression.register(TokenOperatorDereferencing)
def _(node: TokenOperatorDereferencing, data: DataContainer) -> str:
    return f'*({transfer_expression(node.operand, data)})'


@transfer_expression.register(TokenOperatorFieldAccess)
def _(node: TokenOperatorFieldAccess, data: DataContainer) -> str:
    return f'({transfer_expression(node.operand, data)}).{node.field.name}'


@transfer_expression.register(TokenOperatorFieldAccessPointer)
def _(node: TokenOperatorFieldAccessPointer, data: DataContainer) -> str:
    return f'({transfer_expression(node.operand, data)})->{node.field.name}'


@transfer_expression.register(TokenOperatorDeInitializer)
def _(node: TokenOperatorDeInitializer, data: DataContainer) -> str:
    raise ValueError('Что-то пошло не так очень сильно')



