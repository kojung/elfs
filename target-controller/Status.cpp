/*
* Extensible Laser Firing System - ELFS
* Copyright (C) 2023 Jung Ko <kojung@gmail.com>
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

#include <Arduino.h>

#include "Status.h"

// use this struct to hold 4 digits
typedef union digits_u {
    uint32_t value;
    struct {
        uint8_t a;   // most significant digit
        uint8_t b;
        uint8_t c;
        uint8_t d;   // least significant digit
    };
} digits_t;

// convert from integer to digits_t
static digits_t convert(int value) {
    digits_t digits;
    // negative value denote uninitialized data, return blank digits
    if (value < 0) {
        digits.a = MAX7219_VALUE_BLANK;
        digits.b = MAX7219_VALUE_BLANK;
        digits.c = MAX7219_VALUE_BLANK;
        digits.d = MAX7219_VALUE_BLANK;
    } else {
        digits.a = (value / (3 * 10)) % 10;
        digits.b = (value / (2 * 10)) % 10;
        digits.c = (value / (1 * 10)) % 10;
        digits.d = value % 10;
    }
    return digits;
}

Status::Status(uint8_t load_pin, uint8_t intensity) :
    max7219_(STATUS_DIGITS_PER_CHIP, STATUS_CHIPS_PER_CHAIN, load_pin, intensity),
    count_(0),
    start_time_(-1),
    current_time_(-1),
    best_time_(-1) {
    // nothing else to do
}

void Status::start() {
    start_time_ = millis();
}

void Status::update() {
    current_time_ = millis() - start_time_;
    update_current_time_();
}

void Status::stop() {
    if (current_time_ < best_time_ || best_time_ < 0) {
        best_time_ = current_time_;
        update_best_time_();
    }
}

void Status::increment_count() {
    count_++;
    update_count_();
}

void Status::update_count_() {
    digits_t digits = convert(count_);
    // drop digits `a` and `b` for `count`
    max7219_.write_char(0, digits.c);
    max7219_.write_char(1, digits.d);
}

void Status::update_best_time_() {
    digits_t digits = convert(best_time_ / 100);
    // use digit 2 as separator
    max7219_.write_char(3, digits.a);
    max7219_.write_char(4, digits.b);
    max7219_.write_char(5, digits.c, true);
    max7219_.write_char(6, digits.d);
}

void Status::update_current_time_() {
    digits_t digits = convert(current_time_ / 100);
    // use digit 7 as separator
    max7219_.write_char(8, digits.a);
    max7219_.write_char(9, digits.b);
    max7219_.write_char(10, digits.c, true);
    max7219_.write_char(11, digits.d);
}

void Status::bist() {
    max7219_.bist();
}

void Status::clear() {
    max7219_.clear();
}
