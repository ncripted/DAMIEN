# Rev E pin map

Derived from validation/current/schematic.net.xml. Physical module pads differ from GPIO numbers.

## U1 — ESP32-S3-WROOM-1-N8R8

| Physical pin | Function | Net |
|---|---|---|
| 2 | 3V3_2 | +3V3 |
| 4 | IO4_4 | CAM_D0 |
| 5 | IO5_5 | CAM_D1 |
| 6 | IO6_6 | CAM_D2 |
| 7 | IO7_7 | CAM_D3 |
| 12 | IO8_12 | CAM_D4 |
| 17 | IO9_17 | CAM_D5 |
| 18 | IO10_18 | CAM_D6 |
| 19 | IO11_19 | CAM_D7 |
| 22 | IO14_22 | CAM_HREF |
| 20 | IO12_20 | CAM_PCLK |
| 10 | IO17_10 | CAM_SCL |
| 9 | IO16_9 | CAM_SDA |
| 21 | IO13_21 | CAM_VSYNC |
| 8 | IO15_8 | CAM_XCLK |
| 38 | IO2_38 | CELL_TEMP_ADC |
| 35 | IO42_35 | DRIVE_REQ_RAW |
| 27 | IO0_27 | ESP_BOOT |
| 3 | EN_3 | ESP_EN |
| 24 | IO47_24 | FAULT_U2 |
| 25 | IO48_25 | FAULT_U3 |
| 1 | GND_1 | GND |
| 40 | GND_40 | GND |
| 41 | GND_41 | GND |
| 37 | TXD0_37 | LED_STATUS |
| 11 | IO18_11 | M1_IN1 |
| 23 | IO21_23 | M1_IN2 |
| 31 | IO38_31 | M2_IN1 |
| 32 | IO39_32 | M2_IN2 |
| 33 | IO40_33 | M3_IN1 |
| 34 | IO41_34 | M3_IN2 |
| 36 | RXD0_36 | USB_500_ENABLE |
| 13 | IO19_13 | USB_DM |
| 14 | IO20_14 | USB_DP |
| 39 | IO1_39 | VBAT_ADC |
| 15 | IO3_15 | unconnected-(U1-IO3-Pad15) |
| 28 | IO35_28 | unconnected-(U1-IO35-Pad28) |
| 29 | IO36_29 | unconnected-(U1-IO36-Pad29) |
| 30 | IO37_30 | unconnected-(U1-IO37-Pad30) |
| 26 | IO45_26 | unconnected-(U1-IO45-Pad26) |
| 16 | IO46_16 | unconnected-(U1-IO46-Pad16) |

## J3 — M0031 CAMERA FPC24

| Physical pin | Function | Net |
|---|---|---|
| 11 | DOVDD_11 | +3V3 |
| 10 | DVDD_10 | CAM_1V3 |
| 4 | AVDD_4 | CAM_2V8 |
| 19 | Y2_19 | CAM_D0 |
| 21 | Y3_21 | CAM_D1 |
| 22 | Y4_22 | CAM_D2 |
| 20 | Y5_20 | CAM_D3 |
| 18 | Y6_18 | CAM_D4 |
| 16 | Y7_16 | CAM_D5 |
| 14 | Y8_14 | CAM_D6 |
| 12 | Y9_12 | CAM_D7 |
| 9 | HREF_9 | CAM_HREF |
| 17 | PCLK_17 | CAM_PCLK |
| 6 | RESET_6 | CAM_RESET |
| 5 | SCL_5 | CAM_SCL |
| 3 | SDA_3 | CAM_SDA |
| 7 | VSYNC_7 | CAM_VSYNC |
| 13 | XCLK_13 | CAM_XCLK |
| 15 | DGND_15 | GND |
| 2 | AGND_2 | GND |
| 8 | PWDN_8 | GND |
| 1 | STROBE_1 | unconnected-(J3-STROBE-Pad1) |
| 24 | Y0_24 | unconnected-(J3-Y0-Pad24) |
| 23 | Y1_23 | unconnected-(J3-Y1-Pad23) |

## J4 — CELL NTC - CHARGER

| Physical pin | Function | Net |
|---|---|---|
| 1 | Pin_1_1 | CELL_CHG_TEMP |
| 2 | Pin_2_2 | GND |

## J5 — CELL NTC - DRIVE

| Physical pin | Function | Net |
|---|---|---|
| 1 | Pin_1_1 | CELL_TEMP_DIV |
| 2 | Pin_2_2 | GND |

## U7 — BQ298217RUGR

| Physical pin | Function | Net |
|---|---|---|
| 5 | CTR_5 | CELL_N |
| 1 | BAT_1 | PROT_BAT |
| 8 | CHG_8 | PROT_CHG |
| 4 | CS_4 | PROT_CS_SENSE |
| 7 | DSG_7 | PROT_DSG |
| 6 | PACK_6 | PROT_PACK |
| 2 | VDD_2 | PROT_VDD |
| 3 | VSS_3 | PROT_VSS_SENSE |

## R36 — 10m 1% 1W KELVIN

| Physical pin | Function | Net |
|---|---|---|
| 1 | I_CELL_N_1 | CELL_N |
| 2 | I_GND_2 | GND |
| 4 | S_GND_4 | PROT_CS_SENSE |
| 3 | S_CELL_N_3 | PROT_VSS_SENSE |

## U10 — TPS3840DL31DBVR

| Physical pin | Function | Net |
|---|---|---|
| 3 | GND_3 | CELL_N |
| 2 | VDD_2 | CELL_P |
| 4 | MR_N_4 | CELL_P |
| 5 | CT_5 | CELL_UV_CT |
| 1 | RESET_N_1 | CELL_UV_RESET_N |

## Q12 — MMBT3906

| Physical pin | Function | Net |
|---|---|---|
| 2 | E_2 | CELL_P |
| 3 | C_3 | CUT_GATE |
| 1 | B_1 | CUT_PNP_B |

## Q13 — DMP2008UFG-7

| Physical pin | Function | Net |
|---|---|---|
| 4 | G_4 | CUT_GATE |
| 1 | S_[1-3]_1 | PROTECTED_RAW |
| 2 | S_2 | PROTECTED_RAW |
| 3 | S_3 | PROTECTED_RAW |
| 5 | D_[5-8]_5 | VBAT |

## U14 — SN74LVC1G17DBVR

| Physical pin | Function | Net |
|---|---|---|
| 5 | VCC_5 | +3V3 |
| 4 | Y_4 | DRIVE_REQ |
| 2 | A_2 | DRIVE_REQ_RAW |
| 3 | GND_3 | GND |
| 1 | NC_1 | unconnected-(U14-NC-Pad1) |
