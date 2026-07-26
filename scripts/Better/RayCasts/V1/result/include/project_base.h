
#ifndef PROJ_4238894112_BASE_H
#define PROJ_4238894112_BASE_H
#include "base.h"
typedef struct {double arr[3];}doublea3;
static inline size_t doublea3i (size_t i, char* position) {if ( i >= 3 ){printf("Index %zu out of array range 3 on %s\n", i, position);abort();}return i;}
typedef struct {}VectorLibinstance;
typedef struct {double* start;size_t _0;}doubles1;
static inline size_t doubles1i (doubles1 slise, size_t i, char* position) {if ( i >= slise._0 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);abort();}return i;}
typedef void (*_ftdoubles1_doubles1_doubles1__voidft_fp)(doubles1,doubles1,doubles1, void*);
typedef struct {_ftdoubles1_doubles1_doubles1__voidft_fp func;void* env;}_ftdoubles1_doubles1_doubles1__voidft__env;
typedef void (*_ftdoubles1_double_doubles1__voidft_fp)(doubles1,double,doubles1, void*);
typedef struct {_ftdoubles1_double_doubles1__voidft_fp func;void* env;}_ftdoubles1_double_doubles1__voidft__env;
typedef double (*_ftdoubles1_doubles1__doubleft_fp)(doubles1,doubles1, void*);
typedef struct {_ftdoubles1_doubles1__doubleft_fp func;void* env;}_ftdoubles1_doubles1__doubleft__env;
typedef void (*_ftdoubles1__voidft_fp)(doubles1, void*);
typedef struct {_ftdoubles1__voidft_fp func;void* env;}_ftdoubles1__voidft__env;
typedef double (*_ftdoubles1__doubleft_fp)(doubles1, void*);
typedef struct {_ftdoubles1__doubleft_fp func;void* env;}_ftdoubles1__doubleft__env;
typedef struct {_ftdoubles1_doubles1_doubles1__voidft__env add;_ftdoubles1_doubles1_doubles1__voidft__env sub;_ftdoubles1_doubles1_doubles1__voidft__env mul;_ftdoubles1_double_doubles1__voidft__env scale;_ftdoubles1__doubleft__env norm;_ftdoubles1__voidft__env normalize;_ftdoubles1_doubles1__doubleft__env dot;_ftdoubles1_doubles1__doubleft__env cross_2d;_ftdoubles1_doubles1_doubles1__voidft__env cross_3d;_ftdoubles1__voidft__env print;}VectorLibtype;
static inline doubles1 doublea3s1_1(doublea3* array, size_t i_0, size_t d_0, char* position) {if ( i_0 >= 3 ){printf("Index %zu out of array range 3 in 1index of slice creation on %s\n", i_0, position);abort();}size_t max_total_size = (3 - i_0);size_t total_size = d_0;if (total_size > max_total_size){printf("Size of slice %zu out of allowed sliced array size %zu on %s\n", total_size, max_total_size, position);abort();}return (doubles1){&(array->arr[i_0]), d_0};}

#endif
