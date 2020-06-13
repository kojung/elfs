#!/usr/bin/env python3

import threading
import argparse
import serial
import re
import time
from queue import Queue
from datetime import datetime
import logging
from logging import info, debug

FORMAT = "%(asctime)s [%(filename)s:%(lineno)s %(funcName)s()] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

import cmd
import rsp

def int2bytearray(n):
    """Convert an integer into bytearray representing the string version of the integer"""
    return [ord(x) for x in str(n)]

newline = [ord(x) for x in ["\n"]]

class Controller():
    def __init__(self, port, baudrate):
        """Constructor"""
        self.cmd = cmd.Cmd()
        self.rsp = rsp.Rsp()
        self.terminate = False
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = 0.1
        self.ser.setDTR(False)
        self.ser.setRTS(False)
        self.ser.open()
        self.lock = threading.Lock()
        info("Starting serial communication.... please wait")
        time.sleep(2)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def _send(self, payload):
        """serial wrapper"""
        debug(f"trying to acquire lock")
        with self.lock:
            debug(f"acquired lock")
            self.ser.write(payload)

    def _recv(self):
        """Return the next command from the serial link"""
        buf = b''
        while len(buf) == 0 or buf[-1] != 10:  # 10 == "\n"
            with self.lock:
                buf += self.ser.read_until()
            time.sleep(0.1)
            if len(buf) > 0:
                debug(f"received '{buf}' (end of transmission=%s, lastChar=%s)" % (buf[-1] == 10, buf[-1]))
        debug(f"returning '{buf}'")
        return buf.decode('utf-8').strip()

    def set_target(self, tid, mode):
        """Set target mode"""
        assert mode in ['ENABLED', 'TIMED', 'DISABLED']
        opcode_name  = f"CMD_SET_TARGET_{mode}"
        opcode_value = ord(self.cmd[opcode_name])
        payload      = bytearray([opcode_value] + int2bytearray(tid) + newline)
        self._send(payload)

    def run_self_test(self, tid):
        """Run self test"""
        opcode  = ord(self.cmd["CMD_RUN_SELF_TEST"])
        payload = bytearray([opcode] + int2bytearray(tid) + newline)
        self._send(payload)

    def poll_target(self, tid):
        """Poll target"""
        opcode  = ord(self.cmd["CMD_POLL_TARGET"])
        payload = bytearray([opcode] + int2bytearray(tid) + newline)
        self._send(payload)

    def get(self, attr):
        """Get attribute"""
        assert attr in ['SENSOR_THRESHOLD', 'RING_BRIGHTNESS', 'TIMER_INTERVAL']
        opcode_name  = f"CMD_GET_{attr}"
        opcode_value = ord(self.cmd[opcode_name])
        payload = bytearray([opcode_value] + newline)
        self._send(payload)

    def set(self, attr, val):
        """Set attribute"""
        assert attr in ['SENSOR_THRESHOLD', 'RING_BRIGHTNESS', 'TIMER_INTERVAL']
        opcode_name  = f"CMD_SET_{attr}"
        opcode_value = ord(self.cmd[opcode_name])
        payload = bytearray([opcode_value] + int2bytearray(val) + newline)
        self._send(payload)

    def reader(self, queue):
        """method for reader thread"""
        while not self.terminate:
            tokens = self._recv()
            opcode = tokens[0]
            if opcode == self.rsp["RSP_HIT_STATUS"]:
                tid = tokens[1]
                val = tokens[2]
                queue.put(f"RSP_HIT_STATUS {tid} {val}")
            elif opcode == self.rsp["RSP_COUNTDOWN_EXPIRED"]:
                tid = tokens[1]
                val = tokens[2]
                queue.put(f"RSP_COUNTDOWN_EXPIRED {tid} {val}")
            elif opcode == self.rsp["RSP_SENSOR_THRESHOLD"]:
                val = tokens[1:]
                queue.put(f"RSP_SENSOR_THRESHOLD {val}")
            elif opcode == self.rsp["RSP_RING_BRIGHTNESS"]:
                val = tokens[1:]
                queue.put(f"RSP_RING_BRIGHTNESS {val}")
            elif opcode == self.rsp["RSP_TIMER_INTERVAL"]:
                val = tokens[1:]
                queue.put(f"RSP_TIMER_INTERVAL {val}")
            elif opcode == self.rsp["RSP_DEBUG"]:
                msg = tokens[1:]
                queue.put(f"DEBUG: {msg}")
            else:
                debug("Unknown opcode '{opcode}'")
        info("End of read thread")

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
        info(f"Loading configuration from file {filename}")
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
            info("End of writer thread")

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
            info(queue.get())

    except KeyboardInterrupt:
        # terminate threads gracefully
        ctrl.terminate = True
        t1.join()
        t2.join()
        NUM_OF_TARGETS = 4
        for i in range(NUM_OF_TARGETS):
            ctrl.set_target(i, "DISABLED")
