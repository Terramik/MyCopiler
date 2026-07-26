from .Utils import *

expr = []
realization = {}
header = '''
#include <stdlib.h>
'''

module = Module(
    Module.Types.Standard, Path('mem'),
    ControlCodeBlock([
        make_f('alloc',
               [('size', types.uint64)],
               [types.int8p],
               expr, realization, '''
        return malloc(size);
        '''),
        make_f('free',
               [('p', types.int8p)],
               [], expr, realization, '''
        free(p);
        '''),
        make_f('realloc', [('start', types.int8p), ('new_size', types.uint64)],
               [types.int8p], expr, realization, '''
        return realloc(start, new_size);
        '''),
        make_v('NULL', types.int8p, expr, realization, '(int8_t*)0')
    ], zero_origin),
    export_=expr
)