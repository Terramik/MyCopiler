from .Simple import *


__all__ = ('collect_slicing_functions', )


class ItExpr(IteratorExpression):
    def __init__(self, slices: set[TransferSlicingData]):
        self.slices = slices

    def on_slize(self, node: TokenOperatorSlize, parent: TypeExpressionParent):
        self.slices.add(TransferSlicingData(
                node.res_type, node.operand.res_type, len(node.position_start), len(node.result_dimensions)
        ))
        super().on_slize(node, parent)


class ItCont(IteratorControl):
    def __init__(self, exp: ItExpr):
        self.exp = exp

    def on_expr(self, exp: TokenOperatorWvalueABC | TokenOperatorRvalueABC, parent: ControlABC):
        self.exp(exp, parent)


class ItModule(IteratorModule):
    def __init__(self):
        self.slices = set()
        self.it_control = ItCont(ItExpr(self.slices))

    def on_module(self, module: Module):
        self.it_control(module.code)
        super().on_module(module)


def collect_slicing_functions(module: list[Module] | Module) -> set[TransferSlicingData]:
    it_module = ItModule()
    it_module.many_modules(module)
    return it_module.slices
