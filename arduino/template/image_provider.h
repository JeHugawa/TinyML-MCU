#ifndef TINYMLAAS_IMAGE_PROVIDER_H_
#define TINYMLAAS_IMAGE_PROVIDER_H_

#include "tensorflow/lite/c/common.h"

TfLiteStatus GetImage(const TfLiteTensor* tensor);

#endif
