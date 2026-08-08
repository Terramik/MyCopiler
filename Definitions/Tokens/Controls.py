from __future__ import annotations

from .Operators import *
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..Base import *
from ..Enums import *
from .. import TypesShortener as types


class ControlABC(ABC):
    @abstractmethod
    def change_child(self, last_child: TokenOperatorABC, new_child: TokenOperatorABC):
        """
        На стадии обработки выражений используется для модификации ast
        """
        pass


@dataclass(slots=True)
class ControlFunctionDefinition(ControlABC):
    name: str
    parameters: list['TokenOperatorVariableDefinition']
    results: list[Type]
    code_block: 'ControlCodeBlock'
    origin: TokenOrigin
    # внешние переменные, используемые в этой функции
    outer_variables: list['TokenOperatorVariableDefinition'] = field(default_factory=lambda: [])
    # внешние переменные, используемые во внутренних функциях этой функции
    outer_variables_inner: list['TokenOperatorVariableDefinition'] = field(default_factory=lambda: [])
    # все внешние переменные
    outer_variables_all: list['TokenOperatorVariableDefinition'] = field(default_factory=lambda: [])
    # имя структуры для замыкания
    enclosure_struct_name: str | None = None
    global_name: str | None = None
    # переменная, куда "кладётся" функция
    var: TokenOperatorVariableDefinition | None = None
    # является ли функция __init__ класса, если это оно, то там будет лежать имя переменной собственно экзепляра.
    is_class_init: None | str = None
    is_bad: bool = False

    def __repr__(self):
        return (f'{KeyWords.Function.value} {self.name} ({', '.join(map(repr, self.parameters))}) -> '
                f'({', '.join(map(repr, self.results))})\n {self.code_block}')
    
    def change_child(self, last_child: TokenOperatorABC, new_child: TokenOperatorABC):
        raise ValueError('')


@dataclass(slots=True)
class ControlExpression(ControlABC):
    first: TokenOperatorRvalueABC | TokenOperatorWvalueABC
    origin: TokenOrigin

    def __repr__(self):
        return f'{self.first}; '

    def change_child(self, last_child: TokenOperatorABC, new_child: TokenOperatorABC):
        assert last_child is self.first
        assert isinstance(new_child, (TokenOperatorWvalueABC, TokenOperatorRvalueABC))
        self.first = new_child


@dataclass(slots=True)
class ControlReturn(ControlABC):
    results: list[TokenOperatorRvalueABC]
    origin: TokenOrigin
    func: 'ControlFunctionDefinition' | None = None
    is_bad: bool = False

    def __repr__(self):
        return f'return {', '.join((repr(n) for n in self.results))};'

    def change_child(self, last_child: TokenOperatorABC, new_child: TokenOperatorABC):
        assert isinstance(new_child, TokenOperatorRvalueABC)
        assert isinstance(last_child, TokenOperatorRvalueABC)
        assert last_child is self.results
        self.results[self.results.index(last_child)] = new_child


@dataclass(slots=True)
class ControlMassAssignment(ControlABC):
    left: list[TokenOperatorWvalueABC]
    right: list[TokenOperatorRvalueABC]
    origin: TokenOrigin
    processed: list['ControlMassAssignment.Inner'] = field(default_factory=list)
    is_bad: bool = False

    @dataclass(slots=True)
    class Inner:
        """
        Штука нужна для того, что понять, сколько каких wvalue нужно на 1 rvalue, и к каким типам нужно преобразовывать
        """
        rvalue: TokenOperatorRvalueABC
        wvalues: list[int] #list[TokenOperatorWvalueABC]
        t_need: list[Type | None]

    def __repr__(self):
        if self.processed:
            return f'{', '.join(map(repr, self.left))} = {', '.join(
                f'({', '.join(map(lambda x: '...' if x is None else repr(x), p.t_need))}) ({repr(p.rvalue)})'
                for p in self.processed
            )}; '
        else:
            return f'{', '.join(map(repr, self.left))} = {', '.join(map(repr, self.right))}; '

    def change_child(self, last_child: TokenOperatorABC, new_child: TokenOperatorABC):
        if isinstance(last_child, TokenOperatorRvalueABC):
            assert isinstance(new_child, TokenOperatorRvalueABC)
            assert last_child is self.right
            self.right[self.right.index(last_child)] = new_child
        else:
            assert isinstance(last_child, TokenOperatorWvalueABC)
            assert isinstance(new_child, TokenOperatorWvalueABC)
            assert last_child is self.left
            self.left[self.left.index(last_child)] = new_child


