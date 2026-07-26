
#ifndef PROJ_1771142088423290_BASE_H
#define PROJ_1771142088423290_BASE_H
#include "base.h"
typedef struct {}MatrixLibinstance;
typedef struct {double arr[2];}doublea2;
static inline size_t doublea2i (size_t i, char* position) {if ( i >= 2 ){printf("Index %zu out of array range 2 on %s\n", i, position);abort();}return i;}
typedef struct {double* start;size_t _0;}doubles1;
static inline size_t doubles1i (doubles1 slise, size_t i, char* position) {if ( i >= slise._0 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);abort();}return i;}
typedef struct {double* start;size_t _0;size_t _1;}doubles2;
static inline doubles1 doubles2i (doubles2 slise, size_t i, char* position) {if ( i >= slise._1 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._1, position);abort();}return (doubles1){slise.start + slise._0 * i,slise._0};}
typedef struct {doublea2 arr[2];}doublea2a2;
static inline size_t doublea2a2i (size_t i, char* position) {if ( i >= 2 ){printf("Index %zu out of array range 2 on %s\n", i, position);abort();}return i;}
typedef void (*_ftdoubles2_doubles1_doubles1__voidft_fp)(doubles2,doubles1,doubles1, void*);
typedef struct {_ftdoubles2_doubles1_doubles1__voidft_fp func;void* env;}_ftdoubles2_doubles1_doubles1__voidft__env;
typedef void (*_ftdoubles2_int64_t_int64_t__voidft_fp)(doubles2,int64_t,int64_t, void*);
typedef struct {_ftdoubles2_int64_t_int64_t__voidft_fp func;void* env;}_ftdoubles2_int64_t_int64_t__voidft__env;
typedef void (*_ftdoubles2_doubles2_doubles2__voidft_fp)(doubles2,doubles2,doubles2, void*);
typedef struct {_ftdoubles2_doubles2_doubles2__voidft_fp func;void* env;}_ftdoubles2_doubles2_doubles2__voidft__env;
typedef void (*_ftdoubles2_int64_t_int64_t_double__voidft_fp)(doubles2,int64_t,int64_t,double, void*);
typedef struct {_ftdoubles2_int64_t_int64_t_double__voidft_fp func;void* env;}_ftdoubles2_int64_t_int64_t_double__voidft__env;
typedef int64_t (*_ftdoubles2__int64_tft_fp)(doubles2, void*);
typedef struct {_ftdoubles2__int64_tft_fp func;void* env;}_ftdoubles2__int64_tft__env;
typedef void (*_ftdoubles2_double_doubles2__voidft_fp)(doubles2,double,doubles2, void*);
typedef struct {_ftdoubles2_double_doubles2__voidft_fp func;void* env;}_ftdoubles2_double_doubles2__voidft__env;
typedef void (*_ftdoubles2__voidft_fp)(doubles2, void*);
typedef struct {_ftdoubles2__voidft_fp func;void* env;}_ftdoubles2__voidft__env;
typedef double (*_ftdoubles2__doubleft_fp)(doubles2, void*);
typedef struct {_ftdoubles2__doubleft_fp func;void* env;}_ftdoubles2__doubleft__env;
typedef void (*_ftdoubles2_doubles2__voidft_fp)(doubles2,doubles2, void*);
typedef struct {_ftdoubles2_doubles2__voidft_fp func;void* env;}_ftdoubles2_doubles2__voidft__env;
typedef void (*_ftdoubles2_int64_t_double__voidft_fp)(doubles2,int64_t,double, void*);
typedef struct {_ftdoubles2_int64_t_double__voidft_fp func;void* env;}_ftdoubles2_int64_t_double__voidft__env;
typedef bool (*_ftdoubles2_doubles2__boolft_fp)(doubles2,doubles2, void*);
typedef struct {_ftdoubles2_doubles2__boolft_fp func;void* env;}_ftdoubles2_doubles2__boolft__env;
typedef struct {_ftdoubles2__voidft__env print;_ftdoubles2_doubles2_doubles2__voidft__env add;_ftdoubles2_doubles2_doubles2__voidft__env sub;_ftdoubles2_double_doubles2__voidft__env scale;_ftdoubles2_doubles2_doubles2__voidft__env mul;_ftdoubles2_doubles1_doubles1__voidft__env apply;_ftdoubles2_doubles2__voidft__env transpose;_ftdoubles2_int64_t_int64_t__voidft__env _gauss_move;_ftdoubles2_int64_t_double__voidft__env _gauss_scale;_ftdoubles2_int64_t_int64_t__voidft__env _gauss_add_to;_ftdoubles2_int64_t_int64_t_double__voidft__env _gauss_add_to_scale;_ftdoubles2__doubleft__env det;_ftdoubles2__int64_tft__env rank;_ftdoubles2_doubles2__boolft__env inv;}MatrixLibtype;
static inline doubles1 doubles2s2_1(doubles2* slice, size_t i_0, size_t i_1, size_t d_0, char* position) {if (i_0 >= slice->_1){printf("Index %zu out of slice range %zu in 1 index of slice creation on %s\n",i_0, slice->_1, position);abort();}if (i_1 >= slice->_0){printf("Index %zu out of slice range %zu in 2 index of slice creation on %s\n",i_1, slice->_0, position);abort();}size_t max_total_size = (slice->_1 - i_0)*(slice->_0 - i_1);size_t total_size = d_0;if ( total_size > max_total_size ) {printf("Size of slice %zu out of allowed sliced slise size %zu on %s\n", total_size, max_total_size, position);abort();}size_t shift = i_0;size_t stride = slice->_1;shift += i_1 * stride;stride *= slice->_0;return (doubles1){slice->start + shift, d_0};}
static inline doubles2 doublea2a2s2_2(doublea2a2* array, size_t i_0, size_t i_1, size_t d_0, size_t d_1, char* position) {if ( i_0 >= 2 ){printf("Index %zu out of array range 2 in 1index of slice creation on %s\n", i_0, position);abort();}if ( i_1 >= 2 ){printf("Index %zu out of array range 2 in 2index of slice creation on %s\n", i_1, position);abort();}size_t max_total_size = (2 - i_0) * (2 - i_1);size_t total_size = d_0*d_1;if (total_size > max_total_size){printf("Size of slice %zu out of allowed sliced array size %zu on %s\n", total_size, max_total_size, position);abort();}return (doubles2){&(array->arr[i_0].arr[i_1]), d_0, d_1};}

#endif
