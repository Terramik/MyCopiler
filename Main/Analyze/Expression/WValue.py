from ..Simple import *
from .Utils import *


__all__ = ('analyze_wvalue',)


@analyze_wvalue.register(TokenOperatorVariableDefinition)
def _(node: TokenOperatorVariableDefinition, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    if is_in_key_word(node.name):
        errors.append(SemanticError('Имя для переменной не может быть ключевым словом', node.origin))
    elif scope.is_name_occupied(node.name, False):
        errors.append(SemanticError(f'Имя {node.name} уже занято в данной области видимости', node.origin))
    else:
        node.type = analyze_type(node.type, scope, node.origin, errors)
        scope.add_variable(node)
        return node.type
    # в случае ошибки
    node.type = t_error
    return t_error


@analyze_wvalue.register(TokenVariableAccess)
def _(node: TokenVariableAccess, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    # запись (wvalue)
    r = scope.find_variable(node.name, True)
    if r is None:
        errors.append(SemanticError(f'Попытка записи в необъявленную переменную "{node.name}"', node.origin))
        # сделаем такую переменную, чтобы не кидать больше таких ошибок
        err_var = TokenOperatorVariableDefinition(node.name, t_error, node.origin)
        node.is_nonlocal = False
        node.var_def = err_var
        scope.add_variable(err_var)
        return t_error
    var, is_nonlocal = r
    node.is_nonlocal = is_nonlocal
    node.var_def = var
    return var.type


@analyze_wvalue.register(TokenOperatorIndex)
def _(node: TokenOperatorIndex, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    if not isinstance(node.operand, TokenOperatorWvalueABC):
        errors.append(SemanticError('Для индекса, ожидаемого быть wvalue операнд тоже должен быть wvalue', node.operand.origin))
        return err(node)
    type_operand = analyze_wvalue(node.operand, scope, node, errors)

    if not (type_operand.is_mod_array or type_operand.is_mod_slize):
        errors.append(SemanticError(f'Индексировать можно только массивы и срезы, дано {type_operand}', node.operand.origin))
        return err(node)
    type_index = analyze_rvalue(node.index, scope, node, errors)
    type_index_need = type_index.turn_into_int()

    if type_index_need is None:
        errors.append(SemanticError(f'Индексом могут быть только целые положительные числа, дано: {type_index}', node.index.origin))
        return err(node)
    node.index = cast_if_need(node.index, type_index_need)
    node.res_type = type_operand.without_one_dimension()
    return node.res_type


@analyze_wvalue.register(TokenOperatorDereferencing)
def _(node: TokenOperatorDereferencing, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    return analyze_rvalue(node, scope, parent, errors)


@analyze_wvalue.register(TokenOperatorFieldAccess)
def _(node: TokenOperatorFieldAccess, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    return analyze_rvalue(node, scope, parent, errors)


@analyze_wvalue.register(TokenOperatorFieldAccessPointer)
def _(node: TokenOperatorFieldAccessPointer, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    return analyze_rvalue(node, scope, parent, errors)


@analyze_wvalue.register(TokenOperatorError)
def _(node: TokenOperatorError, scope: Scope, parent: TypeExpressionParent, errors: list[SemanticError]) -> Type:
    return t_error

