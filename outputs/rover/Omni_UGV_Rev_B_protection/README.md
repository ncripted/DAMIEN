# Miniature three-wheel camera rover — Rev B

Current state: **step 1 complete, prototype not released for fabrication**. Start with START_HERE.md.

Three independent omni-wheel drives, ESP32-S3-WROOM-1-N8R8, two DRV8833PWP drivers, BQ24074 charger and TPS63802 regulator remain the core design. Rev B adds BQ298217RUGR protection, a CSD17308Q3 common-drain FET pair, a 10 mΩ shunt and a separate cell-temperature ADC input.

## Files

- Native project: omni_ugv.kicad_pro, root and six child .kicad_sch sheets, omni_ugv.kicad_pcb, local symbol/footprint libraries.
- Schematic.pdf and preview/schematics: current readable review drawing and detail images.
- BOM.csv / design_connections.json / engineering/PIN_MAP.csv: current parts, metadata and exported physical pin connections.
- validation/current and validation_summary.json: current checks; STEP1_SHA256.json identifies the checked native files.
- engineering/STEP_1_REVIEW.md: exact changes and verification limits.
- engineering/UNRESOLVED.md: next engineering gates.
- mechanics and mechanical.json: provisional fitting work; no physical-fit certification.
- engineering/history: prior notes retained for traceability; superseded where Rev B differs.

## Cell and temperature interface

J2 pin1 CELL_P, pin2 CELL_N feed onboard protection. Protected VBAT supplies the charger BAT connection and motor-power switching. Motor current does not pass through charger OUT/SYS_RAW. R36 is the intended raw-negative to system-ground connection.

J4 and J5 each use an independent electrically insulated two-wire 103AT-2 probe bonded to the cell. J4 serves charger TS. J5 feeds GPIO1/ADC1 through R42/R43/C25. GPIO43 now drives the status LED; native USB programming remains available.

No selected cell, connector/harness qualification, thermal test, braking test, built firmware or Vita video demonstration is implied by the current rule-check results.

## Repeatability

Run validate.ps1 for configured checks. engineering/scripts/README.md explains the presentation generator and reload limitations. Edits are saved files, not a live IPC session. Avoid saving a stale editor over externally modified files.
