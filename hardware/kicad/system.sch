EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 1 1
Title "ELFS System"
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L MCU_Module:Arduino_UNO_R3 A1
U 1 1 5ED430BD
P 3050 3400
F 0 "A1" H 3050 4581 50  0000 C CNN
F 1 "Arduino_UNO_R3" H 3050 4490 50  0000 C CNN
F 2 "Module:Arduino_UNO_R3" H 3050 3400 50  0001 C CIN
F 3 "https://www.arduino.cc/en/Main/arduinoBoardUno" H 3050 3400 50  0001 C CNN
	1    3050 3400
	-1   0    0    -1  
$EndComp
$Comp
L Relay:ADW11 K1
U 1 1 5ED4B112
P 6650 2250
F 0 "K1" V 6083 2250 50  0000 C CNN
F 1 "ADW11" V 6174 2250 50  0000 C CNN
F 2 "Relay_THT:Relay_1P1T_NO_10x24x18.8mm_Panasonic_ADW11xxxxW_THT" H 7975 2200 50  0001 C CNN
F 3 "https://www.panasonic-electric-works.com/pew/es/downloads/ds_dw_hl_en.pdf" H 6650 2250 50  0001 C CNN
	1    6650 2250
	0    1    1    0   
$EndComp
$Comp
L Relay:ADW11 K2
U 1 1 5ED4CE36
P 6650 3150
F 0 "K2" V 6083 3150 50  0000 C CNN
F 1 "ADW11" V 6174 3150 50  0000 C CNN
F 2 "Relay_THT:Relay_1P1T_NO_10x24x18.8mm_Panasonic_ADW11xxxxW_THT" H 7975 3100 50  0001 C CNN
F 3 "https://www.panasonic-electric-works.com/pew/es/downloads/ds_dw_hl_en.pdf" H 6650 3150 50  0001 C CNN
	1    6650 3150
	0    1    1    0   
$EndComp
$Comp
L Relay:ADW11 K3
U 1 1 5ED4D430
P 6650 4050
F 0 "K3" V 6083 4050 50  0000 C CNN
F 1 "ADW11" V 6174 4050 50  0000 C CNN
F 2 "Relay_THT:Relay_1P1T_NO_10x24x18.8mm_Panasonic_ADW11xxxxW_THT" H 7975 4000 50  0001 C CNN
F 3 "https://www.panasonic-electric-works.com/pew/es/downloads/ds_dw_hl_en.pdf" H 6650 4050 50  0001 C CNN
	1    6650 4050
	0    1    1    0   
$EndComp
$Comp
L Relay:ADW11 K4
U 1 1 5ED4D9BC
P 6650 5000
F 0 "K4" V 6083 5000 50  0000 C CNN
F 1 "ADW11" V 6174 5000 50  0000 C CNN
F 2 "Relay_THT:Relay_1P1T_NO_10x24x18.8mm_Panasonic_ADW11xxxxW_THT" H 7975 4950 50  0001 C CNN
F 3 "https://www.panasonic-electric-works.com/pew/es/downloads/ds_dw_hl_en.pdf" H 6650 5000 50  0001 C CNN
	1    6650 5000
	0    1    1    0   
$EndComp
$Comp
L Device:R ACTUATOR0
U 1 1 5ED4EEA3
P 8100 2550
F 0 "ACTUATOR0" V 7893 2550 50  0000 C CNN
F 1 "R" V 7984 2550 50  0000 C CNN
F 2 "" V 8030 2550 50  0001 C CNN
F 3 "~" H 8100 2550 50  0001 C CNN
	1    8100 2550
	0    1    1    0   
$EndComp
$Comp
L Device:R ACTUATOR1
U 1 1 5ED4F789
P 8100 3450
F 0 "ACTUATOR1" V 7893 3450 50  0000 C CNN
F 1 "R" V 7984 3450 50  0000 C CNN
F 2 "" V 8030 3450 50  0001 C CNN
F 3 "~" H 8100 3450 50  0001 C CNN
	1    8100 3450
	0    1    1    0   
$EndComp
$Comp
L Device:R ACTUATOR2
U 1 1 5ED4FB79
P 8100 4350
F 0 "ACTUATOR2" V 7893 4350 50  0000 C CNN
F 1 "R" V 7984 4350 50  0000 C CNN
F 2 "" V 8030 4350 50  0001 C CNN
F 3 "~" H 8100 4350 50  0001 C CNN
	1    8100 4350
	0    1    1    0   
