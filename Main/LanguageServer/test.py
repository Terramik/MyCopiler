from pathlib import Path
from ...Definitions.Modules import Module
from ...Definitions.Exceptions import OurSyntaxError, SemanticError
from ...Definitions.Tokens import *
from ..Modules import analyze_module
from .PositionToNode import position_to_node, position_to_node_with_scope


modules = {}

mod_path = Path(r'C:\Coding\Python\Two\Test\TheLanguage\test2\scripts\game_of_life\main.mylang')


analyze_module(mod_path, modules)


to_find = TextPosition(11, 33)

node = position_to_node(modules[mod_path], to_find)
print(type(node))

if type(node) == ControlFunctionDefinition:
    print(node.name)
else:
    print(node)


