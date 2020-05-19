#!/usr/bin/env python3.6

class Cmd(dict):
    """Command protocol class"""
    def __init__(self):
        """Constructor"""
        opcodes = """
            CMD_SET_TARGET_ENABLE
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