$EndComp
$Comp
L Device:R ACTUATOR3
U 1 1 5ED4FEAE
P 8100 5300
F 0 "ACTUATOR3" V 7893 5300 50  0000 C CNN
F 1 "R" V 7984 5300 50  0000 C CNN
F 2 "" V 8030 5300 50  0001 C CNN
F 3 "~" H 8100 5300 50  0001 C CNN
	1    8100 5300
	0    1    1    0   
$EndComp
Wire Wire Line
	6950 2550 7800 2550
$Comp
L power:GND #PWR09
U 1 1 5ED5126C
P 8550 5550
F 0 "#PWR09" H 8550 5300 50  0001 C CNN
F 1 "GND" H 8555 5377 50  0000 C CNN
F 2 "" H 8550 5550 50  0001 C CNN
F 3 "" H 8550 5550 50  0001 C CNN
	1    8550 5550
	1    0    0    -1  
$EndComp
Wire Wire Line
	8550 5550 8550 5300
Wire Wire Line
	8550 5300 8400 5300
Wire Wire Line
	8250 4350 8400 4350
Wire Wire Line
	8550 4350 8550 5300
Connection ~ 8550 5300
Wire Wire Line
	8250 3450 8400 3450
Wire Wire Line
	8550 3450 8550 4350
Connection ~ 8550 4350
Wire Wire Line
	8550 2550 8550 3450
Connection ~ 8550 3450
Wire Wire Line
	7950 3450 7800 3450
Wire Wire Line
	6950 4350 7800 4350
Wire Wire Line
	6950 5300 7800 5300
$Comp
L power:GND #PWR08
U 1 1 5ED53B9C
P 7150 5550
F 0 "#PWR08" H 7150 5300 50  0001 C CNN
F 1 "GND" H 7155 5377 50  0000 C CNN
F 2 "" H 7150 5550 50  0001 C CNN
F 3 "" H 7150 5550 50  0001 C CNN
	1    7150 5550
	1    0    0    -1  
$EndComp
Wire Wire Line
	7150 5550 7150 4800
Wire Wire Line
	7150 4800 6950 4800
Wire Wire Line
	7150 4800 7150 3850
Wire Wire Line
	7150 3850 6950 3850
Connection ~ 7150 4800
Wire Wire Line
	7150 3850 7150 2950
Wire Wire Line
	7150 2950 6950 2950
Connection ~ 7150 3850
Wire Wire Line
	7150 2950 7150 2050
Wire Wire Line
	7150 2050 6950 2050
Connection ~ 7150 2950
Wire Wire Line
	8250 2550 8400 2550
Wire Wire Line
	2550 3400 2300 3400
Wire Wire Line
	2550 3500 2300 3500
Wire Wire Line
	2550 3600 2300 3600
Wire Wire Line
	2550 3700 2300 3700
Text Label 2300 3400 2    50   ~ 0
LDR0
Text Label 2300 3500 2    50   ~ 0
LDR1
Text Label 2300 3600 2    50   ~ 0
LDR2
Text Label 2300 3700 2    50   ~ 0
LDR3
Wire Wire Line
	5200 3000 5200 2050
Wire Wire Line
	5200 2050 5600 2050
Wire Wire Line
	5350 3100 5350 2950
Wire Wire Line
	5350 2950 5600 2950
Wire Wire Line
	5200 3200 5200 3850
Wire Wire Line
	5200 3850 5600 3850
Wire Wire Line
	5100 3300 5100 4800
Wire Wire Line
	5100 4800 5600 4800
Wire Wire Line
	3550 3600 3700 3600
Wire Wire Line
	3550 3000 5200 3000
Wire Wire Line
	3550 3100 5350 3100
Wire Wire Line
	3550 3300 5100 3300
Wire Wire Line
	3550 3200 5200 3200
Wire Wire Line
	3550 3700 3700 3700
Wire Wire Line
	3550 3800 3700 3800
Wire Wire Line
	3550 3900 3700 3900
Text Label 3700 3600 0    50   ~ 0
LED0
Text Label 3700 3700 0    50   ~ 0
LED1
Text Label 3700 3800 0    50   ~ 0
LED2
Text Label 3700 3900 0    50   ~ 0
LED3
$Comp
L power:GND #PWR02
U 1 1 5ED6B116
P 3050 5000
F 0 "#PWR02" H 3050 4750 50  0001 C CNN
F 1 "GND" H 3055 4827 50  0000 C CNN
F 2 "" H 3050 5000 50  0001 C CNN
F 3 "" H 3050 5000 50  0001 C CNN
	1    3050 5000
	1    0    0    -1  
