# Miniature omni camera rover — Rev C

Rev C replaces the large camera header with a 24-pin locking FPC interface for Arducam M0031. The camera connector and local supplies use the upper-right sector; power-converter and motor-driver groups retain locality. The solid 100 mm nominal perimeter and three motor openings are retained.

Read START_HERE.md, engineering/CAMERA_REV_C.md, engineering/BATTERY_ASSUMPTIONS.md, engineering/PIN_MAP.md and engineering/UNRESOLVED.md. Native KiCad sources are authoritative. Reversible edits used native text/API operations and KiCad CLI validation; there is no live editor IPC connection. Reload external edits in the editor rather than overwriting them from an older in-memory board.

Reports refer to configured checks and are not proof of electrical, thermal, RF or mechanical operation. Rev B construction/presentation scripts are historical and must not be run over Rev C. A prototype qualification pass and measured camera bracket are still required.
