from pathlib import Path
from ...Definitions.Modules import Module
from ...Definitions.Exceptions import OurSyntaxError, SemanticError
from ...Definitions.Tokens import *
from ..Modules import analyze_module
from .PositionToNode import position_to_node, position_to_node_with_scope


modules = {}

mod_path = Path(r'C:\Coding\Python\Two\Test\TheLanguage\test2\scripts\game_of_life\main.mylang')


analyze_module(mod_path, modules)
with open(mod_path, 'r') as f:
    lines = f.read().split('\n')


# to_find = TextPosition(12, 21)
# to_find = TextPosition(41, 11)
# to_find = TextPosition(42, 10)
to_find = TextPosition(43, 10)

print(lines[to_find.line])
print(' ' * (to_find.column - 1) + '^')


def completion():
    # где мы
    mod = modules[mod_path]
    pos = to_find

    res = []

    tok, scope = position_to_node_with_scope(
        mod, pos
    )

    if isinstance(tok, (TokenOperatorFieldAccess, TokenOperatorFieldAccessPointer)):
        op_type = tok.operand.res_type
        if op_type != t_error:
            if op_type.is_simple_class or op_type.is_simple_class_instance:
                cls: ControlClass = op_type.cls
                if not cls.is_bad:
                    if tok.operand.res_type.is_simple_class_instance:
                        for f in cls.instance_field:
                            res.append(f.name)
                    for f in cls.class_field:
                        res.append(f.name)
            elif op_type.is_simple_enum:
                enum: ControlEnum = op_type.enum
                if not enum.is_bad:
                    for f in enum.states:
                        res.append(f)

    else:
        while True:
            if scope.is_global:
                res.append('GLOB_STUFF')
                break

            for var in scope.variables:
                res.append(var.name)
            for typedef in scope.typedefs:
                res.append(typedef.typedef.name)
            if scope.is_global:
                break
            scope = scope.parent
        res.append('TYPE_STUFF')
        res.append('KEY_WORDS_STUFF')

    return res


for l in completion():
    print(l)

# print()
# print(type(node))
# print(scope.type)
# print('VARS')
# for v in scope.variables:
#     print(v.name)


# if type(node) == ControlFunctionDefinition:
#     print(node.name)
# else:
#     print(node)

