#!/usr/bin/env python3.6

import cmd
import rsp

class Controller():
    def __init__(self):
        """Constructor"""
        self.cmd = cmd.Cmd()
        self.rsp = rsp.Rsp()

    def set_target(self, tid, mode):
        """Set target mode"""
        assert mode in ['ENABLED', 'TIMED', 'DISABLED']
        opcode_name  = f"CMD_SET_TARGET_{mode}"
        opcode_value = self.cmd[f"CMD_SET_TARGET_{mode}"]
        payload      = bytearray([opcode_value, tid])
        print(payload)

if __name__ == '__main__':
    ctrl = Controller()
    ctrl.set_target(0, 'ENABLED')
