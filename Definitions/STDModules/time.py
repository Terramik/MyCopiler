# time.py
from .Utils import *

expr = []
realization = {}
header = '''
#include <time.h>

#ifdef _WIN32
    #include <windows.h>
#endif
'''

module = Module(
    Module.Types.Standard, Path('time'),
    ControlCodeBlock([
        make_f('now', [], [types.int64], expr, realization, '''
#ifdef _WIN32
    LARGE_INTEGER counter, freq;
    QueryPerformanceCounter(&counter);
    QueryPerformanceFrequency(&freq);
    return (int64_t)((double)counter.QuadPart * 1e9 / freq.QuadPart);
#else
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (int64_t)ts.tv_sec * 1000000000LL + ts.tv_nsec;
#endif
        '''),

        make_f('sleep', [('ns', types.int64)], [], expr, realization, '''
#ifdef _WIN32
    DWORD ms = (DWORD)((ns + 999999) / 1000000); // ceil
    if (ms == 0) ms = 1;
    Sleep(ms);
#else
    struct timespec req, rem;
    req.tv_sec = ns / 1000000000LL;
    req.tv_nsec = ns % 1000000000LL;
    while (nanosleep(&req, &rem) == -1) {
        req = rem;
    }
#endif
        '''),
        make_v('NS', types.int64, expr, realization, '1000000000'),
        make_v('US', types.int64, expr, realization, '1000000'),
        make_v('MS', types.int64, expr, realization, '1000'),
    ], zero_origin),
    export_=expr
)