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

typedef enum target_mode_e {
    TARGET_ENABLED = 0,        // target enabled
    TARGET_TIMED,              // target enabled for a limited time
    TARGET_DISABLED            // target disabled
} target_mode_t;

class TargetBase {
 public:
    /** Constructor */
    TargetBase();

    /** Pure virtual destructor */
    virtual ~TargetBase() = 0;

    /** Update target
    * Read the sensor and update internal state. Call this function
    * inside the Arduino main loop as fast as possible.
    * @return True if hit state changed
    */
    virtual bool update();

    /** Run self test */
    virtual void run_self_test();

    /** Set target mode
    * @param mode Target mode
    */
    void set_mode(target_mode_t mode);

    /** Return target state
    * @return True if target has been hit, False otherwise
    */
    bool get_hit_state();

    /** Accessors for sensor threshold */
    void set_sensor_threshold(int sensor_threshold);
    int get_sensor_threshold();

    /** Accessors for timer interval */
    void set_timer_interval(unsigned long timer_interval);
    unsigned long get_timer_interval();

    /** Accessors for ring brightness */
    void set_ring_brightness(int brightness);
    int get_ring_brightness();

 protected:
    // update the ring led
    void set_color(uint8_t count, CRGB color);

    // FastLED controller
    CLEDController* controller_;

    // Current target mode
    target_mode_t mode_;

    // Flag indicating if target has been hit or not
    bool hit_state_;

    // Adjust sensor sensitivity
    int sensor_threshold_;

    // Adjust ring brightness
    int ring_brightness_;

    // Array holding ring colors
    CRGB ring_[TARGET_NUM_LEDS];

    // Counters used in TIMED mode
    uint8_t led_counter_;              // count LEDs
    unsigned long last_update_time_;   // keep track of last time
    unsigned long timer_interval_;     // how often to update the LED counter
};
