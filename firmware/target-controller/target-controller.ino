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
#include "TargetBase.h"

#define NUM_TARGETS (4)

// collect targets into an array
TargetBase* targets[NUM_TARGETS] = {
    &Target<2, A0, 6>(),
    &Target<3, A1, 7>(),
    &Target<4, A2, 8>(),
    &Target<5, A3, 9>()
};

void setup() {
    // enable serial
    Serial.begin(115200);
    while (!Serial) {
        ; // wait for serial port to connect. Needed for native USB port only
    }

    Serial.println("Calling from Setup()");

    // WIP
    targets[0]->set_mode(TARGET_ENABLED);
}

void loop() {
    for (uint8_t i=0; i < NUM_TARGETS; i++) {
        targets[i]->update();
    }
}

