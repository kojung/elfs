#!/usr/bin/env python3

import threading
import argparse
import serial
import re
import time
from queue import Queue

import cmd
import rsp

class Controller():
    def __init__(self, port, baurate):
        """Constructor"""
        self.cmd = cmd.Cmd()
        self.rsp = rsp.Rsp()
        self.terminate = False
        self.ser = serial.Serial(port=port, baudrate=baurate, parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
        self.buffer = []

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

    def next_serial_char(self):
        """Return the next character from the serial buffer"""
        if len(self.buffer) == 0:
            while len(self.buffer) == 0:
                try:
                    self.buffer = [x for x in self.ser.read(100)]
                except serial.SerialException:
                    # ignore this error
                    #    raise SerialException('read failed: {}'.format(e))
                    # serial.serialutil.SerialException: read failed: device reports readiness to read but returned no data (device disconnected or multiple access on port?)
                    pass
        c = self.buffer.pop(0)
        return c

    def reader(self, queue):
        """method for reader thread"""
        while not self.terminate:
            data = self.next_serial_char()
            if data == self.rsp["RSP_HIT_STATUS"]:
                tid = self.next_serial_char()
                val = self.next_serial_char()
                queue.put(f"RSP_HIT_STATUS {tid} {val}")
            elif data == self.rsp["RSP_COUNTDOWN_EXPIRED"]:
                tid = self.next_serial_char()
                val = self.next_serial_char()
                queue.put(f"RSP_COUNTDOWN_EXPIRED {tid} {val}")
            elif data == self.rsp["RSP_SENSOR_THRESHOLD"]:
                msb = self.next_serial_char()
                lsb = self.next_serial_char()
                val = msb << 8 | lsb
                queue.put(f"RSP_SENSOR_THRESHOLD {val}")
            elif data == self.rsp["RSP_RING_BRIGHTNESS"]:
                msb = self.next_serial_char()
                lsb = self.next_serial_char()
                val = msb << 8 | lsb
                queue.put(f"RSP_RING_BRIGHTNESS {val}")
            elif data == self.rsp["RSP_TIMER_INTERVAL"]:
                msb = self.next_serial_char()
                lsb = self.next_serial_char()
                val = msb << 8 | lsb
                queue.put(f"RSP_TIMER_INTERVAL {val}")
            elif data == self.rsp["RSP_DEBUG_START"]:
                msg = ""
                while True:
                    data = self.next_serial_char()
                    if data == self.rsp["RSP_DEBUG_END"]:
                        queue.put(f"DEBUG: {msg}")
                        break
                    else:
                        msg += chr(data)
            else:
                queue.put(f"ERROR: Unknown byte '{data}'")
        print("INFO: End of read thread")

    def writer(self, filename, loop=False):
        """method for reader thread"""
        def execute(lines):
            for line in lines:
                # skip comments and empty lines
                if re.search(r'^\s*#', line) or re.search(r'^\s*$', line):
                    continue
                # parse tokens
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

        # wait for serial port to be ready
        time.sleep(2)

        # execute the command from the user
        with open(filename, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
        execute(lines)

        # loop based on user input
        if loop:
            while not self.terminate:
                # non-blocking user input
                import sys, select
                while sys.stdin in select.select([sys.stdin], [], [], 2)[0]:
                    ignore = sys.stdin.readline()
                    execute(lines)
        print("INFO: End of writer thread")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ELFS main controller',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input", required=True, help="Input file containing target controller commands")
    parser.add_argument("-l", "--loop", default=False, action='store_true', help="Replay the input file in a loop")
    parser.add_argument("-b", "--baudrate", default=9600, help="Serial port baudrate")
    parser.add_argument("-s", "--serial", default="/dev/ttyUSB0", help="Serial port")
    args = parser.parse_args()
    ctrl = Controller(args.serial, args.baudrate)
    args = parser.parse_args()
    queue = Queue()
    t1 = threading.Thread(target=ctrl.writer, args=(args.input, args.loop,))
    t2 = threading.Thread(target=ctrl.reader, args=[queue])
    t1.start()
    t2.start()
    try:
        while True:
            print(queue.get())

    except KeyboardInterrupt:
        # terminate threads gracefully
        ctrl.terminate = True
        t1.join()
        t2.join()
        NUM_OF_TARGETS = 4
        for i in range(NUM_OF_TARGETS):
            ctrl.set_target(i, "DISABLED")
