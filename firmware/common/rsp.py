#!/usr/bin/env python3

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

class Rsp(dict):
    """Response protocol class"""
    def __init__(self):
        """Constructor"""
        self["RSP_HIT_STATUS"]        = "H"
        self["RSP_SENSOR_THRESHOLD"]  = "t"
        self["RSP_RING_BRIGHTNESS"]   = "b"
        self["RSP_TIMER_INTERVAL"]    = "i"
        self["RSP_DEBUG"]             = "D"
        self["RSP_COUNTDOWN_EXPIRED"] = "E"

if __name__ == '__main__':
    print("// This is auto-generated file. Do not edit manually!\n")
    print("#pragma once\n")
    c = Rsp()
    for name, opcode in c.items():
        print(f"#define {name} '{opcode}'")
