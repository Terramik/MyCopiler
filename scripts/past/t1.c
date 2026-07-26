
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
typedef struct
{
    int8_t *start;
    size_t _0;
} int8_ts1;
static inline size_t int8_ts1i(int8_ts1 slise, size_t i, char *position)
{
    if (i >= slise._0)
    {
        printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);
        abort();
    }
    return i;
}
typedef int64_t (*intintfp)(int64_t, void *);
typedef struct
{
    intintfp func;
    void *env;
} intintenv;
typedef void (*fp)(void *);
typedef struct
{
    fp func;
    void *env;
} env;
typedef void (*intboofp)(int8_ts1, bool, void *);
typedef struct
{
    intboofp func;
    void *env;
} intbooenv;
typedef void (*intfp)(int8_ts1, void *);
typedef struct
{
    intfp func;
    void *env;
} intenv;
typedef void (*intdoufp)(int8_ts1, double, void *);
typedef struct
{
    intdoufp func;
    void *env;
} intdouenv;
typedef void (*intintfp_d4a89963e50d475e9e34311d189a2387)(int8_ts1, int8_t, void *);
typedef struct
{
    intintfp_d4a89963e50d475e9e34311d189a2387 func;
    void *env;
} intintenv_91f7d1e7c84e41a7abd9943ef8744c7f;
typedef void (*intintfp_d07e304595f141dda4810020d6afed95)(int8_ts1, int64_t, void *);
typedef struct
{
    intintfp_d07e304595f141dda4810020d6afed95 func;
    void *env;
} intintenv_184dba03616240919f6fd99f7fc66872;
typedef void (*intuinfp)(int8_ts1, uint64_t, void *);
typedef struct
{
    intuinfp func;
    void *env;
} intuinenv;
static inline int8_ts1 c_str_to_slise(char *str, size_t len) { return (int8_ts1){(int8_t *)str, len}; }
intintenv_184dba03616240919f6fd99f7fc66872 print_i;
static inline void print_itemp(int8_ts1 format, int64_t i, void *_env) { printf(format.start, i); }
intintenv_184dba03616240919f6fd99f7fc66872 print_i = (intintenv_184dba03616240919f6fd99f7fc66872){print_itemp, NULL};
intuinenv print_ui;
static inline void print_uitemp(int8_ts1 format, uint64_t i, void *_env) { printf(format.start, i); }
intuinenv print_ui = (intuinenv){print_uitemp, NULL};
intdouenv print_f;
static inline void print_ftemp(int8_ts1 format, double f, void *_env) { printf(format.start, f); }
intdouenv print_f = (intdouenv){print_ftemp, NULL};
intbooenv print_b;
static inline void print_btemp(int8_ts1 format, bool b, void *_env) { printf(format.start, b ? "true" : "false"); }
intbooenv print_b = (intbooenv){print_btemp, NULL};
intintenv_91f7d1e7c84e41a7abd9943ef8744c7f print_c;
static inline void print_ctemp(int8_ts1 format, int8_t c, void *_env) { printf(format.start, c); }
intintenv_91f7d1e7c84e41a7abd9943ef8744c7f print_c = (intintenv_91f7d1e7c84e41a7abd9943ef8744c7f){print_ctemp, NULL};
intenv print_s;
static inline void print_stemp(int8_ts1 format, void *_env) { printf(format.start); }
intenv print_s = (intenv){print_stemp, NULL};
int64_t glob_blob;
intintenv nonconstg;
int64_t nonconsttemp(int64_t i, void *_par)
{
    return ((i) * (i)) * (3);
}
intintenv nonconstg = (intintenv){nonconsttemp, NULL};
typedef struct
{
    int64_t *i;
} main_blockset_10globenv;
void main_blockset_10glob(void *_env)
{
    main_blockset_10globenv *env = (main_blockset_10globenv *)_env;
    {
        ((*env->i)) = (10);
    }
}
typedef struct
{
    int64_t *i;
} main_blockset_0globenv;
void main_blockset_0glob(void *_env)
{
    main_blockset_0globenv *env = (main_blockset_0globenv *)_env;
    {
        ((*env->i)) = (0);
    }
}
int64_t main_blocksqglob(int64_t v, void *_env)
{
    return (v) * (v);
}
env maing;
void maintemp(void *_par)
{
    int64_t i;
    (i) = (10);
    main_blockset_10globenv main_blockset_10globenv_ex = (main_blockset_10globenv){&(i)};
    env main_blockset_10 = (env){main_blockset_10glob, &main_blockset_10globenv_ex};
    main_blockset_0globenv main_blockset_0globenv_ex = (main_blockset_0globenv){&(i)};
    env main_blockset_0 = (env){main_blockset_0glob, &main_blockset_0globenv_ex};
    ((print_i).func)(c_str_to_slise("start: %d\n", 13), i, (print_i).env);
    ((main_blockset_0).func)((main_blockset_0).env);
    ((print_i).func)(c_str_to_slise("0: %d\n", 9), i, (print_i).env);
    ((main_blockset_10).func)((main_blockset_10).env);
    ((print_i).func)(c_str_to_slise("10: %d\n", 10), i, (print_i).env);
    intintenv main_blocksq = (intintenv){main_blocksqglob, NULL};
    ((print_i).func)(c_str_to_slise("sq: %d\n", 10), ((main_blocksq).func)(i, (main_blocksq).env), (print_i).env);
    ((print_i).func)(c_str_to_slise("glob_blob: %d\n", 17), glob_blob, (print_i).env);
}
env maing = (env){maintemp, NULL};
int main(void)
{
    (glob_blob) = (((nonconstg).func)(3, (nonconstg).env));
    maing.func(maing.env);
    return 0;
}
