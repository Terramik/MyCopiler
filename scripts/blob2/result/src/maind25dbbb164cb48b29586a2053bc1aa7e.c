
#include "../include/maind25dbbb164cb48b29586a2053bc1aa7e.h"
_ftvoid__int64_tft__env not_very_main;int64_t not_very_maing(void* _par){IOStream_ourinstance file;
(((IOStream_our).print_f).func)(&(stdout_our),c_str_to_slise("12+2=%12.3f\n\n", 13),102.1514,((IOStream_our).print_f).env);
(((IOStream_our).print_f).func)(&(stdout_our),c_str_to_slise("0.1+0.2=%100.90f\n\n", 18),(0.1)+(0.2),((IOStream_our).print_f).env);
(((IOStream_our).print_u).func)(&(stdout_our),c_str_to_slise("-1 is %u\n", 9),(uint64_t)(-(1)),((IOStream_our).print_u).env);
(((IOStream_our).print_i).func)(&(stdout_our),c_str_to_slise("{{%10i}}\n", 9),(((10)-(100))+(1000))-(10000),((IOStream_our).print_i).env);
(((IOStream_our).print_b).func)(&(stdout_our),c_str_to_slise("%tb\n", 4),false,((IOStream_our).print_b).env);
(((IOStream_our).print_b).func)(&(stdout_our),c_str_to_slise("%b\n", 3),true,((IOStream_our).print_b).env);
(((IOStream_our).print_c).func)(&(stdout_our),c_str_to_slise("%c\t", 3),'1',((IOStream_our).print_c).env);
(((IOStream_our).print_c).func)(&(stdout_our),c_str_to_slise("%c\t", 3),'\n',((IOStream_our).print_c).env);
(((IOStream_our).print_c).func)(&(stdout_our),c_str_to_slise("%c\t", 3),'t',((IOStream_our).print_c).env);
(((IOStream_our).print_c).func)(&(stdout_our),c_str_to_slise("%c\t", 3),(uint8_t)(100),((IOStream_our).print_c).env);
(((IOStream_our).print_c).func)(&(stdout_our),c_str_to_slise("%c\n", 3),(uint8_t)(200),((IOStream_our).print_c).env);
(((IOStream_our).print_b).func)(&(stderr_our),c_str_to_slise("\tSomethign go whong, thing is %tb\n", 34),false,((IOStream_our).print_b).env);
(file)=((((IOStream_our).open).func)(c_str_to_slise("hello.txt", 9),c_str_to_slise("w", 1),((IOStream_our).open).env));
if ((((IOStream_our).good).func)(&(file),((IOStream_our).good).env)){(((IOStream_our).puts).func)(&(file),c_str_to_slise("Hello, World!\n", 14),((IOStream_our).puts).env);
(((IOStream_our).print_f).func)(&(file),c_str_to_slise("0.1+0.2=%1000.980f\n", 19),(0.1)+(0.2),((IOStream_our).print_f).env);
}else{}(((IOStream_our).puts).func)(&(stdout_our),c_str_to_slise("Hello, World!", 13),((IOStream_our).puts).env);
(((IOStream_our).putc).func)(&(stdout_our),'\n',((IOStream_our).putc).env);
return 0;
(((IOStream_our).__del__).func)(file,((IOStream_our).__del__).env);
}_ftvoid__int64_tft__env not_very_main = (_ftvoid__int64_tft__env){not_very_maing, NULL};