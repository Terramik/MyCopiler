
#ifndef PROJ_7194982786838687614_BASE_H
#define PROJ_7194982786838687614_BASE_H
#include "base.h"
typedef uint8_t* uint8_tp;typedef bool* boolp;typedef struct {bool* start;size_t _0;}bools1;
static inline size_t bools1i (bools1 slise, size_t i, char* position) {if ( i >= slise._0 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);abort();}return i;}
typedef struct {uint8_t* start;size_t _0;size_t _1;}uint8_ts2;
static inline str_t uint8_ts2i (uint8_ts2 slise, size_t i, char* position) {if ( i >= slise._1 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._1, position);abort();}return (str_t){slise.start + slise._0 * i,slise._0};}
typedef struct {bool* start;size_t _0;size_t _1;}bools2;
static inline bools1 bools2i (bools2 slise, size_t i, char* position) {if ( i >= slise._1 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._1, position);abort();}return (bools1){slise.start + slise._0 * i,slise._0};}
typedef void (*_ftbools2_uint8_ts2__voidft_fp)(bools2,uint8_ts2, void*);
typedef struct {_ftbools2_uint8_ts2__voidft_fp func;void* env;}_ftbools2_uint8_ts2__voidft__env;
typedef void (*_ftbools2__voidft_fp)(bools2, void*);
typedef struct {_ftbools2__voidft_fp func;void* env;}_ftbools2__voidft__env;
static inline uint8_ts2 uint8_tps1_2(uint8_tp pointer, size_t i_0, size_t d_0, size_t d_1, char* position) {return (uint8_ts2){pointer + i_0, d_0, d_1};}
static inline bools2 boolps1_2(boolp pointer, size_t i_0, size_t d_0, size_t d_1, char* position) {return (bools2){pointer + i_0, d_0, d_1};}

#endif
