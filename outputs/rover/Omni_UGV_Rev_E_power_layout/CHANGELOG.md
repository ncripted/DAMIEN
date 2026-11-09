# Change log

## Rev E — 2026-11-07

- Preserved the original archive and Rev D; created a separate native revision.
- Removed the local M2_A track from In1.Cu; rerouted all six motor outputs and improved current-path widths/vias. The final board retains 363 widened existing segments plus replacement routes.
- Replaced R36 with a four-terminal WSK2512R0100FEA and manufacturer-derived land pattern. Added independent U7 CS/VSS sense nets; relocated U7/C24 and rerouted the raw-cell return.
- Moved L1 closer to U4, reducing each switch connection from 4.706 to 3.456 mm. Added three capacitor-return vias and specified C18/C19/C20 as 22 µF TDK production parts.
- Added Q12/Q13/R65–R67 as a discharge-only switch downstream of the primary protection pair. Changed R46 to a raw-cell reset pullup. Preserved USB motor disable and both cell-mounted probes.
- Documented primary-protector startup compatibility and source-pad via fill/capping as explicit fabrication blockers.
- Reflowed the schematic overview; refreshed native PDF, BOM, placement metadata, physical pin map, copper layers, board previews, bare-board STEP and checks. Final configured ERC/DRC/unconnected/parity counts are zero.

Earlier revision records are preserved under .history/rev-d-import/CHANGELOG.md. Physical qualification, firmware/Vita and final mechanical fit remain open.
