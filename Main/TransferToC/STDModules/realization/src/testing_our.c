
#include "../include/base.h"

#include <stdio.h>
#include <stdlib.h>

_ftbool_str_t__voidft__env assert_our;   
void assert_ourg(bool cond, str_t msg,void* _par){
    
        if (!cond) {
            printf("%s", msg.start);
            abort();
        }
        
}
_ftbool_str_t__voidft__env assert_our = (_ftbool_str_t__voidft__env){assert_ourg, NULL};


_ftvoid__voidft__env abort_our;   
void abort_ourg(void* _par){
    
        abort();
        
}
_ftvoid__voidft__env abort_our = (_ftvoid__voidft__env){abort_ourg, NULL};

void vars_initializer_testing(){}