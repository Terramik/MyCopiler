
#include "../../include/Math/Quaternions.h"
Quaterniontype Quaternion = (Quaterniontype){};Quaternioninstance __init__g_4f07b89763b640558e38d16f53030c03(double w,double x,double y,double z,void* _env){Quaternioninstance self = (Quaternioninstance){};{((self).w)=(w);
((self).x)=(x);
((self).y)=(y);
((self).z)=(z);
return self;
}}void printg(Quaternioninstance self,IOStreaminstance stream,void* _env){(((IOStream).print_f).func)(&(stream),c_str_to_slise("[%12.3f, ", 9),(self).w,((IOStream).print_f).env);
(((IOStream).print_f).func)(&(stream),c_str_to_slise("%12.3fi, ", 9),(self).x,((IOStream).print_f).env);
(((IOStream).print_f).func)(&(stream),c_str_to_slise("%12.3fj, ", 9),(self).y,((IOStream).print_f).env);
(((IOStream).print_f).func)(&(stream),c_str_to_slise("%12.3fk]\n", 9),(self).z,((IOStream).print_f).env);
}Quaternioninstance __mul__g(Quaternioninstance self_,Quaternioninstance other,void* _env){return (((Quaternion).__init__).func)((((((self_).w)*((other).w))-(((self_).x)*((other).x)))-(((self_).y)*((other).y)))-(((self_).z)*((other).z)),(((((self_).w)*((other).x))+(((self_).x)*((other).w)))+(((self_).y)*((other).z)))-(((self_).z)*((other).y)),(((((self_).w)*((other).y))-(((self_).x)*((other).z)))+(((self_).y)*((other).w)))+(((self_).z)*((other).x)),(((((self_).w)*((other).z))+(((self_).x)*((other).y)))-(((self_).y)*((other).x)))+(((self_).z)*((other).w)),((Quaternion).__init__).env);
}double normg(Quaternioninstance self__34139905df474ce5810526642387822a,void* _env){return ((sqrt_our).func)((((((self__34139905df474ce5810526642387822a).x)*((self__34139905df474ce5810526642387822a).x))+(((self__34139905df474ce5810526642387822a).y)*((self__34139905df474ce5810526642387822a).y)))+(((self__34139905df474ce5810526642387822a).z)*((self__34139905df474ce5810526642387822a).z)))+(((self__34139905df474ce5810526642387822a).w)*((self__34139905df474ce5810526642387822a).w)),(sqrt_our).env);
}Quaternioninstance normalizeg(Quaternioninstance self__75a1f161b18c491384871fe9b1695dbc,void* _env){double norm_;
(norm_)=((((Quaternion).norm).func)(self__75a1f161b18c491384871fe9b1695dbc,((Quaternion).norm).env));
if ((((abs_our).func)(norm_,(abs_our).env))>(1e-6)){(norm_)=(((double)(1))/(norm_));
return (((Quaternion).__init__).func)(((self__75a1f161b18c491384871fe9b1695dbc).w)*(norm_),((self__75a1f161b18c491384871fe9b1695dbc).x)*(norm_),((self__75a1f161b18c491384871fe9b1695dbc).y)*(norm_),((self__75a1f161b18c491384871fe9b1695dbc).z)*(norm_),((Quaternion).__init__).env);
}else{}return self__75a1f161b18c491384871fe9b1695dbc;
}Quaternioninstance conjg(Quaternioninstance self__fa0b6b86b1274751915a43ace801c6e9,void* _env){return (((Quaternion).__init__).func)((self__fa0b6b86b1274751915a43ace801c6e9).w,-((self__fa0b6b86b1274751915a43ace801c6e9).x),-((self__fa0b6b86b1274751915a43ace801c6e9).y),-((self__fa0b6b86b1274751915a43ace801c6e9).z),((Quaternion).__init__).env);
}Quaternioninstance from_vectorg(doubles1 vec,void* _env){return (((Quaternion).__init__).func)((double)(0),vec.start[doubles1i(vec, (uint64_t)(0), "75:19-75:20")],vec.start[doubles1i(vec, (uint64_t)(1), "75:27-75:28")],vec.start[doubles1i(vec, (uint64_t)(2), "75:35-75:36")],((Quaternion).__init__).env);
}void to_vectorg(Quaternioninstance self__4f400cf07da94af4a805ca307dbe8fb6,doubles1 vec_,void* _env){(vec_.start[doubles1i(vec_, (uint64_t)(0), "80:12-80:13")])=((self__4f400cf07da94af4a805ca307dbe8fb6).x);
(vec_.start[doubles1i(vec_, (uint64_t)(1), "81:12-81:13")])=((self__4f400cf07da94af4a805ca307dbe8fb6).y);
(vec_.start[doubles1i(vec_, (uint64_t)(2), "82:12-82:13")])=((self__4f400cf07da94af4a805ca307dbe8fb6).z);
}void applyg(Quaternioninstance self__8c40b362473145b9936bf14f8d077d8d,doubles1 vec__bf656acc125d4176b4b9fa66917c6c5f,void* _env){Quaternioninstance q;
((assert_our).func)(((vec__bf656acc125d4176b4b9fa66917c6c5f)._0)==(3),c_str_to_slise("Bad vector", 10),(assert_our).env);
(q)=((((Quaternion).from_vector).func)(vec__bf656acc125d4176b4b9fa66917c6c5f,((Quaternion).from_vector).env));
(q)=((((Quaternion).__mul__).func)((((Quaternion).__mul__).func)(self__8c40b362473145b9936bf14f8d077d8d,q,((Quaternion).__mul__).env),(((Quaternion).conj).func)(self__8c40b362473145b9936bf14f8d077d8d,((Quaternion).conj).env),((Quaternion).__mul__).env));
(((Quaternion).to_vector).func)(q,vec__bf656acc125d4176b4b9fa66917c6c5f,((Quaternion).to_vector).env);
}Quaternioninstance from_axis_and_angleg(double angle,doublea3 axis,void* _env){double sin_;
(angle)=((angle)/((double)(2)));
(sin_)=(((sin_our).func)(angle,(sin_our).env));
return (((Quaternion).normalize).func)((((Quaternion).__init__).func)(((cos_our).func)(angle,(cos_our).env),(axis.arr[doublea3i((uint64_t)(0), "97:17-97:18")])*(sin_),(axis.arr[doublea3i((uint64_t)(1), "98:17-98:18")])*(sin_),(axis.arr[doublea3i((uint64_t)(2), "99:17-99:18")])*(sin_),((Quaternion).__init__).env),((Quaternion).normalize).env);
}void vars_initializer_5ee1d227985548cf8364093f4657b8e0(){{_ftdouble_double_double_double__Quaternionft__env __init__ = (_ftdouble_double_double_double__Quaternionft__env){__init__g_4f07b89763b640558e38d16f53030c03, NULL};_ftQuaternion_IOStreamin__voidft__env print = (_ftQuaternion_IOStreamin__voidft__env){printg, NULL};_ftQuaternion_Quaternion__Quaternionft__env __mul__ = (_ftQuaternion_Quaternion__Quaternionft__env){__mul__g, NULL};_ftQuaternion__doubleft__env norm = (_ftQuaternion__doubleft__env){normg, NULL};_ftQuaternion__Quaternionft__env normalize = (_ftQuaternion__Quaternionft__env){normalizeg, NULL};_ftQuaternion__Quaternionft__env conj = (_ftQuaternion__Quaternionft__env){conjg, NULL};_ftdoubles1__Quaternionft__env from_vector = (_ftdoubles1__Quaternionft__env){from_vectorg, NULL};_ftQuaternion_doubles1__voidft__env to_vector = (_ftQuaternion_doubles1__voidft__env){to_vectorg, NULL};_ftQuaternion_doubles1__voidft__env apply = (_ftQuaternion_doubles1__voidft__env){applyg, NULL};_ftdouble_doublea3__Quaternionft__env from_axis_and_angle = (_ftdouble_doublea3__Quaternionft__env){from_axis_and_angleg, NULL};Quaternion.__init__ = __init__;Quaternion.print = print;Quaternion.__mul__ = __mul__;Quaternion.norm = norm;Quaternion.normalize = normalize;Quaternion.conj = conj;Quaternion.from_vector = from_vector;Quaternion.to_vector = to_vector;Quaternion.apply = apply;Quaternion.from_axis_and_angle = from_axis_and_angle;}}