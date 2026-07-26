from .Utils import *

"""
Заменяет все Enum.state на соответствующие литералы
"""


__all__ = ('turn_all_enums_to_constants',)


class ItExpr(IteratorExpression):
    def on_field_access(self, node: TokenOperatorFieldAccess, parent: TypeExpressionParent):
        if node.res_type.is_simple_enum_instance and node.operand.res_type.is_simple_enum:
            # заменяем
            enum = node.res_type.enum
            change_child(parent, node, enum.state_to_number[node.name])


    def on_var_access(self, node: TokenVariableAccess, parent: TypeExpressionParent):
        # хз, это просто костыль
        if node.res_type is not None and node.res_type.is_simple_enum:
            change_child(parent, node, TokenLiteral.from_raw(TokenRawLiteral('0', zero_origin)))


it = ItExpr()


class ItCont(IteratorControl):
    def __call__(self, control: ControlABC):
        super().__call__(control)


    def on_expr(self, exp: TokenOperatorWvalueABC | TokenOperatorRvalueABC, parent: ControlABC):
        it(exp, parent)


itc = ItCont()


class ItModule(IteratorModule):
    def on_module(self, module: Module):
        super().on_module(module)
        itc(module.code)

        # уберём импорт и экспорт перечислений
        module.export_ = list(filter(
            lambda x: not (isinstance(x.thing, TokenOperatorVariableDefinition) and x.thing.type.is_simple_enum),
            module.export_
        ))

        module.import_ = list(filter(
            lambda x: not (isinstance(x.thing, TokenOperatorVariableDefinition) and x.thing.type.is_simple_enum),
            module.import_
        ))


def turn_all_enums_to_constants(modules: Module | list[Module], data: DataContainer):
    ItModule().many_modules(modules)
