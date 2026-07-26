from .Simple import *
from .Pointer import transfer_pointer_slice
from .Array import transfer_array_slice
from .Slice import transfer_slice_slice


__all__ = ('make_slicing_functions',)


def make_slicing_functions(file: TextIO, data: DataContainer, slice_data: set[TransferSlicingData]):
    """
    Создаёт функции для создания среза.
    """

    for slice in slice_data:
        if slice.arg_type.is_mod_pointer:
            transfer_pointer_slice(file, data, slice)
        elif slice.arg_type.is_mod_array:
            transfer_array_slice(file, data, slice)
        elif slice.arg_type.is_mod_slize:
            transfer_slice_slice(file, data, slice)
        else:
            raise ValueError('что-то пошло не так')









































