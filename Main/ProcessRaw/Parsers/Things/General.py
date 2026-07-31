from .. import Definitions
from ..Definitions import *
from .....Definitions.Exceptions import OurSyntaxError
from .....Definitions.Tokens import *

# Должен парсить обычные штуки, 3 вида операторов и скобки.
# Также передавать управление остальным парсерам при необходимости


__all__ = ('_parse_general',)


def should_we_pop_it(stack_operator: TreeOperatorABC | BracketOpen, operator: TreeOperatorABC) -> bool:
    """
    Проверяет, нужно ли доставать из стека оператор stack_operator, если мы хотим положить внутрь operator
    """
    # проверяем только операторы
    if not isinstance(stack_operator, TreeOperatorABC):
        return False
    # Если лево ассоциативный - достаём если его если его приоритет < нашего, для право - если его <= наш.
    # Приоритеты развёрнуты относительно обычного алгоритма из-за того, что у нас они развернуты (0 - много, 100 - мало)
    if operator.associativity == Associativity.left:
        return stack_operator.priority <= operator.priority
    return stack_operator.priority < operator.priority


def put_operator_in(op: TreeOperatorABC, operands: OperandsStack, operators: OperatorsStack):
    """
    Помещает оператор в стек операторов (и делает дополнительные штуки)
    """
    if operators:
        first = operators[-1]
        while should_we_pop_it(first, op):
            first.reduce(operands, operators)
            operators.pop()
            if not operators:
                break
            first = operators[-1]
    operators.append(op)


