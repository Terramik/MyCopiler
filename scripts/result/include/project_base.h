
#ifndef PROJ_2656716606458886651_BASE_H
#define PROJ_2656716606458886651_BASE_H
#include "base.h"
typedef struct {}MatrixLibinstance;
typedef struct {double* start;size_t _0;}doubles1;
static inline size_t doubles1i (doubles1 slise, size_t i, char* position) {if ( i >= slise._0 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);abort();}return i;}
typedef uint64_t* uint64_tp;typedef struct {double arr[4];}doublea4;
static inline size_t doublea4i (size_t i, char* position) {if ( i >= 4 ){printf("Index %zu out of array range 4 on %s\n", i, position);abort();}return i;}
typedef struct {uint64_t* start;size_t _0;}uint64_ts1;
static inline size_t uint64_ts1i (uint64_ts1 slise, size_t i, char* position) {if ( i >= slise._0 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);abort();}return i;}
typedef struct {}VectorLibinstance;
typedef double (*_ftdoubles1_doubles1__doubleft_fp)(doubles1,doubles1, void*);
typedef struct {_ftdoubles1_doubles1__doubleft_fp func;void* env;}_ftdoubles1_doubles1__doubleft__env;
typedef void (*_ftdoubles1__voidft_fp)(doubles1, void*);
typedef struct {_ftdoubles1__voidft_fp func;void* env;}_ftdoubles1__voidft__env;
typedef struct {doublea4 arr[4];}doublea4a4;
static inline size_t doublea4a4i (size_t i, char* position) {if ( i >= 4 ){printf("Index %zu out of array range 4 on %s\n", i, position);abort();}return i;}
typedef struct {double* start;size_t _0;size_t _1;}doubles2;
static inline doubles1 doubles2i (doubles2 slise, size_t i, char* position) {if ( i >= slise._1 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._1, position);abort();}return (doubles1){slise.start + slise._0 * i,slise._0};}
typedef double (*_ftdoubles1__doubleft_fp)(doubles1, void*);
typedef struct {_ftdoubles1__doubleft_fp func;void* env;}_ftdoubles1__doubleft__env;
typedef void (*_ftdoubles1_double_doubles1__voidft_fp)(doubles1,double,doubles1, void*);
typedef struct {_ftdoubles1_double_doubles1__voidft_fp func;void* env;}_ftdoubles1_double_doubles1__voidft__env;
typedef struct {doublea4 arr[3];}doublea4a3;
static inline size_t doublea4a3i (size_t i, char* position) {if ( i >= 3 ){printf("Index %zu out of array range 3 on %s\n", i, position);abort();}return i;}
typedef void (*_ftdoubles1_IOStream_o__voidft_fp)(doubles1,IOStream_ourinstance, void*);
typedef struct {_ftdoubles1_IOStream_o__voidft_fp func;void* env;}_ftdoubles1_IOStream_o__voidft__env;
typedef void (*_ftdoubles1_doubles1_doubles1__voidft_fp)(doubles1,doubles1,doubles1, void*);
typedef struct {_ftdoubles1_doubles1_doubles1__voidft_fp func;void* env;}_ftdoubles1_doubles1_doubles1__voidft__env;
typedef void (*_ftdoubles2_doubles1_doubles1__voidft_fp)(doubles2,doubles1,doubles1, void*);
typedef struct {_ftdoubles2_doubles1_doubles1__voidft_fp func;void* env;}_ftdoubles2_doubles1_doubles1__voidft__env;
typedef void (*_ftdoubles2_IOStream_o__voidft_fp)(doubles2,IOStream_ourinstance, void*);
typedef struct {_ftdoubles2_IOStream_o__voidft_fp func;void* env;}_ftdoubles2_IOStream_o__voidft__env;
typedef struct {_ftdoubles1_doubles1_doubles1__voidft__env add;_ftdoubles1_doubles1_doubles1__voidft__env sub;_ftdoubles1_doubles1_doubles1__voidft__env mul;_ftdoubles1_double_doubles1__voidft__env scale;_ftdoubles1__doubleft__env norm;_ftdoubles1__voidft__env normalize;_ftdoubles1_doubles1__doubleft__env dot;_ftdoubles1_doubles1__doubleft__env cross_2d;_ftdoubles1_doubles1_doubles1__voidft__env cross_3d;_ftdoubles1_IOStream_o__voidft__env print;}VectorLibtype;
typedef uint64_t (*_ftdoubles2_doubles2__uint64_tft_fp)(doubles2,doubles2, void*);
typedef struct {_ftdoubles2_doubles2__uint64_tft_fp func;void* env;}_ftdoubles2_doubles2__uint64_tft__env;
typedef void (*_ftdoubles2_doubles2_doubles2__voidft_fp)(doubles2,doubles2,doubles2, void*);
typedef struct {_ftdoubles2_doubles2_doubles2__voidft_fp func;void* env;}_ftdoubles2_doubles2_doubles2__voidft__env;
typedef uint64_t (*_ftdoubles2__uint64_tft_fp)(doubles2, void*);
typedef struct {_ftdoubles2__uint64_tft_fp func;void* env;}_ftdoubles2__uint64_tft__env;
typedef double (*_ftdoubles2__doubleft_fp)(doubles2, void*);
typedef struct {_ftdoubles2__doubleft_fp func;void* env;}_ftdoubles2__doubleft__env;
typedef void (*_ftdoubles2_uint64_t_double_uint64_t__voidft_fp)(doubles2,uint64_t,double,uint64_t, void*);
typedef struct {_ftdoubles2_uint64_t_double_uint64_t__voidft_fp func;void* env;}_ftdoubles2_uint64_t_double_uint64_t__voidft__env;
typedef void (*_ftdoubles2_doubles2__voidft_fp)(doubles2,doubles2, void*);
typedef struct {_ftdoubles2_doubles2__voidft_fp func;void* env;}_ftdoubles2_doubles2__voidft__env;
typedef void (*_ftdoubles2_uint64_t_uint64_t_double_uint64_t__voidft_fp)(doubles2,uint64_t,uint64_t,double,uint64_t, void*);
typedef struct {_ftdoubles2_uint64_t_uint64_t_double_uint64_t__voidft_fp func;void* env;}_ftdoubles2_uint64_t_uint64_t_double_uint64_t__voidft__env;
typedef bool (*_ftdoubles2_doubles2__boolft_fp)(doubles2,doubles2, void*);
typedef struct {_ftdoubles2_doubles2__boolft_fp func;void* env;}_ftdoubles2_doubles2__boolft__env;
typedef uint64_ts1 (*_ftdoubles2__uint64_ts1ft_fp)(doubles2, void*);
typedef struct {_ftdoubles2__uint64_ts1ft_fp func;void* env;}_ftdoubles2__uint64_ts1ft__env;
typedef void (*_ftdoubles2_uint64_t_uint64_t_uint64_t__voidft_fp)(doubles2,uint64_t,uint64_t,uint64_t, void*);
typedef struct {_ftdoubles2_uint64_t_uint64_t_uint64_t__voidft_fp func;void* env;}_ftdoubles2_uint64_t_uint64_t_uint64_t__voidft__env;
typedef void (*_ftdoubles2_double_doubles2__voidft_fp)(doubles2,double,doubles2, void*);
typedef struct {_ftdoubles2_double_doubles2__voidft_fp func;void* env;}_ftdoubles2_double_doubles2__voidft__env;
typedef struct {_ftdoubles2_IOStream_o__voidft__env print_;_ftdoubles2_doubles2_doubles2__voidft__env add_;_ftdoubles2_doubles2_doubles2__voidft__env sub_;_ftdoubles2_double_doubles2__voidft__env scale__eb1d84c591e644f6a52b4befeb6cd6bc;_ftdoubles2_doubles2_doubles2__voidft__env mul_;_ftdoubles2_doubles1_doubles1__voidft__env apply;_ftdoubles2_doubles2__voidft__env transpose;_ftdoubles2_uint64_t_uint64_t_uint64_t__voidft__env _gauss_move;_ftdoubles2_uint64_t_uint64_t_uint64_t__voidft__env _gauss_copy;_ftdoubles2_uint64_t_double_uint64_t__voidft__env _gauss_scale;_ftdoubles2_uint64_t_uint64_t_uint64_t__voidft__env _gauss_add_to;_ftdoubles2_uint64_t_uint64_t_double_uint64_t__voidft__env _gauss_add_to_scale;_ftdoubles2__doubleft__env det;_ftdoubles2__uint64_tft__env rank;_ftdoubles2_doubles2__boolft__env inv;_ftdoubles2__uint64_tft__env ref;_ftdoubles2__uint64_tft__env rref;_ftdoubles2_doubles2__uint64_tft__env span;_ftdoubles2__uint64_ts1ft__env find_pivots;_ftdoubles2_doubles2__uint64_tft__env ker;}MatrixLibtype;
static inline uint64_ts1 uint64_tps1_1(uint64_tp pointer, size_t i_0, size_t d_0, char* position) {return (uint64_ts1){pointer + i_0, d_0};}
static inline doubles2 doublea4a3s2_2(doublea4a3* array, size_t i_0, size_t i_1, size_t d_0, size_t d_1, char* position) {if ( i_0 >= 3 ){printf("Index %zu out of array range 3 in 1index of slice creation on %s\n", i_0, position);abort();}if ( i_1 >= 4 ){printf("Index %zu out of array range 4 in 2index of slice creation on %s\n", i_1, position);abort();}size_t max_total_size = (3 - i_0) * (4 - i_1);size_t total_size = d_0*d_1;if (total_size > max_total_size){printf("Size of slice %zu out of allowed sliced array size %zu on %s\n", total_size, max_total_size, position);abort();}return (doubles2){&(array->arr[i_0].arr[i_1]), d_0, d_1};}
static inline doubles1 doubles2s2_1(doubles2* slice, size_t i_0, size_t i_1, size_t d_0, char* position) {if (i_0 >= slice->_1){printf("Index %zu out of slice range %zu in 1 index of slice creation on %s\n",i_0, slice->_1, position);abort();}if (i_1 >= slice->_0){printf("Index %zu out of slice range %zu in 2 index of slice creation on %s\n",i_1, slice->_0, position);abort();}size_t max_total_size = (slice->_1 - i_0)*(slice->_0 - i_1);size_t total_size = d_0;if ( total_size > max_total_size ) {printf("Size of slice %zu out of allowed sliced slise size %zu on %s\n", total_size, max_total_size, position);abort();}size_t shift = i_0;size_t stride = slice->_1;shift += i_1 * stride;stride *= slice->_0;return (doubles1){slice->start + shift, d_0};}
static inline doubles2 doublea4a4s2_2(doublea4a4* array, size_t i_0, size_t i_1, size_t d_0, size_t d_1, char* position) {if ( i_0 >= 4 ){printf("Index %zu out of array range 4 in 1index of slice creation on %s\n", i_0, position);abort();}if ( i_1 >= 4 ){printf("Index %zu out of array range 4 in 2index of slice creation on %s\n", i_1, position);abort();}size_t max_total_size = (4 - i_0) * (4 - i_1);size_t total_size = d_0*d_1;if (total_size > max_total_size){printf("Size of slice %zu out of allowed sliced array size %zu on %s\n", total_size, max_total_size, position);abort();}return (doubles2){&(array->arr[i_0].arr[i_1]), d_0, d_1};}

#endif
