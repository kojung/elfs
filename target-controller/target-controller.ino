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

#include "Max7219Chain.h"

#define STATUS_DIGITS_PER_CHIP  (6)
#define STATUS_CHIPS_PER_CHAIN  (2)
#define STATUS_DIGITS_PER_CHAIN (STATUS_DIGITS_PER_CHIP * STATUS_CHIPS_PER_CHAIN)
#define STATUS_LOAD_PIN         (6)
#define STATUS_INTENSITY        (15)

Max7219Chain status(STATUS_DIGITS_PER_CHIP, STATUS_CHIPS_PER_CHAIN, STATUS_LOAD_PIN, STATUS_INTENSITY);

void setup() {
    // Serial (uncomment if needed for debug)
    Serial.begin(9600);
    Serial.println("ELFS single actuator");
    status.bist();
}

void loop() {
}
