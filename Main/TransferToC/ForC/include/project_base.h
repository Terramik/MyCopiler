
#ifndef PROJ_7504539501547011932_BASE_H
#define PROJ_7504539501547011932_BASE_H
#include "base.h"
typedef int64_t* int64_tp;typedef struct {int64_t arr[5];}int64_ta5;
static inline size_t int64_ta5i (size_t i, char* position) {if ( i >= 5 ){printf("Index %zu out of array range 5 on %s\n", i, position);abort();}return i;}
typedef struct {int64_t arr[3];}int64_ta3;
static inline size_t int64_ta3i (size_t i, char* position) {if ( i >= 3 ){printf("Index %zu out of array range 3 on %s\n", i, position);abort();}return i;}
typedef struct {int64_t* start;size_t _0;}int64_ts1;
static inline size_t int64_ts1i (int64_ts1 slise, size_t i, char* position) {if ( i >= slise._0 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);abort();}return i;}
typedef struct {int64_t* start;size_t _0;size_t _1;}int64_ts2;
static inline int64_ts1 int64_ts2i (int64_ts2 slise, size_t i, char* position) {if ( i >= slise._1 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._1, position);abort();}return (int64_ts1){slise.start + slise._0 * i,slise._0};}
typedef struct {int64_ta3 arr[3];}int64_ta3a3;
static inline size_t int64_ta3a3i (size_t i, char* position) {if ( i >= 3 ){printf("Index %zu out of array range 3 on %s\n", i, position);abort();}return i;}
static inline int64_ts2 int64_ta3a3s2_2(int64_ta3a3* array, size_t i_0, size_t i_1, size_t d_0, size_t d_1, char* position) {if ( i_0 >= 3 ){printf("Index %zu out of array range 3 in 1index of slice creation on %s\n", i_0, position);abort();}if ( i_1 >= 3 ){printf("Index %zu out of array range 3 in 2index of slice creation on %s\n", i_1, position);abort();}size_t max_total_size = (3 - i_0) * (3 - i_1);size_t total_size = d_0*d_1;if (total_size > max_total_size){printf("Size of slice %zu out of allowed sliced array size %zu on %s\n", total_size, max_total_size, position);abort();}return (int64_ts2){&(array->arr[i_0].arr[i_1]), d_0, d_1};}
static inline int64_ts1 int64_ts1s1_1(int64_ts1* slice, size_t i_0, size_t d_0, char* position) {if (i_0 >= slice->_0){printf("Index %zu out of slice range %zu in 1 index of slice creation on %s\n",i_0, slice->_0, position);abort();}size_t max_total_size = (slice->_0 - i_0);size_t total_size = d_0;if ( total_size > max_total_size ) {printf("Size of slice %zu out of allowed sliced slise size %zu on %s\n", total_size, max_total_size, position);abort();}size_t shift = i_0;size_t stride = slice->_0;return (int64_ts1){slice->start + shift, d_0};}
static inline int64_ts1 int64_tps1_1(int64_tp pointer, size_t i_0, size_t d_0, char* position) {return (int64_ts1){pointer + i_0, d_0};}
static inline int64_ts1 int64_ta5s1_1(int64_ta5* array, size_t i_0, size_t d_0, char* position) {if ( i_0 >= 5 ){printf("Index %zu out of array range 5 in 1index of slice creation on %s\n", i_0, position);abort();}size_t max_total_size = (5 - i_0);size_t total_size = d_0;if (total_size > max_total_size){printf("Size of slice %zu out of allowed sliced array size %zu on %s\n", total_size, max_total_size, position);abort();}return (int64_ts1){&(array->arr[i_0]), d_0};}

#endif
