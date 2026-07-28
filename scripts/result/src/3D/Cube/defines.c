
#include "../../../include/3D/Cube/defines.h"
Quaternioninstance Q_ROTATE;
int64_t FPS;
int64_t CAM_SIZE_Y;
int64_t CAM_SIZE_X;
double POV_SIZE_Y;
double POV_SIZE_X;
double POV_EYE_DIST;
double POV_DIST;
void vars_initializer_4871d5decdf6443bb85a3ccd5a6da81a(){(POV_DIST)=((double)(-(3)));
(POV_EYE_DIST)=((double)(1));
(POV_SIZE_X)=(1.1);
(POV_SIZE_Y)=(1.1);
(CAM_SIZE_X)=(70);
(CAM_SIZE_Y)=(25);
(FPS)=(10);
(Q_ROTATE)=((((Quaternion).from_axis_and_angle).func)(0.5e-1,(doublea3){{(double)(1),0.5,(double)(2)}},((Quaternion).from_axis_and_angle).env));
}