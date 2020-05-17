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
#define TARGET_DEFAULT_RING_BRIGHTNESS   (128)

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
    * @return True if hit state changed
    */
    bool update();

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

 private:
    void set_color(uint8_t count, CRGB color);

    // FastLED controller
    CLEDController* controller_;

    // provide feedback for hit
    void hit_feedback();

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

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
Target<LED, LDR, TRIGGER>::Target() :
    sensor_threshold_(TARGET_DEFAULT_SENSOR_THRESHOLD),
    timer_interval_(TARGET_DEFAULT_TIMER_INTERVAL) {
    // configure pins
    pinMode(LED,     OUTPUT);
    pinMode(LDR,     INPUT);  // analog
    pinMode(TRIGGER, OUTPUT);

    // create ring of led
    controller_ = &FastLED.addLeds<NEOPIXEL, LED>(ring_, TARGET_NUM_LEDS);

    // turn off the ring by default
    set_mode(TARGET_DISABLED);
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
void Target<LED, LDR, TRIGGER>::set_mode(target_mode_t mode) {
    mode_ = mode;
    if (mode_ == TARGET_ENABLED) {
        set_color(TARGET_NUM_LEDS, CRGB::Green);
    } else if (mode_ == TARGET_TIMED) {
        led_counter_ = TARGET_NUM_LEDS;
        set_color(led_counter_, CRGB::Green);
        last_update_time_ = millis();
    } else if (mode_ == TARGET_DISABLED) {
        set_color(TARGET_NUM_LEDS, CRGB::Black);
    }
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
                }
                last_update_time_ = now;
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
        if (i==5) {
            digitalWrite(TRIGGER, LOW);
        }
    }
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
bool Target<LED, LDR, TRIGGER>::get_hit_state() {
    return hit_state_;
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
void Target<LED, LDR, TRIGGER>::set_color(uint8_t count, CRGB color) {
    for (uint8_t i=0; i<count; i++) {
        ring_[i] = color;
    }
    for (uint8_t i=count; i<TARGET_NUM_LEDS; i++) {
        ring_[i] = CRGB::Black;
    }
    controller_->showLeds(ring_brightness_);
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
void Target<LED, LDR, TRIGGER>::set_sensor_threshold(int sensor_threshold) {
    sensor_threshold_ = sensor_threshold;
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
int Target<LED, LDR, TRIGGER>::get_sensor_threshold() {
    return sensor_threshold_;
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
void Target<LED, LDR, TRIGGER>::set_timer_interval(unsigned long timer_interval) {
    timer_interval_ = timer_interval;
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
unsigned long Target<LED, LDR, TRIGGER>::get_timer_interval() {
    return timer_interval_;
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
void Target<LED, LDR, TRIGGER>::set_ring_brightness(int ring_brightness) {
    ring_brightness_ = ring_brightness;
}

template<pin_t LED, pin_t LDR, pin_t TRIGGER>
int Target<LED, LDR, TRIGGER>::get_ring_brightness() {
    return ring_brightness_;
}
