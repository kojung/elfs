/*
* Enhanced Laser Firing System - ELFS
* Copyright (C) 2020 Jung Ko <kojung@gmail.com>
* 
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
* 
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

#pragma once

#include <Arduino.h>
#include "TargetBase.h"

typedef uint8_t pin_t;

#define TARGET_DEFAULT_SENSOR_THRESHOLD  (500)
#define TARGET_DEFAULT_TIMER_INTERVAL   (1000)
#define TARGET_DEFAULT_RING_BRIGHTNESS    (20)

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
class Target : public TargetBase {
 public:
    /** Constructor */
    Target();

    /** Destructor */
    ~Target();

    /** Update target
    * Read the sensor and update internal state. Call this function
    * inside the Arduino main loop as fast as possible.
    * @return True if hit state changed
    */
    bool update() override;

    /** Run selftest */
    void run_self_test() override;

 private:
    // provide feedback for hit
    void hit_feedback();
};

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
Target<LED, LDR, TRIGGER>::Target() {
    // default values
    sensor_threshold_ = TARGET_DEFAULT_SENSOR_THRESHOLD;
    ring_brightness_  = TARGET_DEFAULT_RING_BRIGHTNESS;
    timer_interval_   = TARGET_DEFAULT_TIMER_INTERVAL;

    // configure pins
    pinMode(LED,     OUTPUT);
    pinMode(LDR,     INPUT);  // analog
    pinMode(TRIGGER, OUTPUT);

    // create ring of led
    controller_ = &FastLED.addLeds<NEOPIXEL, LED>(ring_, TARGET_NUM_LEDS);
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
Target<LED, LDR, TRIGGER>::~Target() {
    // nothing to destroy
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
bool Target<LED, LDR, TRIGGER>::update() {
    // update only if target is enabled AND hasn't been hit yet
    if (mode_ != TARGET_DISABLED && !hit_state_) {
        if (analogRead(LDR) < sensor_threshold_) {
            hit_state_ = true;
            hit_feedback();
            return true;
        } else {
            // update timer?
            if (mode_ == TARGET_TIMED && led_counter_ > 0) {
                unsigned long now = millis();
                if (now - last_update_time_ > timer_interval_) {
                    led_counter_--;
                    set_color(led_counter_, CRGB::Green);
                    last_update_time_ = now;
                }

                // if timer expired, disable the target
                if (led_counter_ == 0) {
                    set_mode(TARGET_DISABLED);
                }
            }
        }
    }
    // no state changes
    return false;
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
void Target<LED, LDR, TRIGGER>::hit_feedback() {
    // trigger actuator
    digitalWrite(TRIGGER, HIGH);
    // blink red
    for(int i=0; i<10; i++) {
        set_color(TARGET_NUM_LEDS, CRGB::Red);
        delay(30);
        set_color(TARGET_NUM_LEDS, CRGB::Black);
        delay(30);
        digitalWrite(TRIGGER, LOW);
    }
    set_color(TARGET_NUM_LEDS, CRGB::Red);
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
void Target<LED, LDR, TRIGGER>::run_self_test() {
    // exercise all LEDs in white
    for(int i=0; i<TARGET_NUM_LEDS; i++) {
        set_color(i, CRGB::White);
        delay(50);
    }
    set_color(TARGET_NUM_LEDS, CRGB::Black);

    // exercise trigger
    digitalWrite(TRIGGER, HIGH);
    delay(1000);
    digitalWrite(TRIGGER, LOW);
}
