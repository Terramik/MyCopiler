
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
typedef struct {int8_t* start;size_t _0;}int8_ts1;
static inline size_t int8_ts1i (int8_ts1 slise, size_t i, char* position) {if ( i >= slise._0 ){printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);abort();}return i;}
typedef int32_t (*intfp)(void*);
typedef struct {intfp func;void* env;}intenc;
static inline int8_ts1 c_str_to_slise (char* str, size_t len) {return (int8_ts1){(int8_t*)str, len};}
static inline void print_i(int8_ts1 format, int64_t i){ printf(format.start, i); }
static inline void print_ui(int8_ts1 format, uint64_t i){ printf(format.start, i); }
static inline void print_f(int8_ts1 format, double f){ printf(format.start, f); }
static inline void print_b(int8_ts1 format, bool b){ printf(format.start, b ? "true" : "false"); }
static inline void print_c(int8_ts1 format, int8_t c){ printf(format.start, c); }
static inline void print_s(int8_ts1 s){ printf(s.start); }
intenc main_0670a5f948164d71aa4ba9eddda0150d;int32_t maintemp(void* _par){int32_t s;
int32_t i;
(i)=((int32_t)(0));
(s)=((int32_t)(0));
while (((int64_t)(i))<(10)){(s)=((s)+(i));
(i)=((int32_t)(((int64_t)(i))+(1)));
}return s;
}intenc main_0670a5f948164d71aa4ba9eddda0150d = (intenc){maintemp, NULL};