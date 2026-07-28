
#include "../../include/Math/Quaternions.h"
Quaterniontype Quaternion = (Quaterniontype){};Quaternioninstance __init__g_dbdc9a857b5147dbaa9b1d9871aad60f(double w,double x,double y,double z,void* _env){Quaternioninstance self = (Quaternioninstance){};{((self).w)=(w);
((self).x)=(x);
((self).y)=(y);
((self).z)=(z);
return self;
}}void printg(Quaternioninstance self,IOStream_ourinstance stream,void* _env){(((IOStream_our).print_f).func)(&(stream),c_str_to_slise("[%12.3f, ", 9),(self).w,((IOStream_our).print_f).env);
(((IOStream_our).print_f).func)(&(stream),c_str_to_slise("%12.3fi, ", 9),(self).x,((IOStream_our).print_f).env);
(((IOStream_our).print_f).func)(&(stream),c_str_to_slise("%12.3fj, ", 9),(self).y,((IOStream_our).print_f).env);
(((IOStream_our).print_f).func)(&(stream),c_str_to_slise("%12.3fk]\n", 9),(self).z,((IOStream_our).print_f).env);
}Quaternioninstance __mul__g(Quaternioninstance self_,Quaternioninstance other,void* _env){return (((Quaternion).__init__).func)((((((self_).w)*((other).w))-(((self_).x)*((other).x)))-(((self_).y)*((other).y)))-(((self_).z)*((other).z)),(((((self_).w)*((other).x))+(((self_).x)*((other).w)))+(((self_).y)*((other).z)))-(((self_).z)*((other).y)),(((((self_).w)*((other).y))-(((self_).x)*((other).z)))+(((self_).y)*((other).w)))+(((self_).z)*((other).x)),(((((self_).w)*((other).z))+(((self_).x)*((other).y)))-(((self_).y)*((other).x)))+(((self_).z)*((other).w)),((Quaternion).__init__).env);
}double normg(Quaternioninstance self__7af4d09106ac4691b557d20235e9d408,void* _env){return ((sqrt_our).func)((((((self__7af4d09106ac4691b557d20235e9d408).x)*((self__7af4d09106ac4691b557d20235e9d408).x))+(((self__7af4d09106ac4691b557d20235e9d408).y)*((self__7af4d09106ac4691b557d20235e9d408).y)))+(((self__7af4d09106ac4691b557d20235e9d408).z)*((self__7af4d09106ac4691b557d20235e9d408).z)))+(((self__7af4d09106ac4691b557d20235e9d408).w)*((self__7af4d09106ac4691b557d20235e9d408).w)),(sqrt_our).env);
}Quaternioninstance normalizeg(Quaternioninstance self__742117b8003646c393f1e5c2e61ea7fc,void* _env){double norm_;
(norm_)=((((Quaternion).norm).func)(self__742117b8003646c393f1e5c2e61ea7fc,((Quaternion).norm).env));
if ((((abs_our).func)(norm_,(abs_our).env))>(1e-6)){(norm_)=(((double)(1))/(norm_));
return (((Quaternion).__init__).func)(((self__742117b8003646c393f1e5c2e61ea7fc).w)*(norm_),((self__742117b8003646c393f1e5c2e61ea7fc).x)*(norm_),((self__742117b8003646c393f1e5c2e61ea7fc).y)*(norm_),((self__742117b8003646c393f1e5c2e61ea7fc).z)*(norm_),((Quaternion).__init__).env);
}else{}return self__742117b8003646c393f1e5c2e61ea7fc;
}Quaternioninstance conjg(Quaternioninstance self__33c1f6a4c9d245fea6212202e85749dc,void* _env){return (((Quaternion).__init__).func)((self__33c1f6a4c9d245fea6212202e85749dc).w,-((self__33c1f6a4c9d245fea6212202e85749dc).x),-((self__33c1f6a4c9d245fea6212202e85749dc).y),-((self__33c1f6a4c9d245fea6212202e85749dc).z),((Quaternion).__init__).env);
}Quaternioninstance from_vectorg(doubles1 vec,void* _env){return (((Quaternion).__init__).func)((double)(0),vec.start[doubles1i(vec, (uint64_t)(0), "76:19-76:20")],vec.start[doubles1i(vec, (uint64_t)(1), "76:27-76:28")],vec.start[doubles1i(vec, (uint64_t)(2), "76:35-76:36")],((Quaternion).__init__).env);
}void to_vectorg(Quaternioninstance self__0c08a3bfc4a644ae9c4c6582fa2ce04c,doubles1 vec_,void* _env){(vec_.start[doubles1i(vec_, (uint64_t)(0), "81:12-81:13")])=((self__0c08a3bfc4a644ae9c4c6582fa2ce04c).x);
(vec_.start[doubles1i(vec_, (uint64_t)(1), "82:12-82:13")])=((self__0c08a3bfc4a644ae9c4c6582fa2ce04c).y);
(vec_.start[doubles1i(vec_, (uint64_t)(2), "83:12-83:13")])=((self__0c08a3bfc4a644ae9c4c6582fa2ce04c).z);
}void applyg(Quaternioninstance self__a4b825bd9b044d4ca7664ac059869571,doubles1 vec__1851c1f2db6f44b3a90fcf72a5dc7182,void* _env){Quaternioninstance q;
((assert_our).func)(((vec__1851c1f2db6f44b3a90fcf72a5dc7182)._0)==(3),c_str_to_slise("Bad vector", 10),(assert_our).env);
(q)=((((Quaternion).from_vector).func)(vec__1851c1f2db6f44b3a90fcf72a5dc7182,((Quaternion).from_vector).env));
(q)=((((Quaternion).__mul__).func)((((Quaternion).__mul__).func)(self__a4b825bd9b044d4ca7664ac059869571,q,((Quaternion).__mul__).env),(((Quaternion).conj).func)(self__a4b825bd9b044d4ca7664ac059869571,((Quaternion).conj).env),((Quaternion).__mul__).env));
(((Quaternion).to_vector).func)(q,vec__1851c1f2db6f44b3a90fcf72a5dc7182,((Quaternion).to_vector).env);
}Quaternioninstance from_axis_and_angleg(double angle,doublea3 axis,void* _env){double sin_;
(angle)=((angle)/((double)(2)));
(sin_)=(((sin_our).func)(angle,(sin_our).env));
return (((Quaternion).normalize).func)((((Quaternion).__init__).func)(((cos_our).func)(angle,(cos_our).env),(axis.arr[doublea3i((uint64_t)(0), "98:17-98:18")])*(sin_),(axis.arr[doublea3i((uint64_t)(1), "99:17-99:18")])*(sin_),(axis.arr[doublea3i((uint64_t)(2), "100:17-100:18")])*(sin_),((Quaternion).__init__).env),((Quaternion).normalize).env);
}void vars_initializer_692e44635b6241daa4d58e4ee4268af0(){{_ftdouble_double_double_double__Quaternionft__env __init__ = (_ftdouble_double_double_double__Quaternionft__env){__init__g_dbdc9a857b5147dbaa9b1d9871aad60f, NULL};_ftQuaternion_IOStream_o__voidft__env print = (_ftQuaternion_IOStream_o__voidft__env){printg, NULL};_ftQuaternion_Quaternion__Quaternionft__env __mul__ = (_ftQuaternion_Quaternion__Quaternionft__env){__mul__g, NULL};_ftQuaternion__doubleft__env norm = (_ftQuaternion__doubleft__env){normg, NULL};_ftQuaternion__Quaternionft__env normalize = (_ftQuaternion__Quaternionft__env){normalizeg, NULL};_ftQuaternion__Quaternionft__env conj = (_ftQuaternion__Quaternionft__env){conjg, NULL};_ftdoubles1__Quaternionft__env from_vector = (_ftdoubles1__Quaternionft__env){from_vectorg, NULL};_ftQuaternion_doubles1__voidft__env to_vector = (_ftQuaternion_doubles1__voidft__env){to_vectorg, NULL};_ftQuaternion_doubles1__voidft__env apply = (_ftQuaternion_doubles1__voidft__env){applyg, NULL};_ftdouble_doublea3__Quaternionft__env from_axis_and_angle = (_ftdouble_doublea3__Quaternionft__env){from_axis_and_angleg, NULL};Quaternion.__init__ = __init__;Quaternion.print = print;Quaternion.__mul__ = __mul__;Quaternion.norm = norm;Quaternion.normalize = normalize;Quaternion.conj = conj;Quaternion.from_vector = from_vector;Quaternion.to_vector = to_vector;Quaternion.apply = apply;Quaternion.from_axis_and_angle = from_axis_and_angle;}}