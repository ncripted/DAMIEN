# Nate's rover — current Rev E

1. Open **omni_ugv.kicad_pro**, then the PCB or schematic editor. The physical board preview is **preview/board-top.png**; the underside is **preview/board-bottom.png**. Custom 3D models are incomplete.
2. Read **engineering/SIX_STEP_REVIEW.md** for the six completed design-side steps and their evidence. **engineering/UNRESOLVED.md** lists the remaining fabrication/qualification gates.
3. **Schematic.pdf** has eleven pages, including the new discharge-cutoff sheet. **engineering/PIN_MAP.csv** is derived from the final native netlist. BOM.csv and design_connections.json match the current revision.
4. **validation/current** contains native reports, electrical differences, preserved-geometry proof and intermediate accepted checkpoints. Run **validate.ps1** to repeat configured native checks with the installed KiCad 10 CLI. Native zero-rule-check results do not establish component, thermal, assembly or mechanical qualification.

The board remains a nominal 100 mm solid circle except for the three motor openings. Wheels/couplings extend beyond it. No motor or mounting geometry was changed in Rev E. The camera remains the previously selected Arducam M0031 ribbon module/24-pin interface; the earlier Waveshare 18-pin design is historical.

TH1 and TH2 are separate insulated probes bonded to the actual cell. Accepted battery ratings and dimensions remain assumptions until the exact pack is documented and measured. Q13 provides an operating discharge cutoff; residual raw-cell current means it is not a storage disconnect.

**Do not order the standard assembly from this revision:** BQ298217 startup/wake compatibility and the two source-pad via manufacturing requirements need resolution first. No purchase or publication is authorized.
