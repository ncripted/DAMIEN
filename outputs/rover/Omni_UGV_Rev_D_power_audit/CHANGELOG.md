# Rev D — 2026-11-06 — power audit

- Preserved Rev C and reproduced its clean native checks before editing.
- Added U10/Q9/Q10/Q11, R46–R54 and C30/C31 for independent low-cell operating-load shutdown and recovery delay.
- Moved TH1/J4 from direct BQ TS to USB-powered U11/U12/U13 hot/cold charging window; added R55–R63/C32–C36; biased U5 TS with fixed R60 and controlled U5 CE. Both probes remain on the cell.
- Replaced Q1/Q2 with pin-compatible DMP2035U-7. Changed R24 to22k and R25 to56k. Added U14/R64/C37 to buffer GPIO42, named its raw request DRIVE_REQ_RAW and changed R28 to1M. Strengthened UV clamp R52 to3.3k.
- Routed new low-current controls without adding In1 signal tracks. Isolated CE from former GND copper; removed two resulting redundant GND stubs. Preserved outline, motor pads, mounting geometry, camera and ESP32 placement.
- Added connected functional schematics, visible 0.8mm labels, fresh native reports/previews/board-only STEP, calculations, explicit pin/net and copper deltas. Corrected an explanatory ADC GPIO reversal; actual native ADC assignments did not change.
- Clean configured checks are not physical qualification. U7 emergency UV/cell compatibility, Kelvin/thermal/current paths, harness, effective capacitors and braking/regen remain explicit blockers.

Earlier revision history follows.

# Change log

## 2026-11-05 — Rev B step 1

- Reorganized seven native schematic pages with functional grouping and visible local wiring; repaired label direction, clipped notes and root-sheet placement.
- Preserved 111 component identities, 96 net names and all 365 pin memberships against the pre-cleanup XML baseline; ERC remains 0.
- Moved R42 0.2 mm left to fix two clearance errors; no trace/via edits.
- Corrected U1 library keepout from absolute board coordinates to footprint-local coordinates and made footprint keepout explicitly cover all four copper layers. No pad or module placement changes.
- Native DRC: 0 errors, 0 warnings, 0 opens, 0 parity issues. No warning exclusions added.
- Refreshed schematic PDF, previews, pin map, validation records and open-issue list. Fabrication release remains blocked by engineering qualification.

## Earlier Rev B work

Added onboard BQ298217 protection, two CSD17308Q3 FETs, 10 mΩ shunt, supporting components and second cell-probe interface. GPIO1 now measures cell temperature; status LED moved to GPIO43. See current schematic/BOM and historical construction notes. Original ZIP and Rev A were preserved.

Final saved-file audit restored original model references and the board-coordinate antenna polygon after editor serialization changed them. Final checks apply to the corrected saved sources.

2026-11-06: ESP32 substrate notch filled at Nate’s request; circular perimeter restored, motor openings retained. See engineering/OUTLINE_CHANGE.md. RF qualification required with the added FR-4.

2026-11-06: Nate authorized provisional battery assumptions for PHB1S100020CJST (20C). BOM external BAT1 and editable tray updated; see engineering/BATTERY_ASSUMPTIONS.md. Cell envelope/limits are provisional. Existing 2.6 V hardware UV cutoff and charger TS window remain qualification blockers.

## Rev C — 2026-11-06

Selected Arducam M0031; remapped J3 to locking FPC24; added U8/U9 core/analog supplies, C26–C29 and R44/R45; routed camera interface; relocated J5 for access; removed obsolete header stubs; corrected camera/revision silkscreen. Retained outline, motor geometry and all other existing pin/net assignments. Final configured ERC/DRC/parity/connectivity checks are clean. No hardware or bracket fit tests.
