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
        self["CMD_SET_TARGET_ENABLED"]   = "E"
        self["CMD_SET_TARGET_TIMED"]     = "M"
        self["CMD_SET_TARGET_DISABLED"]  = "D"
        self["CMD_RUN_SELF_TEST"]        = "R"
        self["CMD_POLL_TARGET "]         = "P"
        self["CMD_SET_SENSOR_THRESHOLD"] = "T"
        self["CMD_GET_SENSOR_THRESHOLD"] = "t"
        self["CMD_SET_RING_BRIGHTNESS"]  = "B"
        self["CMD_GET_RING_BRIGHTNESS"]  = "b"
        self["CMD_SET_TIMER_INTERVAL"]   = "I"
        self["CMD_GET_TIMER_INTERVAL"]   = "i"

if __name__ == '__main__':
    print("// This is auto-generated file. Do not edit manually!\n")
    print("#pragma once\n")
    c = Cmd()
    for name, opcode in c.items():
        print(f"#define {name} '{opcode}'")
