from .Simple import *
from math import log2, ceil


def transfer_enum(file: TextIO, data: DataContainer, t: Type):
    enum = t.enum
    assert isinstance(enum, ControlEnum)
    elements_num_l2 = ceil(log2(len(enum.states)))
    instance_type = Type(Type.SimpleTypeEnumInstance(enum), [])

    if elements_num_l2 < 8:
        data.type_to_name[instance_type] = data.type_to_name[types.uint8]
    elif elements_num_l2 < 16:
        data.type_to_name[instance_type] = data.type_to_name[types.uint16]
    elif elements_num_l2 < 32:
        data.type_to_name[instance_type] = data.type_to_name[types.uint32]
    elif elements_num_l2 < 64:
        data.type_to_name[instance_type] = data.type_to_name[types.uint64]
    else:
        raise ValueError(f'Ну я даже не знаю что сказать.... ты мощный. более чем 18446744073709551615 состояний?')

    # теперь присвоим каждому имени свой литерал
    i = -1
    enum.state_to_number = {
        var.name: TokenLiteral.from_raw(TokenRawLiteral(str(i := (i + 1)), zero_origin)) for var in enum.states_vars
    }

