from __future__ import annotations
from ..Analyze_test.Simple import *
from ...Definitions.Modules import *
from ...Definitions import STDModules as std

# @dataclass(slots=True)
class CheckModule(CheckNode):
    type: Module.Types
    code: CheckControlCodeBlock
    scope: CheckScope
    import_: list[CheckImportData]
    export_: list[CheckExportData]
    imported_modules: list[CheckModule]
    mod: Module | None

    # вы возможно спросите, почему тут стоит __init__ а не датакласс, как обычно?
    # дело в том, что пайчарм почему очень не хочет отображать аргументы инита из датакласса.
    def __init__(self, type: Module.Types, code: CheckControlCodeBlock, scope: CheckScope,
                 import_: list[CheckImportData], export_: list[CheckExportData],
                 imported_modules: list[CheckModule], mod: Module | None = None):
        self.type = type
        self.code = code
        self.scope = scope
        self.import_ = import_
        self.export_ = export_
        self.imported_modules = imported_modules
        self.mod = mod

    @classmethod
    def std(cls, std_module: Module) -> CheckModule:
        return CheckModule(
            Module.Types.Standard, None, None, None, None, None, std_module
        )

    @dataclass(slots=True)
    class CheckExportData(CheckNode):
        alias: str
        thing: CheckControlTypedef | CheckTokenOperatorVariableDefinition

        def is_match(self, node: Module.ExportData):
            assert isinstance(node, Module.ExportData)
            assert self.alias == node.alias
            self.thing.is_match(node.thing)

    @dataclass(slots=True)
    class CheckImportData(CheckNode):
        name: str
        thing: CheckControlTypedef | CheckTokenOperatorVariableDefinition

        def is_match(self, node: Module.ImportData):
            assert isinstance(node, Module.ImportData)
            assert self.name == node.name
            self.thing.is_match(node.thing)

    def is_match(self, node: Module):
        if self.type == Module.Types.Standard:
            assert self.mod is node
        else:
            assert isinstance(node, Module)
            assert self.type == node.type
            self.code.is_match(node.code)
            self.scope.is_match(node.scope)

            assert len(self.import_) == len(node.import_)
            import_ = self.import_[:]
            for imp_h in node.import_:
                for imp_n in import_:
                    if imp_n.name == imp_h.name:
                        imp_n.is_match(imp_h)
                        import_.remove(imp_n)
            assert len(import_) == 0

            assert len(self.export_) == len(node.export_)
            export_ = self.export_[:]
            for exp_h in node.export_:
                for exp_n in export_:
                    if exp_n.alias == exp_h.alias:
                        exp_n.is_match(exp_h)
                        export_.remove(exp_n)
            assert len(export_) == 0

            check_list(self.imported_modules, node.imported_modules)




