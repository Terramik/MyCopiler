
#ifndef PROJ_843463961029364644_BASE_H
#define PROJ_843463961029364644_BASE_H
#include "base.h"
typedef struct {uint64_t* start;size_t _0;}uint64_ts1;
static inline size_t uint64_ts1i (uint64_ts1 slise, size_t i, char* position) {if ( i >= slise._0 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);abort();}return i;}
typedef struct {int64_t arr[3];}int64_ta3;
static inline size_t int64_ta3i (size_t i, char* position) {if ( i >= 3 ){printf("Index %zu out of array range 3 on %s\n", i, position);abort();}return i;}
typedef struct {int8_t symbol;double dist;}Pixselinstance;
typedef struct {}VectorLibinstance;
typedef struct {}MatrixLibinstance;
typedef struct {double arr[3];}doublea3;
static inline size_t doublea3i (size_t i, char* position) {if ( i >= 3 ){printf("Index %zu out of array range 3 on %s\n", i, position);abort();}return i;}
typedef uint64_t* uint64_tp;typedef struct {double* start;size_t _0;}doubles1;
static inline size_t doubles1i (doubles1 slise, size_t i, char* position) {if ( i >= slise._0 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);abort();}return i;}
typedef struct {double w;double x;double y;double z;}Quaternioninstance;
typedef struct {double arr[2];}doublea2;
static inline size_t doublea2i (size_t i, char* position) {if ( i >= 2 ){printf("Index %zu out of array range 2 on %s\n", i, position);abort();}return i;}
typedef struct {doublea2 arr[3];}doublea2a3;
static inline size_t doublea2a3i (size_t i, char* position) {if ( i >= 3 ){printf("Index %zu out of array range 3 on %s\n", i, position);abort();}return i;}
typedef void (*_ftdoubles1_doubles1_doubles1__voidft_fp)(doubles1,doubles1,doubles1, void*);
typedef struct {_ftdoubles1_doubles1_doubles1__voidft_fp func;void* env;}_ftdoubles1_doubles1_doubles1__voidft__env;
typedef struct {int8_t symbol;int64_ta3 idxs;}Polygoninstance;
typedef void (*_ftdoubles1_IOStream_o__voidft_fp)(doubles1,IOStream_ourinstance, void*);
typedef struct {_ftdoubles1_IOStream_o__voidft_fp func;void* env;}_ftdoubles1_IOStream_o__voidft__env;
typedef Quaternioninstance (*_ftQuaternion_Quaternion__Quaternionft_fp)(Quaternioninstance,Quaternioninstance, void*);
typedef struct {_ftQuaternion_Quaternion__Quaternionft_fp func;void* env;}_ftQuaternion_Quaternion__Quaternionft__env;
typedef struct {bool bad;bool is_max_min_left;int8_t symbol;uint8_t type;doublea3 dist_equation;int64_t y_max;int64_t y_mid;int64_t y_min;doublea2 equation_max_mid;doublea2 equation_mid_min;doublea2 equation_max_min;}ProjectedPolygoninstance;
typedef Quaternioninstance (*_ftQuaternion__Quaternionft_fp)(Quaternioninstance, void*);
typedef struct {_ftQuaternion__Quaternionft_fp func;void* env;}_ftQuaternion__Quaternionft__env;
typedef Quaternioninstance (*_ftdouble_doublea3__Quaternionft_fp)(double,doublea3, void*);
typedef struct {_ftdouble_doublea3__Quaternionft_fp func;void* env;}_ftdouble_doublea3__Quaternionft__env;
typedef Pixselinstance (*_ftint8_t_double__Pixselinstft_fp)(int8_t,double, void*);
typedef struct {_ftint8_t_double__Pixselinstft_fp func;void* env;}_ftint8_t_double__Pixselinstft__env;
typedef struct {doublea2 arr[2];}doublea2a2;
static inline size_t doublea2a2i (size_t i, char* position) {if ( i >= 2 ){printf("Index %zu out of array range 2 on %s\n", i, position);abort();}return i;}
typedef void (*_ftdoubles1_double_doubles1__voidft_fp)(doubles1,double,doubles1, void*);
typedef struct {_ftdoubles1_double_doubles1__voidft_fp func;void* env;}_ftdoubles1_double_doubles1__voidft__env;
typedef Pixselinstance* Pixselinstancep;typedef double (*_ftdoubles1__doubleft_fp)(doubles1, void*);
typedef struct {_ftdoubles1__doubleft_fp func;void* env;}_ftdoubles1__doubleft__env;
typedef void (*_ftQuaternion_IOStream_o__voidft_fp)(Quaternioninstance,IOStream_ourinstance, void*);
typedef struct {_ftQuaternion_IOStream_o__voidft_fp func;void* env;}_ftQuaternion_IOStream_o__voidft__env;
typedef Quaternioninstance (*_ftdouble_double_double_double__Quaternionft_fp)(double,double,double,double, void*);
typedef struct {_ftdouble_double_double_double__Quaternionft_fp func;void* env;}_ftdouble_double_double_double__Quaternionft__env;
typedef void (*_ftdoublea2_doublea2_doubles1__voidft_fp)(doublea2,doublea2,doubles1, void*);
typedef struct {_ftdoublea2_doublea2_doubles1__voidft_fp func;void* env;}_ftdoublea2_doublea2_doubles1__voidft__env;
typedef struct {Pixselinstance* start;size_t _0;}Pixselinstances1;
static inline size_t Pixselinstances1i (Pixselinstances1 slise, size_t i, char* position) {if ( i >= slise._0 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);abort();}return i;}
typedef double (*_ftdoubles1_doubles1__doubleft_fp)(doubles1,doubles1, void*);
typedef struct {_ftdoubles1_doubles1__doubleft_fp func;void* env;}_ftdoubles1_doubles1__doubleft__env;
typedef void (*_ftdoubles1__voidft_fp)(doubles1, void*);
typedef struct {_ftdoubles1__voidft_fp func;void* env;}_ftdoubles1__voidft__env;
typedef double (*_ftQuaternion__doubleft_fp)(Quaternioninstance, void*);
typedef struct {_ftQuaternion__doubleft_fp func;void* env;}_ftQuaternion__doubleft__env;
typedef Quaternioninstance (*_ftdoubles1__Quaternionft_fp)(doubles1, void*);
typedef struct {_ftdoubles1__Quaternionft_fp func;void* env;}_ftdoubles1__Quaternionft__env;
typedef void (*_ftQuaternion_doubles1__voidft_fp)(Quaternioninstance,doubles1, void*);
typedef struct {_ftQuaternion_doubles1__voidft_fp func;void* env;}_ftQuaternion_doubles1__voidft__env;
typedef struct {doublea3 arr[3];}doublea3a3;
static inline size_t doublea3a3i (size_t i, char* position) {if ( i >= 3 ){printf("Index %zu out of array range 3 on %s\n", i, position);abort();}return i;}
typedef struct {doublea3 arr[4];}doublea3a4;
static inline size_t doublea3a4i (size_t i, char* position) {if ( i >= 4 ){printf("Index %zu out of array range 4 on %s\n", i, position);abort();}return i;}
typedef struct {double* start;size_t _0;size_t _1;}doubles2;
static inline doubles1 doubles2i (doubles2 slise, size_t i, char* position) {if ( i >= slise._1 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._1, position);abort();}return (doubles1){slise.start + slise._0 * i,slise._0};}
typedef void (*_ftdoubles2_doubles1_doubles1__voidft_fp)(doubles2,doubles1,doubles1, void*);
typedef struct {_ftdoubles2_doubles1_doubles1__voidft_fp func;void* env;}_ftdoubles2_doubles1_doubles1__voidft__env;
typedef void (*_ftdoubles2_IOStream_o__voidft_fp)(doubles2,IOStream_ourinstance, void*);
typedef struct {_ftdoubles2_IOStream_o__voidft_fp func;void* env;}_ftdoubles2_IOStream_o__voidft__env;
typedef void (*_ftdoubles2_doubles2__voidft_fp)(doubles2,doubles2, void*);
typedef struct {_ftdoubles2_doubles2__voidft_fp func;void* env;}_ftdoubles2_doubles2__voidft__env;
typedef ProjectedPolygoninstance (*_ftPolygonins_doubles2__ProjectedPft_fp)(Polygoninstance,doubles2, void*);
typedef struct {_ftPolygonins_doubles2__ProjectedPft_fp func;void* env;}_ftPolygonins_doubles2__ProjectedPft__env;
typedef ProjectedPolygoninstance (*_ftint8_t_int64_ta3_doubles2__ProjectedPft_fp)(int8_t,int64_ta3,doubles2, void*);
typedef struct {_ftint8_t_int64_ta3_doubles2__ProjectedPft_fp func;void* env;}_ftint8_t_int64_ta3_doubles2__ProjectedPft__env;
typedef uint64_t (*_ftdoubles2__uint64_tft_fp)(doubles2, void*);
typedef struct {_ftdoubles2__uint64_tft_fp func;void* env;}_ftdoubles2__uint64_tft__env;
typedef struct {Polygoninstance arr[4];}Polygoninstancea4;
static inline size_t Polygoninstancea4i (size_t i, char* position) {if ( i >= 4 ){printf("Index %zu out of array range 4 on %s\n", i, position);abort();}return i;}
typedef void (*_ftdoubles2_doubles2_Quaternion__voidft_fp)(doubles2,doubles2,Quaternioninstance, void*);
typedef struct {_ftdoubles2_doubles2_Quaternion__voidft_fp func;void* env;}_ftdoubles2_doubles2_Quaternion__voidft__env;
typedef uint64_ts1 (*_ftdoubles2__uint64_ts1ft_fp)(doubles2, void*);
typedef struct {_ftdoubles2__uint64_ts1ft_fp func;void* env;}_ftdoubles2__uint64_ts1ft__env;
typedef void (*_ftdoubles2_uint64_t_double_uint64_t__voidft_fp)(doubles2,uint64_t,double,uint64_t, void*);
typedef struct {_ftdoubles2_uint64_t_double_uint64_t__voidft_fp func;void* env;}_ftdoubles2_uint64_t_double_uint64_t__voidft__env;
typedef struct {ProjectedPolygoninstance arr[4];}ProjectedPolygoninstancea4;
static inline size_t ProjectedPolygoninstancea4i (size_t i, char* position) {if ( i >= 4 ){printf("Index %zu out of array range 4 on %s\n", i, position);abort();}return i;}
typedef uint64_t (*_ftdoubles2_doubles2__uint64_tft_fp)(doubles2,doubles2, void*);
typedef struct {_ftdoubles2_doubles2__uint64_tft_fp func;void* env;}_ftdoubles2_doubles2__uint64_tft__env;
typedef struct {_ftint8_t_double__Pixselinstft__env __init___;}Pixseltype;
typedef double (*_ftdoubles2__doubleft_fp)(doubles2, void*);
typedef struct {_ftdoubles2__doubleft_fp func;void* env;}_ftdoubles2__doubleft__env;
typedef void (*_ftdoubles2_double_doubles2__voidft_fp)(doubles2,double,doubles2, void*);
typedef struct {_ftdoubles2_double_doubles2__voidft_fp func;void* env;}_ftdoubles2_double_doubles2__voidft__env;
typedef struct {_ftdoubles1_doubles1_doubles1__voidft__env add;_ftdoubles1_doubles1_doubles1__voidft__env sub;_ftdoubles1_doubles1_doubles1__voidft__env mul;_ftdoubles1_double_doubles1__voidft__env scale;_ftdoubles1__doubleft__env norm__257a6534a1704e90a4657cd9ede1bc09;_ftdoubles1__voidft__env normalize_;_ftdoubles1_doubles1__doubleft__env dot;_ftdoubles1_doubles1__doubleft__env cross_2d;_ftdoubles1_doubles1_doubles1__voidft__env cross_3d;_ftdoubles1_IOStream_o__voidft__env print_;}VectorLibtype;
typedef bool (*_ftdoubles2_doubles2__boolft_fp)(doubles2,doubles2, void*);
typedef struct {_ftdoubles2_doubles2__boolft_fp func;void* env;}_ftdoubles2_doubles2__boolft__env;
typedef struct {_ftdouble_double_double_double__Quaternionft__env __init__;_ftQuaternion_IOStream_o__voidft__env print;_ftQuaternion_Quaternion__Quaternionft__env __mul__;_ftQuaternion__doubleft__env norm;_ftQuaternion__Quaternionft__env normalize;_ftQuaternion__Quaternionft__env conj;_ftdoubles1__Quaternionft__env from_vector;_ftQuaternion_doubles1__voidft__env to_vector;_ftQuaternion_doubles1__voidft__env apply;_ftdouble_doublea3__Quaternionft__env from_axis_and_angle;}Quaterniontype;
typedef void (*_ftdoubles2_uint64_t_uint64_t_double_uint64_t__voidft_fp)(doubles2,uint64_t,uint64_t,double,uint64_t, void*);
typedef struct {_ftdoubles2_uint64_t_uint64_t_double_uint64_t__voidft_fp func;void* env;}_ftdoubles2_uint64_t_uint64_t_double_uint64_t__voidft__env;
typedef Polygoninstance (*_ftint8_t_int64_ta3__Polygoninsft_fp)(int8_t,int64_ta3, void*);
typedef struct {_ftint8_t_int64_ta3__Polygoninsft_fp func;void* env;}_ftint8_t_int64_ta3__Polygoninsft__env;
typedef struct {Pixselinstance* start;size_t _0;size_t _1;}Pixselinstances2;
static inline Pixselinstances1 Pixselinstances2i (Pixselinstances2 slise, size_t i, char* position) {if ( i >= slise._1 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._1, position);abort();}return (Pixselinstances1){slise.start + slise._0 * i,slise._0};}
typedef void (*_ftdoubles2_doubles2_doubles2__voidft_fp)(doubles2,doubles2,doubles2, void*);
typedef struct {_ftdoubles2_doubles2_doubles2__voidft_fp func;void* env;}_ftdoubles2_doubles2_doubles2__voidft__env;
typedef void (*_ftdoubles2_uint64_t_uint64_t_uint64_t__voidft_fp)(doubles2,uint64_t,uint64_t,uint64_t, void*);
typedef struct {_ftdoubles2_uint64_t_uint64_t_uint64_t__voidft_fp func;void* env;}_ftdoubles2_uint64_t_uint64_t_uint64_t__voidft__env;
typedef struct {_ftint8_t_int64_ta3__Polygoninsft__env __init____d645dd4bfa43460789e2dafbd2006c23;_ftPolygonins_doubles2__ProjectedPft__env project;}Polygontype;
typedef struct {Pixselinstances2 canvas;}Canvasinstance;
typedef struct {_ftdoubles2_IOStream_o__voidft__env print__b011809066824b62ab5d3639c45ad674;_ftdoubles2_doubles2_doubles2__voidft__env add_;_ftdoubles2_doubles2_doubles2__voidft__env sub_;_ftdoubles2_double_doubles2__voidft__env scale__d7c4ff6bd7c64c2f886be49c576f906d;_ftdoubles2_doubles2_doubles2__voidft__env mul_;_ftdoubles2_doubles1_doubles1__voidft__env apply_;_ftdoubles2_doubles2__voidft__env transpose;_ftdoubles2_uint64_t_uint64_t_uint64_t__voidft__env _gauss_move;_ftdoubles2_uint64_t_uint64_t_uint64_t__voidft__env _gauss_copy;_ftdoubles2_uint64_t_double_uint64_t__voidft__env _gauss_scale;_ftdoubles2_uint64_t_uint64_t_uint64_t__voidft__env _gauss_add_to;_ftdoubles2_uint64_t_uint64_t_double_uint64_t__voidft__env _gauss_add_to_scale;_ftdoubles2__doubleft__env det;_ftdoubles2__uint64_tft__env rank;_ftdoubles2_doubles2__boolft__env inv;_ftdoubles2__uint64_tft__env ref;_ftdoubles2__uint64_tft__env rref;_ftdoubles2_doubles2__uint64_tft__env span;_ftdoubles2__uint64_ts1ft__env find_pivots;_ftdoubles2_doubles2__uint64_tft__env ker;}MatrixLibtype;
typedef Canvasinstance* Canvasinstancep;typedef void (*_ftProjectedP_Canvasinst__voidft_fp)(ProjectedPolygoninstance,Canvasinstance, void*);
typedef struct {_ftProjectedP_Canvasinst__voidft_fp func;void* env;}_ftProjectedP_Canvasinst__voidft__env;
typedef void (*_ftCanvasinst__voidft_fp)(Canvasinstance, void*);
typedef struct {_ftCanvasinst__voidft_fp func;void* env;}_ftCanvasinst__voidft__env;
typedef Canvasinstance (*_ftvoid__Canvasinstft_fp)(void*);
typedef struct {_ftvoid__Canvasinstft_fp func;void* env;}_ftvoid__Canvasinstft__env;
typedef bool (*_ftCanvasinst__boolft_fp)(Canvasinstancep, void*);
typedef struct {_ftCanvasinst__boolft_fp func;void* env;}_ftCanvasinst__boolft__env;
typedef struct {_ftint8_t_int64_ta3_doubles2__ProjectedPft__env __init____61d3c2a8f4404bb4bd5b30564a87ddfb;_ftProjectedP_Canvasinst__voidft__env write;}ProjectedPolygontype;
typedef void (*_ftCanvasinst__voidft_fp_a8851b4ecc5940669bd6591fbbe6010c)(Canvasinstancep, void*);
typedef struct {_ftCanvasinst__voidft_fp_a8851b4ecc5940669bd6591fbbe6010c func;void* env;}_ftCanvasinst__voidft__env_c24bb811afac416a957ecc04be946b65;
typedef struct {_ftvoid__Canvasinstft__env __init____2dafa209eda84bd5ad9dae00c0d5a5b5;_ftCanvasinst__boolft__env init;_ftCanvasinst__voidft__env __del__;_ftCanvasinst__voidft__env_c24bb811afac416a957ecc04be946b65 clean;_ftCanvasinst__voidft__env print__540520989bb04c28ac012b81e05923fe;}Canvastype;
static inline doubles2 doublea2a2s2_2(doublea2a2* array, size_t i_0, size_t i_1, size_t d_0, size_t d_1, char* position) {if ( i_0 >= 2 ){printf("Index %zu out of array range 2 in 1index of slice creation on %s\n", i_0, position);abort();}if ( i_1 >= 2 ){printf("Index %zu out of array range 2 in 2index of slice creation on %s\n", i_1, position);abort();}size_t max_total_size = (2 - i_0) * (2 - i_1);size_t total_size = d_0*d_1;if (total_size > max_total_size){printf("Size of slice %zu out of allowed sliced array size %zu on %s\n", total_size, max_total_size, position);abort();}return (doubles2){&(array->arr[i_0].arr[i_1]), d_0, d_1};}
static inline doubles2 doublea3a4s2_2(doublea3a4* array, size_t i_0, size_t i_1, size_t d_0, size_t d_1, char* position) {if ( i_0 >= 4 ){printf("Index %zu out of array range 4 in 1index of slice creation on %s\n", i_0, position);abort();}if ( i_1 >= 3 ){printf("Index %zu out of array range 3 in 2index of slice creation on %s\n", i_1, position);abort();}size_t max_total_size = (4 - i_0) * (3 - i_1);size_t total_size = d_0*d_1;if (total_size > max_total_size){printf("Size of slice %zu out of allowed sliced array size %zu on %s\n", total_size, max_total_size, position);abort();}return (doubles2){&(array->arr[i_0].arr[i_1]), d_0, d_1};}
static inline doubles1 doublea3s1_1(doublea3* array, size_t i_0, size_t d_0, char* position) {if ( i_0 >= 3 ){printf("Index %zu out of array range 3 in 1index of slice creation on %s\n", i_0, position);abort();}size_t max_total_size = (3 - i_0);size_t total_size = d_0;if (total_size > max_total_size){printf("Size of slice %zu out of allowed sliced array size %zu on %s\n", total_size, max_total_size, position);abort();}return (doubles1){&(array->arr[i_0]), d_0};}
static inline doubles1 doublea2s1_1(doublea2* array, size_t i_0, size_t d_0, char* position) {if ( i_0 >= 2 ){printf("Index %zu out of array range 2 in 1index of slice creation on %s\n", i_0, position);abort();}size_t max_total_size = (2 - i_0);size_t total_size = d_0;if (total_size > max_total_size){printf("Size of slice %zu out of allowed sliced array size %zu on %s\n", total_size, max_total_size, position);abort();}return (doubles1){&(array->arr[i_0]), d_0};}
static inline doubles1 doubles2s2_1(doubles2* slice, size_t i_0, size_t i_1, size_t d_0, char* position) {if (i_0 >= slice->_1){printf("Index %zu out of slice range %zu in 1 index of slice creation on %s\n",i_0, slice->_1, position);abort();}if (i_1 >= slice->_0){printf("Index %zu out of slice range %zu in 2 index of slice creation on %s\n",i_1, slice->_0, position);abort();}size_t max_total_size = (slice->_1 - i_0)*(slice->_0 - i_1);size_t total_size = d_0;if ( total_size > max_total_size ) {printf("Size of slice %zu out of allowed sliced slise size %zu on %s\n", total_size, max_total_size, position);abort();}size_t shift = i_0;size_t stride = slice->_1;shift += i_1 * stride;stride *= slice->_0;return (doubles1){slice->start + shift, d_0};}
static inline uint64_ts1 uint64_tps1_1(uint64_tp pointer, size_t i_0, size_t d_0, char* position) {return (uint64_ts1){pointer + i_0, d_0};}
static inline Pixselinstances2 Pixselinstanceps1_2(Pixselinstancep pointer, size_t i_0, size_t d_0, size_t d_1, char* position) {return (Pixselinstances2){pointer + i_0, d_0, d_1};}
static inline doubles2 doublea3a3s2_2(doublea3a3* array, size_t i_0, size_t i_1, size_t d_0, size_t d_1, char* position) {if ( i_0 >= 3 ){printf("Index %zu out of array range 3 in 1index of slice creation on %s\n", i_0, position);abort();}if ( i_1 >= 3 ){printf("Index %zu out of array range 3 in 2index of slice creation on %s\n", i_1, position);abort();}size_t max_total_size = (3 - i_0) * (3 - i_1);size_t total_size = d_0*d_1;if (total_size > max_total_size){printf("Size of slice %zu out of allowed sliced array size %zu on %s\n", total_size, max_total_size, position);abort();}return (doubles2){&(array->arr[i_0].arr[i_1]), d_0, d_1};}

#endif
