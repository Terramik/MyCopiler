
#include "../include/base.h"

#include <stdlib.h>
#include <time.h>

_ftuint64_t__voidft__env seed_our;   
void seed_ourg(uint64_t s,void* _par){
    
        srand((unsigned)s);
        
}
_ftuint64_t__voidft__env seed_our = (_ftuint64_t__voidft__env){seed_ourg, NULL};


_ftvoid__uint64_tft__env rand_our;   
uint64_t rand_ourg(void* _par){
    
        return rand();
        
}
_ftvoid__uint64_tft__env rand_our = (_ftvoid__uint64_tft__env){rand_ourg, NULL};


_ftint64_t_int64_t__int64_tft__env rand_range_our;   
int64_t rand_range_ourg(int64_t min, int64_t max,void* _par){
    
        return (int64_t)((uint64_t)rand() % (uint64_t)(max - min + 1)) + min;
        
}
_ftint64_t_int64_t__int64_tft__env rand_range_our = (_ftint64_t_int64_t__int64_tft__env){rand_range_ourg, NULL};


_ftvoid__doubleft__env randf_our;   
double randf_ourg(void* _par){
    
        return (double)rand() / RAND_MAX;
        
}
_ftvoid__doubleft__env randf_our = (_ftvoid__doubleft__env){randf_ourg, NULL};


_ftdouble_double__doubleft__env randf_range_our;   
double randf_range_ourg(double min, double max,void* _par){
    
        return min + (double)rand() / RAND_MAX * (max - min);
        
}
_ftdouble_double__doubleft__env randf_range_our = (_ftdouble_double__doubleft__env){randf_range_ourg, NULL};

void vars_initializer_rand(){}