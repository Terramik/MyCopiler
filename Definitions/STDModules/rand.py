from .Utils import *

expr = []
realization = {}
header = '''
#include <stdlib.h>
#include <time.h>
'''

module = Module(
    Module.Types.Standard, Path('rand'),
    ControlCodeBlock([
        make_f('seed', [('s', types.uint64)], [], expr, realization, '''
        srand((unsigned)s);
        '''),
        make_f('rand', [], [types.uint64], expr, realization, '''
        return rand();
        '''),
        make_f('rand_range', [('min', types.int64), ('max', types.int64)], [types.int64], expr, realization, '''
        return (int64_t)((uint64_t)rand() % (uint64_t)(max - min + 1)) + min;
        '''),
        make_f('randf', [], [types.float64], expr, realization, '''
        return (double)rand() / RAND_MAX;
        '''),
        make_f('randf_range', [('min', types.float64), ('max', types.float64)], [types.float64], expr, realization, '''
        return min + (double)rand() / RAND_MAX * (max - min);
        '''),
    ], zero_origin),
    export_=expr
)