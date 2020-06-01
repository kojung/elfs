# Common

## Introduction

This directory contains the communication protocol used by the main controller and target controller. The protocol is implemented on top of UART.

Main controller uses the **command** protocol to communicate with the target-controller.

Target controller uses with the **response** protocol to communicate with the main controller.

## Command protocol

The command protocol consists of a 1-byte `OPCODE` followed by zero or one 1-byte `ARG` field.

| OPCODE [1 byte]          | ARG [1 byte] | Meaning                            |
| ------------------------ | ------------ | ---------------------------------- |
| CMD_SET_TARGET_ENABLED   | target_id    | Enable the target                  |
| CMD_SET_TARGET_TIMED     | target_id    | Enable the target in timed mode    |
| CMD_SET_TARGET_DISABLED  | target_id    | Disable the target                 |
| CMD_RUN_SELF_TEST        | target_id    | Run target self-test sequence      |
| CMD_POLL_TARGET          | target_id    | Poll the hit status in the targets |
| CMD_SET_SENSOR_THRESHOLD | value        | Adjust sensor threshold            |
| CMD_GET_SENSOR_THRESHOLD |              | Get sensor threshold               |
| CMD_SET_RING_BRIGHTNESS  | value        | Set ring brightness                |
| CMD_GET_RING_BRIGHTNESS  |              | Get ring brightness                |
| CMD_SET_TIMER_INTERVAL   | value        | Set timer interval                 |
| CMD_GET_TIMER_INTERVAL   |              | Get timer interval                 |

See [cmd.h](cmd.h) header file for `OPCODE` encoding.

## Response protocol

The response protocol is composed of 3 fields:

* 1-byte OPCODE
* 1-byte ARG1
* 1-byte ARG2

| OPCODE [1 byte]       | ARG1 [1-byte]      | ARG2 [1-byte]      | Meaning                                                      |
| --------------------- | ------------------ | ------------------ | ------------------------------------------------------------ |
| RSP_HIT_STATUS        | target id          | bool               | True if target is hit                                        |
| RSP_SENSOR_THRESHOLD  | threshold MSB      | threshold LSB      | Return sensor threshold in response to CMD_GET_SENSOR_THRESHOLD |
| RSP_RING_BRIGHTNESS   | brightness MSB     | brightness LSB     | Return ring brightness in response to CMD_GET_RING_BRIGHTNESS |
| RSP_TIMER_INTERVAL    | timer interval MSB | timer interval LSB | Return timer interval in response to CMD_GET_TIMER_INTERVAL  |
| RSP_COUNTDOWN_EXPIRED | target id          | bool               | True if target count down expired                            |
| RSP_DEBUG_START       | n/a                | n/a                | Start of debug message                                       |
| RSP_DEBUG_END         | n/a                | n/a                | End of debug message                                         |

See [rsp.h](rsp.h) header file for `OPCODE` encoding.