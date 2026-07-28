
#include "../include/base.h"

#include <stdlib.h>

_ftuint64_t__int8_tpft__env alloc_our;   
int8_tp alloc_ourg(uint64_t size,void* _par){
    
        return malloc(size);
        
}
_ftuint64_t__int8_tpft__env alloc_our = (_ftuint64_t__int8_tpft__env){alloc_ourg, NULL};


_ftint8_tp__voidft__env free_our;   
void free_ourg(int8_tp p,void* _par){
    
        free(p);
        
}
_ftint8_tp__voidft__env free_our = (_ftint8_tp__voidft__env){free_ourg, NULL};


_ftint8_tp_uint64_t__int8_tpft__env realloc_our;   
int8_tp realloc_ourg(int8_tp start, uint64_t new_size,void* _par){
    
        return realloc(start, new_size);
        
}
_ftint8_tp_uint64_t__int8_tpft__env realloc_our = (_ftint8_tp_uint64_t__int8_tpft__env){realloc_ourg, NULL};

int8_tp NULL_our;
void vars_initializer_mem(){NULL_our = (int8_t*)0;
}