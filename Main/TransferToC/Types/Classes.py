from .Simple import *


def transfer_class_instance(file: TextIO, data: DataContainer, t: Type):
    cls = t.cls
    assert isinstance(cls, ControlClass)

    instance_name = get_unique_name(data.all_names, f'{cls.name}instance')

    # костыль для std
    if cls.data_for_std is not None:
        file.write(
        'typedef struct {'
            f'{cls.data_for_std}'
        '}' f'{instance_name};\n'
        )
    else:
        # просто структура
        file.write(
            'typedef struct {'
                f'{''.join(
                    f'{data.type_to_name[fld.type]} {fld.name};'
                    for fld in cls.instance_field
                )}'
            '}' f'{instance_name};\n'
        )
    data.type_to_name[
        Type(Type.SimpleTypeClassInstance(cls), [])
    ] = instance_name


def transfer_class_itself(file: TextIO, data: DataContainer, t: Type):
    cls = t.cls
    assert isinstance(cls, ControlClass)

    # структура для класса
    class_name = get_unique_name(data.all_names, f'{cls.name}type')

    file.write(
        'typedef struct {'
            f'{''.join(
                f'{
                    f'{data.type_to_name[fld.type]} {fld.name};'
                    if not (fld.type.is_simple_func and fld.type.is_mod_usual) else
                    f'{data.type_func_to_enclosure_struct[fld.type]} {fld.name};'
                }'
                
                for fld in cls.class_field
            )}'
        '}' f'{class_name};\n'
    )
    data.type_to_name[cls.class_var.type] = class_name

