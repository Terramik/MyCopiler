from ...Definitions.Scopes import Scope
from ...Definitions.TreeInterface import IteratorExpression, IteratorControl
from ...Definitions.Tokens import *


"""
Должен заменить преобразование класса (as) на явный вызов нужного метода
"""




class ItExpr(IteratorExpression):
    def on_f_call(self, node: TokenOperatorFunctionCall, parent: TypeExpressionParent):
        super().on_f_call(node, parent)

    def on_cast(self, node: TokenOperatorCast, parent: TypeExpressionParent):
        if node.operand.res_type.is_simple_class_instance and node.operand.res_type.is_mod_usual:
            assert node.cast_type == t_bool
            cls = node.operand.res_type.cls
            assert isinstance(cls, ControlClass)
            # заменим obj as bool на Cls.__bool__(obj)
            new_node = TokenOperatorFunctionCall(
                TokenOperatorFieldAccess(
                    TokenVariableAccess(
                        cls.name, node.origin, False, cls.class_var
                    ), '__bool__', node.origin,
                    Type(Type.SimpleTypeFunc([node.operand.res_type], [t_bool]), []),
                    cls.find_class_field('__bool__')
                ),
                [
                    node.operand
                ], node.origin,
                t_bool
            )
            change_child(parent, node, new_node)


class ItCont(IteratorControl):
    def on_expr(self, exp: TokenOperatorWvalueABC | TokenOperatorRvalueABC, parent: ControlABC):
        ItExpr()(exp, parent)


def replace_class_instance_cast_to_explicit_method_use(code: ControlCodeBlock, scope: Scope):
    ItCont()(code)
