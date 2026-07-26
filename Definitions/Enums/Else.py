from enum import Enum


class KeyWords(Enum):
    Function = 'def'
    Return = 'return'
    Variable = 'var'
    ConditionalStart = 'if'
    ConditionalMiddle = 'elif'
    ConditionalEnd = 'else'
    CycleWhile = 'while'
    CycleControlBreak = 'break'
    CycleControlContinue = 'continue'
    Lenof = 'lenof'
    Sizeof = 'sizeof'
    Cast = 'as'
    FunctionTypeDeclarator = 'func'
    Typedef = 'alias'
    Import_Part1 = 'from'
    Import_Part2 = 'import'
    Export = 'export'
    Import_Export_Alias = 'as'
    Import_Export_All = 'all'
    Modules_std = 'std'
    Class_Definition = 'class'
    DeInitializer = 'del'
    Enum_Definition = 'enum'


class KeySymbols(Enum):
    BracketOpen = '('
    BracketClose = ')'
    BraceOpen = '{'
    BraceClose = '}'
    SquareBracketOpen = '['
    SquareBracketClose = ']'
    Arrow = '->'
    Semicolon = ';'
    Separator = ','
    Point = '.'


class TokenLiteralTypes(Enum):
    Int = 'int'
    Float = 'float'
    Str = 'str'
    Bool = 'bool'
    Char = 'char'


class ConditionalPartTypes(Enum):
    start = 1
    middle = 2
    end = 3


class CycleControlTypes(Enum):
    break_ = 1
    continue_ = 2


