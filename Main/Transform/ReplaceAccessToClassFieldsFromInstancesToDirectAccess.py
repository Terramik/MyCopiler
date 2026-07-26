from ...Definitions.Scopes import Scope
from ...Definitions.TreeInterface import IteratorExpression, IteratorControl
from ...Definitions.Tokens import *

"""
Должен замени обращение к полям класс через его экземпляр на прямое обращение через класс
(obj.class_field -> class.class_field)
"""


__all__ = ('replace_access_to_class_fields_from_instances_to_direct_access',)


class ItExpr(IteratorExpression):
    def on_f_call(self, node: TokenOperatorFunctionCall, parent: TypeExpressionParent):
        super().on_f_call(node, parent)


    def on_field_access(self, node: TokenOperatorFieldAccess, parent: TypeExpressionParent):
        # в обратном порядке
        super().on_field_access(node, parent)

        operand = node.operand
        # оно должно быть экземпляром
        if operand.res_type.is_simple_class_instance:
            cls = operand.res_type.cls
            assert isinstance(cls, ControlClass)
            # мы не нашли поля в экзепляре - значит оно из класса
            if cls.find_instance_field(node.name) is None:
                # заменим операнд на обращение к переменной класса
                new_operand = TokenVariableAccess(cls.name, operand.origin, False, cls.class_var)
                node.operand = new_operand

    # тоже самое
    def on_field_access_pointer(self, node: TokenOperatorFieldAccess, parent: TypeExpressionParent):
        # в обратном порядке
        super().on_field_access(node, parent)

        operand = node.operand
        if operand.res_type.is_simple_class_instance:
            cls = operand.res_type.cls
            assert isinstance(cls, ControlClass)
            if cls.find_instance_field(node.name) is None:
                # заменим операнд на обращение к переменной класса
                new_operand = TokenVariableAccess(cls.name, operand.origin, False, cls.class_var)
                # а сам нод на обычный доступ к полю
                new_node = TokenOperatorFieldAccess(
                    new_operand, node.name, node.origin, node.res_type, cls.find_class_field(node.name)
                )
                change_child(parent, node, new_node)


class ItCont(IteratorControl):
    def on_expr(self, exp: TokenOperatorWvalueABC | TokenOperatorRvalueABC, parent: ControlABC):
        ItExpr()(exp, parent)


def replace_access_to_class_fields_from_instances_to_direct_access(code: ControlCodeBlock, scope: Scope):
    ItCont()(code)