@dataclass(slots=True)
class ControlCodeBlock(ControlABC):
    block_parts: list[ControlABC]
    origin: TokenOrigin

    def __repr__(self):
        return f'{{\n\t{'\n\t'.join(map(repr, self.block_parts))}\n}}'

    def change_child(self, last_child: TokenOperatorABC, new_child: TokenOperatorABC):
        raise ValueError('')


@dataclass(slots=True)
class ControlIf(ControlABC):
    condition: TokenOperatorRvalueABC
    block_if: ControlCodeBlock
    block_else: ControlCodeBlock
    origin: TokenOrigin
    is_bad: bool = False

    def __repr__(self):
        return (
            f'{KeyWords.ConditionalStart.value} ({self.condition}) \n{self.block_if}'
            f'{KeyWords.ConditionalEnd.value} {self.block_else}\n'
        )

    def change_child(self, last_child: TokenOperatorABC, new_child: TokenOperatorABC):
        assert isinstance(new_child, TokenOperatorRvalueABC)
        if new_child.res_type:
            assert new_child.res_type == t_bool
        self.condition = new_child


@dataclass(slots=True)
class ControlWhile(ControlABC):
    condition: TokenOperatorRvalueABC
    code_block: ControlCodeBlock
    origin: TokenOrigin
    is_bad: bool = False

    def __repr__(self):
        return f'while {repr(self.condition)} \n {self.code_block}'

    def change_child(self, last_child: TokenOperatorABC, new_child: TokenOperatorABC):
        assert isinstance(new_child, TokenOperatorRvalueABC)
        assert last_child is self.condition
        self.condition = new_child


@dataclass(slots=True)
class ControlCycleControl(ControlABC):
    type: CycleControlTypes
    origin: TokenOrigin

    def __repr__(self):
        match self.type:
            case CycleControlTypes.break_: return KeyWords.CycleControlBreak.value + ';'
            case CycleControlTypes.continue_: return KeyWords.CycleControlContinue.value + ';'

    def change_child(self, last_child: TokenOperatorABC, new_child: TokenOperatorABC):
        raise ValueError('')


@dataclass(slots=True)
class ControlTypedef(ControlABC):
    typedef: Type.Typedef
    origin: TokenOrigin

    def __repr__(self):
        return f'{KeyWords.Typedef.value} {self.typedef.name} {self.typedef.type}'

    def change_child(self, last_child: TokenOperatorABC, new_child: TokenOperatorABC):
        raise ValueError('')


@dataclass(slots=True)
class ControlImport(ControlABC):
    path: str
    all: bool
    names: list[tuple[str, str]]
    origin: TokenOrigin
    is_allowed: bool = False

    def __repr__(self):
        return (f'{KeyWords.Import_Part1} {self.path} '
                f'{KeyWords.Import_Part2} {', '.join(f'{n[0]} as {n[1]}' for n in self.names)};')

    def change_child(self, last_child: TokenOperatorABC, new_child: TokenOperatorABC):
        raise ValueError('')


@dataclass(slots=True)
class ControlExport(ControlABC):
    all: bool
    names: list[tuple[str, str]]
    origin: TokenOrigin

    def __repr__(self):
        return f'{KeyWords.Export} {', '.join(f'{n[0]} as {n[1]}' for n in self.names)};'

    def change_child(self, last_child: TokenOperatorABC, new_child: TokenOperatorABC):
        raise ValueError('')


