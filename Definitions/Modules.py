from __future__ import annotations
from .Tokens import ControlCodeBlock, TokenOperatorVariableDefinition, ControlTypedef, Type
from .Scopes import Scope
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum


__all__ = ('Module',)


@dataclass(slots=True)
class Module:
    class Types(Enum):
        Main = 'Main'
        Usual = 'Usual'
        Standard = 'Standard'

    type: Module.Types
    path_to_file: Path
    code: ControlCodeBlock
    scope: Scope | None = None
    fully_processed: bool = False
    imported_modules: list[Module] = field(default_factory=lambda: [])
    global_variables_initializer: str | None = None
    transfer_path: Path | None = None
    relative_path: Path | None = None
    path_h: Path | None = None
    path_c: Path | None = None


    @dataclass(slots=True, frozen=True)
    class ExportData:
        thing: ControlTypedef | TokenOperatorVariableDefinition
        alias: str # псевдоним, с которым экспортируем

    export_: list[Module.ExportData] = field(default_factory=lambda: [])

    def add_export(self, thing: ControlTypedef | TokenOperatorVariableDefinition, alias: str):
        self.export_.append(Module.ExportData(thing, alias))

    def find_export(self, name: str) -> Module.ExportData | None:
        for exp in self.export_:
            if exp.alias == name:
                return exp

    @dataclass(slots=True, frozen=True)
    class ImportData:
        from_: Module
        name: str # имя, с которым импортируем
        thing: ControlTypedef | TokenOperatorVariableDefinition

    def add_import(self, from_: Module, name: str, alias: str) -> ControlTypedef | TokenOperatorVariableDefinition | None:
        thing = from_.find_export(name).thing
        if thing is not None:
            if isinstance(thing, TokenOperatorVariableDefinition):
                new = TokenOperatorVariableDefinition(alias, thing.type, thing.origin)
            else:
                new = ControlTypedef(Type.Typedef(thing.typedef.type, alias), thing.origin)
            self.import_.append(Module.ImportData(from_, name, new))
            return new

    import_: list[Module.ImportData] = field(default_factory=lambda: [])

    @property
    def is_std(self) -> bool:
        return self.type == Module.Types.Standard

    @property
    def is_main(self) -> bool:
        return self.type == Module.Types.Main
