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

#pragma once

#include "Max7219Chain.h"

#define STATUS_DIGITS_PER_CHIP  (6)
#define STATUS_CHIPS_PER_CHAIN  (2)
#define STATUS_DIGITS_PER_CHAIN (STATUS_DIGITS_PER_CHIP * STATUS_CHIPS_PER_CHAIN)

/* Models a status bar with 12 7-segment displays */
class Status {
  public:
    /** constructor
    * @param digits_per_chip  Number of digits per chip
    * @param chips_per_chain  Number of MAX7219 chips per chain
    * @param load             Load pin
    */
    Status(uint8_t load_pin, uint8_t intensity);

    /** start of a target */
    void start();

    /** update status. call this method as often as possible
    * between start() and stop() methods
    */
    void update();

    /** target hit, record best time  */
    void stop();

    /** increment count */
    void increment_count();

    /** run bist */
    void bist();

    /** clear status */
    void clear();

 private:
    // Max7219 controller
    Max7219Chain max7219_;

    // update count value
    void update_count_();

    // update best time
    void update_best_time_();

    // update best time
    void update_current_time_();

    // number of targets shot
    int32_t count_;

    // start time in milliseconds
    int32_t start_time_;

    // current time in milliseconds
    int32_t current_time_;

    // best time in milliseconds
    int32_t best_time_;
};
