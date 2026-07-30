
#include "../include/defines.h"
uint64_t RAND_SEED;
int8_t CELL_DEAD;
int8_t CELL_ALIVE;
uint64_t UPS;
uint64_t SIZE_Y;
uint64_t SIZE_X;
void vars_initializer(){(SIZE_X)=((uint64_t)(70));
(SIZE_Y)=((uint64_t)(15));
(UPS)=((uint64_t)(5));
(CELL_ALIVE)=((int8_t)('O'));
(CELL_DEAD)=((int8_t)(' '));
(RAND_SEED)=((uint64_t)(((now_our).func)((now_our).env)));
}