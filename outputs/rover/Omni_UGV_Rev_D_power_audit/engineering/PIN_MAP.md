# Rev D pin map from the saved native netlist

Physical pad numbers are not GPIO numbers.

## U1 — ESP32-S3-WROOM-1-N8R8

| Physical pin | Pin function | Net |
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
| 35 | IO42_35 | DRIVE_REQ_RAW |
| 36 | RXD0_36 | USB_500_ENABLE |
| 37 | TXD0_37 | LED_STATUS |
| 38 | IO2_38 | CELL_TEMP_ADC |
| 39 | IO1_39 | VBAT_ADC |
| 40 | GND_40 | GND |
| 41 | GND_41 | GND |

## J3 — M0031 CAMERA FPC24

| Physical pin | Pin function | Net |
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

## J4 — CELL NTC - CHARGER

| Physical pin | Pin function | Net |
|---|---|---|
| 1 | Pin_1_1 | CELL_CHG_TEMP |
| 2 | Pin_2_2 | GND |

## J5 — CELL NTC - DRIVE

| Physical pin | Pin function | Net |
|---|---|---|
| 1 | Pin_1_1 | CELL_TEMP_DIV |
| 2 | Pin_2_2 | GND |

## U7 — BQ298217RUGR

| Physical pin | Pin function | Net |
|---|---|---|
| 1 | BAT_1 | PROT_BAT |
| 2 | VDD_2 | PROT_VDD |
| 3 | VSS_3 | CELL_N |
| 4 | CS_4 | GND |
| 5 | CTR_5 | CELL_N |
| 6 | PACK_6 | PROT_PACK |
| 7 | DSG_7 | PROT_DSG |
| 8 | CHG_8 | PROT_CHG |

## U10 — TPS3840DL31DBVR

| Physical pin | Pin function | Net |
|---|---|---|
| 1 | RESET_N_1 | CELL_UV_RESET_N |
| 2 | VDD_2 | CELL_P |
| 3 | GND_3 | CELL_N |
| 4 | MR_N_4 | CELL_P |
| 5 | CT_5 | CELL_UV_CT |

## U11 — TLV75533PDBVR

| Physical pin | Pin function | Net |
|---|---|---|
| 1 | IN_1 | USB_5V |
| 2 | GND_2 | GND |
| 3 | EN_3 | USB_5V |
| 4 | NC_4 | unconnected-(U11-NC-Pad4) |
| 5 | OUT_5 | CHG_3V3 |

## U12 — TLV6700DDCR

| Physical pin | Pin function | Net |
|---|---|---|
| 1 | OUTA_1 | CHG_TEMP_OK_OD |
| 2 | GND_2 | GND |
| 3 | INA+_3 | CHG_HOT_SENSE |
| 4 | INB-_4 | CHG_COLD_SENSE |
| 5 | VDD_5 | USB_5V |
| 6 | OUTB_6 | CHG_TEMP_OK_OD |

## U13 — SN74LVC1G14DBVR

| Physical pin | Pin function | Net |
|---|---|---|
| 1 | NC_1 | unconnected-(U13-NC-Pad1) |
| 2 | A_2 | CHG_TEMP_ALLOW_RC |
| 3 | GND_3 | GND |
| 4 | Y_4 | CHG_DISABLE |
| 5 | VCC_5 | USB_5V |

## U14 — SN74LVC1G17DBVR

| Physical pin | Pin function | Net |
|---|---|---|
| 1 | NC_1 | unconnected-(U14-NC-Pad1) |
| 2 | A_2 | DRIVE_REQ_RAW |
| 3 | GND_3 | GND |
| 4 | Y_4 | DRIVE_REQ |
| 5 | VCC_5 | +3V3 |

GPIO2 / module pad38 is CELL_TEMP_ADC. GPIO1 / pad39 is VBAT_ADC. An earlier explanatory sentence reversed these; the native pad assignments did not. GPIO42 / pad35 is now DRIVE_REQ_RAW, buffered by U14. GPIO44 / pad36 selects USB input mode. GPIO43 / pad37 drives status LED. GPIO35/36/37 remain reserved for N8R8 PSRAM and unused.

J4 is the independent charging-temperature probe input to U12. J5 is the separate drive-temperature ADC probe. Both sensor heads attach to the insulated cell surface; neither lead connects to CELL_N.
