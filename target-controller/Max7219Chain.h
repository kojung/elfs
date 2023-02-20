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

/* Control a daisy chained string of Max7219 chips
* For simplicity, we assume the following:
* - all chips have equal number of digits
* - chain is driven by SPI
* - code B decode mode used for all chips
*/
class Max7219Chain {
  public:
    /** constructor
    * @param digits_per_chip  Number of digits per chip
    * @param chips_per_chain  Number of MAX7219 chips per chain
    * @param load             Load pin
    */
    Max7219Chain(uint8_t digits_per_chip, uint8_t chips_per_chain, uint8_t load_pin, uint8_t intensity);

    /** write character at given position in the chain
    * @param pos  Character position [0 .. digits_per_chain - 1]
    * @param data Character to write
    * @param dp   Decimal point
    */
    void write_char(uint8_t pos, uint8_t data, bool dp = false);

    /** clear all digits in the chain */
    void clear();

 private:
    // number of digits per chip
    uint8_t digits_per_chip_;

    // number of chips per chain
    uint8_t chips_per_chain_;

    // load pin
    const uint8_t load_pin_;

    // number of digits per chain
    uint8_t digits_per_chain_;

    // write register at the given address
    // does not toggle load pin
    void write_reg_(uint8_t addr, uint8_t data);

    // write register at the given address for all chips in the chain
    // toggles load pin
    void write_regs_in_chain_(uint8_t addr, uint8_t data);
};
