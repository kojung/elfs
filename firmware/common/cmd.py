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
        opcodes = """
            CMD_SET_TARGET_ENABLED
            CMD_SET_TARGET_TIMED
            CMD_SET_TARGET_DISABLED
            CMD_RUN_SELF_TEST
            CMD_POLL_TARGET 
            CMD_SET_SENSOR_THRESHOLD
            CMD_GET_SENSOR_THRESHOLD
            CMD_SET_RING_BRIGHTNESS
            CMD_GET_RING_BRIGHTNESS
            CMD_SET_TIMER_INTERVAL
            CMD_GET_TIMER_INTERVAL""".split()
        for idx, opcode in enumerate(opcodes):
            self[opcode] = 0x80 + idx

if __name__ == '__main__':
    print("// This is auto-generated file. Do not edit manually!\n")
    print("#pragma once\n")
    c = Cmd()
    for opcode, value in c.items():
        print(f"#define {opcode} ({hex(value)})")