def _parse_general(data: list[PreprocessResults], operands: OperandsStack,
      operators: OperatorsStack, start: int, end: int) -> tuple[int, TokenOperatorABC]:
    last_token_type = LastTokensTypes.none
    put_operator_in_cur = lambda op: put_operator_in(op, operands, operators)
    i = start
    while i < end:
        cur = data[i]

        match cur:
            case RawOperator():
                # то, чем ожидается быть текущий оператор зависит от того, чем был прошлый
                match last_token_type:
                    # операнд, после него должен быть или постфиксный или бинарный оператор
                    # постфиксный, после него должен быть или постфиксный или бинарный оператор
                    case LastTokensTypes.operand | LastTokensTypes.postfix:
                        # проверяем, что следующий токен - оператор, ведь после
                        # постфиксного должен быть как минимум один оператор
                        is_next_operator = False
                        if i + 1 < end and isinstance(data[i+1], RawOperator) and not data[i+1].symbol in TokenOperatorPrefixTypes or i + 1 >= end:
                            is_next_operator = True

                        if cur.symbol in TokenOperatorPostfixTypes and is_next_operator:
                            put_operator_in_cur(TreeOperatorPostfix(
                                TokenOperatorPostfixTypes(cur.symbol), cur.origin
                            ))
                            last_token_type = LastTokensTypes.postfix
                        elif cur.symbol in TokenOperatorBinaryTypes:
                            # парсит особые штуки отдельно
                            if cur.symbol == TokenOperatorBinaryTypes.Cast.value:
                                i, cast = Definitions.parse_cast(data, operands, operators, i, end)
                                put_operator_in_cur(cast)
                            else:
                                # обычный
                                put_operator_in_cur(TreeOperatorBinary(
                                    TokenOperatorBinaryTypes(cur.symbol), cur.origin
                                ))
                            last_token_type = LastTokensTypes.binary
                        else:
                            if last_token_type == LastTokensTypes.operand:
                                raise OurSyntaxError(
                                    'После оператора должен быть или постфиксный или бинарный оператор',
                                    cur.origin)
                            else:
                                raise OurSyntaxError('После постфиксного оператора должен быть или постфиксный или '
                                                     'бинарный оператор', cur.origin)

                    # бинарный, после него или префиксный, или операнд
                    # префиксный, после него должен быть или префиксный, или операнд
                    case LastTokensTypes.binary | LastTokensTypes.prefix:
                        if cur.symbol in TokenOperatorPrefixTypes:
                            if cur.symbol == TokenOperatorPrefixTypes.VarDef.value:
                                i, vardef = Definitions.parse_vardef(data, operands, operators, i, end)
                                operands.append(vardef)
                                last_token_type = LastTokensTypes.operand
                            elif cur.symbol == TokenOperatorPrefixTypes.Sizeof.value:
                                i, sizeof = Definitions.parse_sizeof(data, operands, operators, i, end)
                                operands.append(sizeof)
                                last_token_type = LastTokensTypes.binary
                            else:
                                put_operator_in_cur(TreeOperatorPrefix(
                                    TokenOperatorPrefixTypes(cur.symbol), cur.origin
                                ))
                                last_token_type = LastTokensTypes.binary
                        else:
                            raise OurSyntaxError('После бинарного оператора должен быть или префиксный '
                                                 'оператор или операнд', cur.origin)

            case RawOperand():
                # просто добавим операнд
                thing = cur.thing
                if last_token_type not in (LastTokensTypes.prefix, LastTokensTypes.binary):
                    raise OurSyntaxError('До операнда должен быть префиксный или бинарный оператор', thing.origin)
                if isinstance(thing, TokenRawWord):
                    operands.append(TokenVariableAccess(thing.word, thing.origin))
                else:
                    operands.append(TokenLiteral.from_raw(thing))
                last_token_type = LastTokensTypes.operand

            case BracketOpen():
                # тут может быть 2 случай - или обычные открытие скобок, или вызов функции
                # вызов функции
                if last_token_type in (LastTokensTypes.operand,):
                    i, op = Definitions.parse_fcall(data, operands, operators, i, end)
                    put_operator_in_cur(op)
                    last_token_type = LastTokensTypes.operand
                # просто открытие
                elif last_token_type in (LastTokensTypes.prefix, LastTokensTypes.binary):
                    operators.append(cur)
                    last_token_type = LastTokensTypes.none
                else:
                    raise OurSyntaxError('До открытия скобки может стоять либо операнд(вызов функции) '
                                         'либо префиксный|бинарный(просто скобки)', cur.origin)

            case BracketClose():
                # вытолкнем всё до первых "("
                while operators:
                    opr = operators.pop()
                    if isinstance(opr, BracketOpen):
                        break
                    opr.reduce(operands, operators)
                    last_token_type = LastTokensTypes.operand
                else:
                    raise OurSyntaxError('Неоткрытая скобка', cur.origin)

            case SquareBracketOpen():
                # это или массив или срез|индексация
                if last_token_type in (LastTokensTypes.operand, LastTokensTypes.postfix):
                    i, index = Definitions.parse_index_or_slice(data, operands, operators, i, end)
                    put_operator_in_cur(index)
                    last_token_type = LastTokensTypes.postfix
                    # это срез|индексация
                    pass
                elif last_token_type in (LastTokensTypes.binary, last_token_type.prefix):
                    i, arr = Definitions.parse_array(data, operands, operators, i, end)
                    operands.append(arr)
                    last_token_type = LastTokensTypes.operand
                else:
                    raise ValueError('')
            case SquareBracketClose():
                raise OurSyntaxError('"]" может встречаться только на конце '
                                     'созданий массивов, индексаций и срезов', cur.origin)
            case Separator():
                raise SemanticError('"," может встречаться только в '
                                    'вызовах функций, массивах, срезах и индексов', cur.origin)
            case Delimiter():
                raise SemanticError('":" может встречаться только в срезах', cur.origin)
        i += 1

    # мы закончили, теперь выдвинем всё из операторов
    for op in operators[::-1]:
        if isinstance(op, BracketOpen):
            raise OurSyntaxError('Незакрытая скобка', op.origin)
        op.reduce(operands, operators)
    if not operands:
        raise OurSyntaxError('Не обнаружено операндов',
                             data[start].origin + data[end-1].origin)
    if len(operands) != 1:
        raise OurSyntaxError('Обнаружено более 1 операнда',
                             operands[0].origin + operands[-1].origin)
    return i, operands[0]

