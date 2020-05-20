#!/usr/bin/env python3.6

import threading
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
        self.ser = ser = serial.Serial(port=PORT, baudrate=BAUDRATE, parity=serial.PARITY_NONE,
                                       stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=None)

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

    def set(self, attr, val):
        """Set attribute"""
        assert attr in ['SENSOR_THRESHOLD', 'RING_BRIGHTNESS', 'TIMER_INTERVAL']
        opcode_name  = f"CMD_SET_{attr}"
        opcode_value = self.cmd[opcode_name]
        msb = (val >> 8) & 0xFF
        lsb = val & 0xFF
        payload = bytearray([opcode_value, msb, lsb])
        self.ser.write(payload)

    def reader(self):
        """method for reader thread"""
        while True:
            data = self.ser.read().decode('utf-8')
            print(data, end="")

    def writer(self):
        """method for reader thread"""
        while True:
            print("Enable target 0 as TIMED")
            ctrl.set('TIMER_INTERVAL', 300)
            ctrl.set('RING_BRIGHTNESS', 10)
            ctrl.set('SENSOR_THRESHOLD', 500)
            ctrl.set_target(0, 'TIMED')
            for i in range(1, 4):
                ctrl.set_target(i, 'DISABLED')
            foo = input("\n")

if __name__ == '__main__':
    ctrl = Controller(PORT)
    t1 = threading.Thread(target=ctrl.writer)
    t2 = threading.Thread(target=ctrl.reader)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
