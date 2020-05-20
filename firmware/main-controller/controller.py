#!/usr/bin/env python3.6

import serial
import cmd
import rsp

BAUDRATE = 115200
PORT     = '/dev/ttyUSB0'

class Controller():
    def __init__(self, port):
        """Constructor"""
        self.cmd = cmd.Cmd()
        self.rsp = rsp.Rsp()
        self.ser = serial.Serial(port, BAUDRATE, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

    def set_target(self, tid, mode):
        """Set target mode"""
        assert mode in ['ENABLED', 'TIMED', 'DISABLED']
        opcode_name  = f"CMD_SET_TARGET_{mode}"
        opcode_value = self.cmd[opcode_name]
        payload      = bytearray([opcode_value, tid])
        self.ser.write(payload)

    def run_self_test(self, tid):
        """Run self test"""
        opcode  = self.cmd[f"CMD_RUN_SELF_TEST"]
        payload = bytearray([opcode, tid])
        self.ser.write(payload)

    def poll_target(self, tid):
        """Poll target"""
        opcode  = self.cmd[f"CMD_POLL_TARGET"]
        payload = bytearray([opcode, tid])
        self.ser.write(payload)

    def get(self, attr):
        """Get attribute"""
        assert attr in ['SENSOR_THRESHOLD', 'RING_BRIGHTNESS', 'TIMER_INTERVAL']
        opcode_name  = f"CMD_GET_{attr}"
        opcode_value = self.cmd[opcode_name]
        payload = bytearray([opcode_value])
        self.ser.write(payload)

    def get(self, attr, val):
        """Set attribute"""
        assert attr in ['SENSOR_THRESHOLD', 'RING_BRIGHTNESS', 'TIMER_INTERVAL']
        opcode_name  = f"CMD_SET_{attr}"
        opcode_value = self.cmd[opcode_name]
        payload = bytearray([opcode_value, val])
        self.ser.write(payload)

if __name__ == '__main__':
    ctrl = Controller(PORT)
    while True:
        for i in range(4):
            ctrl.set_target(i, 'ENABLED')
        input("Press any key")
