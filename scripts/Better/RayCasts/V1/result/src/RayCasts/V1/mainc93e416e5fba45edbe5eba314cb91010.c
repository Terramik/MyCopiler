
#include "../../../include/RayCasts/V1/mainc93e416e5fba45edbe5eba314cb91010.h"
_ftvoid__int64_tft__env not_very_main;
int64_t not_very_maing(void *_par)
{
    doubles1 vr__7bfe7bdf29634a03bc66d2ec5a13647c;
    doublea3 vr__;
    doubles1 v2__3808daf4cf324eebb1b4bad0cd2b0f25;
    doublea3 v2__;
    doubles1 v1__6858798e0c4e497ebdb989b08ad6cd14;
    doublea3 v1__;
    (v1__) = ((doublea3){{1.5, (double)(3), 4.5}});
    (v1__6858798e0c4e497ebdb989b08ad6cd14) = (doublea3s1_1(&(v1__), (uint64_t)(0), (uint64_t)(3), "6:26-6:31"));
    (v2__) = ((doublea3){{(double)(0), 3.14, (double)(100)}});
    (v2__3808daf4cf324eebb1b4bad0cd2b0f25) = (doublea3s1_1(&(v2__), (uint64_t)(0), (uint64_t)(3), "8:26-8:31"));
    vr__;
    (vr__7bfe7bdf29634a03bc66d2ec5a13647c) = (doublea3s1_1(&(vr__), (uint64_t)(0), (uint64_t)(3), "10:26-10:31"));
    (((VectorLib).print).func)(v1__6858798e0c4e497ebdb989b08ad6cd14, ((VectorLib).print).env);
    (((VectorLib).print).func)(v2__3808daf4cf324eebb1b4bad0cd2b0f25, ((VectorLib).print).env);
    (((VectorLib).add).func)(v1__6858798e0c4e497ebdb989b08ad6cd14, v2__3808daf4cf324eebb1b4bad0cd2b0f25, vr__7bfe7bdf29634a03bc66d2ec5a13647c, ((VectorLib).add).env);
    (((VectorLib).print).func)(vr__7bfe7bdf29634a03bc66d2ec5a13647c, ((VectorLib).print).env);
    return 0;
}
_ftvoid__int64_tft__env not_very_main = (_ftvoid__int64_tft__env){not_very_maing, NULL};