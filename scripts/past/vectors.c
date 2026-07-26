
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
typedef struct
{
    double arr[6];
} doublea6;
static inline size_t doublea6i(size_t i, char *position)
{
    if (i >= 6)
    {
        printf("Index %zu out of array range 6 on %s\n", i, position);
        abort();
    }
    return i;
}
typedef struct
{
    double arr[4];
} doublea4;
static inline size_t doublea4i(size_t i, char *position)
{
    if (i >= 4)
    {
        printf("Index %zu out of array range 4 on %s\n", i, position);
        abort();
    }
    return i;
}
typedef struct
{
    double *start;
    size_t _0;
} doubles1;
static inline size_t doubles1i(doubles1 slise, size_t i, char *position)
{
    if (i >= slise._0)
    {
        printf("Index %zu out of slise range %zu on %s\n", i, slise._0, position);
        abort();
    }
    return i;
}
typedef int64_t (*intfp)(void *);
typedef struct
{
    intfp func;
    void *env;
} intenv;
typedef void (*intintfp)(int8_ts1, int8_t, void *);
typedef struct
{
    intintfp func;
    void *env;
} intintenv;
typedef void (*doudoudoufp)(doubles1, doubles1, doubles1, void *);
typedef struct
{
    doudoudoufp func;
    void *env;
} doudoudouenv;
typedef void (*intintfp_740954a038924b4eba17903fe13ca869)(int8_ts1, int64_t, void *);
typedef struct
{
    intintfp_740954a038924b4eba17903fe13ca869 func;
    void *env;
} intintenv_26d62ffe7e7c4f6cb638a9b1b366ac35;
typedef void (*intboofp)(int8_ts1, bool, void *);
typedef struct
{
    intboofp func;
    void *env;
} intbooenv;
typedef void (*doufp)(doubles1, void *);
typedef struct
{
    doufp func;
    void *env;
} douenv;
typedef double (*doudoudoufp_dbecae969ab14a38af76b6827e033a5e)(doubles1, doubles1, void *);
typedef struct
{
    doudoudoufp_dbecae969ab14a38af76b6827e033a5e func;
    void *env;
} doudoudouenv_a2f139c00d0646d69a0e67b3c0732fd9;
typedef void (*intdoufp)(int8_ts1, double, void *);
typedef struct
{
    intdoufp func;
    void *env;
} intdouenv;
typedef void (*intfp_e6621f3e6ed547bebdd60613fab4aa9f)(int8_ts1, void *);
typedef struct
{
    intfp_e6621f3e6ed547bebdd60613fab4aa9f func;
    void *env;
} intenv_5c2901accaaf4c42aa427afb0f604d37;
typedef void (*intuinfp)(int8_ts1, uint64_t, void *);
typedef struct
{
    intuinfp func;
    void *env;
} intuinenv;
static inline doubles1 doublea4s1_1(doublea4 *array, size_t i_0, size_t d_0, char *position)
{
    if (i_0 >= 4)
    {
        printf("Index %zu out of array range 4 in 1index of slice creation on %s\n", i_0, position);
        abort();
    }
    size_t max_total_size = (4 - i_0);
    size_t total_size = d_0;
    if (total_size > max_total_size)
    {
        printf("Size of slice %zu out of allowed sliced array size %zu on %s\n", total_size, max_total_size, position);
        abort();
    }
    return (doubles1){&(array->arr[i_0]), d_0};
}
static inline doubles1 doublea6s1_1(doublea6 *array, size_t i_0, size_t d_0, char *position)
{
    if (i_0 >= 6)
    {
        printf("Index %zu out of array range 6 in 1index of slice creation on %s\n", i_0, position);
        abort();
    }
    size_t max_total_size = (6 - i_0);
    size_t total_size = d_0;
    if (total_size > max_total_size)
    {
        printf("Size of slice %zu out of allowed sliced array size %zu on %s\n", total_size, max_total_size, position);
        abort();
    }
    return (doubles1){&(array->arr[i_0]), d_0};
}
static inline int8_ts1 c_str_to_slise(char *str, size_t len) { return (int8_ts1){(int8_t *)str, len}; }
intintenv_26d62ffe7e7c4f6cb638a9b1b366ac35 print_i;
static inline void print_itemp(int8_ts1 format, int64_t i, void *_env) { printf(format.start, i); }
intintenv_26d62ffe7e7c4f6cb638a9b1b366ac35 print_i = (intintenv_26d62ffe7e7c4f6cb638a9b1b366ac35){print_itemp, NULL};
intuinenv print_ui;
static inline void print_uitemp(int8_ts1 format, uint64_t i, void *_env) { printf(format.start, i); }
intuinenv print_ui = (intuinenv){print_uitemp, NULL};
intdouenv print_f;
static inline void print_ftemp(int8_ts1 format, double f, void *_env) { printf(format.start, f); }
intdouenv print_f = (intdouenv){print_ftemp, NULL};
intbooenv print_b;
static inline void print_btemp(int8_ts1 format, bool b, void *_env) { printf(format.start, b ? "true" : "false"); }
intbooenv print_b = (intbooenv){print_btemp, NULL};
intintenv print_c;
static inline void print_ctemp(int8_ts1 format, int8_t c, void *_env) { printf(format.start, c); }
intintenv print_c = (intintenv){print_ctemp, NULL};
intenv_5c2901accaaf4c42aa427afb0f604d37 print_s;
static inline void print_stemp(int8_ts1 format, void *_env) { printf(format.start); }
intenv_5c2901accaaf4c42aa427afb0f604d37 print_s = (intenv_5c2901accaaf4c42aa427afb0f604d37){print_stemp, NULL};
douenv v_printg;
void v_printtemp(doubles1 v, void *_par)
{
    uint64_t i;
    uint64_t n;
    (n) = ((uint64_t)((v)._0));
    (i) = ((uint64_t)(0));
    ((print_s).func)(c_str_to_slise("[", 3), (print_s).env);
    while ((i) < (n))
    {
        ((print_f).func)(c_str_to_slise("%9.3f ", 8), v.start[doubles1i(v, i, "10:28-10:29")], (print_f).env);
        (i) = ((i) + ((uint64_t)(1)));
    }
    ((print_s).func)(c_str_to_slise("]\n", 5), (print_s).env);
}
douenv v_printg = (douenv){v_printtemp, NULL};
doudoudouenv v_addg;
void v_addtemp(doubles1 v1, doubles1 v2, doubles1 vr, void *_par)
{
    uint64_t i;
    uint64_t n;
    (n) = ((uint64_t)((v1)._0));
    (i) = ((uint64_t)(0));
    while ((i) < (n))
    {
        (vr.start[doubles1i(vr, i, "19:11-19:12")]) = ((v1.start[doubles1i(v1, i, "19:19-19:20")]) + (v2.start[doubles1i(v2, i, "19:27-19:28")]));
        (i) = ((i) + ((uint64_t)(1)));
    }
}
doudoudouenv v_addg = (doudoudouenv){v_addtemp, NULL};
doudoudouenv v_subg;
void v_subtemp(doubles1 v1, doubles1 v2, doubles1 vr, void *_par)
{
    uint64_t i;
    uint64_t n;
    (n) = ((uint64_t)((v1)._0));
    (i) = ((uint64_t)(0));
    while ((i) < (n))
    {
        (vr.start[doubles1i(vr, i, "27:11-27:12")]) = ((v1.start[doubles1i(v1, i, "27:19-27:20")]) - (v2.start[doubles1i(v2, i, "27:27-27:28")]));
        (i) = ((i) + ((uint64_t)(1)));
    }
}
doudoudouenv v_subg = (doudoudouenv){v_subtemp, NULL};
doudoudouenv v_mulg;
void v_multemp(doubles1 v1, doubles1 v2, doubles1 vr, void *_par)
{
    uint64_t i;
    uint64_t n;
    (n) = ((uint64_t)((v1)._0));
    (i) = ((uint64_t)(0));
    while ((i) < (n))
    {
        (vr.start[doubles1i(vr, i, "35:11-35:12")]) = ((v1.start[doubles1i(v1, i, "35:19-35:20")]) * (v2.start[doubles1i(v2, i, "35:27-35:28")]));
        (i) = ((i) + ((uint64_t)(1)));
    }
}
doudoudouenv v_mulg = (doudoudouenv){v_multemp, NULL};
doudoudouenv_a2f139c00d0646d69a0e67b3c0732fd9 v_dotg;
double v_dottemp(doubles1 v1, doubles1 v2, void *_par)
{
    double accumulator;
    uint64_t i;
    uint64_t n;
    (n) = ((uint64_t)((v1)._0));
    (i) = ((uint64_t)(0));
    (accumulator) = (0.0);
    while ((i) < (n))
    {
        (accumulator) = ((accumulator) + ((v1.start[doubles1i(v1, i, "44:39-44:40")]) * (v2.start[doubles1i(v2, i, "44:47-44:48")])));
        (i) = ((i) + ((uint64_t)(1)));
    }
    return accumulator;
}
doudoudouenv_a2f139c00d0646d69a0e67b3c0732fd9 v_dotg = (doudoudouenv_a2f139c00d0646d69a0e67b3c0732fd9){v_dottemp, NULL};
douenv sortg;
void sorttemp(doubles1 arr, void *_par)
{
    uint64_t i1;
    uint64_t n;
    (n) = ((uint64_t)((arr)._0));
    (i1) = ((uint64_t)(0));
    while ((i1) < (n))
    {
        uint64_t max_index;
        double max_val;
        uint64_t i2;
        (i2) = (i1);
        (max_val) = (arr.start[doubles1i(arr, i2, "55:34-55:36")]);
        (max_index) = (i2);
        while ((i2) < (n))
        {
            if ((arr.start[doubles1i(arr, i2, "59:19-59:21")]) > (max_val))
            {
                (max_val) = (arr.start[doubles1i(arr, i2, "60:30-60:32")]);
                (max_index) = (i2);
            }
            (i2) = ((i2) + ((uint64_t)(1)));
        }
        {
            double _0 = arr.start[doubles1i(arr, max_index, "66:38-66:47")];
            double _1 = arr.start[doubles1i(arr, i1, "66:54-66:56")];
            arr.start[doubles1i(arr, i1, "66:12-66:14")] = _0;
            arr.start[doubles1i(arr, max_index, "66:21-66:30")] = _1;
        }
        (i1) = ((i1) + ((uint64_t)(1)));
    }
}
douenv sortg = (douenv){sorttemp, NULL};
intenv maing;
int64_t maintemp(void *_par)
{
    doublea6 arr;
    doublea4 vr;
    doublea4 v2;
    doublea4 v1;
    (v1) = ((doublea4){{1.5, 2.1, 3.5, 4.1}});
    (v2) = ((doublea4){{5.5, 6.1, 7.5, 8.1}});
    (vr) = ((doublea4){{1.5, 1.1, 2.5, 2.1}});
    ((v_addg).func)(doublea4s1_1(&(v1), (uint64_t)(0), 4, "77:12-77:15"), doublea4s1_1(&(v2), (uint64_t)(0), 4, "77:19-77:22"), doublea4s1_1(&(vr), (uint64_t)(0), 4, "77:26-77:29"), (v_addg).env);
    ((v_printg).func)(doublea4s1_1(&(vr), (uint64_t)(0), 4, "78:14-78:17"), (v_printg).env);
    ((v_mulg).func)(doublea4s1_1(&(v1), (uint64_t)(0), 4, "79:12-79:15"), doublea4s1_1(&(v1), (uint64_t)(0), 4, "79:19-79:22"), doublea4s1_1(&(vr), (uint64_t)(0), 4, "79:26-79:29"), (v_mulg).env);
    ((v_printg).func)(doublea4s1_1(&(vr), (uint64_t)(0), 4, "80:14-80:17"), (v_printg).env);
    ((print_f).func)(c_str_to_slise("%9.3f\n", 9), ((v_dotg).func)(doublea4s1_1(&(v1), (uint64_t)(0), 4, "81:31-81:34"), doublea4s1_1(&(v2), (uint64_t)(0), 4, "81:38-81:41"), (v_dotg).env), (print_f).env);
    (arr) = ((doublea6){{3.14, 4.0, 5.0, 100.0, -(300.0), ((1.0) * ((double)(2))) * ((double)(3))}});
    ((sortg).func)(doublea6s1_1(&(arr), (uint64_t)(0), 6, "83:12-83:15"), (sortg).env);
    ((v_printg).func)(doublea6s1_1(&(arr), (uint64_t)(0), 6, "84:15-84:18"), (v_printg).env);
    return 0;
}
intenv maing = (intenv){maintemp, NULL};
int main(void)
{
    maing.func(maing.env);
    return 0;
}
