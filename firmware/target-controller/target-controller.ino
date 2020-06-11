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
#include "cmd.h"
#include "rsp.h"

#define NUM_TARGETS (4)

// Targets pins: LED, LDR, TRIGGER
Target<8,  A0, 2> t0;
Target<9,  A1, 3> t1;
Target<10, A2, 4> t2;
Target<11, A3, 5> t3;

// collect targets into an array
TargetBase* targets[NUM_TARGETS] = {&t0, &t1, &t2, &t3};

void setup() {
    // enable serial
    Serial.begin(57600);
    while (!Serial) {
        ; // wait for serial port to connect. Needed for native USB port only
    }

    // disable all targets by default
    for (uint8_t i=0; i < NUM_TARGETS; i++) {
        targets[i]->set_mode(TARGET_DISABLED);
    }
}

void debug(const String msg) {
    Serial.print(RSP_DEBUG_START);
    Serial.print(msg);
    Serial.println(RSP_DEBUG_END);
}

void loop() {
    if (Serial.available() > 0) {
        String cmd = Serial.readString();
        char opcode = cmd[0];
        uint8_t tid, state;
        int value;
        switch(opcode) {
            case CMD_SET_TARGET_ENABLED:
                tid = atoi(cmd[1]);
                targets[tid]->set_mode(TARGET_ENABLED);
                break;

            case CMD_SET_TARGET_TIMED: 
                tid = atoi(cmd[1]);
                targets[tid]->set_mode(TARGET_TIMED);
                break;

            case CMD_SET_TARGET_DISABLED: 
                tid = atoi(cmd[1]);
                targets[tid]->set_mode(TARGET_DISABLED);
                break;

            case CMD_SET_SENSOR_THRESHOLD:
                value = cmd.substring(1).toInt();
                for (uint8_t i=0; i < NUM_TARGETS; i++) {
                    targets[i]->set_sensor_threshold(value);
                }
                break;
        
            case CMD_SET_TIMER_INTERVAL:
                value = cmd.substring(1).toInt();
                for (uint8_t i=0; i < NUM_TARGETS; i++) {
                    targets[i]->set_timer_interval(value);
                }
                break;

            case CMD_SET_RING_BRIGHTNESS: 
                value = cmd.substring(1).toInt();
                for (uint8_t i=0; i < NUM_TARGETS; i++) {
                    targets[i]->set_ring_brightness(value);
                }
                break;

            case CMD_RUN_SELF_TEST:
                tid = atoi(cmd[1]);
                targets[tid]->run_self_test();
                break;

            case CMD_GET_SENSOR_THRESHOLD:
                value = targets[0]->get_sensor_threshold();
                Serial.print(RSP_SENSOR_THRESHOLD);
                Serial.println(value);
                break;

            case CMD_GET_RING_BRIGHTNESS:
                value = targets[0]->get_ring_brightness();
                Serial.print(RSP_RING_BRIGHTNESS);
                Serial.println(value);
                break;

            case CMD_GET_TIMER_INTERVAL:
                value = targets[0]->get_timer_interval();
                Serial.print(RSP_TIMER_INTERVAL);
                Serial.println(value);
                break;

            case CMD_POLL_TARGET:
                tid = atoi(cmd[1]);
                state = targets[tid]->get_hit_state();
                Serial.print(RSP_HIT_STATUS);
                Serial.print(tid);
                Serial.println(state);
                break;

            default:
                // unrecognized or unimplemented commands
                break;
        }
    }

    for (uint8_t i=0; i < NUM_TARGETS; i++) {
        int value = targets[i]->update();
        if (value > 0) {
            Serial.print(RSP_HIT_STATUS);
            Serial.print(i);
            Serial.println(1);
        } else if (value < 0) {
            Serial.print(RSP_COUNTDOWN_EXPIRED);
            Serial.print(i);
            Serial.println(1);
        } else {
            // no change, do nothing
        }
    }
}