@dataclass(slots=True)
class ControlClass(ControlABC):
    name: str
    instance_field: list[TokenOperatorVariableDefinition]
    rest: ControlCodeBlock
    origin: TokenOrigin
    # эти поля для работы с классом как с классом
    class_var: TokenOperatorVariableDefinition | None = None # переменная, где лежит сам собственно класс
    class_field: list[TokenOperatorVariableDefinition] = field(default_factory=list)
    magic_methods: dict[str, ControlFunctionDefinition] = field(default_factory=dict)
    scope: 'Scope' | None = None
    data_for_std: str | None = None
    is_bad: bool = False

    def __repr__(self):
        return f'{KeyWords.Class_Definition} {self.name} {{ {{{self.instance_field}}} {self.rest}}}'

    def change_child(self, last_child: TokenOperatorABC, new_child: TokenOperatorABC):
        assert last_child is self.rest
        assert isinstance(new_child, ControlCodeBlock)
        self.rest = new_child

    def find_instance_field(self, name: str) -> TokenOperatorVariableDefinition | None:
        for var in self.instance_field:
            if var.name == name:
                return var

    def find_class_field(self, name: str) -> TokenOperatorVariableDefinition | None:
        for name_, magic in self.magic_methods.items():
            if name_ == name:
                return magic.var

        for var in self.class_field:
            if var.name == name:
                return var
        # если инита нет, а он нужен, то сделаем его
        if name == '__init__':
            # если нет полей, то экзепляра нет, и __init__ тоже
            if len(self.instance_field) == 0:
                return
            from ..Scopes import Scope
            # переменная что будет в __init__
            self_var = TokenOperatorVariableDefinition(
                'self', types.class_instance(self), self.origin
            )
            # просто def __init__(self Class) -> (Class) {return self;}
            ret = ControlReturn([
                        TokenVariableAccess('self', self.origin, False, self_var)
                ], self.origin)

            init = ControlFunctionDefinition(
                '__init__', [], [types.class_instance(self)],
                ControlCodeBlock([
                    ret
                ], self.origin), self.origin
            )
            f_var = TokenOperatorVariableDefinition('__init__', types.func([], [types.class_instance(self)]), self.origin)
            init.var = f_var
            init.is_class_init = 'self'
            ret.func = init
            # теперь добавим всё это дело в скоупы
            init_scope = Scope(Scope.Types.Function, init, self.scope)
            self.scope.add_child(init_scope)
            init_scope.add_variable(self_var)
            self.scope.add_function(init)
            self.scope.add_variable(f_var)
            # и теперь в наши поля
            self.magic_methods['__init__'] = init
            self.class_field.append(f_var)
            return f_var

    def is_bool(self) -> bool:
        return '__bool__' in self.magic_methods

    def is_del(self) -> bool:
        return '__del__' in self.magic_methods

    def __eq__(self, other):
        if not isinstance(other, ControlClass):
            return False
        return self.name == other.name # надо написать что-то лучше

    def __hash__(self):
        return hash(self.name) # действительно надо


@dataclass(slots=True)
class ControlEnum(ControlABC):
    name: str
    states: list[str]
    origin: TokenOrigin
    # в процессе анализа
    enum_var: TokenOperatorVariableDefinition | None = None # переменная с перечислением
    states_vars: list[TokenOperatorVariableDefinition] | None = None # переменные с собственно состояниями
    state_to_number: dict[str, TokenOperatorRvalueABC] = field(default_factory=dict) # для трансляции
    is_bad: bool = False

    def find_var(self, name: str) -> TokenOperatorVariableDefinition | None:
        assert self.states_vars
        for var in self.states_vars:
            if var.name == name:
                return var

    def __repr__(self):
        return f'{KeyWords.Enum_Definition.value} {self.name} {{{''.join(f'{s};' for s in self.states)}}}'

    def change_child(self, last_child: TokenOperatorABC, new_child: TokenOperatorABC):
        return NotImplementedError('')

    def __eq__(self, other):
        if not isinstance(other, ControlEnum):
            return False
        return self.name == other.name and self.states == other.states

    def __hash__(self):
        return hash(self.name)


