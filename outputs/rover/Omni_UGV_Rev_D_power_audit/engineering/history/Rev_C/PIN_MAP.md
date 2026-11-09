# Rev C actual ESP32 module pin map

Exported from the current native KiCad XML netlist. Physical module pad numbers are not GPIO numbers.

| Physical pad | Pin function | Net |
|---|---|---|
| 1 | GND_1 | GND |
| 2 | 3V3_2 | +3V3 |
| 3 | EN_3 | ESP_EN |
| 4 | IO4_4 | CAM_D0 |
| 5 | IO5_5 | CAM_D1 |
| 6 | IO6_6 | CAM_D2 |
| 7 | IO7_7 | CAM_D3 |
| 8 | IO15_8 | CAM_XCLK |
| 9 | IO16_9 | CAM_SDA |
| 10 | IO17_10 | CAM_SCL |
| 11 | IO18_11 | M1_IN1 |
| 12 | IO8_12 | CAM_D4 |
| 13 | IO19_13 | USB_DM |
| 14 | IO20_14 | USB_DP |
| 15 | IO3_15 | unconnected-(U1-IO3-Pad15) |
| 16 | IO46_16 | unconnected-(U1-IO46-Pad16) |
| 17 | IO9_17 | CAM_D5 |
| 18 | IO10_18 | CAM_D6 |
| 19 | IO11_19 | CAM_D7 |
| 20 | IO12_20 | CAM_PCLK |
| 21 | IO13_21 | CAM_VSYNC |
| 22 | IO14_22 | CAM_HREF |
| 23 | IO21_23 | M1_IN2 |
| 24 | IO47_24 | FAULT_U2 |
| 25 | IO48_25 | FAULT_U3 |
| 26 | IO45_26 | unconnected-(U1-IO45-Pad26) |
| 27 | IO0_27 | ESP_BOOT |
| 28 | IO35_28 | unconnected-(U1-IO35-Pad28) |
| 29 | IO36_29 | unconnected-(U1-IO36-Pad29) |
| 30 | IO37_30 | unconnected-(U1-IO37-Pad30) |
| 31 | IO38_31 | M2_IN1 |
| 32 | IO39_32 | M2_IN2 |
| 33 | IO40_33 | M3_IN1 |
| 34 | IO41_34 | M3_IN2 |
| 35 | IO42_35 | DRIVE_REQ |
| 36 | RXD0_36 | USB_500_ENABLE |
| 37 | TXD0_37 | LED_STATUS |
| 38 | IO2_38 | CELL_TEMP_ADC |
| 39 | IO1_39 | VBAT_ADC |
| 40 | GND_40 | GND |
| 41 | GND_41 | GND |

GPIO1 / module pad38 is CELL_TEMP_ADC. GPIO43 / pad37 drives LED_STATUS and TP7. Native USB GPIO19/20 remains the programming interface. GPIO35/36/37 remain unused because this N8R8 module reserves them for PSRAM.

J4: charger cell probe, pin1 BAT_NTC / pin2 GND. J5: independent drive cell probe, pin1 CELL_TEMP_DIV / pin2 GND. Both sensor heads attach to the cell, with insulated leads; neither connects to raw CELL_N.


## Rev C camera J3 physical pin map

| Pin | Function | Net |
|---|---|---|
| 1 | STROBE_1 | unconnected-(J3-STROBE-Pad1) |
| 2 | AGND_2 | GND |
| 3 | SDA_3 | CAM_SDA |
| 4 | AVDD_4 | CAM_2V8 |
| 5 | SCL_5 | CAM_SCL |
| 6 | RESET_6 | CAM_RESET |
| 7 | VSYNC_7 | CAM_VSYNC |
| 8 | PWDN_8 | GND |
| 9 | HREF_9 | CAM_HREF |
| 10 | DVDD_10 | CAM_1V3 |
| 11 | DOVDD_11 | +3V3 |
| 12 | Y9_12 | CAM_D7 |
| 13 | XCLK_13 | CAM_XCLK |
| 14 | Y8_14 | CAM_D6 |
| 15 | DGND_15 | GND |
| 16 | Y7_16 | CAM_D5 |
| 17 | PCLK_17 | CAM_PCLK |
| 18 | Y6_18 | CAM_D4 |
| 19 | Y2_19 | CAM_D0 |
| 20 | Y5_20 | CAM_D3 |
| 21 | Y3_21 | CAM_D1 |
| 22 | Y4_22 | CAM_D2 |
| 23 | Y1_23 | unconnected-(J3-Y1-Pad23) |
| 24 | Y0_24 | unconnected-(J3-Y0-Pad24) |
