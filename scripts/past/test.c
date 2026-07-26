
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>

static inline void iprint(int64_t i) { printf("%lld\n", i); }
static inline void uiprint(int64_t i) { printf("%llu\n", i); }
static inline void fprint(double f) { printf("%f\n", f); }
static inline void bprint(bool b) { printf("%s\n", b ? "true" : "false" ); }

struct _main__2_res_results {int64_t _0;int32_t _1;};struct _main__2_res_results _main__2_res(void){return (struct _main__2_res_results){(int64_t)(5.0),(int32_t)(10.0)};}int64_t _main_nth(int64_t n){if ((n)<(1)){return 0;}else{return (n)+(_main_nth((n)-(1)));}}void blob(int32_t var1,int32_t var2){iprint((int64_t)((var1)*(var2)));}float coss(float v){float v2;float v4;(v4)=(((v2)=((v)*(v)))*(v2));return (float)((((1.0)-((double)((v2)/((float)(2)))))+((double)((v4)/((float)(24)))))-((double)(((v4)*(v2))/((float)(720)))));}int32_t main(void){int64_t _481;int64_t _325;int64_t _143;int64_t _458;double _F_;int32_t tom;int32_t bob;(bob)=((int32_t)(~(1)));{struct _main__2_res_results _0 = _main__2_res();bob = (int32_t)(_0._0);tom = (_0._1);}{float x;(x)=((float)(((((double)(-(2)))/(-(2.0)))*((double)(3)))+((double)(2))));fprint((double)(((x)-((float)(1)))+((float)(tom))));}{int32_t _0 = (int32_t)(((int64_t)(tom))+(10));float _1 = (float)((double)((3.1415)/((double)(4))));bob = (_0);_F_ = (double)(_1);}(_F_)=((_F_)=(_F_));blob(bob,tom);iprint((int64_t)(tom));iprint((int64_t)(bob));bprint(!((_F_)<((double)(1))));fprint((double)(coss((float)(_F_))));iprint(((int64_t)(((true)+(true))-(false)))*(3));iprint(_main_nth(50));bprint((((((1)<((_458)=(3)))&&((_458)<((_143)=(4))))&&((_143)<((_325)=(5))))&&((_325)>((_481)=(0))))&&((_481)==(0)));if ((bool)(1)){}if (!(false)){}{int16_t i;int64_t res;(res)=(0);(i)=((int16_t)(50));while (true){(res)=((res)+((int64_t)(i)));(i)=((int16_t)(((int64_t)(i))-(1)));if (((int64_t)(i))<(1)){break;}}iprint(res);}return (int32_t)(0);}