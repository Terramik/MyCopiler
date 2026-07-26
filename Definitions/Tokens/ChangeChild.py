from functools import singledispatch
from typing import Any

from .Operators import *
from .Controls import *


__all__ = ('change_child',)


@singledispatch
def change_child(node: Any, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    raise NotImplementedError(f"change_child не реализован для типа {type(node)}")


# да восславить бог-машина за написание этого


@change_child.register(TokenOperatorVariableDefinition)
def _(node: TokenOperatorVariableDefinition, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    """У переменной нет дочерних узлов"""
    pass


@change_child.register(TokenVariableAccess)
def _(node: TokenVariableAccess, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    """Доступ к переменной не имеет детей"""
    pass


@change_child.register(TokenLiteral)
def _(node: TokenLiteral, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    """Литерал не содержит дочерних узлов"""
    pass


@change_child.register(TokenOperatorAssignment)
def _(node: TokenOperatorAssignment, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    if last_child is node.left:
        assert isinstance(new_child, TokenOperatorWvalueABC)
        node.left = new_child
    elif last_child is node.right:
        assert isinstance(new_child, TokenOperatorRvalueABC)
        node.right = new_child
    else:
        raise AssertionError("last_child не является потомком узла присваивания")


@change_child.register(TokenOperatorFunctionCall)
def _(node: TokenOperatorFunctionCall, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert isinstance(new_child, TokenOperatorRvalueABC)
    assert isinstance(last_child, TokenOperatorRvalueABC)
    if last_child in node.arguments:
        idx = node.arguments.index(last_child)
        node.arguments[idx] = new_child
    else:
        assert node.func is last_child
        node.func = new_child


@change_child.register(TokenOperatorBinary)
def _(node: TokenOperatorBinary, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert isinstance(new_child, TokenOperatorRvalueABC)
    if last_child is node.left:
        node.left = new_child
    elif last_child is node.right:
        node.right = new_child
    else:
        raise AssertionError("last_child не является потомком бинарного оператора")


@change_child.register(TokenOperatorPrefix)
def _(node: TokenOperatorPrefix, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert isinstance(new_child, TokenOperatorRvalueABC)
    assert node.operand is last_child
    node.operand = new_child


@change_child.register(TokenOperatorPostfix)
def _(node: TokenOperatorPostfix, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert isinstance(new_child, TokenOperatorRvalueABC)
    assert node.operand is last_child
    node.operand = new_child


@change_child.register(TokenOperatorCast)
def _(node: TokenOperatorCast, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert isinstance(new_child, TokenOperatorRvalueABC)
    assert node.operand is last_child
    node.operand = new_child


@change_child.register(TokenOperatorSizeof)
def _(node: TokenOperatorSizeof, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    pass


@change_child.register(TokenOperatorLenof)
def _(node: TokenOperatorLenof, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert isinstance(new_child, TokenOperatorRvalueABC)
    assert node.operand is last_child
    node.operand = new_child


@change_child.register(TokenOperatorSlize)
def _(node: TokenOperatorSlize, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert isinstance(new_child, TokenOperatorRvalueABC)
    if node.operand is last_child:
        node.operand = new_child
    elif node.position_start is not None and last_child in node.position_start:
        idx = node.position_start.index(last_child)
        node.position_start[idx] = new_child
    elif node.result_dimensions is not None and last_child in node.result_dimensions:
        idx = node.result_dimensions.index(last_child)
        node.result_dimensions[idx] = new_child
    else:
        raise AssertionError("last_child не является потомком оператора среза")


@change_child.register(TokenOperatorIndex)
def _(node: TokenOperatorIndex, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert isinstance(new_child, TokenOperatorRvalueABC)
    if last_child is node.operand:
        node.operand = new_child
    elif last_child is node.index:
        node.index = new_child
    else:
        raise AssertionError("last_child не является потомком оператора индексации")


@change_child.register(TokenOperatorArrayCreation)
def _(node: TokenOperatorArrayCreation, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert isinstance(new_child, TokenOperatorRvalueABC)
    assert last_child in node.operands, "last_child не найден в списке операндов"
    idx = node.operands.index(last_child)
    node.operands[idx] = new_child


@change_child.register(TokenOperatorReferencing)
def _(node: TokenOperatorReferencing, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert isinstance(new_child, TokenOperatorWvalueABC)
    assert node.operand is last_child
    node.operand = new_child


@change_child.register(TokenOperatorDereferencing)
def _(node: TokenOperatorDereferencing, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert isinstance(new_child, TokenOperatorRvalueABC)
    assert node.operand is last_child
    node.operand = new_child


@change_child.register(ControlFunctionDefinition)
def _(node: ControlFunctionDefinition, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    raise ValueError("ControlFunctionDefinition не поддерживает change_child")


@change_child.register(ControlExpression)
def _(node: ControlExpression, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert node.first is last_child
    assert isinstance(new_child, (TokenOperatorWvalueABC, TokenOperatorRvalueABC))
    node.first = new_child


@change_child.register(TokenOperatorFieldAccess)
def _(node: TokenOperatorFieldAccess, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert node.operand is last_child
    assert isinstance(new_child, (TokenOperatorWvalueABC, TokenOperatorRvalueABC))
    node.first = new_child


@change_child.register(TokenOperatorFieldAccessPointer)
def _(node: TokenOperatorFieldAccessPointer, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert node.operand is last_child
    assert isinstance(new_child, (TokenOperatorWvalueABC, TokenOperatorRvalueABC))
    node.first = new_child


@change_child.register(TokenOperatorDeInitializer)
def _(node: TokenOperatorDeInitializer, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert node.operand is last_child
    assert isinstance(new_child, (TokenOperatorRvalueABC))
    node.first = new_child


@change_child.register(ControlReturn)
def _(node: ControlReturn, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert isinstance(new_child, TokenOperatorRvalueABC)
    assert last_child in node.results, "last_child не найден в возвращаемых значениях"
    idx = node.results.index(last_child)
    node.results[idx] = new_child


@change_child.register(ControlMassAssignment)
def _(node: ControlMassAssignment, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    if isinstance(last_child, TokenOperatorRvalueABC):
        # замена в правой части
        assert isinstance(new_child, TokenOperatorRvalueABC)
        assert last_child in node.right, "last_child не найден в правой части"
        idx = node.right.index(last_child)
        node.right[idx] = new_child
    else:
        # замена в левой части (предполагается TokenOperatorWvalueABC)
        assert isinstance(last_child, TokenOperatorWvalueABC)
        assert isinstance(new_child, TokenOperatorWvalueABC)
        assert last_child in node.left, "last_child не найден в левой части"
        idx = node.left.index(last_child)
        node.left[idx] = new_child


@change_child.register(ControlCodeBlock)
def _(node: ControlCodeBlock, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    raise ValueError("ControlCodeBlock не поддерживает change_child")


@change_child.register(ControlIf)
def _(node: ControlIf, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert isinstance(new_child, TokenOperatorRvalueABC)
    if new_child.res_type:
        assert new_child.res_type == t_bool
    node.condition = new_child


@change_child.register(ControlWhile)
def _(node: ControlWhile, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    assert isinstance(new_child, TokenOperatorRvalueABC)
    assert node.condition is last_child
    node.condition = new_child


@change_child.register(ControlCycleControl)
def _(node: ControlCycleControl, last_child: TokenOperatorABC, new_child: TokenOperatorABC) -> None:
    raise ValueError("ControlCycleControl не поддерживает change_child")
