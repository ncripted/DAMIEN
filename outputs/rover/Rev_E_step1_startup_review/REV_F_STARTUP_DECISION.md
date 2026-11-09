# Rev F battery startup decision

2026-11-08 · Preferred architecture selected for qualification. Rev E fabrication remains on hold.

## Decision

Use the MAX17301G+T as the lead replacement candidate for U7. Design for an intentional battery-only start using its dedicated ALRT/PIO wake input, with PCKP permanently sensing the actual protected output. Treat the part as a new protection design with production-programmed nonvolatile settings. The user-visible behavior is to insert a healthy cell and use the power control to start the rover without USB. The implementation can use a momentary wake control alongside the existing power switch until their integration is verified. [Analog Devices MAX17301 product page](https://www.analog.com/en/products/max17301.html) · [Datasheet, pp. 26 and 48–51](https://www.analog.com/media/en/technical-documentation/data-sheets/max17300-max17313.pdf)

## Why change the protector

The native Rev E netlist connects U7 PACK through R39 to PROTECTED_RAW. Q13 separates that node from VBAT at the BQ24074 BAT output. A full 4.20 V cell needs more than 4.90 V at PACK to satisfy the typical BQ298217 startup comparator. The upper regulated BAT specification gives only 4.23 V before any Q13 path loss. TI lists a UV_SHUT-disabled factory configuration in the family range, but the comparison table does not identify an orderable device with the Rev E settings and that option. The BQ2970 family likewise documents possible first-insertion discharge inhibition, so it does not establish a guaranteed automatic replacement. [TI BQ298x datasheet, §§4, 7.3.2 and 7.4.1.1](https://www.ti.com/lit/ds/symlink/bq2980.pdf) · [TI BQ24074 datasheet, §8.5](https://www.ti.com/lit/ds/symlink/bq24074.pdf) · [TI BQ297xx datasheet, §8.4.1](https://www.ti.com/lit/ds/symlink/bq2970.pdf)

The isolated PACK stimulus remains a bench discriminator. Rev E uses that same pin to distinguish a removed load from a persistent discharge fault. A control that forces the voltage at that pin can obscure the fault. A separate wake input avoids that interaction by design. MAX17301 has a documented PCKP load-removal check using 30 µA and a threshold above 1 V. For a passive resistive load with USB absent, the nominal threshold is 1 V ÷ 30 µA = 33.33 kΩ. This is a release test after trip. It does not set the fault trip current or guarantee that a powered system has enough off-state impedance for recovery. [TI BQ298x datasheet, §7.3.4](https://www.ti.com/lit/ds/symlink/bq2980.pdf) · [Analog Devices datasheet, p. 36](https://www.analog.com/media/en/technical-documentation/data-sheets/max17300-max17313.pdf)

## Rev F design inputs

| Function | Requirement or evidence |
| --- | --- |
| Battery-only wake | ALRT/PIO pin 10 is the candidate's wake input. Set nConfig.PBen in production and verify the saved image after reset. Button returns to the protector's local reference using the manufacturer's application circuit. DeepShip2 entered on undervoltage is charger-only. Button behavior from cold insertion of a programmed unit is a separate test from Ship/DeepShip wake. |
| Pack sensing | Keep pin 11 PCKP on the physical protected output. Include every attached passive and active load in the recovery review. Confirm charger attachment cannot mask a short or drive the unprotected cell. |
| Cell current | Rev E R36 is 10 mΩ, 1%, 1 W, Kelvin. Rev E nominal thresholds are 6 A discharge overcurrent and 20 A short detection. The MAX17301 short comparator tops out at 155 mV, or 15.5 A with 10 mΩ. Recalculate threshold bands and the FET/shunt pulse rating from cell limits, startup inrush and fault energy before choosing shunt and register settings. |
| Charge recovery | Keep USB motor inhibit independent of the protector. Assess charger BAT behavior through Q13 and the protection switches for cell undervoltage and full-cell insertion. Evaluate disabling zero-volt charging via ZVC pin 13 as part of the selected cell's charging policy. |
| Temperature | Preserve the cell-mounted charger thermistor and the dedicated cell-mounted monitoring path. Any additional protector TH connection must have an independent sensor or a manufacturer-supported sharing circuit so its bias cannot shift the charger's thresholds. |
| Manufacturing | Define I²C programming access and power for a blank unit, then program, read back and verify the protection profile independently of rover firmware. Confirm footprint, driver headroom for the selected MOSFETs, and Kelvin reference polarity before layout. |

Sources for candidate pinout, thresholds, and programming: [Analog Devices datasheet, pp. 26, 36–38, 48–51 and Nonvolatile Memory](https://www.analog.com/media/en/technical-documentation/data-sheets/max17300-max17313.pdf).

## Verification gates

1. On a candidate evaluation fixture, verify cold insertion at 4.20 V and 3.10 V, with USB absent and present. Record cell voltage, PCKP, VBAT and both FET gate-to-source voltages. Confirm one valid user wake starts the healthy battery-only path and that the motors stay disabled until the existing interlock and command conditions permit motion.
2. Verify permitted undervoltage recovery through the intended charger and full rejection of a held short with USB absent, during USB insertion, and with the wake input held. Verify recovery after the short is removed. Use a current-limited cell simulator and keep motors disconnected.
3. Check current thresholds, cell temperature limits and recovery against the selected battery before releasing a PCB. The behavioral simulator now includes the nominal load-removal calculation for this candidate. It does not model first insertion, a charger driving PCKP, or transient protection behavior.

This decision completes the desktop architecture comparison. The selected direction is provisional until the verification gates pass. The Rev E native schematic, board, and BOM remain the baseline.
