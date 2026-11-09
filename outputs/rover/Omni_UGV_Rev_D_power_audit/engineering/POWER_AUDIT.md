# Rev D power-system audit — 2026-11-06

The design-side audit and the corrections below are implemented in native KiCad files. **Fabrication/functional qualification: BLOCKED.** No PCB, battery, motor, temperature, USB or transient measurements have been performed. A clean configured rule check is not a qualification result.

## Source of truth and revision

Rev C was independently checked before copying: ERC 0, DRC errors/warnings 0, unconnected 0, parity 0. Rev D is a separate editable project. Rev C and the supplied ZIP remain preserved. The native `.kicad_sch` and `.kicad_pcb` files govern; older Rev A/B/C notes and presentation generators are historical. `validation/current` contains the final checks, canonical connection delta and board-change proof. KiCad 10.0.8 CLI and its installed pcbnew Python API were used. There is no live editor IPC connection; an older open board must be reloaded before editing.

## Implemented corrections

1. **Independent low-cell shutdown:** U10 TPS3840DL31DBVR senses raw CELL_P relative to CELL_N. Q9 inverts its active-low output; Q10 clamps regulator EN and Q11 clamps DRIVE_ENABLE. R54 separates the power-switch request from EN so an ON switch cannot defeat the clamp. Q9 and reset pullups run from protected VBAT, preventing their fault-state current from bypassing U7 after its emergency cutoff. C31 delays recovery about 62 ms nominal. Charging remains available while the logic is inhibited. Falling threshold is 3.0535–3.1465 V; recovery threshold spans approximately 3.2285–3.3715 V before delay. These are supervisor limits, not cell-vendor approval or a guarantee of brownout-free driving at full load. [TI supervisor datasheet](https://www.ti.com/lit/ds/symlink/tps3840.pdf), [exact orderable device](https://www.ti.com/product/TPS3840/part-details/TPS3840DL31DBVR).

2. **Independent charging-temperature window:** TH1 remains a separate insulated 103AT-2 probe bonded to the actual cell, connected at J4. U11 creates a USB-powered 3.3 V reference; U12 TLV6700 compares the loaded NTC divider against hot/cold limits. Its outputs must both release before U13 drives the BQ24074 CE pin low. Open/short probe causes a fault. R61/C35 delay initial charge permission; R62 limits discharge current into the comparator. R60 intentionally replaces the direct BQ TS probe with the documented fixed 10 kΩ bias. The external window now performs the cell-temperature decision, even with ESP32/main switch off. It is not a PCB-temperature measurement. Nominal beta-model cutoffs are approximately 6.68 °C cold / 40.00 °C hot; full modeled tolerance results are in `POWER_CALCULATIONS.json`. [TI charger datasheet](https://www.ti.com/lit/ds/symlink/bq24074.pdf), [TI window comparator](https://www.ti.com/lit/ds/symlink/tlv6700.pdf).

3. **Lower motor-switch loss:** Q1/Q2 become DMP2035U-7, retaining SOT23 G1/S2/D3 and the common-source topology. Q5 remains AO3401A. At VGS = −2.5 V the new pair's specified 25 °C resistance is at most 90 mΩ, versus 170 mΩ for the old pair. At 2.4 A this gives 0.518 W versus 0.979 W total conduction loss. Low-cell gate drive may require the new part's −1.8 V / 62 mΩ-per-device bound; do not use the −2.5 V estimate universally. R24 becomes 22 kΩ and R25 56 kΩ to strengthen gate turnoff and account for gate leakage/loading. [Diodes exact device datasheet](https://www.diodes.com/datasheet/download/DMP2035U.pdf).

4. **Drive-enable logic margin:** U14 SN74LVC1G17 buffers GPIO42's DRIVE_REQ_RAW. R64 defaults its input low, C37 bypasses its supply, and R28 becomes 1 MΩ. The buffer supplies the two nSLEEP inputs and Q3 base through the retained 1 kΩ R27. At a conservative 3.2 V rail and 100 µA output-load envelope, VOH ≥ 3.0 V; the calculated line remains above 2.9 V versus the driver's 2.5 V required high. USB Q4 and UV Q11 clamp the line after R27, limiting their sink current to approximately 3.3 mA. Both DRV8833 internal sleep pulldowns remain in parallel with R28. Neither buffer nor firmware overrides these clamps. [TI buffer](https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf), [TI motor driver](https://www.ti.com/lit/ds/symlink/drv8833.pdf).

New monitoring components occupy the left sector. Motor locations, mounting holes, outline, camera connector and ESP32 placement are unchanged. No new signal track was added to In1.Cu. The inherited M2_A route there remains an explicit layout issue, not an ignored violation.

## Power tree and current ownership

```text
raw 1S cell J2 CELL_P/CELL_N
  ├─ U7 + Q7/Q8 high-side protection ─ VBAT ─ Q1/Q2 ─ VMOTOR ─ U2/U3 ─ motors
  │                                  └─ U5 BAT/OUT power path ─ SYS_RAW ─ U4 ─ 3.3 V
  │                                                                         ├─ ESP32
  │                                                                         ├─ U14
  │                                                                         └─ U8/U9 camera supplies
  └─ nanopower U10 (raw-cell voltage supervision only)
USB 5 V ─ U5 charger/input power path
        ├─ U11/U12/U13 independent cell-temperature charging permission
        └─ Q4 hardware drive disable
all main cell return current: GND ─ R36 (10 mΩ) ─ CELL_N
```

**Motor current bypasses U5 OUT and its USB/input limits.** Charging current, USB input current and motor current are distinct quantities. Motor regeneration also bypasses the charger's programmed current regulation. J4 and J5 probe returns are system GND; neither probe lead connects to raw CELL_N. The small UV monitoring circuit references CELL_N intentionally; do not extend that raw-ground connection to other loads.

| Rail/domain | Expected use | Limits/evidence |
|---|---|---|
| Raw cell | 1S, 3.7 V nominal | Accepted assumptions: 4.2 V charge target, 3.0 V operating minimum; exact battery limits unverified |
| VBAT | protected cell / charger BAT | Main logic and motor supply; includes shunt/protection drops |
| VMOTOR | switched protected battery | DRV8833 recommended minimum 2.7 V; must be scoped under low-cell/load transients |
| SYS_RAW | BQ power path | About 4.4 V on USB, follows battery through internal path otherwise |
| +3V3 | U4 TPS63802 | Nominal 3.3077 V from 511 kΩ / 91 kΩ feedback; effective capacitance/transients unqualified |
| CAM_1V3 / CAM_2V8 | U8/U9 | Camera rails only; current/sequence and actual M0031 revision unverified |
| CHG_3V3 | U11, USB only | Dedicated reference for TH1 divider; not the main 3.3 V rail |

## Charger and recovery

R14 = 3.57 kΩ gives nominal 249 mA charge current, approximately 221–276 mA with stated KISET limits and a 1% resistor. This is about 0.25C for the assumed 1 Ah pack. EN2 is grounded; GPIO44 selects USB100/USB500 via EN1. R15's ILIM setting is not selected in those modes. Default USB100 may not sustain Wi-Fi and camera: the battery can supplement the load, and absent/dead-cell USB boot is not guaranteed. Firmware must obey the actual USB power allowance before selecting USB500. R16 = 46.4 kΩ sets roughly 6.2 h nominal fast-charge timing; verify the full CC/CV cycle and timer extensions on the selected cell. [BQ24074](https://www.ti.com/lit/ds/symlink/bq24074.pdf).

U10 shuts down main logic while the raw cell is low, leaving charging able to recover it. U7's UV_SHUT behavior still requires charger-assisted wake after emergency cutoff. BQ298217 disables zero-volt charging; this design is not intended to recover a deeply damaged cell. USB insertion disables driving independently of firmware and regardless of charger CE state.

## Current budget, protection and heating

R6/R7/R9 = 0.25 Ω give nominal 0.8 A winding-current chopping. The driver's 160–240 mV trip range gives approximately 0.634–0.970 A with 1% resistors, before blanking-time overshoot. Three channels therefore sum to about 2.91 A at the upper static corner. This is not battery current at every PWM duty and is not permission to stall continuously. Pololu's 6 V, 1.5 A stall value implies an approximate 4 Ω winding resistance, so 4.2 V / 4 Ω = 1.05 A is only a first estimate before electrical losses. Carpet load and motor heating require tests. [Pololu #3065 specifications](https://www.pololu.com/product/3065/specs).

A **provisional** 0.5 A allocation on 3.3 V requires about 0.626 A from a 3.1 V source at an **assumed** 85% converter efficiency. Together with the upper motor corner this is about 3.54 A. Thus 4 A continuous / 5 A short transient are harness design targets, not measured consumption or established PCB capability. U4's 2 A capability is not permission to allocate that much continuously while all motors are loaded. [TPS63802](https://www.ti.com/lit/ds/symlink/tps63802.pdf).

U7's 60 mV OCD threshold and 10 mΩ ±1% shunt give approximately 5.45–6.57 A using the correct ±5 mV detector accuracy; nominal delay is 16 ms. OCC is approximately 3.27–3.94 A, nominal 8 ms. The 200 mV short detector is approximately 18.6–21.4 A, nominal 250 µs. Include timing tolerance and dynamic overshoot in fault qualification. These are fault trips, not regulated current limits. A connector sold as “5 A peak” without duration/temperature data is insufficient evidence. R36 loss is 0.16 W at 4 A and 0.25 W at 5 A before temperature/tolerance; its 1 W headline still needs pad/ambient derating. [BQ2980/2982](https://www.ti.com/lit/ds/symlink/bq2980.pdf).

At 2.91 A, the Q1/Q2 pair's −2.5 V conduction estimate is about 0.762 W total at 25 °C; at the −1.8 V bound it is about 1.05 W. Hot resistance and the actual copper thermal path increase junction temperature. At 4 A even the 25 °C / −2.5 V estimate is 1.44 W per pair: **4 A continuous through this PCB is not thermally qualified.** Q7/Q8, DRV8833 dissipation (including PWM loss), charger exposed-pad cooling, shunt and connector contacts all need temperature measurements. A representative charger scenario, 5.25 V input, 3.0 V cell at 276 mA and 300 mA system load at 4.4 V, dissipates roughly 0.88 W before other losses; thermal regulation may reduce charging. Do not treat datasheet JEDEC thermal resistance as this board's measured value.

## Temperature calculation and limitations

The loaded divider model includes both comparator input branches, independent input biases (25 nA / 15 nA), reference ±1.5%, 1.5% resistor envelopes including a provisional TCR budget, NTC R25 ±1%, B ±1%, and full-temperature comparator trip limits. Across 4096 endpoint evaluations, cold-fault assertion spans about **1.78–11.16 °C** and hot-fault assertion **36.70–43.59 °C**. This is intentionally narrower than the accepted 0–45 °C limits. Nominal behavior and a temperature sweep are reproduced by `calculate.py` and `POWER_CALCULATIONS.json`.

The beta equation is an approximation, not a manufacturer guaranteed full R–T curve. Probe self-heating is at most about 0.273 mW in the simple divider; bonding/insulation, thermal lag, lead resistance, contamination leakage and soldering drift still need evaluation. Charge re-entry uses comparator hysteresis and should be measured separately. Exact passive MPNs/TCR/DC-bias curves remain unlocked. No claim of a production-guaranteed 0–45 °C window is made before those checks. TH2 at J5 remains the independent drive-temperature probe; discharge overtemperature handling still requires firmware.

## Layout and transient findings

- [SPEC] No new In1.Cu signal routing. The inherited M2_A segment on the primary ground plane is approximately 11.05 mm long at 0.2 mm width (exact total in `power-layout-inventory.json`). It interrupts the reference plane locally; a later power-layout pass must inspect return continuity and move it if feasible. It was not concealed by a rule exclusion.
- [TBD-MEASURE] Shared VBAT/VMOTOR trunks include 1.0 mm copper and narrower pad escapes; motor-output networks contain long 0.2 mm routes. Width alone does not establish ampacity. With 35 µm copper, an isolated 73 mm × 0.2 mm route is about 0.18 Ω at 20 °C; actual parallel copper, path lengths and temperature must be considered individually.
- [TBD-MEASURE] U7 CS is assigned to global GND, not a separately named Kelvin net. Inspect/prove the pickup at R36's GND pad and VSS return at its CELL_N pad against power-current voltage gradients. Connectivity and parity cannot establish sense accuracy. No unsubstantiated Kelvin-layout signoff is claimed.
- [SPEC] U4's two switch-node connections remain local, about 4.71 mm each / 0.4 mm on F.Cu, without vias. This does not close the complete switching-loop/return/thermal review. New slow monitoring traces are 0.15 mm; their width is not used for main motor current.
- [TBD-MEASURE] C18 nominal 10 µF and C19/C20 nominal 22 µF each must provide the manufacturer's effective minimums (input 4 µF, output 7 µF) after bias, tolerance and temperature. Similarly verify BQ and camera/U11 bypass capacitors. Nominal values are not DC-bias proof.
- [TBD-MEASURE] C90 = 220 µF / 10 V is not an energy dump. Charging it from 4.2 to 6 V absorbs only about 2.02 mJ. Q1/Q2 opening or U7 fault can isolate the cell from motor energy. Scope VMOTOR, VBAT and SYS_RAW during coast, reverse, obstruction, USB insertion and protection trip. No TVS was chosen without a measured energy/pulse requirement.
- [SPEC] The charger's 249 mA limit does not limit regenerative battery charging. U7's approximately 3.6 A charge-overcurrent threshold exceeds the assumed 1 A cell charge limit. Default firmware stopping should coast, and reversal/braking must remain limited until battery charge current and rail overshoot are characterized. This is a release blocker.

## Operating-state table

| State | Main logic | Motor permission | Charging |
|---|---|---|---|
| Cell healthy, switch OFF, no USB | off | default off | absent |
| Cell healthy, switch ON, boot/reset | powers up | R64 / driver pulldowns default off | absent |
| Firmware armed, valid link | on | only with no USB and no UV clamp | absent |
| USB connected | optionally on | Q4 forces off independently | only if TH1 window valid |
| Cell below U10 threshold | Q10 inhibits U4 | Q11 forces off | USB can recover cell if U7 permits |
| TH1 open/short/hot/cold | unaffected | USB already forces off | U12/U13 inhibit CE |
| U7 emergency fault | protected rail disconnected | unavailable | fault-specific recovery; bench test |
| TH2 hot/open/short or link lost | firmware responsibility | must stop; firmware not implemented | TH1 remains independent |

## Required qualification before release

1. Confirm the exact PHB1S100020CJST cell limits, dimensions, protection status, connector series/polarity, wires and allowed pulse durations. The accepted assumptions are not a signed manufacturer specification.
2. Lock exact capacitors/resistors and package/land-pattern overlays; prove the shunt sense pickup and current-return/thermal paths. Resolve motor routing on In1.Cu, J1 fabrication exception and camera/RF/mechanical gates.
3. On a current-limited cell simulator, sweep supply down/up and record U10, EN, DRIVE_ENABLE, VMOTOR and 3.3 V. Verify cutoff/recovery, switch OFF, boot and USB recovery before connecting motors.
4. Substitute precision resistances at J4; verify both trip/re-entry points, open/short behavior, USB hot plug, switch OFF and absent firmware. Then repeat with both insulated probes bonded to the cell and a calibrated temperature reference.
5. Measure charge/input/system currents in USB100/500, empty/full battery, concurrent camera load and timeout/termination; verify USB enumeration/power permission.
6. Measure worst-load supply droop and braking/regenerative current with an oscilloscope/current probe. Exercise hardware USB/UV/fault shutdown while motors run. Establish allowable ramps, duty and stop mode before carpet trials.
7. Measure FET, shunt, driver, charger, regulator, connector and cell temperatures at representative ambient and obstruction durations. Verify driver faults, physical cell-probe response and protection recovery.

All of these are pending, not reported as tests already passed. The next step is the focused PCB power/return review followed by prototype bench qualification, not ordering boards from this audit alone.

**Emergency undervoltage limit:** U10 is an operating-load shutdown, not a new high-side pack disconnect. U7 still has its 2.6 V factory backstop. Against a strict 3.0 V absolute cell minimum, the emergency/storage protection gate remains open: confirm the actual cell specification or implement a reviewed higher-threshold disconnect. Do not describe that compatibility issue as closed by U10.
