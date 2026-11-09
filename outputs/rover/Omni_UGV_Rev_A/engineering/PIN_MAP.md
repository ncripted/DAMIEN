# ESP32-S3 actual pin map

| Module pin | Function/GPIO | Net |
|---|---|---|
| 1 | GND | GND |
| 2 | 3V3 | +3V3 |
| 3 | EN | ESP_EN |
| 4 | IO4 | CAM_D0 |
| 5 | IO5 | CAM_D1 |
| 6 | IO6 | CAM_D2 |
| 7 | IO7 | CAM_D3 |
| 8 | IO15 | CAM_XCLK |
| 9 | IO16 | CAM_SDA |
| 10 | IO17 | CAM_SCL |
| 11 | IO18 | M1_IN1 |
| 12 | IO8 | CAM_D4 |
| 13 | IO19 | USB_DM |
| 14 | IO20 | USB_DP |
| 15 | IO3 | unconnected-(U1-IO3-Pad15) |
| 16 | IO46 | unconnected-(U1-IO46-Pad16) |
| 17 | IO9 | CAM_D5 |
| 18 | IO10 | CAM_D6 |
| 19 | IO11 | CAM_D7 |
| 20 | IO12 | CAM_PCLK |
| 21 | IO13 | CAM_VSYNC |
| 22 | IO14 | CAM_HREF |
| 23 | IO21 | M1_IN2 |
| 24 | IO47 | FAULT_U2 |
| 25 | IO48 | FAULT_U3 |
| 26 | IO45 | unconnected-(U1-IO45-Pad26) |
| 27 | IO0 | ESP_BOOT |
| 28 | IO35 | unconnected-(U1-IO35-Pad28) |
| 29 | IO36 | unconnected-(U1-IO36-Pad29) |
| 30 | IO37 | unconnected-(U1-IO37-Pad30) |
| 31 | IO38 | M2_IN1 |
| 32 | IO39 | M2_IN2 |
| 33 | IO40 | M3_IN1 |
| 34 | IO41 | M3_IN2 |
| 35 | IO42 | DRIVE_REQ |
| 36 | RXD0 | USB_500_ENABLE |
| 37 | TXD0 | UART_TX |
| 38 | IO2 | LED_STATUS |
| 39 | IO1 | VBAT_ADC |
| 40 | GND | GND |
| 41 | GND | GND |

GPIO35/36/37 are reserved for N8R8 PSRAM. See AUDIT.md for boot, camera, drive-order and validation limits.
