# Omni rover — Rev B, step 1 complete

Open **omni_ugv.kicad_pro** in KiCad 10.0.8. This directory is the current working revision; the original ZIP and Rev A remain preserved.

The seven-page **Schematic.pdf** is the current review drawing. Native schematics now group functions and show local wiring. The XML comparison preserves 111 component identities, 96 named nets and 365 pin memberships.

On 2026-11-05: ERC 0, DRC errors 0, DRC warnings 0, unconnected items 0, schematic-parity issues 0. See validation_summary.json and validation/current. These results apply to configured checks and the recorded snapshot, not physical qualification.

Read engineering/STEP_1_REVIEW.md for changes, engineering/PIN_MAP.md for GPIOs, and engineering/UNRESOLVED.md before fabrication. The board remains an unbuilt engineering prototype. No fabrication release or order is authorized.

Rev B includes onboard cell protection and two separate off-board cell-temperature probes. J2 is raw cell input; J4 is the charger probe; J5 is the drive-monitor probe. Both probe heads must contact the actual cell through electrical insulation. Drive temperature shutdown still needs firmware.

Current previews: preview/protection-top.png, preview/protection-bottom.png and preview/schematics. Missing custom-package 3D bodies mean renders are not assembly-clearance proof. Mechanics remain provisional.

2026-11-06: Nate authorized provisional battery assumptions for PHB1S100020CJST (20C). BOM external BAT1 and editable tray updated; see engineering/BATTERY_ASSUMPTIONS.md. Cell envelope/limits are provisional. Existing 2.6 V hardware UV cutoff and charger TS window remain qualification blockers.
