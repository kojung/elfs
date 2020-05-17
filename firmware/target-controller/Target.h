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
#include "FastLED.h"

#define TARGET_NUM_LEDS (16)

typedef uint8_t pin_t;

typedef enum target_mode_e {
    ENABLED = 0,        // target enabled
    TIMED,              // target enabled for a limited time
    DISABLED            // target disabled
} target_mode_t;

class Target {
 public:
    /** constructor
    * Provide the 3 pins that defines the target
    * @param led     DI pin of Neopixel LED
    * @param ldr     Light dependent resistor pin
    * @param trigger Active high relay that controls the target actuator
    */
    Target(pin_t led, pin_t ldr, pin_t trigger);

    /** Set target mode
    * @param mode Target mode
    */
    void set_mode(target_mode_t mode);

    /** Update target
    * Read the sensor and update internal state. Call this function
    * inside the Arduino main loop as fast as possible.
    * @return True if internal state changed
    */
    bool update();

    /** Return target state
    * @return True if target has been hit, False otherwise
    */
    bool get_hit_state();

 private:
    void set_color(uint8_t count, CRGB color);

    bool hit_state_;
    pin_t led_;
    pin_t ldr_;
    pin_t trigger_;
};

