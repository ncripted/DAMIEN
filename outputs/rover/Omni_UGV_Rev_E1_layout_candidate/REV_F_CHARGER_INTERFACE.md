# Rev F protector and Rev E charger interface

2026-11-09 · Circuit release **blocked** pending a verified charger/protector pairing.

## Connections established from KiCad

The Rev E native netlist places U5 BAT pins 2 and 3 on VBAT. Q13 source pins 1–3 are on PROTECTED_RAW, its drain pad 5 is on VBAT, and its gate is on CUT_GATE. When Q13 is off, its intrinsic diode can conduct from VBAT to PROTECTED_RAW. When it is on, the channel connects the nodes in either direction. U5 OUT is SYS_RAW. USB motor inhibition acts downstream and does not remove this BAT-to-PROTECTED_RAW path. Rev F draft U1 PCKP pin 11 is on PROTECTED_RAW. [TI BQ24074 datasheet](https://www.ti.com/lit/ds/symlink/bq24074.pdf) · [Diodes Incorporated Q13 datasheet](https://www.diodes.com/datasheet/download/DMP2008UFG.pdf)

## Fault recovery

The MAX17301 sources a nominal 30 µA into PCKP after a discharge-current fault and uses a rise above 1 V to detect load removal. ADI also describes charging detection as a separate overdischarge-release mechanism. The BQ24074 can source precharge current during battery detection. With R14 = 3.57 kΩ, the data-sheet typical precharge setting is 88 AΩ ÷ 3570 Ω = 24.65 mA. The current actually reaching PCKP depends on charger state, Q13, both protection MOSFETs, and the fault. [Analog Devices datasheet, p. 36](https://www.analog.com/media/en/technical-documentation/data-sheets/max17300-max17313.pdf) · [TI BQ24074 datasheet, §§8.5 and 9.3.5.4](https://www.ti.com/lit/ds/symlink/bq24074.pdf)

| Case | Established behavior or model result | Required evidence |
| --- | --- | --- |
| USB absent, PCKP hard short | The short clamps PCKP. Nominal 30 µA alone reaches 1 V only at 33.33 kΩ. | Confirm the configured device stays off under a held fault, including after a wake button press. |
| USB present, hard short | A hard short at PCKP holds it low in the ideal model. A short on VBAT with Q13 off can be isolated from PCKP by Q13's channel/diode orientation. | Scope both nodes and FET gates. Confirm reconnecting Q13 or cycling USB cannot reapply cell power into the fault. |
| USB present, finite fault impedance | Only 1 mA total is needed to reach 1 V into 1 kΩ. A 970 µA contribution alongside the protector's 30 µA reaches equality. The circuit can cross the nominal voltage threshold if the charger supplies more. This example establishes a sensing sensitivity rather than a prediction of a high-current fault at 1 kΩ. | Sweep a current-limited, programmable load while observing charger and protector states. Include the range between a hard short and a removed load, plus startup inrush and loads that turn on with voltage. |
| Cold insertion and undervoltage | Dedicated ALRT/PIO wake is documented in supported sleep modes. Undervoltage DeepShip2 is charger-only. | Verify cold insertion of a programmed part and recovery with the actual Q13 path and BQ24074 profile. |

The startup simulator includes the nominal finite-resistance comparison with adjustable charger contribution. It has no charger state machine or switching model and cannot establish fault safety. Keep PCKP physically connected. Before freezing a Rev F PCB, qualify the pairing on a current-limited fixture or qualify hardware that isolates the charger while a discharge fault is latched, with a separate, bounded path for authorized undervoltage recovery. A wake or enable command must not bypass the fault state.
