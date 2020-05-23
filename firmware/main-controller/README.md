# Main Controller

## Description

The main controller is a Python class that handles the low level [communication protocol](../common/README.md) with the [target-controller](../target-controller/README.md). This class has an optional command line interface that can be used to interact directly with the `target-controller`, which is very useful for debugging purposes. For normal usage, the main-controller is instantiated as an object in the [user interface](../../software/README.md) component.

## Prerequisite

* Target controller firmware is loaded through the Arduino IDE
* Serial cables are connected between the Raspberry Pi and the Arduino Uno (a level shifter is needed) (See [Hardware](../../hardware/README.md) section for more details)

## Usage

TODO



