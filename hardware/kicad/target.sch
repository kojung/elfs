EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 1 1
Title "ELFS Target"
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:R_PHOTO R2
U 1 1 5ED41192
P 6050 4000
F 0 "R2" H 6120 4046 50  0000 L CNN
F 1 "R_PHOTO" H 6120 3955 50  0000 L CNN
F 2 "" V 6100 3750 50  0001 L CNN
F 3 "~" H 6050 3950 50  0001 C CNN
	1    6050 4000
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R1
U 1 1 5ED419F9
P 6050 3300
F 0 "R1" H 6118 3346 50  0000 L CNN
F 1 "1K" H 6118 3255 50  0000 L CNN
F 2 "" V 6090 3290 50  0001 C CNN
F 3 "~" H 6050 3300 50  0001 C CNN
	1    6050 3300
	1    0    0    -1  
$EndComp
$Comp
L LED:WS2812B D1
U 1 1 5ED420F0
P 4800 3650
F 0 "D1" H 5144 3696 50  0000 L CNN
F 1 "WS2812B" H 5144 3605 50  0000 L CNN
F 2 "LED_SMD:LED_WS2812B_PLCC4_5.0x5.0mm_P3.2mm" H 4850 3350 50  0001 L TNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf" H 4900 3275 50  0001 L TNN
	1    4800 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	6050 3450 6050 3650
$Comp
L power:GND #PWR02
U 1 1 5ED434BC
P 5450 4700
F 0 "#PWR02" H 5450 4450 50  0001 C CNN
F 1 "GND" H 5455 4527 50  0000 C CNN
F 2 "" H 5450 4700 50  0001 C CNN
F 3 "" H 5450 4700 50  0001 C CNN
	1    5450 4700
	1    0    0    -1  
$EndComp
Wire Wire Line
	6050 4150 6050 4450
Wire Wire Line
	4800 3350 4800 3000
Wire Wire Line
	4800 3000 5400 3000
Wire Wire Line
	6050 3000 6050 3150
Wire Wire Line
	4800 3950 4800 4450
Wire Wire Line
	4800 4450 5450 4450
$Comp
L power:VDD #PWR01
U 1 1 5ED44144
P 5400 2750
F 0 "#PWR01" H 5400 2600 50  0001 C CNN
F 1 "VDD" H 5415 2923 50  0000 C CNN
F 2 "" H 5400 2750 50  0001 C CNN
F 3 "" H 5400 2750 50  0001 C CNN
	1    5400 2750
	1    0    0    -1  
$EndComp
Wire Wire Line
	5400 2750 5400 3000
Connection ~ 5400 3000
Wire Wire Line
	5400 3000 6050 3000
Wire Wire Line
	5450 4700 5450 4450
Connection ~ 5450 4450
Wire Wire Line
	5450 4450 6050 4450
NoConn ~ 5100 3650
Wire Wire Line
	6050 3650 6750 3650
Connection ~ 6050 3650
Wire Wire Line
	6050 3650 6050 3850
Wire Wire Line
	4500 3650 3800 3650
Text Label 3800 3650 0    50   ~ 0
LED
Text Label 6750 3650 0    50   ~ 0
LDR
Text Notes 3750 4050 0    50   ~ 0
This is the 16 neopixel cascaded as a ring
Text Notes 6400 3250 0    50   ~ 0
Adjust resistor value to approximate equal to\nthe LDR resistance when a laser light is hitting the LDR
$EndSCHEMATC
