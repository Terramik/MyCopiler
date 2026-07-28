
#include "../include/base.h"

#include <math.h>

_ftdouble__doubleft__env abs_our;   
double abs_ourg(double f,void* _par){
    
        return fabs(f);
        
}
_ftdouble__doubleft__env abs_our = (_ftdouble__doubleft__env){abs_ourg, NULL};


_ftint64_t__int64_tft__env absi_our;   
int64_t absi_ourg(int64_t i,void* _par){
    
        return (i < 0) ? -i : i;
        
}
_ftint64_t__int64_tft__env absi_our = (_ftint64_t__int64_tft__env){absi_ourg, NULL};


_ftdouble__doubleft__env sin_our;   
double sin_ourg(double f,void* _par){
    
        return sin(f);
        
}
_ftdouble__doubleft__env sin_our = (_ftdouble__doubleft__env){sin_ourg, NULL};


_ftdouble__doubleft__env cos_our;   
double cos_ourg(double f,void* _par){
    
        return cos(f);
        
}
_ftdouble__doubleft__env cos_our = (_ftdouble__doubleft__env){cos_ourg, NULL};


_ftdouble__doubleft__env tan_our;   
double tan_ourg(double f,void* _par){
    
        return tan(f);
        
}
_ftdouble__doubleft__env tan_our = (_ftdouble__doubleft__env){tan_ourg, NULL};


_ftdouble__doubleft__env asin_our;   
double asin_ourg(double f,void* _par){
    
        return asin(f);
        
}
_ftdouble__doubleft__env asin_our = (_ftdouble__doubleft__env){asin_ourg, NULL};


_ftdouble__doubleft__env acos_our;   
double acos_ourg(double f,void* _par){
    
        return acos(f);
        
}
_ftdouble__doubleft__env acos_our = (_ftdouble__doubleft__env){acos_ourg, NULL};


_ftdouble__doubleft__env atan_our;   
double atan_ourg(double f,void* _par){
    
        return atan(f);
        
}
_ftdouble__doubleft__env atan_our = (_ftdouble__doubleft__env){atan_ourg, NULL};


_ftdouble_double__doubleft__env atan2_our;   
double atan2_ourg(double x, double y,void* _par){
    
        return atan2(y, x);
        
}
_ftdouble_double__doubleft__env atan2_our = (_ftdouble_double__doubleft__env){atan2_ourg, NULL};


_ftdouble__doubleft__env exp_our;   
double exp_ourg(double f,void* _par){
    
        return exp(f);
        
}
_ftdouble__doubleft__env exp_our = (_ftdouble__doubleft__env){exp_ourg, NULL};


_ftdouble__doubleft__env log_our;   
double log_ourg(double f,void* _par){
    
        return log(f);
        
}
_ftdouble__doubleft__env log_our = (_ftdouble__doubleft__env){log_ourg, NULL};


_ftdouble__doubleft__env log2_our;   
double log2_ourg(double f,void* _par){
    
        return log2(f);
        
}
_ftdouble__doubleft__env log2_our = (_ftdouble__doubleft__env){log2_ourg, NULL};


_ftdouble__doubleft__env log10_our;   
double log10_ourg(double f,void* _par){
    
        return log10(f);
        
}
_ftdouble__doubleft__env log10_our = (_ftdouble__doubleft__env){log10_ourg, NULL};


_ftdouble_double__doubleft__env pow_our;   
double pow_ourg(double base, double power,void* _par){
    
        return pow(base, power);
        
}
_ftdouble_double__doubleft__env pow_our = (_ftdouble_double__doubleft__env){pow_ourg, NULL};


_ftdouble__doubleft__env sqrt_our;   
double sqrt_ourg(double f,void* _par){
    
        return sqrt(f);
        
}
_ftdouble__doubleft__env sqrt_our = (_ftdouble__doubleft__env){sqrt_ourg, NULL};


_ftdouble__doubleft__env floor_our;   
double floor_ourg(double f,void* _par){
    
        return floor(f);
        
}
_ftdouble__doubleft__env floor_our = (_ftdouble__doubleft__env){floor_ourg, NULL};


_ftdouble__doubleft__env round_our;   
double round_ourg(double f,void* _par){
    
        return round(f);
        
}
_ftdouble__doubleft__env round_our = (_ftdouble__doubleft__env){round_ourg, NULL};


_ftdouble__doubleft__env ceil_our;   
double ceil_ourg(double f,void* _par){
    
        return ceil(f);
        
}
_ftdouble__doubleft__env ceil_our = (_ftdouble__doubleft__env){ceil_ourg, NULL};


_ftdouble_double_double__doubleft__env clamp_our;   
double clamp_ourg(double f, double min, double max,void* _par){
    
        if (f < min) return min;
        if (f > max) return max;
        return f;
        
}
_ftdouble_double_double__doubleft__env clamp_our = (_ftdouble_double_double__doubleft__env){clamp_ourg, NULL};

double PI_our;
double E_our;
void vars_initializer_math(){PI_our = 3.141592653589793238462643383279;
E_our = 2.718281828459045235360287471352;
}