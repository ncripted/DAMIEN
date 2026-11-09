# Miniature omni camera rover — Rev D

Rev D implements the design-side power-audit corrections in native KiCad sources: independent 3.1 V operating-load shutdown, independent USB-powered charging-temperature monitoring of the actual cell, buffered default-low drive request, and lower-loss motor-power FETs. The 100 mm nominal solid perimeter, three motor openings, camera connector, motor pads and mounting geometry are retained. New monitoring circuitry uses the left sector.

Start with START_HERE.md and engineering/POWER_AUDIT.md. engineering/POWER_CALCULATIONS.json contains repeatable estimates; engineering/PIN_MAP.csv is derived from the final native netlist. validation/current holds configured checks and explicit electrical/copper deltas. The original ZIP and Rev C project remain preserved.

All configured checks pass only as recorded in validation_summary.json. Physical function, heating, cell/harness ratings, emergency UV compatibility, regen/braking, shunt sensing, effective capacitors, mechanical fit, RF and firmware/Vita qualification remain open. Read engineering/UNRESOLVED.md before any manufacturing work. There is no live editor IPC link and no manufacturing order has been made.
