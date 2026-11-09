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
