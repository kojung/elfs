#!/usr/bin/env python3.6

class Rsp(dict):
    """Response protocol class"""
    def __init__(self):
        """Constructor"""
        opcodes = """
            RSP_HIT_STATUS
            RSP_SENSOR_THRESHOLD
            RPS_RING_BRIGHTNESS
            RSP_TIMER_INTERVAL""".split()
        for idx, opcode in enumerate(opcodes):
            self[opcode] = 0x80 + idx

if __name__ == '__main__':
    print("// This is auto-generated file. Do not edit manually!\n")
    print("#pragma once\n")
    c = Rsp()
    for opcode, value in c.items():
        print(f"#define {opcode} ({hex(value)})")
