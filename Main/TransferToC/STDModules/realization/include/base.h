
#ifndef PROJECT_BASE_H
#define PROJECT_BASE_H

#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

typedef void (*_ftuint64_t__voidft_fp)(uint64_t, void*);
typedef struct {_ftuint64_t__voidft_fp func;void* env;}_ftuint64_t__voidft__env;
typedef int64_t (*_ftint64_t_int64_t__int64_tft_fp)(int64_t,int64_t, void*);
typedef struct {_ftint64_t_int64_t__int64_tft_fp func;void* env;}_ftint64_t_int64_t__int64_tft__env;
typedef double (*_ftvoid__doubleft_fp)(void*);
typedef struct {_ftvoid__doubleft_fp func;void* env;}_ftvoid__doubleft__env;
typedef void (*_ftint64_t__voidft_fp)(int64_t, void*);
typedef struct {_ftint64_t__voidft_fp func;void* env;}_ftint64_t__voidft__env;
typedef double (*_ftdouble__doubleft_fp)(double, void*);
typedef struct {_ftdouble__doubleft_fp func;void* env;}_ftdouble__doubleft__env;
typedef int64_t (*_ftvoid__int64_tft_fp)(void*);
typedef struct {_ftvoid__int64_tft_fp func;void* env;}_ftvoid__int64_tft__env;
typedef int64_t (*_ftint64_t__int64_tft_fp)(int64_t, void*);
typedef struct {_ftint64_t__int64_tft_fp func;void* env;}_ftint64_t__int64_tft__env;
typedef uint64_t (*_ftvoid__uint64_tft_fp)(void*);
typedef struct {_ftvoid__uint64_tft_fp func;void* env;}_ftvoid__uint64_tft__env;
typedef struct {
            FILE* file;
            }IOStreaminstance;
