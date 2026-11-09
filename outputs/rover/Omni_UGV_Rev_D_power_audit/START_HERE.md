# Omni rover — Rev D power audit

Open **omni_ugv.kicad_pro** in KiCad 10.0.8, then the PCB Editor or 3D Viewer (Alt+3). Rev C is preserved in its separate project directory. There is no live editor IPC connection: close/reload an older open revision before editing.

Read **engineering/POWER_AUDIT.md** for implemented power changes, calculations, assumptions and pending qualification. Native editable files are authoritative. The ten-page Schematic.pdf, BOM.csv, design_connections.json, engineering/PIN_MAP.csv and validation/current apply to Rev D. Check validation_summary.json for the recorded final native results.

Rev D adds independent low-cell load shutdown, an analog cell-temperature charging window, a drive-request buffer, and lower-loss motor-switch FETs. New monitoring parts occupy the left sector. Both TH1/J4 and TH2/J5 are independent insulated probes attached to the actual cell. TH1 now feeds the external analog window; U5 TS uses a fixed 10k bias. GPIO2/pad38 is the drive-temperature ADC and GPIO1/pad39 the battery ADC.

Camera J3 remains the Arducam M0031 24-pin DVP flex interface with Hirose FH12-24S-0.5SH(55), incompatible with the old Waveshare 18-pin carrier. Camera fit, sequencing and operation remain unqualified.

Current views: preview/rev-d-top.png, preview/rev-d-bottom.png and preview/schematics. mechanics/Rev_D_board_only.step contains the bare board, not a complete fitted assembly. Historical STEP/renders are marked under history. Custom protection-package bodies, camera, motors, wheels and battery are not fully represented in 3D.

This is an unbuilt engineering prototype, not a fabrication release. No physical power, fault, thermal, motor, battery, camera, RF or carpet tests have been performed. U7's 2.6 V emergency cutoff still needs compatibility resolution against the assumed cell minimum; U10 removes operating loads earlier but is not a zero-leakage storage disconnect. See engineering/UNRESOLVED.md. Do not run historical generation scripts over the current native sources.
