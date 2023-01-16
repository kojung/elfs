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
#define TRIM A5

#define BUZZER           (3)
#define BUZZER_DELAY_US  (120)   // aim for 4kHz tone
#define BUZZER_CYCLES    (800)  // aim for 0.5 sec beep

// Targets pins: LED, LDR, TRIGGER
// TRIGGER is shared because of single actuator
Target<8,  A0, 2> t0;
Target<9,  A1, 2> t1;
Target<10, A2, 2> t2;
Target<11, A3, 2> t3;

// collect targets into an array
// relies on virtual methods to dispatch the correct method
TargetBase* targets[NUM_TARGETS] = {&t0, &t1, &t2, &t3};

static int sensor_threshold = 500;
static int loop_counter = 0;

// make a beep sound at pin BUZZER
static void beep() {
    for (int i=0; i < BUZZER_CYCLES; i++) {
        digitalWrite(BUZZER, HIGH);
        delayMicroseconds(BUZZER_DELAY_US);
        digitalWrite(BUZZER, LOW);
        delayMicroseconds(BUZZER_DELAY_US);
    }
}

void setup() {
    // Serial (uncomment if needed for debug)
    Serial.begin(9600);
    Serial.println("ELFS single actuator");

    // set up trim input
    pinMode(TRIM, INPUT);  // analog

    // set up buzzer output
    pinMode(BUZZER, OUTPUT);

    // run self-test
    for (uint8_t i=0; i < NUM_TARGETS; i++) {
        targets[i]->run_self_test();
    }
    t0.toggle_actuator();

}

static void update_thresholds() {
    sensor_threshold = analogRead(TRIM);
    for (uint8_t i=0; i < NUM_TARGETS; i++) {
        targets[i]->set_sensor_threshold(sensor_threshold);
    }
}

void loop() {
    // read sensor threshold once every N loops
    if (loop_counter % 300 == 0) {
        update_thresholds();
    }

    loop_counter++;

    // update target
    for (uint8_t i=0; i < NUM_TARGETS; i++) {
        if (targets[i]->update() > 0) {
            update_thresholds();
        }
    }
}
