/*
* Extensible Laser Firing System - ELFS
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
#define TARGET_DEFAULT_RING_BRIGHTNESS    (20)

/** Template class for a Target
* Why template? Because FastLED library designates pins using
* templates
*/
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
    * @return value > 0 if target is hit. value represents the LDR value
    * @return value == 0 if target is not hit
    */
    int update() override;

    /** Run selftest */
    void run_self_test() override;

    /** enable actuator */
    void enable_actuator() override;

    /** disable actuator */
    void disable_actuator() override;

    /** toggle actuator */
    void toggle_actuator() override;

    /** enable target */
    void enable() override;

    /** disable target */
    void disable() override;

 private:
    // provide feedback for hit
    void hit_feedback();
};

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
Target<LED, LDR, TRIGGER>::Target() {
    // default values
    sensor_threshold_ = TARGET_DEFAULT_SENSOR_THRESHOLD;
    ring_brightness_  = TARGET_DEFAULT_RING_BRIGHTNESS;

    // configure pins
    pinMode(LED,     OUTPUT);
    pinMode(LDR,     INPUT);  // analog
    pinMode(TRIGGER, OUTPUT);
    disable_actuator();

    // create ring of led
    controller_ = &FastLED.addLeds<NEOPIXEL, LED>(ring_, TARGET_NUM_LEDS);
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
Target<LED, LDR, TRIGGER>::~Target() {
    // nothing to destroy
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
int Target<LED, LDR, TRIGGER>::update() {
    // check if target is hit
    int ldr = analogRead(LDR);
    if (ldr < sensor_threshold_) {
        hit_feedback();
        return ldr;
    }
    // not hit
    return 0;
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
void Target<LED, LDR, TRIGGER>::hit_feedback() {
    // trigger actuator
    enable_actuator();
    // blink red
    for(int i=0; i<10; i++) {
        set_color(TARGET_NUM_LEDS, CRGB::Red);
        delay(30);
        set_color(TARGET_NUM_LEDS, CRGB::Black);
        delay(30);
        // early actuator disable
        if (i == 5) {
            disable_actuator();
        }
    }
    set_color(TARGET_NUM_LEDS, CRGB::Black);

    // rest a bit
    delay(500);
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
void Target<LED, LDR, TRIGGER>::run_self_test() {
    // exercise all LEDs in white
    for(int i=1; i<=TARGET_NUM_LEDS; i++) {
        set_color(i, CRGB::White);
        delay(50);
    }
    set_color(TARGET_NUM_LEDS, CRGB::Black);

}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
void Target<LED, LDR, TRIGGER>::enable_actuator() {
    digitalWrite(TRIGGER, HIGH);
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
void Target<LED, LDR, TRIGGER>::disable_actuator() {
    digitalWrite(TRIGGER, LOW);
}


template<pin_t LED, pin_t LDR, pin_t TRIGGER>
void Target<LED, LDR, TRIGGER>::toggle_actuator() {
    enable_actuator();
    delay(750);
    disable_actuator();
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
void Target<LED, LDR, TRIGGER>::enable() {
    set_color(TARGET_NUM_LEDS, CRGB::Green);
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
void Target<LED, LDR, TRIGGER>::disable() {
    set_color(TARGET_NUM_LEDS, CRGB::Black);
}
