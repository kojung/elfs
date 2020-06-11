#!/usr/bin/env python3.6

# 
# Extensible Laser Firing System - ELFS
# Copyright (C) 2020 Jung Ko <kojung@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# 

class Cmd(dict):
    """Command protocol class"""
    def __init__(self):
        """Constructor"""
        self.opcodes = {
           "E": "CMD_SET_TARGET_ENABLED",
           "M": "CMD_SET_TARGET_TIMED",
           "D": "CMD_SET_TARGET_DISABLED",
           "R": "CMD_RUN_SELF_TEST",
           "P": "CMD_POLL_TARGET ",
           "T": "CMD_SET_SENSOR_THRESHOLD",
           "t": "CMD_GET_SENSOR_THRESHOLD",
           "B": "CMD_SET_RING_BRIGHTNESS",
           "b": "CMD_GET_RING_BRIGHTNESS",
           "I": "CMD_SET_TIMER_INTERVAL",
           "i": "CMD_GET_TIMER_INTERVAL",
        }

if __name__ == '__main__':
    print("// This is auto-generated file. Do not edit manually!\n")
    print("#pragma once\n")
    c = Cmd()
    for opcode, name in c.opcodes.items():
        print(f"#define {name} '{opcode}'")