$EndComp
Wire Wire Line
	3050 5000 3050 4700
Wire Wire Line
	3050 4700 2950 4700
Wire Wire Line
	2950 4700 2950 4500
Wire Wire Line
	3050 4500 3050 4700
Connection ~ 3050 4700
Wire Wire Line
	3150 4500 3150 4700
Wire Wire Line
	3150 4700 3050 4700
$Comp
L power:+5V #PWR01
U 1 1 5ED6E41E
P 2850 2000
F 0 "#PWR01" H 2850 1850 50  0001 C CNN
F 1 "+5V" H 2865 2173 50  0000 C CNN
F 2 "" H 2850 2000 50  0001 C CNN
F 3 "" H 2850 2000 50  0001 C CNN
	1    2850 2000
	1    0    0    -1  
$EndComp
Wire Wire Line
	2850 2000 2850 2400
$Comp
L power:+12V #PWR07
U 1 1 5ED702C7
P 6000 1550
F 0 "#PWR07" H 6000 1400 50  0001 C CNN
F 1 "+12V" H 6015 1723 50  0000 C CNN
F 2 "" H 6000 1550 50  0001 C CNN
F 3 "" H 6000 1550 50  0001 C CNN
	1    6000 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	6000 1550 6000 2450
Wire Wire Line
	6000 2450 6350 2450
Wire Wire Line
	6000 2450 6000 3350
Wire Wire Line
	6000 3350 6350 3350
Connection ~ 6000 2450
Wire Wire Line
	6000 3350 6000 4250
Wire Wire Line
	6000 4250 6350 4250
Connection ~ 6000 3350
Wire Wire Line
	6000 4250 6000 5200
Wire Wire Line
	6000 5200 6350 5200
Connection ~ 6000 4250
Text Notes 1950 5600 0    50   ~ 0
Connect USB-B connector to Raspberry Pi 4 USB port
Text Notes 1500 3550 0    50   ~ 0
To targets
Text Notes 4000 3750 0    50   ~ 0
To targets
$Comp
L power:GND #PWR06
U 1 1 5ED77EE7
P 5600 5350
F 0 "#PWR06" H 5600 5100 50  0001 C CNN
F 1 "GND" H 5605 5177 50  0000 C CNN
F 2 "" H 5600 5350 50  0001 C CNN
F 3 "" H 5600 5350 50  0001 C CNN
	1    5600 5350
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R4
U 1 1 5ED7944E
P 5600 5150
F 0 "R4" H 5668 5196 50  0000 L CNN
F 1 "10K" H 5668 5105 50  0000 L CNN
F 2 "" V 5640 5140 50  0001 C CNN
F 3 "~" H 5600 5150 50  0001 C CNN
	1    5600 5150
	1    0    0    -1  
$EndComp
Wire Wire Line
	5600 5300 5600 5350
Wire Wire Line
	5600 5000 5600 4800
Connection ~ 5600 4800
Wire Wire Line
	5600 4800 6350 4800
$Comp
L Device:R_US R2
U 1 1 5ED7DBF7
P 5600 3200
F 0 "R2" H 5668 3246 50  0000 L CNN
F 1 "10K" H 5668 3155 50  0000 L CNN
F 2 "" V 5640 3190 50  0001 C CNN
F 3 "~" H 5600 3200 50  0001 C CNN
	1    5600 3200
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR04
U 1 1 5ED7E8B7
P 5600 3350
F 0 "#PWR04" H 5600 3100 50  0001 C CNN
F 1 "GND" H 5605 3177 50  0000 C CNN
F 2 "" H 5600 3350 50  0001 C CNN
F 3 "" H 5600 3350 50  0001 C CNN
	1    5600 3350
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R3
U 1 1 5ED844A4
P 5600 4150
F 0 "R3" H 5668 4196 50  0000 L CNN
F 1 "10K" H 5668 4105 50  0000 L CNN
F 2 "" V 5640 4140 50  0001 C CNN
F 3 "~" H 5600 4150 50  0001 C CNN
	1    5600 4150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR05
