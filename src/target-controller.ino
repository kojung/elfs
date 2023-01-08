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

#include "Target.h"
#include "TargetBase.h"

#define NUM_TARGETS (4)

// Targets pins: LED, LDR, TRIGGER
// TRIGGER is shared because of single actuator
Target<8,  A0, 2> t0;
Target<9,  A1, 2> t1;
Target<10, A2, 2> t2;
Target<11, A3, 2> t3;

// collect targets into an array
TargetBase* targets[NUM_TARGETS] = {&t0, &t1, &t2, &t3};

void setup() {
    // nothing to do
}

void loop() {
    for (uint8_t i=0; i < NUM_TARGETS; i++) {
        targets[i]->update();
        targets[i]->set_mode(TARGET_ENABLED);
    }
}
