from .Utils import *


"""
В си нельзя создавать переменные прямо в выражениях. Поэтому мы заменим 
создания просто обращениями, а сами объявления сдвинем в начала их блоков кода.
"""


__all__ = ('move_all_vdef_to_beginning',)


class ItExpr(IteratorExpression):
    def __init__(self, code_block: ControlCodeBlock):
        self.code_block = code_block

    def on_var_def(self, node: TokenOperatorVariableDefinition, parent: TypeExpressionParent):
        # заменим объявление на обращение
        access = TokenVariableAccess(
            node.name, zero_origin, False, node
        )
        change_child(parent, node, access)
        # засунем объявление в начало
        def_expression = ControlExpression(
            node, zero_origin
        )
        self.code_block.block_parts.insert(0, def_expression)


class ItCont(IteratorControl):
    def __init__(self, data: DataContainer):
        self.data = data
        self.code_blocks = []

    def on_code_block(self, code: ControlCodeBlock):
        self.code_blocks.append(code)
        super().on_code_block(code)
        self.code_blocks.pop()

    def on_expr(self, exp: TokenOperatorWvalueABC | TokenOperatorRvalueABC, parent: ControlABC):
        self.code_blocks: list[ControlCodeBlock]
        ItExpr(
            self.code_blocks[-1]
               )(
            exp, parent
        )


class ItModule(IteratorModule):
    def __init__(self, data: DataContainer):
        self.it_control = ItCont(data)

    def on_module(self, module: Module):
        self.it_control(module.code)
        super().on_module(module)


def move_all_vdef_to_beginning(modules: Module | list[Module], data: DataContainer):
    """
    Заменяет все создания переменных в выражениях на обращения к ним,
    а их самих двигает в начало блока в их собственных выражениях.
    """
    it_module = ItModule(data)
    it_module.many_modules(modules)