typedef void (*_ftvoid__voidft_fp)(void*);
typedef struct {_ftvoid__voidft_fp func;void* env;}_ftvoid__voidft__env;
typedef double (*_ftdouble_double__doubleft_fp)(double,double, void*);
typedef struct {_ftdouble_double__doubleft_fp func;void* env;}_ftdouble_double__doubleft__env;
typedef double (*_ftdouble_double_double__doubleft_fp)(double,double,double, void*);
typedef struct {_ftdouble_double_double__doubleft_fp func;void* env;}_ftdouble_double_double__doubleft__env;
typedef struct {uint8_t* start;size_t _0;}str_t;
static inline size_t str_ti (str_t slise, size_t i, char* position) {if ( i >= slise._0 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);abort();}return i;}
typedef int8_t* int8_tp;typedef void (*_ftint8_tp__voidft_fp)(int8_tp, void*);
typedef struct {_ftint8_tp__voidft_fp func;void* env;}_ftint8_tp__voidft__env;
typedef IOStreaminstance (*_ftstr_t_str_t__IOStreaminft_fp)(str_t,str_t, void*);
typedef struct {_ftstr_t_str_t__IOStreaminft_fp func;void* env;}_ftstr_t_str_t__IOStreaminft__env;
typedef int8_tp (*_ftint8_tp_uint64_t__int8_tpft_fp)(int8_tp,uint64_t, void*);
typedef struct {_ftint8_tp_uint64_t__int8_tpft_fp func;void* env;}_ftint8_tp_uint64_t__int8_tpft__env;
typedef IOStreaminstance* IOStreaminstancep;typedef int8_tp (*_ftuint64_t__int8_tpft_fp)(uint64_t, void*);
typedef struct {_ftuint64_t__int8_tpft_fp func;void* env;}_ftuint64_t__int8_tpft__env;
typedef void (*_ftbool_str_t__voidft_fp)(bool,str_t, void*);
typedef struct {_ftbool_str_t__voidft_fp func;void* env;}_ftbool_str_t__voidft__env;
typedef void (*_ftIOStreamin__voidft_fp)(IOStreaminstance, void*);
typedef struct {_ftIOStreamin__voidft_fp func;void* env;}_ftIOStreamin__voidft__env;
typedef IOStreaminstance (*_ftvoid__IOStreaminft_fp)(void*);
typedef struct {_ftvoid__IOStreaminft_fp func;void* env;}_ftvoid__IOStreaminft__env;
typedef void (*_ftIOStreamin_uint8_t__voidft_fp)(IOStreaminstancep,uint8_t, void*);
typedef struct {_ftIOStreamin_uint8_t__voidft_fp func;void* env;}_ftIOStreamin_uint8_t__voidft__env;
typedef void (*_ftIOStreamin_str_t_uint64_t__voidft_fp)(IOStreaminstancep,str_t,uint64_t, void*);
typedef struct {_ftIOStreamin_str_t_uint64_t__voidft_fp func;void* env;}_ftIOStreamin_str_t_uint64_t__voidft__env;
typedef void (*_ftIOStreamin__voidft_fp_6d27eed8860443e18bc847e547633e92)(IOStreaminstancep, void*);
typedef struct {_ftIOStreamin__voidft_fp_6d27eed8860443e18bc847e547633e92 func;void* env;}_ftIOStreamin__voidft__env_9cf0ff69457546c0bbcef63b459833a7;
typedef void (*_ftIOStreamin_str_t_int64_t__voidft_fp)(IOStreaminstancep,str_t,int64_t, void*);
typedef struct {_ftIOStreamin_str_t_int64_t__voidft_fp func;void* env;}_ftIOStreamin_str_t_int64_t__voidft__env;
typedef bool (*_ftIOStreamin__boolft_fp)(IOStreaminstancep, void*);
typedef struct {_ftIOStreamin__boolft_fp func;void* env;}_ftIOStreamin__boolft__env;
typedef void (*_ftIOStreamin_int64_t__voidft_fp)(IOStreaminstancep,int64_t, void*);
typedef struct {_ftIOStreamin_int64_t__voidft_fp func;void* env;}_ftIOStreamin_int64_t__voidft__env;
typedef void (*_ftIOStreamin_str_t_bool__voidft_fp)(IOStreaminstancep,str_t,bool, void*);
typedef struct {_ftIOStreamin_str_t_bool__voidft_fp func;void* env;}_ftIOStreamin_str_t_bool__voidft__env;
typedef uint64_t (*_ftIOStreamin_str_t__uint64_tft_fp)(IOStreaminstancep,str_t, void*);
typedef struct {_ftIOStreamin_str_t__uint64_tft_fp func;void* env;}_ftIOStreamin_str_t__uint64_tft__env;
typedef void (*_ftIOStreamin_str_t_uint8_t__voidft_fp)(IOStreaminstancep,str_t,uint8_t, void*);
typedef struct {_ftIOStreamin_str_t_uint8_t__voidft_fp func;void* env;}_ftIOStreamin_str_t_uint8_t__voidft__env;
typedef void (*_ftIOStreamin_str_t_double__voidft_fp)(IOStreaminstancep,str_t,double, void*);
typedef struct {_ftIOStreamin_str_t_double__voidft_fp func;void* env;}_ftIOStreamin_str_t_double__voidft__env;
typedef int64_t (*_ftIOStreamin__int64_tft_fp)(IOStreaminstancep, void*);
typedef struct {_ftIOStreamin__int64_tft_fp func;void* env;}_ftIOStreamin__int64_tft__env;
typedef uint8_t (*_ftIOStreamin__uint8_tft_fp)(IOStreaminstancep, void*);
typedef struct {_ftIOStreamin__uint8_tft_fp func;void* env;}_ftIOStreamin__uint8_tft__env;
typedef struct {_ftvoid__IOStreaminft__env __init__;_ftstr_t_str_t__IOStreaminft__env open;_ftIOStreamin__voidft__env __del__;_ftIOStreamin__boolft__env is_eof;_ftIOStreamin__boolft__env is_err;_ftIOStreamin__boolft__env good;_ftIOStreamin__uint8_tft__env getc;_ftIOStreamin_str_t__uint64_tft__env getl;_ftIOStreamin_str_t__uint64_tft__env gets;_ftIOStreamin_uint8_t__voidft__env putc;_ftIOStreamin_str_t__uint64_tft__env puts;_ftIOStreamin__int64_tft__env pos;_ftIOStreamin_int64_t__voidft__env gotos;_ftIOStreamin_int64_t__voidft__env jump;_ftIOStreamin_int64_t__voidft__env gotoe;_ftIOStreamin__voidft__env_9cf0ff69457546c0bbcef63b459833a7 flush;_ftIOStreamin_str_t_int64_t__voidft__env print_i;_ftIOStreamin_str_t_uint64_t__voidft__env print_u;_ftIOStreamin_str_t_double__voidft__env print_f;_ftIOStreamin_str_t_bool__voidft__env print_b;_ftIOStreamin_str_t_uint8_t__voidft__env print_c;}IOStreamtype;
static inline str_t c_str_to_slise(char* str, size_t len){return (str_t){(uint8_t*)str, len};}
        
#endif

