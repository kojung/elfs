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

#define TARGET_NUM_LEDS                   (16)
#define TARGET_DEFAULT_SENSOR_THRESHOLD  (400)
#define TARGET_DEFAULT_TIMER_INTERVAL   (1000)

typedef uint8_t pin_t;

typedef enum target_mode_e {
    TARGET_ENABLED = 0,        // target enabled
    TARGET_TIMED,              // target enabled for a limited time
    TARGET_DISABLED            // target disabled
} target_mode_t;

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
class Target {
 public:
    /** constructor
    */
    Target();

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

    /** Set sensor threshold
    */
    void set_sensor_threshold(int sensor_threshold);

    /** Get sensor threshold
    */
    int get_sensor_threshold();

    /** Set timer interval
    */
    void set_timer_interval(unsigned long timer_interval);

    /** Get timer interval
    */
    unsigned long get_timer_interval();

 private:
    void set_color(uint8_t count, CRGB color);

    // Current target mode
    target_mode_t mode_;

    // Flag indicating if target has been hit or not
    bool hit_state_;

    // Adjust sensor sensitivity
    int sensor_threshold_;

    // Array holding ring colors
    CRGB ring_[TARGET_NUM_LEDS];

    // Counters used in TIMED mode
    uint8_t led_counter_;              // count LEDs
    unsigned long last_update_time_;   // keep track of last time
    unsigned long timer_interval_;     // how often to update the LED counter
};

