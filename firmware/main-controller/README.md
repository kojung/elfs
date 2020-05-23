# Main Controller

## Description

The main controller is a Python class that handles the low level [communication protocol](../common/README.md) with the [target-controller](../target-controller/README.md). This class has an optional command line interface that can be used to interact directly with the `target-controller`, which is very useful for debugging purposes. For normal usage, the main-controller is instantiated as an object in the [user interface](../../software/README.md) component.

## Prerequisite

* Target controller firmware is loaded through the Arduino IDE
* Raspberry Pi and Arduino are connected through USB-A to USB-B cable
  * The USB cable powers up the Arduino and provides serial communication between the two boards

## Usage

```bash
$ ./controller.py -h
usage: controller.py [-h] -i INPUT [-l] [-b BAUDRATE] [-s SERIAL]

ELFS main controller

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file containing target controller commands
                        (default: None)
  -l, --loop            Replay the input file in a loop (default: False)
  -b BAUDRATE, --baudrate BAUDRATE
                        Serial port baudrate (default: 9600)
  -s SERIAL, --serial SERIAL
                        Serial port (default: /dev/ttyUSB0)

```

To exercise the targets through command line, simply use the `controller.py` script from the command line. Pass a command file with the `--input` argument. Sample command file can be found in [inputs](inputs) directory.

For example:

```bash
./controller.py -i inputs/target_0_timed.txt -l
```