#!/usr/bin/env python3.6

import threading
import argparse
import serial
import cmd
import rsp

parser = argparse.ArgumentParser(description='ELFS main controller',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i", "--input", required=True, help="Input file containing target controller commands")
parser.add_argument("-l", "--loop", type=bool, default=False, help="Replay the input file in a loop")
parser.add_argument("-b", "--baudrate", default=115200, help="Serial port baudrate")
parser.add_argument("-s", "--serial", default="/dev/ttyUSB0", help="Serial port")
args = parser.parse_args()

class Controller():
    def __init__(self, port="/dev/ttyUSB0", baurate=115200):
        """Constructor"""
        self.cmd = cmd.Cmd()
        self.rsp = rsp.Rsp()
        self.ser = ser = serial.Serial(port=port, baudrate=baurate, parity=serial.PARITY_NONE,
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

    def writer(self, filename):
        """method for reader thread"""
        with open(filename, 'r') as f:
            lines = f.readlines()
        while True:
            for line in lines:
                tokens = line.split()
                cmd = tokens[0]
                if len(tokens) > 1:
                    arg = int(tokens[1])
                if cmd == "CMD_SET_TARGET_ENABLED":
                    self.set_target(arg, "ENABLED")
                elif cmd == "CMD_SET_TARGET_TIMED":
                    self.set_target(arg, "TIMED")
                elif cmd == "CMD_SET_TARGET_DISABLED":
                    self.set_target(arg, "DISABLED")
                elif cmd == "CMD_RUN_SELF_TEST":
                    self.run_self_test(arg)
                elif cmd == "CMD_POLL_TARGET":
                    self.poll_target(arg)
                elif cmd == "CMD_GET_SENSOR_THRESHOLD":
                    self.get("SENSOR_THRESHOLD")
                elif cmd == "CMD_GET_RING_BRIGHTNESS":
                    self.get("RING_BRIGHTNESS")
                elif cmd == "CMD_GET_TIMER_INTERVAL":
                    self.get("TIMER_INTERVAL")
                elif cmd == "CMD_SET_SENSOR_THRESHOLD":
                    self.set("SENSOR_THRESHOLD", arg)
                elif cmd == "CMD_SET_RING_BRIGHTNESS":
                    self.set("RING_BRIGHTNESS", arg)
                elif cmd == "CMD_SET_TIMER_INTERVAL":
                    self.set("TIMER_INTERVAL", arg)

                foo = input("")  # wait for input

if __name__ == '__main__':
    ctrl = Controller(args.serial, args.baudrate)
    args = parser.parse_args()
    t1 = threading.Thread(target=ctrl.writer, args=(args.input,))
    t2 = threading.Thread(target=ctrl.reader)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
