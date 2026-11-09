# Rev E protector startup review

2026-11-08. Status: BLOCKED pending startup and recovery evidence on a current-limited fixture.

The authoritative sources are the Rev E KiCad project and its freshly exported native netlist. The archived project and the working schematic agree. The working PCB differs from its archive only in 3D model path lines. Board, net class and schematic settings match the archive. Fresh KiCad checks found zero ERC violations, zero DRC violations, zero opens and zero schematic parity issues.

## Root cause and voltage budget

The cell enters through J2. U7 BAT reads CELL_P through R38 and its VDD is supplied separately from the raw cell. U7 pin 6 reads PROTECTED_RAW through R39. U5 BAT is on VBAT, downstream of Q13. Q13 can conduct charge toward PROTECTED_RAW through its body diode when its channel is off. U5 OUT feeds SYS_RAW and cannot be treated as the voltage at U7 PACK. The switched 3.3 V rail and firmware cannot be assumed to start in a battery-only boot while the protection FETs are open.

BQ298217 has UV_SHUT enabled and starts in shutdown. TI specifies battery voltage above the UV threshold and charger detection for that transition. The charger-detection differential is 0.7 V typical. The BQ24074 BAT regulation range is 4.16 to 4.23 V under the specified conditions. At a 4.20 V simulated cell, even using 4.23 V and assuming a lossless path gives only +0.03 V at PACK relative to BAT, a 0.67 V shortfall from the typical threshold. Q13 diode drop or charger detection cycling can reduce the available margin. At 3.10 V the optimistic margin is +1.06 to +1.13 V, so a successful test with a partly discharged cell does not establish full-cell startup.

Sources: [TI BQ298xx datasheet, sections 4, 6, 7.3 and 7.4](https://www.ti.com/lit/ds/symlink/bq2980.pdf) and [TI BQ24074 datasheet, section 8.5](https://www.ti.com/lit/ds/symlink/bq24074.pdf).

## Options screened

- Keep U7 and momentarily drive its PACK sense input from an isolated wake source. R39 must be disconnected from the power rail during the pulse and restored afterward. PACK also determines recovery from overcurrent and short circuit. A permanent bias or repeated retries could make a persistent fault look like a removed load. This is the preferred bench discriminator because it tests the documented wake mechanism without connecting a boosted rail to the charger or cell.
- Change U7. The named BQ298xx variants in TI's comparison table all enable UV shutdown. A configurable family option is not an identified orderable replacement. ABLIC S-821AA also documents possible first-connect discharge inhibition. Listed NB7120 variants use high-side shunt sensing and the examined 601EZ/FZ variants have a 4.50 V overcharge threshold, making them unsuitable drop-ins for the Rev E 4.25 V primary threshold.

Sources: [TI variant table](https://www.ti.com/lit/ds/symlink/bq2980.pdf), [ABLIC S-821AA operation](https://www.ablic.com/en/doc/datasheet/battery_protection/S821AA_E.pdf) and [Nisshinbo NB7120 ordering table](https://www.nisshinbo-microdevices.co.jp/en/pdf/datasheet/nb7120-s-e.pdf).

## Bench discriminator

Use an assembled board, a floating current-limited cell simulator that can sink charger current, and differential probes. CELL_N and system GND are separated by R36. The test fixture must preserve that connection through the shunt and avoid additional ground bonds. Leave motors and the real LiPo disconnected.

1. Record CELL_P relative to CELL_N, PACK relative to U7 VSS, PROTECTED_RAW, VBAT and both protection FET gate-to-source voltages. Test a fresh 4.20 V connection with USB absent, then with USB applied. Repeat at 3.10 V. Record actual PACK voltage while the charger is detecting a battery.
2. On an unpowered bench unit, isolate the existing R39 connection. Use a break-before-make fixture to connect the U7 PACK side either through 1 kΩ to the original PROTECTED_RAW node or through a separate 1 kΩ to a floating, current-limited 6.0 V test source referenced to CELL_N. Verify with continuity measurements that the wake position has no connection to PROTECTED_RAW or VBAT. Use one bounded stimulus and observe both gate outputs. At a 100 kΩ modeled input pull-down the expected PACK voltage is about 5.94 V. TI gives a typical wake differential and no guaranteed pulse width for this fixture, so log voltage and timing and treat the result as a measurement.
3. Remove the wake source and restore the original sense path before applying load. Verify that the protector stays in normal operation. Test safe recovery using a programmable, current-limited load and the real sense path. Confirm that overcurrent and short protection do not repeatedly re-enable into a persistent fault.
4. Use the traces to choose the production topology. A candidate with U7 retained must define how a removable cell starts with USB absent, how an undervoltage trip recovers with USB present, and how the circuit prevents a wake pulse from defeating protection. A production design also needs evidence for supply and temperature limits, hot plug, and any wake-switch failure modes.

The 6.0 V source is a bench stimulus only. TI's evaluation guide uses a simulated charger to investigate wake behavior. This fixture isolates the stimulus at the sense pin. [TI evaluation guide](https://www.ti.com/lit/ug/slvub38/slvub38.pdf)

## Findings

| ID | Severity | Finding | Status |
|---|---|---|---|
| START-1 | Major | The regulated Rev E charger path misses the documented typical full-cell wake differential | Calculated from native connectivity and datasheets |
| START-2 | Major | Gate behavior across POR, fixture removal and protection recovery needs physical traces | Open |
| START-3 | Critical | A sustained or repeated artificial PACK reading can affect fault recovery | Production wake path requires validation |

This review qualifies the diagnosis and defines the bench test. No wake circuit has been validated for production. Fabrication remains blocked. The report is outside the archived Rev E design package so that its hashes remain meaningful.
