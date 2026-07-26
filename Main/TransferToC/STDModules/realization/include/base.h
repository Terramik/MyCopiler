
#ifndef PROJECT_BASE_H
#define PROJECT_BASE_H

#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

typedef double (*_ftdouble__doubleft_fp)(double, void*);
typedef struct {_ftdouble__doubleft_fp func;void* env;}_ftdouble__doubleft__env;
typedef int64_t (*_ftint64_t_int64_t__int64_tft_fp)(int64_t,int64_t, void*);
typedef struct {_ftint64_t_int64_t__int64_tft_fp func;void* env;}_ftint64_t_int64_t__int64_tft__env;
typedef struct {
            FILE* file;
            }IOStream_ourinstance;
typedef void (*_ftuint64_t__voidft_fp)(uint64_t, void*);
typedef struct {_ftuint64_t__voidft_fp func;void* env;}_ftuint64_t__voidft__env;
typedef void (*_ftint64_t__voidft_fp)(int64_t, void*);
typedef struct {_ftint64_t__voidft_fp func;void* env;}_ftint64_t__voidft__env;
typedef struct {uint8_t* start;size_t _0;}str_t;
static inline size_t str_ti (str_t slise, size_t i, char* position) {if ( i >= slise._0 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);abort();}return i;}
typedef int64_t (*_ftint64_t__int64_tft_fp)(int64_t, void*);
typedef struct {_ftint64_t__int64_tft_fp func;void* env;}_ftint64_t__int64_tft__env;
typedef int64_t (*_ftvoid__int64_tft_fp)(void*);
typedef struct {_ftvoid__int64_tft_fp func;void* env;}_ftvoid__int64_tft__env;
typedef double (*_ftdouble_double_double__doubleft_fp)(double,double,double, void*);
typedef struct {_ftdouble_double_double__doubleft_fp func;void* env;}_ftdouble_double_double__doubleft__env;
typedef double (*_ftdouble_double__doubleft_fp)(double,double, void*);
typedef struct {_ftdouble_double__doubleft_fp func;void* env;}_ftdouble_double__doubleft__env;
typedef void (*_ftvoid__voidft_fp)(void*);
typedef struct {_ftvoid__voidft_fp func;void* env;}_ftvoid__voidft__env;
typedef uint64_t (*_ftvoid__uint64_tft_fp)(void*);
typedef struct {_ftvoid__uint64_tft_fp func;void* env;}_ftvoid__uint64_tft__env;
typedef double (*_ftvoid__doubleft_fp)(void*);
typedef struct {_ftvoid__doubleft_fp func;void* env;}_ftvoid__doubleft__env;
typedef int8_t* int8_tp;typedef IOStream_ourinstance* IOStream_ourinstancep;typedef int8_tp (*_ftint8_tp_uint64_t__int8_tpft_fp)(int8_tp,uint64_t, void*);
typedef struct {_ftint8_tp_uint64_t__int8_tpft_fp func;void* env;}_ftint8_tp_uint64_t__int8_tpft__env;
typedef IOStream_ourinstance (*_ftvoid__IOStream_oft_fp)(void*);
typedef struct {_ftvoid__IOStream_oft_fp func;void* env;}_ftvoid__IOStream_oft__env;
typedef int8_tp (*_ftuint64_t__int8_tpft_fp)(uint64_t, void*);
typedef struct {_ftuint64_t__int8_tpft_fp func;void* env;}_ftuint64_t__int8_tpft__env;
typedef void (*_ftbool_str_t__voidft_fp)(bool,str_t, void*);
typedef struct {_ftbool_str_t__voidft_fp func;void* env;}_ftbool_str_t__voidft__env;
typedef IOStream_ourinstance (*_ftstr_t_str_t__IOStream_oft_fp)(str_t,str_t, void*);
typedef struct {_ftstr_t_str_t__IOStream_oft_fp func;void* env;}_ftstr_t_str_t__IOStream_oft__env;
typedef void (*_ftIOStream_o__voidft_fp)(IOStream_ourinstance, void*);
typedef struct {_ftIOStream_o__voidft_fp func;void* env;}_ftIOStream_o__voidft__env;
typedef void (*_ftint8_tp__voidft_fp)(int8_tp, void*);
typedef struct {_ftint8_tp__voidft_fp func;void* env;}_ftint8_tp__voidft__env;
typedef void (*_ftIOStream_o__voidft_fp_01124abdff20496cb7b017fd6d1e1f13)(IOStream_ourinstancep, void*);
typedef struct {_ftIOStream_o__voidft_fp_01124abdff20496cb7b017fd6d1e1f13 func;void* env;}_ftIOStream_o__voidft__env_58035f55156c462cbeaa80a7bba4f8b2;
typedef void (*_ftIOStream_o_str_t_uint64_t__voidft_fp)(IOStream_ourinstancep,str_t,uint64_t, void*);
typedef struct {_ftIOStream_o_str_t_uint64_t__voidft_fp func;void* env;}_ftIOStream_o_str_t_uint64_t__voidft__env;
typedef bool (*_ftIOStream_o__boolft_fp)(IOStream_ourinstancep, void*);
typedef struct {_ftIOStream_o__boolft_fp func;void* env;}_ftIOStream_o__boolft__env;
typedef void (*_ftIOStream_o_int64_t__voidft_fp)(IOStream_ourinstancep,int64_t, void*);
typedef struct {_ftIOStream_o_int64_t__voidft_fp func;void* env;}_ftIOStream_o_int64_t__voidft__env;
typedef int64_t (*_ftIOStream_o__int64_tft_fp)(IOStream_ourinstancep, void*);
typedef struct {_ftIOStream_o__int64_tft_fp func;void* env;}_ftIOStream_o__int64_tft__env;
typedef void (*_ftIOStream_o_uint8_t__voidft_fp)(IOStream_ourinstancep,uint8_t, void*);
typedef struct {_ftIOStream_o_uint8_t__voidft_fp func;void* env;}_ftIOStream_o_uint8_t__voidft__env;
typedef void (*_ftIOStream_o_str_t_double__voidft_fp)(IOStream_ourinstancep,str_t,double, void*);
typedef struct {_ftIOStream_o_str_t_double__voidft_fp func;void* env;}_ftIOStream_o_str_t_double__voidft__env;
typedef uint8_t (*_ftIOStream_o__uint8_tft_fp)(IOStream_ourinstancep, void*);
typedef struct {_ftIOStream_o__uint8_tft_fp func;void* env;}_ftIOStream_o__uint8_tft__env;
typedef uint64_t (*_ftIOStream_o_str_t__uint64_tft_fp)(IOStream_ourinstancep,str_t, void*);
typedef struct {_ftIOStream_o_str_t__uint64_tft_fp func;void* env;}_ftIOStream_o_str_t__uint64_tft__env;
typedef void (*_ftIOStream_o_str_t_bool__voidft_fp)(IOStream_ourinstancep,str_t,bool, void*);
typedef struct {_ftIOStream_o_str_t_bool__voidft_fp func;void* env;}_ftIOStream_o_str_t_bool__voidft__env;
typedef void (*_ftIOStream_o_str_t_uint8_t__voidft_fp)(IOStream_ourinstancep,str_t,uint8_t, void*);
typedef struct {_ftIOStream_o_str_t_uint8_t__voidft_fp func;void* env;}_ftIOStream_o_str_t_uint8_t__voidft__env;
typedef void (*_ftIOStream_o_str_t_int64_t__voidft_fp)(IOStream_ourinstancep,str_t,int64_t, void*);
typedef struct {_ftIOStream_o_str_t_int64_t__voidft_fp func;void* env;}_ftIOStream_o_str_t_int64_t__voidft__env;
typedef struct {_ftvoid__IOStream_oft__env __init__;_ftstr_t_str_t__IOStream_oft__env open;_ftIOStream_o__voidft__env __del__;_ftIOStream_o__boolft__env is_eof;_ftIOStream_o__boolft__env is_err;_ftIOStream_o__boolft__env good;_ftIOStream_o__uint8_tft__env getc;_ftIOStream_o_str_t__uint64_tft__env getl;_ftIOStream_o_str_t__uint64_tft__env gets;_ftIOStream_o_uint8_t__voidft__env putc;_ftIOStream_o_str_t__uint64_tft__env puts;_ftIOStream_o__int64_tft__env pos;_ftIOStream_o_int64_t__voidft__env gotos;_ftIOStream_o_int64_t__voidft__env jump;_ftIOStream_o_int64_t__voidft__env gotoe;_ftIOStream_o__voidft__env_58035f55156c462cbeaa80a7bba4f8b2 flush;_ftIOStream_o_str_t_int64_t__voidft__env print_i;_ftIOStream_o_str_t_uint64_t__voidft__env print_u;_ftIOStream_o_str_t_double__voidft__env print_f;_ftIOStream_o_str_t_bool__voidft__env print_b;_ftIOStream_o_str_t_uint8_t__voidft__env print_c;}IOStream_ourtype;
static inline str_t c_str_to_slise(char* str, size_t len){return (str_t){(uint8_t*)str, len};}
        
#endif

