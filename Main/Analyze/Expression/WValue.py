from ..Simple import *
from .Utils import *


__all__ = ('analyze_wvalue',)


@analyze_wvalue.register(TokenOperatorVariableDefinition)
def _(node: TokenOperatorVariableDefinition, scope: Scope, parent: TypeExpressionParent) -> Type:
    if is_in_key_word(node.name):
        raise SemanticError('Имя для переменной не может быть ключевым словом', node.origin)
    if scope.is_name_occupied(node.name, False):
        raise SemanticError(f'Имя {node.name} уже занято в данной области видимости', node.origin)
    analyze_type(node.type, scope, node.origin)
    scope.add_variable(node)
    return node.type


@analyze_wvalue.register(TokenVariableAccess)
def _(node: TokenVariableAccess, scope: Scope, parent: TypeExpressionParent) -> Type:
    # запись (wvalue)
    r = scope.find_variable(node.name, True)
    if r is None:
        raise SemanticError(f'Попытка записи в необъявленную переменную "{node.name}"', node.origin)
    var, is_nonlocal = r
    node.is_nonlocal = is_nonlocal
    node.var_def = var
    return var.type


@analyze_wvalue.register(TokenOperatorIndex)
def _(node: TokenOperatorIndex, scope: Scope, parent: TypeExpressionParent) -> Type:
    if not isinstance(node.operand, TokenOperatorWvalueABC):
        raise SemanticError('Для индекса, ожидаемого быть wvalue операнд тоже должен быть wvalue', node.operand.origin)
    type_operand = analyze_wvalue(node.operand, scope, node)
    if not (type_operand.is_mod_array or type_operand.is_mod_slize):
        raise SemanticError('Индексировать можно только массивы и срезы', node.operand.origin)
    type_index = analyze_rvalue(node.index, scope, node)
    type_index_need = type_index.turn_into_int()
    if type_index_need is None:
        raise SemanticError('Как индекс могут быть только целые положительные числа', node.index.origin)
    node.index = cast_if_need(node.index, type_index_need)
    node.res_type = type_operand.without_one_dimension()
    return node.res_type


@analyze_wvalue.register(TokenOperatorDereferencing)
def _(node: TokenOperatorDereferencing, scope: Scope, parent: TypeExpressionParent) -> Type:
    return analyze_rvalue(node, scope, parent)


@analyze_wvalue.register(TokenOperatorFieldAccess)
def _(node: TokenOperatorFieldAccess, scope: Scope, parent: TypeExpressionParent) -> Type:
    return analyze_rvalue(node, scope, parent)


@analyze_wvalue.register(TokenOperatorFieldAccessPointer)
def _(node: TokenOperatorFieldAccessPointer, scope: Scope, parent: TypeExpressionParent) -> Type:
    return analyze_rvalue(node, scope, parent)