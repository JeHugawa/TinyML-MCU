#ifndef TINYMLAAS_DETECTION_RESPONDER_H_
#define TINYMLAAS_DETECTION_RESPONDER_H_

#include "tensorflow/lite/c/common.h"

void RespondToDetection(float target_score, float not_target_score);

#endif  // TINYMLAAS_DETECTION_RESPONDER_H_
