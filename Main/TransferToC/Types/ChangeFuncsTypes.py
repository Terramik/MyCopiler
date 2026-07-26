from .Simple import *


def change_funcs_types(data: DataContainer):
    """
    Меняет типы функций с их типов на структуры-замыкания
    """
    for type, name in data.type_func_to_enclosure_struct.items():
        data.type_to_name[type] = name






