
#ifndef PROJ_4238894112_BASE_H
#define PROJ_4238894112_BASE_H
#include "base.h"
typedef struct {double x;double y;}MyClassinstance;
typedef void (*_ftMyClassins__voidft_fp)(MyClassinstance, void*);
typedef struct {_ftMyClassins__voidft_fp func;void* env;}_ftMyClassins__voidft__env;
typedef MyClassinstance (*_ftMyClassins_MyClassins__MyClassinsft_fp)(MyClassinstance,MyClassinstance, void*);
typedef struct {_ftMyClassins_MyClassins__MyClassinsft_fp func;void* env;}_ftMyClassins_MyClassins__MyClassinsft__env;
typedef MyClassinstance (*_ftdouble_double__MyClassinsft_fp)(double,double, void*);
typedef struct {_ftdouble_double__MyClassinsft_fp func;void* env;}_ftdouble_double__MyClassinsft__env;
typedef struct {_ftdouble_double__MyClassinsft__env __init__;_ftMyClassins_MyClassins__MyClassinsft__env __add__;_ftMyClassins__voidft__env print;}MyClasstype;

#endif
