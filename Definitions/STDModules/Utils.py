from ..Modules import *
from ..Tokens import *
from .. import TypesShortener as types
from ..Enums import magic_methods
from pathlib import Path


zero_path = Path('')
zero_code_block = ControlCodeBlock([], zero_origin)


def make_f(name: str, args: list[tuple[str, Type]], res: list[Type],
           export_data: list, real_dict: dict, real: str, export: bool = True) -> ControlFunctionDefinition:
    var_defs = [TokenOperatorVariableDefinition(d[0], d[1], zero_origin) for d in args]
    nontrue_name = f'{name}_our'
    var = TokenOperatorVariableDefinition(nontrue_name,
                                          Type(Type.SimpleTypeFunc([d[1] for d in args], res), [],
                                               zero_origin), zero_origin)

    if export:
        export_data.append(Module.ExportData(
            var, name
        ))
        real_dict[nontrue_name] = real

    return ControlFunctionDefinition(
        nontrue_name, var_defs, res, zero_code_block, zero_origin,
        var=var
    )


def make_v(name: str, type: Type, export_data: list, real_dict: dict, real: str):
    nontrue_name = f'{name}_our'
    var = TokenOperatorVariableDefinition(nontrue_name, type, zero_origin)

    export_data.append(Module.ExportData(
        var, name
    ))
    real_dict[nontrue_name] = real

    return ControlExpression(var, zero_origin)


def make_cls(name: str, export_data: list, real_dict: dict, real_field: str) -> ControlClass:
    nontrue_name = f'{name}_our'

    cls = ControlClass(nontrue_name, [], ControlCodeBlock([], zero_origin), zero_origin)
    cls_var = TokenOperatorVariableDefinition(
        nontrue_name, types.class_type(cls), zero_origin
    )
    cls.class_var = cls_var
    export_data.append(Module.ExportData(
        cls_var, name
    ))
    cls.data_for_std = real_field # время костылей
    real_dict[nontrue_name] = real_field

    return cls


def make_cls_f(cls: ControlClass, name: str, args: list[tuple[str, Type]], res: list[Type],
           export_data: list, real_dict: dict, real: str):

    f = make_f(name, args, res, export_data, real_dict, real, False)
    if name in magic_methods:
        cls.magic_methods[name] = f
    f.name = name
    f.var.name = name
    real_dict[(cls.name, f.name)] = real

    if name == '__init__':
        f.is_class_init = f.parameters[0].name
        # теперь, уберём self из аргументов, так как это скорее для нотации
        f.parameters = f.parameters[1:]
        f.var.type = Type(
            Type.SimpleTypeFunc(
                f.var.type.simple.arguments[1:], f.var.type.simple.results
            ), f.var.type.modifiers
        )

    cls.class_field.append(f.var)
    cls.rest.block_parts.append(f)

