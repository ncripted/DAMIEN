from pathlib import Path
import json,shutil
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');e=r/'engineering';h=e/'history/Rev_C';h.mkdir(parents=True,exist_ok=True)
for fn in ['START_HERE.md','README.md']:
 if not (h/fn).exists():shutil.copy2(r/fn,h/fn)
(r/'START_HERE.md').write_text('''# Omni rover — Rev D power audit

Open **omni_ugv.kicad_pro** in KiCad 10.0.8, then the PCB Editor or 3D Viewer (Alt+3). Rev C is preserved in its separate project directory. There is no live editor IPC connection: close/reload an older open revision before editing.

Read **engineering/POWER_AUDIT.md** for implemented power changes, calculations, assumptions and pending qualification. Native editable files are authoritative. The ten-page Schematic.pdf, BOM.csv, design_connections.json, engineering/PIN_MAP.csv and validation/current apply to Rev D. Check validation_summary.json for the recorded final native results.

Rev D adds independent low-cell load shutdown, an analog cell-temperature charging window, a drive-request buffer, and lower-loss motor-switch FETs. New monitoring parts occupy the left sector. Both TH1/J4 and TH2/J5 are independent insulated probes attached to the actual cell. TH1 now feeds the external analog window; U5 TS uses a fixed 10k bias. GPIO2/pad38 is the drive-temperature ADC and GPIO1/pad39 the battery ADC.

Camera J3 remains the Arducam M0031 24-pin DVP flex interface with Hirose FH12-24S-0.5SH(55), incompatible with the old Waveshare 18-pin carrier. Camera fit, sequencing and operation remain unqualified.

Current views: preview/rev-d-top.png, preview/rev-d-bottom.png and preview/schematics. mechanics/Rev_D_board_only.step contains the bare board, not a complete fitted assembly. Historical STEP/renders are marked under history. Custom protection-package bodies, camera, motors, wheels and battery are not fully represented in 3D.

This is an unbuilt engineering prototype, not a fabrication release. No physical power, fault, thermal, motor, battery, camera, RF or carpet tests have been performed. U7's 2.6 V emergency cutoff still needs compatibility resolution against the assumed cell minimum; U10 removes operating loads earlier but is not a zero-leakage storage disconnect. See engineering/UNRESOLVED.md. Do not run historical generation scripts over the current native sources.
''',encoding='utf-8')
(r/'README.md').write_text('''# Miniature omni camera rover — Rev D

Rev D implements the design-side power-audit corrections in native KiCad sources: independent 3.1 V operating-load shutdown, independent USB-powered charging-temperature monitoring of the actual cell, buffered default-low drive request, and lower-loss motor-power FETs. The 100 mm nominal solid perimeter, three motor openings, camera connector, motor pads and mounting geometry are retained. New monitoring circuitry uses the left sector.

Start with START_HERE.md and engineering/POWER_AUDIT.md. engineering/POWER_CALCULATIONS.json contains repeatable estimates; engineering/PIN_MAP.csv is derived from the final native netlist. validation/current holds configured checks and explicit electrical/copper deltas. The original ZIP and Rev C project remain preserved.

All configured checks pass only as recorded in validation_summary.json. Physical function, heating, cell/harness ratings, emergency UV compatibility, regen/braking, shunt sensing, effective capacitors, mechanical fit, RF and firmware/Vita qualification remain open. Read engineering/UNRESOLVED.md before any manufacturing work. There is no live editor IPC link and no manufacturing order has been made.
''',encoding='utf-8')
(e/'UNRESOLVED.md').write_text('''# Rev D unresolved qualification and next work

The file-based power audit is implemented. Production/fabrication gate remains **BLOCKED**. No physical tests have been performed.

1. **Exact cell/harness:** validate PHB1S100020CJST limits, actual envelope, connector/polarity, contacts, wiring and pulse-duration ratings. Accepted 1S/1Ah/20C and charge/temperature assumptions are provisional. 4A continuous / 5A transient are harness design targets, not an established board rating.
2. **Emergency undervoltage:** U10 now removes operating loads around 3.1V. U7 still disconnects at its factory 2.6V backstop. A strict 3.0V absolute cell minimum is not fully enforced during prolonged storage/faults; confirm cell compatibility or design a reviewed higher-threshold pack disconnect. Verify cutoff/recovery/USB wake and off-state current on a cell simulator.
3. **Temperature:** verify U12's modeled window against the actual NTC curve, passive tolerances, open/short/startup behavior and measured bonded-cell temperature. TH1 and TH2 must be insulated, independently wired and strain relieved. Firmware still must handle TH2 faults/temperature.
4. **Power layout/sourcing:** prove Kelvin pickup at R36, return gradients, driver/regulator/charger/FET thermal paths, current-path/via ratings, effective capacitance and exact package/land overlays. U10's exact part is active but direct TI stock was unavailable at review; qualify procurement before freeze. Passive MPNs are not fully locked. Review/move inherited M2_A on In1.Cu. No new In1 signal tracks were added. Retain visibility of the inherited J1-specific 0.19mm hole-clearance exception pending fabricator acceptance.
5. **Transient and regen:** scope VMOTOR/VBAT/SYS_RAW/3.3V during stall, coast, reverse, USB insertion and protection cutoff. The charger does not limit regenerative battery charging; U7's charge-overcurrent trip is above the assumed cell charge limit. Establish stop mode/ramps and any energy clamp from measurements. Drivers may reach UVLO before the cell supervisor under low-cell/high-load conditions; normal firmware must stop earlier.
6. **Mechanical/RF/camera:** measure motor terminals, shafts, hubs, wheels, cell, camera flex/head and brackets. Recheck printed-support and protection-cover clearance around new components. Validate camera rails/sequencing/timing and FPC orientation. The copper antenna keepout is preserved; added perimeter FR-4 still requires RF testing. Existing CAD remains provisional.
7. **Firmware and Vita:** implement default-off arming, command timeout, ramps/limits, battery/driver/TH2 monitoring and fault latching; GPIO42 now feeds U14 as DRIVE_REQ_RAW. Verify Vita networking/decoding before choosing the camera protocol. No working firmware is delivered by this power-audit step.

See POWER_AUDIT.md for calculations, sources and the staged bench procedure. Next work: focused PCB power/return/sourcing review, then an authorized prototype and measured bring-up. No board order or publication is authorized.
''',encoding='utf-8')
p=e/'BATTERY_ASSUMPTIONS.md';s=p.read_text(encoding='utf-8');s+='''

## Rev D implementation update — 2026-11-06

U10 now shuts operating loads down around 3.1V independently of firmware; U7 retains its 2.6V emergency backstop. This does not close a strict 3.0V emergency/storage compatibility requirement. An independent USB-powered analog window now monitors TH1 at J4 and controls charger CE. The BQ TS input is intentionally fixed at 10k; it is no longer directly connected to TH1. The modeled tolerance envelope is 1.78–11.16C cold and 36.70–43.59C hot using a beta approximation; exact R-T and bonded-cell tests remain mandatory. Earlier paragraphs describe the pre-Rev-D state. POWER_AUDIT.md and UNRESOLVED.md govern current status.
''';p.write_text(s,encoding='utf-8')
p=r/'CHANGELOG.md';s=p.read_text(encoding='utf-8');p.write_text('''# Rev D — 2026-11-06 — power audit

- Preserved Rev C and reproduced its clean native checks before editing.
- Added U10/Q9/Q10/Q11, R46–R54 and C30/C31 for independent low-cell operating-load shutdown and recovery delay.
- Moved TH1/J4 from direct BQ TS to USB-powered U11/U12/U13 hot/cold charging window; added R55–R63/C32–C36; biased U5 TS with fixed R60 and controlled U5 CE. Both probes remain on the cell.
- Replaced Q1/Q2 with pin-compatible DMP2035U-7. Changed R24 to10k and R25 to47k. Added U14/R64/C37 to buffer GPIO42, named its raw request DRIVE_REQ_RAW and changed R28 to1M. Strengthened UV clamp R52 to3.3k.
- Routed new low-current controls without adding In1 signal tracks. Isolated CE from former GND copper; removed two resulting redundant GND stubs. Preserved outline, motor pads, mounting geometry, camera and ESP32 placement.
- Added connected functional schematics, visible 0.8mm labels, fresh native reports/previews/board-only STEP, calculations, explicit pin/net and copper deltas. Corrected an explanatory ADC GPIO reversal; actual native ADC assignments did not change.
- Clean configured checks are not physical qualification. U7 emergency UV/cell compatibility, Kelvin/thermal/current paths, harness, effective capacitors and braking/regen remain explicit blockers.

Earlier revision history follows.

'''+s,encoding='utf-8')
m=json.loads((r/'mechanical.json').read_text());m['revision']='D';m['power_revision_notes']='New monitoring components in left sector; motor/mount/outline geometry unchanged. Bare-board STEP only. Recheck cover/clamp/battery clearances around all new parts; no new physical fit tests.';(r/'mechanical.json').write_text(json.dumps(m,indent=2))
(r/'.pcba-workflow/layout-review.json').write_text(json.dumps({'revision':'D','status':'BLOCKED','configured_checks':'PASS as recorded in validation/current','new_In1_signal_tracks':0,'mechanical_status':'UNVERIFIED','release_blockers':'engineering/UNRESOLVED.md','review':'engineering/POWER_AUDIT.md'},indent=2))
print('Updated current revision entry points and unresolved qualification list')
