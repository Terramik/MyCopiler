
#ifndef PROJ_4862879510861858218_BASE_H
#define PROJ_4862879510861858218_BASE_H
#include "base.h"
typedef struct {double* start;size_t _0;}doubles1;
static inline size_t doubles1i (doubles1 slise, size_t i, char* position) {if ( i >= slise._0 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);abort();}return i;}
typedef uint64_t* uint64_tp;typedef bool (*_ftuint8_t__boolft_fp)(uint8_t, void*);
typedef struct {_ftuint8_t__boolft_fp func;void* env;}_ftuint8_t__boolft__env;
typedef double* doublep;typedef uint8_t (*_ftuint8_t__uint8_tft_fp)(uint8_t, void*);
typedef struct {_ftuint8_t__uint8_tft_fp func;void* env;}_ftuint8_t__uint8_tft__env;
typedef struct {doubles1 data;uint64_t size;uint64_t elements_num;bool good;}StackFloatinstance;
typedef uint8_t* uint8_tp;typedef double (*_ftstr_t_uint64_tp__doubleft_fp)(str_t,uint64_tp, void*);
typedef struct {_ftstr_t_uint64_tp__doubleft_fp func;void* env;}_ftstr_t_uint64_tp__doubleft__env;
typedef uint8_t (*_ftuint8_t__uint8_tft_fp_875a1ab69bc4473998d6ca10a3b62969)(uint8_t, void*);
typedef struct {_ftuint8_t__uint8_tft_fp_875a1ab69bc4473998d6ca10a3b62969 func;void* env;}_ftuint8_t__uint8_tft__env_c5c68045b8f44722a178da55ee9ec233;
typedef uint32_t (*_ftuint8_t__uint32_tft_fp)(uint8_t, void*);
typedef struct {_ftuint8_t__uint32_tft_fp func;void* env;}_ftuint8_t__uint32_tft__env;
typedef struct {uint8_t* start;size_t _0;}uint8_ts1;
static inline size_t uint8_ts1i (uint8_ts1 slise, size_t i, char* position) {if ( i >= slise._0 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);abort();}return i;}
typedef bool (*_ftuint8_t_uint8_t__boolft_fp)(uint8_t,uint8_t, void*);
typedef struct {_ftuint8_t_uint8_t__boolft_fp func;void* env;}_ftuint8_t_uint8_t__boolft__env;
typedef StackFloatinstance* StackFloatinstancep;typedef StackFloatinstance (*_ftuint64_t__StackFloatft_fp)(uint64_t, void*);
typedef struct {_ftuint64_t__StackFloatft_fp func;void* env;}_ftuint64_t__StackFloatft__env;
typedef bool (*_ftStackFloat__boolft_fp)(StackFloatinstance, void*);
typedef struct {_ftStackFloat__boolft_fp func;void* env;}_ftStackFloat__boolft__env;
typedef struct {uint8_ts1 data;uint64_t size;uint64_t elements_num;bool good;}StackOperatorsinstance;
typedef void (*_ftStackFloat__voidft_fp)(StackFloatinstance, void*);
typedef struct {_ftStackFloat__voidft_fp func;void* env;}_ftStackFloat__voidft__env;
typedef double (*_ftStackFloat__doubleft_fp)(StackFloatinstancep, void*);
typedef struct {_ftStackFloat__doubleft_fp func;void* env;}_ftStackFloat__doubleft__env;
typedef StackOperatorsinstance (*_ftuint64_t__StackOperaft_fp)(uint64_t, void*);
typedef struct {_ftuint64_t__StackOperaft_fp func;void* env;}_ftuint64_t__StackOperaft__env;
typedef StackOperatorsinstance* StackOperatorsinstancep;typedef bool (*_ftStackOpera__boolft_fp)(StackOperatorsinstance, void*);
typedef struct {_ftStackOpera__boolft_fp func;void* env;}_ftStackOpera__boolft__env;
typedef void (*_ftStackFloat_uint64_t__voidft_fp)(StackFloatinstancep,uint64_t, void*);
typedef struct {_ftStackFloat_uint64_t__voidft_fp func;void* env;}_ftStackFloat_uint64_t__voidft__env;
typedef void (*_ftStackOpera__voidft_fp)(StackOperatorsinstance, void*);
typedef struct {_ftStackOpera__voidft_fp func;void* env;}_ftStackOpera__voidft__env;
typedef void (*_ftStackFloat_double__voidft_fp)(StackFloatinstancep,double, void*);
typedef struct {_ftStackFloat_double__voidft_fp func;void* env;}_ftStackFloat_double__voidft__env;
typedef void (*_ftStackFloat_StackOpera__voidft_fp)(StackFloatinstancep,StackOperatorsinstancep, void*);
typedef struct {_ftStackFloat_StackOpera__voidft_fp func;void* env;}_ftStackFloat_StackOpera__voidft__env;
typedef void (*_ftStackFloat_StackOpera_uint8_t__voidft_fp)(StackFloatinstancep,StackOperatorsinstancep,uint8_t, void*);
typedef struct {_ftStackFloat_StackOpera_uint8_t__voidft_fp func;void* env;}_ftStackFloat_StackOpera_uint8_t__voidft__env;
typedef struct {_ftuint64_t__StackFloatft__env __init__;_ftStackFloat__boolft__env __bool__;_ftStackFloat__voidft__env __del__;_ftStackFloat_uint64_t__voidft__env _extend;_ftStackFloat_double__voidft__env put;_ftStackFloat__doubleft__env pop;}StackFloattype;
typedef void (*_ftStackOpera_uint64_t__voidft_fp)(StackOperatorsinstancep,uint64_t, void*);
typedef struct {_ftStackOpera_uint64_t__voidft_fp func;void* env;}_ftStackOpera_uint64_t__voidft__env;
typedef void (*_ftStackOpera_uint8_t__voidft_fp)(StackOperatorsinstancep,uint8_t, void*);
typedef struct {_ftStackOpera_uint8_t__voidft_fp func;void* env;}_ftStackOpera_uint8_t__voidft__env;
typedef uint8_t (*_ftStackOpera__uint8_tft_fp)(StackOperatorsinstancep, void*);
typedef struct {_ftStackOpera__uint8_tft_fp func;void* env;}_ftStackOpera__uint8_tft__env;
typedef struct {_ftuint64_t__StackOperaft__env __init___;_ftStackOpera__boolft__env __bool___;_ftStackOpera__voidft__env __del___;_ftStackOpera_uint64_t__voidft__env _extend_;_ftStackOpera_uint8_t__voidft__env put_;_ftStackOpera__uint8_tft__env pop_;_ftStackOpera__uint8_tft__env head;}StackOperatorstype;
static inline doubles1 doubleps1_1(doublep pointer, size_t i_0, size_t d_0, char* position) {return (doubles1){pointer + i_0, d_0};}
static inline uint8_ts1 uint8_tps1_1(uint8_tp pointer, size_t i_0, size_t d_0, char* position) {return (uint8_ts1){pointer + i_0, d_0};}

#endif
