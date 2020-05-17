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

#include "Target.h"

template<pin_t LED>
Target<LED>::Target(pin_t ldr, pin_t trigger) :
    ldr_(ldr),
    trigger_(trigger),
    sensor_threshold_(TARGET_DEFAULT_SENSOR_THRESHOLD),
    timer_interval_(TARGET_DEFAULT_TIMER_INTERVAL) {
    // configure pins
    pinMode(ldr_,     INPUT);  // analog
    pinMode(trigger_, OUTPUT);

    // create ring of led
    FastLED.addLeds<NEOPIXEL, LED>(ring_, TARGET_NUM_LEDS);

    // turn off the ring by default
    set_mode(TARGET_DISABLED);
}

template<pin_t LED>
void Target<LED>::set_mode(target_mode_t mode) {
    if (mode == TARGET_ENABLED) {
        set_color(TARGET_NUM_LEDS, CRGB::Green);
    } else if (mode == TARGET_TIMED) {
        set_color(TARGET_NUM_LEDS, CRGB::Green);
        last_update_time_ = millis();
        led_counter_ = TARGET_NUM_LEDS;
    } else if (mode == TARGET_DISABLED) {
        set_color(TARGET_NUM_LEDS, CRGB::Black);
    }
}

template<pin_t LED>
bool Target<LED>::update() {
    // update only if target is enabled AND hasn't been hit yet
    if (mode_ != TARGET_DISABLED && !hit_state_) {
        if (analogRead(ldr_) < sensor_threshold_) {
            hit_state_ = true;
            // @TODO
            // change color, trigger actuator, etc...
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

template<pin_t LED>
bool Target<LED>::get_hit_state() {
    return hit_state_;
}

template<pin_t LED>
void Target<LED>::set_color(uint8_t count, CRGB color) {
    for (uint8_t i=0; i<count; i++) {
        ring_[i] = color;
    }
    for (uint8_t i=count; i<TARGET_NUM_LEDS; i++) {
        ring_[i] = CRGB::Black;
    }
}

template<pin_t LED>
void Target<LED>::set_sensor_threshold(int sensor_threshold) {
    sensor_threshold_ = sensor_threshold;
}

template<pin_t LED>
int Target<LED>::get_sensor_threshold() {
    return sensor_threshold_;
}

template<pin_t LED>
void Target<LED>::set_timer_interval(unsigned long timer_interval) {
    timer_interval_ = timer_interval;
}

template<pin_t LED>
unsigned long Target<LED>::get_timer_interval() {
    return timer_interval_;
}
