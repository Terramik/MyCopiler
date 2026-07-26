# math.py
from .Utils import *

expr = []
realization = {}
header = '''
#include <math.h>
'''

module = Module(
    Module.Types.Standard, Path('math'),
    ControlCodeBlock([
        make_f('abs', [('f', types.float64)], [types.float64], expr, realization, '''
        return fabs(f);
        '''),
        make_f('absi', [('i', types.int64)], [types.int64], expr, realization, '''
        return (i < 0) ? -i : i;
        '''),
        make_f('sin', [('f', types.float64)], [types.float64], expr, realization, '''
        return sin(f);
        '''),
        make_f('cos', [('f', types.float64)], [types.float64], expr, realization, '''
        return cos(f);
        '''),
        make_f('tan', [('f', types.float64)], [types.float64], expr, realization, '''
        return tan(f);
        '''),
        make_f('asin', [('f', types.float64)], [types.float64], expr, realization, '''
        return asin(f);
        '''),
        make_f('acos', [('f', types.float64)], [types.float64], expr, realization, '''
        return acos(f);
        '''),
        make_f('atan', [('f', types.float64)], [types.float64], expr, realization, '''
        return atan(f);
        '''),
        make_f('atan2', [('x', types.float64), ('y', types.float64)], [types.float64], expr, realization, '''
        return atan2(y, x);
        '''),
        make_f('exp', [('f', types.float64)], [types.float64], expr, realization, '''
        return exp(f);
        '''),
        make_f('log', [('f', types.float64)], [types.float64], expr, realization, '''
        return log(f);
        '''),
        make_f('log2', [('f', types.float64)], [types.float64], expr, realization, '''
        return log2(f);
        '''),
        make_f('log10', [('f', types.float64)], [types.float64], expr, realization, '''
        return log10(f);
        '''),
        make_f('pow', [('base', types.float64), ('power', types.float64)], [types.float64], expr, realization, '''
        return pow(base, power);
        '''),
        make_f('sqrt', [('f', types.float64)], [types.float64], expr, realization, '''
        return sqrt(f);
        '''),
        make_f('floor', [('f', types.float64)], [types.float64], expr, realization, '''
        return floor(f);
        '''),
        make_f('round', [('f', types.float64)], [types.float64], expr, realization, '''
        return round(f);
        '''),
        make_f('ceil', [('f', types.float64)], [types.float64], expr, realization, '''
        return ceil(f);
        '''),
        make_f('clamp', [('f', types.float64), ('min', types.float64), ('max', types.float64)], [types.float64], expr, realization, '''
        if (f < min) return min;
        if (f > max) return max;
        return f;
        '''),
        make_v('PI', types.float64, expr, realization, '3.141592653589793238462643383279'),
        make_v('E', types.float64, expr, realization, '2.718281828459045235360287471352'),
    ], zero_origin),
    export_=expr
)