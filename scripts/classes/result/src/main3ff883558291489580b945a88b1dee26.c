
#include "../include/main3ff883558291489580b945a88b1dee26.h"
MyClasstype MyClass = (MyClasstype){};MyClassinstance __init__g(double x,double y,void* _env){MyClassinstance self = (MyClassinstance){};{((self).x)=(x);
((self).y)=(y);
return self;
}}MyClassinstance __add__g(MyClassinstance self,MyClassinstance other,void* _env){return (((MyClass).__init__).func)(((self).x)+((other).x),((self).y)+((other).y),((MyClass).__init__).env);
}void printg(MyClassinstance self_,void* _env){((print_f_our).func)(c_str_to_slise("[%12.4f", 7),(self_).x,(print_f_our).env);
((print_f_our).func)(c_str_to_slise(" %12.4f]", 8),(self_).y,(print_f_our).env);
}_ftvoid__int64_tft__env not_very_main;int64_t not_very_maing(void* _par){MyClassinstance obj;
(obj)=((((MyClass).__add__).func)((((MyClass).__init__).func)((double)(1),(double)(1),((MyClass).__init__).env),(((MyClass).__init__).func)((double)(-(1)),(double)(2),((MyClass).__init__).env),((MyClass).__add__).env));
(((MyClass).print).func)(obj,((MyClass).print).env);
return 0;
}_ftvoid__int64_tft__env not_very_main = (_ftvoid__int64_tft__env){not_very_maing, NULL};void vars_initializer(){{_ftdouble_double__MyClassinsft__env __init__ = (_ftdouble_double__MyClassinsft__env){__init__g, NULL};_ftMyClassins_MyClassins__MyClassinsft__env __add__ = (_ftMyClassins_MyClassins__MyClassinsft__env){__add__g, NULL};_ftMyClassins__voidft__env print = (_ftMyClassins__voidft__env){printg, NULL};MyClass.__init__ = __init__;MyClass.__add__ = __add__;MyClass.print = print;}}