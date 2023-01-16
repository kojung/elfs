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
#include "FastLED.h"

#define TARGET_NUM_LEDS  (16)

/** Virtual class for Target
* Why virtual class? Because Target class is templatized and the main
* application wants to iterate through targets in an array
*/
class TargetBase {
 public:
    /** Constructor */
    TargetBase();

    /** Pure virtual destructor */
    virtual ~TargetBase() = 0;

    /** Update target
    * Read the sensor and update internal state. Call this function
    * inside the Arduino main loop as fast as possible.
    */
    virtual int update();

    /** Run self test */
    virtual void run_self_test();

    /** enable actuator */
    virtual void enable_actuator();

    /** disable actuator */
    virtual void disable_actuator();

    /** toggle actuator */
    virtual void toggle_actuator() ;

    /** enable target */
    virtual void enable();

    /** enable target */
    virtual void disable();

    /** Accessors for sensor threshold */
    void set_sensor_threshold(int sensor_threshold);
    int get_sensor_threshold();

    /** Accessors for ring brightness */
    void set_ring_brightness(int brightness);
    int get_ring_brightness();

 protected:
    // update the ring led
    void set_color(uint8_t count, CRGB color);

    // FastLED controller
    CLEDController* controller_;

    // Adjust sensor sensitivity
    int sensor_threshold_;

    // Adjust ring brightness
    int ring_brightness_;

    // Array holding ring colors
    CRGB ring_[TARGET_NUM_LEDS];
};
