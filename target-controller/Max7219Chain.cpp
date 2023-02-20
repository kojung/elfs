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

#include <SPI.h>

#include "Max7219Chain.h"

// register addresses
#define MAX7219_REG_NOOP         (0x0)
#define MAX7219_REG_DECODEMODE   (0x9)
#define MAX7219_REG_INTENSITY    (0xA)
#define MAX7219_REG_SCANLIMIT    (0xB)
#define MAX7219_REG_SHUTDOWN     (0xC)
#define MAX7219_REG_DISPLAYTEST  (0xF)

Max7219Chain::Max7219Chain(uint8_t digits_per_chip, uint8_t chips_per_chain, uint8_t load_pin, uint8_t intensity) :
    digits_per_chip_(digits_per_chip),
    chips_per_chain_(chips_per_chain),
    load_pin_(load_pin) {
    digits_per_chain_ = digits_per_chip_ * chips_per_chain_;

    // configure load pin and park it in HIGH
    pinMode (load_pin_, OUTPUT);
    digitalWrite (load_pin_, HIGH);

    SPI.begin();

    write_regs_in_chain_(MAX7219_REG_SCANLIMIT, digits_per_chip_);   // limit scan to digits in each chip
    write_regs_in_chain_(MAX7219_REG_DECODEMODE, 0xFF);              // all digits in code B decode mode
    write_regs_in_chain_(MAX7219_REG_DISPLAYTEST, 0);                // not in display test
    write_regs_in_chain_(MAX7219_REG_INTENSITY, intensity);          // character intensity: range: 0 to 15
    write_regs_in_chain_(MAX7219_REG_SHUTDOWN, 1);                   // 1 = normal operation
    clear();  // clear display
}


// write register
void Max7219Chain::write_reg_(uint8_t addr, uint8_t data) {
    SPI.transfer(addr);
    SPI.transfer(data);
}

void Max7219Chain::write_regs_in_chain_(uint8_t addr, uint8_t data) {
    digitalWrite(load_pin_, LOW);
    // broadcast `data` to all `addr` register in all chips
    for (uint8_t i = 0; i < chips_per_chain_; i++) {
        write_reg_(addr, data);
    }
    digitalWrite(load_pin_, HIGH);
}

void Max7219Chain::write_char(uint8_t pos, uint8_t data, bool dp) {
    // conditionally add decimal point
    if (dp) {
        data |= 0x80;
    }

    // write data
    digitalWrite(load_pin_, LOW);
    uint8_t rel_pos = pos % digits_per_chip_;
    write_reg_(rel_pos + 1, data);

    // shift data to the correct chip
    uint8_t chip_num = pos / digits_per_chip_;
    for (uint8_t i = 0; i < chip_num; i++) {
        write_reg_(MAX7219_REG_NOOP, 0);  // write no-op
    }
    digitalWrite(load_pin_, HIGH);
    flush_();
}

void Max7219Chain::clear() {
    for (int pos = 0; pos < digits_per_chain_; pos++) {
        write_char(pos, MAX7219_VALUE_BLANK);
    }
}

void Max7219Chain::flush_() {
    digitalWrite(load_pin_, LOW);
    for (int pos = 0; pos < chips_per_chain_; pos++) {
        write_reg_(MAX7219_REG_NOOP, 0);  // write no-op
    }
    digitalWrite(load_pin_, HIGH);
}


void Max7219Chain::bist() {
    clear();
    for (int data = 0; data < 10; data++) {
        for (int pos = 0; pos < digits_per_chain_; pos++) {
            write_char(pos, data, true);
        }
        delay(150);
    }
    clear();
}
