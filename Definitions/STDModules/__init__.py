from .io import module as io, realization as io_realization, header as io_header
from .mem import module as mem, realization as mem_realization, header as mem_header
from .time import module as time, realization as time_realization, header as time_header
from .math import module as math, realization as math_realization, header as math_header
from .rand import module as rand, realization as rand_realization, header as rand_header
from .testing import module as testing, realization as testing_realization, header as testing_header

__all__ = ('std_modules', 'std_realization', 'std_headers')

std_modules = {
    'io': io,
    'mem': mem,
    'time': time,
    'math': math,
    'rand': rand,
    'testing': testing,
}

std_realization = {
    'io': io_realization,
    'mem': mem_realization,
    'time': time_realization,
    'math': math_realization,
    'rand': rand_realization,
    'testing': testing_realization,
}

std_headers = {
    'io': io_header,
    'mem': mem_header,
    'time': time_header,
    'math': math_header,
    'rand': rand_header,
    'testing': testing_header,
}


