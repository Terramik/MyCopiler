from .Utils import *
from ..Simple import *
from ..Types.Simple import TransferSlicingData
import pickle


__all__ = ('load_std_data', 'get_path_to_std_module', 'get_path_to_std_header')

path_to_file = Path(__file__).resolve().parent


def load_std_data() -> tuple[
    set[Type], set[TransferSlicingData], DataContainer
]:
    path = path_to_file / 'pickle_things'
    with open(path / 'all_types.pkl', 'rb') as f:
        all_types = pickle.load(f)
    with open(path / 'all_slices.pkl', 'rb') as f:
        all_slices = pickle.load(f)
    with open(path / 'data.pkl', 'rb') as f:
        data = pickle.load(f)

    return all_types, all_slices, data


def get_path_to_std_module(name: str) -> str:
    match name:
        case 'io':
            return (path_to_file / r'realization\src\io_our.c').as_posix()
        case 'math':
            return (path_to_file / r'realization\src\math_our.c').as_posix()
        case 'mem':
            return (path_to_file / r'realization\src\mem_our.c').as_posix()
        case 'rand':
            return (path_to_file / r'realization\src\rand_our.c').as_posix()
        case 'testing':
            return (path_to_file / r'realization\src\testing_our.c').as_posix()
        case 'time':
            return (path_to_file / r'realization\src\time_our.c').as_posix()
        case _:
            raise ValueError()


def get_path_to_std_header() -> str:
    return (path_to_file / r'realization\include').as_posix()
