from .Utils import *

expr = []
realization = {}
header = '''
#include <stdio.h>
#include <stdlib.h>
'''

module = Module(
    Module.Types.Standard, Path('testing'),
    ControlCodeBlock([
        make_f('assert', [('cond', types.bool), ('msg', types.str)], [], expr, realization, '''
        if (!cond) {
            printf("%s", msg.start);
            abort();
        }
        '''),
        make_f('abort', [], [], expr, realization, '''
        abort();
        '''),
    ], zero_origin),
    export_=expr
)