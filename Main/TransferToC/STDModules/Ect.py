from .Utils import *
from ..Simple import *
from ..Types.Simple import TransferSlicingData
import pickle


__all__ = ('load_std_data', 'get_path_to_std_module', 'get_path_to_std_header')


def load_std_data() -> tuple[
    set[Type], set[TransferSlicingData], DataContainer
]:
    file_path = Path(__file__).parent / 'pickle_things'
    with open(file_path / 'all_types.pkl', 'rb') as f:
        all_types = pickle.load(f)
    with open(file_path / 'all_slices.pkl', 'rb') as f:
        all_slices = pickle.load(f)
    with open(file_path / 'data.pkl', 'rb') as f:
        data = pickle.load(f)

    return all_types, all_slices, data


def get_path_to_std_module(name: str) -> str:
    match name:
        case 'io':
            return r'C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\io_our.c'
        case 'math':
            return r'C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\math_our.c'
        case 'mem':
            return r'C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\mem_our.c'
        case 'rand':
            return r'C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\rand_our.c'
        case 'testing':
            return r'C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\testing_our.c'
        case 'time':
            return r'C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\src\time_our.c'
        case _:
            raise ValueError()


def get_path_to_std_header() -> str:
    return r'C:\Coding\Python\Two\Test\TheLanguage\test\V6\Main\TransferToC\STDModules\realization\include'
