#if defined(ARDUINO) && !defined(ARDUINO_ARDUINO_NANO33BLE)
#define ARDUINO_EXCLUDE_CODE
#endif  // defined(ARDUINO) && !defined(ARDUINO_ARDUINO_NANO33BLE)

#ifndef ARDUINO_EXCLUDE_CODE

#include <cmath>

#include "Arduino.h"
#include "detection_responder.h"
#include "tensorflow/lite/micro/micro_log.h"

// Flash the yellow (builtin) LED after each inference
void RespondToDetection(float target_score, float not_target_score) {
  static bool is_initialized = false;
  if (!is_initialized) {
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
    // Pins for the built-in RGB LEDs on the Arduino Nano 33 BLE Sense
    pinMode(LEDR, OUTPUT);
    pinMode(LEDG, OUTPUT);
    pinMode(LEDB, OUTPUT);
    // Switch the LEDs off
    digitalWrite(LEDG, HIGH);
    digitalWrite(LEDB, HIGH);
    digitalWrite(LEDR, HIGH);
    is_initialized = true;
  }

  // Note: The RGB LEDs on the Arduino Nano 33 BLE
  // Sense are on when the pin is LOW, off when HIGH.

  // Switch on the green LED when a person is detected,
  // the blue when no person is detected
  if (target_score > not_target_score) {
    digitalWrite(LEDG, LOW);
    digitalWrite(LEDB, HIGH);
  } else {
    digitalWrite(LEDG, HIGH);
    digitalWrite(LEDB, LOW);
  }

  // Flash the yellow LED after every inference.
  // The builtin LED is on when the pin is HIGH
  digitalWrite(LED_BUILTIN, LOW);
  delay(100);
  digitalWrite(LED_BUILTIN, HIGH);

  float target_score_frac, target_score_int;
  float not_target_score_frac, not_target_score_int;
  target_score_frac = std::modf(target_score * 100, &target_score_int);
  not_target_score_frac = std::modf(not_target_score * 100, &not_target_score_int);
  MicroPrintf("Target score: %d.%d%% No target score: %d.%d%%",
              static_cast<int>(target_score_int),
              static_cast<int>(target_score_frac * 100),
              static_cast<int>(not_target_score_int),
              static_cast<int>(not_target_score_frac * 100));
}

#endif  // ARDUINO_EXCLUDE_CODE