U 1 1 5ED844AA
P 5600 4300
F 0 "#PWR05" H 5600 4050 50  0001 C CNN
F 1 "GND" H 5605 4127 50  0000 C CNN
F 2 "" H 5600 4300 50  0001 C CNN
F 3 "" H 5600 4300 50  0001 C CNN
	1    5600 4300
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R1
U 1 1 5ED85DA3
P 5600 2300
F 0 "R1" H 5668 2346 50  0000 L CNN
F 1 "10K" H 5668 2255 50  0000 L CNN
F 2 "" V 5640 2290 50  0001 C CNN
F 3 "~" H 5600 2300 50  0001 C CNN
	1    5600 2300
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR03
U 1 1 5ED85DA9
P 5600 2450
F 0 "#PWR03" H 5600 2200 50  0001 C CNN
F 1 "GND" H 5605 2277 50  0000 C CNN
F 2 "" H 5600 2450 50  0001 C CNN
F 3 "" H 5600 2450 50  0001 C CNN
	1    5600 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	5600 2150 5600 2050
Connection ~ 5600 2050
Wire Wire Line
	5600 2050 6350 2050
Wire Wire Line
	5600 3050 5600 2950
Connection ~ 5600 2950
Wire Wire Line
	5600 2950 6350 2950
Wire Wire Line
	5600 4000 5600 3850
Connection ~ 5600 3850
Wire Wire Line
	5600 3850 6350 3850
$Comp
L pspice:DIODE D?
U 1 1 5EE5789A
P 8100 2800
F 0 "D?" H 8100 2535 50  0000 C CNN
F 1 "DIODE" H 8100 2626 50  0000 C CNN
F 2 "" H 8100 2800 50  0001 C CNN
F 3 "~" H 8100 2800 50  0001 C CNN
	1    8100 2800
	-1   0    0    1   
$EndComp
$Comp
L pspice:DIODE D?
U 1 1 5EE5870B
P 8100 3750
F 0 "D?" H 8100 3485 50  0000 C CNN
F 1 "DIODE" H 8100 3576 50  0000 C CNN
F 2 "" H 8100 3750 50  0001 C CNN
F 3 "~" H 8100 3750 50  0001 C CNN
	1    8100 3750
	-1   0    0    1   
$EndComp
$Comp
L pspice:DIODE D?
U 1 1 5EE58B50
P 8100 4600
F 0 "D?" H 8100 4335 50  0000 C CNN
F 1 "DIODE" H 8100 4426 50  0000 C CNN
F 2 "" H 8100 4600 50  0001 C CNN
F 3 "~" H 8100 4600 50  0001 C CNN
	1    8100 4600
	-1   0    0    1   
$EndComp
$Comp
L pspice:DIODE D?
U 1 1 5EE58F47
P 8100 5550
F 0 "D?" H 8100 5285 50  0000 C CNN
F 1 "DIODE" H 8100 5376 50  0000 C CNN
F 2 "" H 8100 5550 50  0001 C CNN
F 3 "~" H 8100 5550 50  0001 C CNN
	1    8100 5550
	-1   0    0    1   
$EndComp
Wire Wire Line
	7900 2800 7800 2800
Wire Wire Line
	7800 2800 7800 2550
Connection ~ 7800 2550
Wire Wire Line
	7800 2550 7950 2550
Connection ~ 8400 2550
Wire Wire Line
	8400 2550 8550 2550
Wire Wire Line
	8400 2550 8400 2800
Wire Wire Line
	8400 2800 8300 2800
Wire Wire Line
	8300 3750 8400 3750
Wire Wire Line
	8400 3750 8400 3450
Connection ~ 8400 3450
Wire Wire Line
	8400 3450 8550 3450
Wire Wire Line
	7900 3750 7800 3750
Wire Wire Line
	7800 3750 7800 3450
Connection ~ 7800 3450
Wire Wire Line
	7800 3450 6950 3450
Wire Wire Line
	7900 4600 7800 4600
Wire Wire Line
	7800 4600 7800 4350
Connection ~ 7800 4350
Wire Wire Line
	7800 4350 7950 4350
Wire Wire Line
	8300 4600 8400 4600
Wire Wire Line
	8400 4600 8400 4350
Connection ~ 8400 4350
Wire Wire Line
	8400 4350 8550 4350
Wire Wire Line
	8300 5550 8400 5550
Wire Wire Line
	8400 5550 8400 5300
Connection ~ 8400 5300
Wire Wire Line
	8400 5300 8250 5300
Wire Wire Line
	7900 5550 7800 5550
Wire Wire Line
	7800 5550 7800 5300
Connection ~ 7800 5300
Wire Wire Line
	7800 5300 7950 5300
$EndSCHEMATC
