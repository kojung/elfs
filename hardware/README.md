# Hardware

## Bill of material

### Target

**Each** target consists of the following:

| Component                                               | Quantity | Possible supplier                                            |
| ------------------------------------------------------- | -------- | ------------------------------------------------------------ |
| Neopixel Ring 16 x 5050 RGB LED with Integrated Drivers | 1        | [Adafruit](https://www.adafruit.com/product/1463)            |
| Large Photoresistor - 20mm                              | 1        | [Tinkersphere](https://tinkersphere.com/sensors/2185-large-photoresistor-20mm.html) |
| 1K resistor                                             | 1        |                                                              |
| 10K resistor                                            | 1        |                                                              |
| Actuator                                                | 1        | [Amazon](https://www.amazon.com/dp/B07FY9KXB5/ref=cm_sw_em_r_mt_dp_U_GsiWEbMZS77H9) |
| 1/4" bearings                                           | 1        |                                                              |
| Male/Female connector                                   | 1        |                                                              |
| 1/4" - 20 nuts to hold bearings                         | 4        |                                                              |

This project supports up to 4 targets, so multiply the above component count by 4.

### Target Controller

| Component             | Quantity | Possible supplier                                            |
| --------------------- | -------- | ------------------------------------------------------------ |
| Arduino UNO Rev 3     | 1        | [Arduino Store](https://store.arduino.cc/usa/arduino-uno-rev3) |
| 5V Relay - 4 channels | 1        | [Amazon](https://www.amazon.com/dp/B00KTEN3TM/ref=cm_sw_em_r_mt_dp_U_OviWEbK5ZWK2H) |

### Main Controller

| Component             | Quantity | Possible Supplier                                            |
| --------------------- | -------- | ------------------------------------------------------------ |
| Raspberry Pi 4B (2GB) | 1        | [Raspberry Pi Foundation](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) |

Any raspberry pi system should work, but we recommend a RPI4B with at least 2GB memory.

### Others

| Component                         | Quantity | Possible Supplier                                            |
| --------------------------------- | -------- | ------------------------------------------------------------ |
| Dual output 5V / 12V power supply | 1        | [Amazon](https://www.amazon.com/dp/B07RT54H9V/ref=cm_sw_em_r_mt_dp_U_pAiWEbQV0GEES) |
| 1/4" threaded rod                 | 1        |                                                              |

# Schematics

File [system schematic](system_schematic.pdf) shows the electrical connection at the system level. 

File [target schematic](target_schematic.pdf) shows the electrical connection at the target level.

# Plans

A sample plan on how to build a target can be found in [target drawing](target_drawing.pdf). Once assembled, simply attach some heavy steel bar to the bottom of the target to weight down the target. 