from .Things import *
from ....Definitions.Tokens import *
from ....Definitions.Raw import *
from ....Definitions.Exceptions import OurSyntaxError
from .Definitions import *
from .PreProcessor import preprocess


__all__ = ('process_rvalue', 'process_wvalue', 'process_any_value', 'process_type', 'process_define')


def process_rvalue(expr: list[TokenRawABC]) -> TokenOperatorRvalueABC:
    expr = preprocess(expr)
    _, thing = parse_general(expr, [], [], 0, len(expr))
    if not isinstance(thing, TokenOperatorRvalueABC):
        raise OurSyntaxError('Ожидалось rvalue', expr[0].origin + expr[-1].origin)
    return thing


def process_wvalue(expr: list[TokenRawABC]) -> TokenOperatorWvalueABC:
    expr = preprocess(expr)
    _, thing = parse_general(expr, [], [], 0, len(expr))
    if not isinstance(thing, TokenOperatorWvalueABC):
        raise OurSyntaxError('Ожидалось wvalue', expr[0].origin + expr[-1].origin)
    return thing


def process_any_value(expr: list[TokenRawABC]) -> TokenOperatorRvalueABC | TokenOperatorWvalueABC:
    expr = preprocess(expr)
    _, thing = parse_general(expr, [], [], 0, len(expr))
    if not isinstance(thing, (TokenOperatorWvalueABC, TokenOperatorRvalueABC)):
        raise OurSyntaxError('Ожидалось rvalue|wvalue', expr[0].origin + expr[-1].origin)
    return thing


def process_type(expr: list[TokenRawABC]) -> Type:
    expr = preprocess(expr)
    _, _type = parse_type(expr, 0, len(expr))
    return _type


def process_define(expr: list[TokenRawABC]) -> TokenOperatorVariableDefinition:
    """Обрабатывает то, что должно быть объявлением переменной, вставляет первым токеном 'var' """
    expr.insert(0, TokenRawSymbol(KeyWords.Variable.value, zero_origin))
    expr = preprocess(expr)
    _, thing = parse_vardef(expr, [], [], 0, len(expr))
    return thing
