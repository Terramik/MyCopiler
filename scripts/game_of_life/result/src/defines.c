
#include "../include/defines.h"
uint64_t RAND_SEED_;
int8_t CELL_DEAD_;
int8_t CELL_ALIVE_;
uint64_t UPS_;
uint64_t SIZE_Y_;
uint64_t SIZE_X_;
void vars_initializer(){(SIZE_X_)=((uint64_t)(70));
(SIZE_Y_)=((uint64_t)(15));
(UPS_)=((uint64_t)(5));
(CELL_ALIVE_)=('O');
(CELL_DEAD_)=(' ');
(RAND_SEED_)=((uint64_t)(((now_our).func)((now_our).env)));
}