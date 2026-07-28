
#include "../include/base.h"

#include <time.h>

#ifdef _WIN32
    #include <windows.h>
#endif

_ftvoid__int64_tft__env now_our;   
int64_t now_ourg(void* _par){
    
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
        
}
_ftvoid__int64_tft__env now_our = (_ftvoid__int64_tft__env){now_ourg, NULL};


_ftint64_t__voidft__env sleep_our;   
void sleep_ourg(int64_t ns,void* _par){
    
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
        
}
_ftint64_t__voidft__env sleep_our = (_ftint64_t__voidft__env){sleep_ourg, NULL};

int64_t NS_our;
int64_t US_our;
int64_t MS_our;
void vars_initializer_time(){NS_our = 1000000000;
US_our = 1000000;
MS_our = 1000;
}