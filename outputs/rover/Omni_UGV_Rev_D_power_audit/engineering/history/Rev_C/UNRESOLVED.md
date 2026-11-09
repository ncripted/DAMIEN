# Open issues after step 1

The completed rule-check cleanup is not a fabrication release.

1. **Power/protection qualification:** finish exact package/land overlays, sense-return review, FET/shunt/connector temperature estimates and measurements, protection thresholds/delays/recovery, charger power-path behavior, regulator startup and motor braking overshoot. Existing AO3401A motor switching still needs thermal verification.
2. **Battery and probes:** select an exact 1S cell with verified current/charge ratings and dimensions; qualify connector/harness. Four amperes continuous / five amperes peak remains a conservative design target, not measured rover consumption. Confirm the cell's allowed charging temperature window against BQ24074 TS behavior. Two independently insulated probes must be bonded to the cell and strain-relieved.
3. **PCB layout beyond DRC:** inspect inherited In1.Cu M2_A motor route and return continuity, shunt pickup, shared power trunks/vias, switching loops, effective capacitance, USB/camera signal integrity and thermal spreading. Confirm fabrication support for J1's local hole-clearance exception.
4. **Mechanical fit:** measure motor terminals/height, shaft engagement, wheel/coupling envelope, battery and camera assembly. Validate clamps carry loads, backside cover clearance and camera field of view. Printed support sources remain provisional.
5. **Firmware and Vita:** implement and test default-off driving, fault/temperature/battery monitoring, link-loss stopping, acceleration limiting, motor signs and wheel order. Verify Vita networking/video decoding before selecting a final streaming protocol. No built firmware is delivered by step 1.
6. **Bench qualification:** staged power-up, faults, USB motor disable, thermal runs, braking transients, concurrent camera/motor loads and carpet trials. No physical tests have been performed.

- Before manufacturing release, ensure the released revision matches the board silkscreen (now REV C).

2026-11-06: ESP32 substrate notch filled at Nate’s request; circular perimeter restored, motor openings retained. See engineering/OUTLINE_CHANGE.md. RF qualification required with the added FR-4.

2026-11-06: Nate authorized provisional battery assumptions for PHB1S100020CJST (20C). BOM external BAT1 and editable tray updated; see engineering/BATTERY_ASSUMPTIONS.md. Cell envelope/limits are provisional. Existing 2.6 V hardware UV cutoff and charger TS window remain qualification blockers.

## Rev C camera qualification

Verify supplied M0031 revision, flex contact side/thickness/pin-1 and connector drawing overlay. Measure lens/head/flex dimensions for the printed bracket. Check 1.3/2.8/3.3 V rails, sequencing, effective capacitors, SCCB logic levels, regulator thermal margin and added 3.3 V load. Scope XCLK/PCLK/data and prove camera capture/streaming. Camera cabling and bracket must avoid the antenna and motor leads. Motor/power audit remains unresolved as above.
