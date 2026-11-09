# Step 1 review — 2026-11-05

Completed the authorized schematic organization and known rule-check cleanup in actual KiCad sources.

## Changes

1. Reorganized all seven pages: root overview, controller/camera/service points, regulator, motor channels, interlock/measurement, USB/charger, and protection/cell probes. Added native orthogonal wiring for reset/boot, decoupling, USB data, charger configuration, feedback, driver support, transistor controls and temperature divider. Global labels remain for cross-sheet and long connections. Moved the overlapping root sheet and previously off-page power flags into the drawing.
2. Made Q7/Q8 pin-explicit symbols show source and drain groups on opposite sides and the common-drain connection visibly. Hidden stacked pins remain in the XML pin map. Updated the bundled symbol to match. No physical pin assignment or component value changed during presentation cleanup.
3. Moved R42 on B.Cu from (125.5,88.0) to (125.3,88.0) mm. This removed two 0.0953 mm clearances to CELL_TEMP_ADC while preserving the 0.15 mm rule. Existing copper still terminates inside the pads. No trace/via routing was changed in step 1.
4. Investigated U1 using KiCad's native Compare Footprint with Library dialog. Its exact finding was that rule-area corners differed. The library polygon had board coordinates (87..135,40.25..61.25), rather than coordinates local to U1 at (111,68). Corrected the library polygon to (-24..24,-27.75..-6.75). The board's X/Y keepout extent did not move. Explicitly included F.Cu, In1.Cu, In2.Cu and B.Cu in the footprint keepout and recorded its four-layer stackup. Pads, pad numbers and module placement did not move. The mismatch warning now clears without an exclusion or severity change.

## Checks actually performed

KiCad 10.0.8 native ERC: 0 violations. Native DRC with zone refill and schematic parity: 0 errors, 0 warnings, 0 unconnected items, 0 parity issues. Native XML connectivity compared with the pre-cleanup snapshot: exact match of 111 component identities, 96 named nets and 365 pin memberships.

Rendered all seven pages and inspected full sheets plus detailed controller, regulator, driver, interlock, USB/charger and protection crops. Corrected label orientation/justification, title-block clipping, text crossing power leads and ambiguous collinear wire paths. The generator separately rejects different net labels sharing a continuous wire graph.

Schematic edits and board fixes were separate stages. See validation/current/board-change-proof.json for allowed board differences and STEP1_SHA256.json for native-file hashes. No geometry change to the original 100 mm outline or motor terminals was made.

The native KiCad editor was opened on this Rev B project to inspect the footprint warning. There is no live IPC connection: external file edits require reload.

## Limits

These are configured checks; the inherited ignored categories remain visible in the JSON report. No new checks were disabled. The inherited J1-only 0.19 mm hole-clearance rule still needs fabricator acceptance. A clean footprint-library comparison does not establish agreement with the module manufacturer's land pattern. Current thermal, power-transient, sourcing, mechanical and firmware qualification is still pending.

KiCad documents the native comparison workflow in its [PCB Editor manual](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html). This review used the installed editor's comparison result and native files, not an assumption that exporting a footprint makes it equivalent.

Final saved-file audit restored original model references and the board-coordinate antenna polygon after editor serialization changed them. Final checks apply to the corrected saved sources.
