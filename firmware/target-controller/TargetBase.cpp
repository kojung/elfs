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

#include "TargetBase.h"

TargetBase::TargetBase() {
    // nothing to initialize
}

TargetBase::~TargetBase() {
    // nothing to destroy
}

void TargetBase::set_mode(target_mode_t mode) {
    mode_ = mode;
    hit_state_ = false;
    if (mode_ == TARGET_ENABLED) {
        set_color(TARGET_NUM_LEDS, CRGB::Green);
    } else if (mode_ == TARGET_TIMED) {
        led_counter_ = TARGET_NUM_LEDS;
        set_color(led_counter_, CRGB::Green);
        last_update_time_ = millis();
    } else if (mode_ == TARGET_DISABLED) {
        set_color(TARGET_NUM_LEDS, CRGB::Black);
    }
    disable_actuator();
}

bool TargetBase::get_hit_state() {
    return hit_state_;
}

void TargetBase::set_color(uint8_t count, CRGB color) {
    for (uint8_t i=0; i<count; i++) {
        ring_[i] = color;
    }
    for (uint8_t i=count; i<TARGET_NUM_LEDS; i++) {
        ring_[i] = CRGB::Black;
    }
    controller_->showLeds(ring_brightness_);
}

void TargetBase::set_sensor_threshold(int sensor_threshold) {
    sensor_threshold_ = sensor_threshold;
}

int TargetBase::get_sensor_threshold() {
    return sensor_threshold_;
}

void TargetBase::set_timer_interval(unsigned long timer_interval) {
    timer_interval_ = timer_interval;
}

unsigned long TargetBase::get_timer_interval() {
    return timer_interval_;
}

void TargetBase::set_ring_brightness(int ring_brightness) {
    ring_brightness_ = ring_brightness;
}

int TargetBase::get_ring_brightness() {
    return ring_brightness_;
}
