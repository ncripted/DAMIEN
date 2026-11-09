# Open the Omni UGV PCB in KiCad

**Updated review:** Read `engineering/AUDIT.md`, `CHANGELOG.md`, and
`validation/current/` first. This working copy contains actual electrical and
routing corrections. Current KiCad10.0.8 checks report0DRC errors,1warning,
0unconnected,0parity,0ERC. J1 has an explicit local0.19mm hole-clearance
manufacturing exception requiring fab acceptance. The status text below records
the supplied baseline and is superseded by these new reports.

This is an editable engineering prototype for Nate Sanford's three-wheel camera rover.

1. Install KiCad 9 or later from https://www.kicad.org/download/.
2. Extract the entire project ZIP into a folder. Keep `UGV.pretty`, the symbol library, and all schematic sheets together.
3. In KiCad, choose File > Open Project and select `omni_ugv.kicad_pro`.
4. Open `omni_ugv.kicad_pcb` to see and edit the routed board. Open `omni_ugv.kicad_sch` for the schematic and its five functional sheets.
5. Use the PCB Editor's View > 3D Viewer for the board view. Component models depend on your installed KiCad model libraries; the included `PCB_chassis_fit.step` is explicitly a bare-board fit model.

The project already contains the board outline, component placement, copper routing, motor solder pads, drivers, ESP32-S3, camera header, charging circuit and power controls. The bundled libraries keep its symbols and footprints available when opened on another computer.

## Check status

- All 313 schematic net-assigned pins match the PCB.
- Zero unconnected items, zero DRC errors, zero schematic parity issues.
- Schematic ERC: zero reported violations.
- Four DRC warnings remain for review: three dangling track stubs and one ESP32 footprint/library difference. The antenna-end module silkscreen was deliberately moved to the fabrication layer to avoid the board opening; review the footprint comparison before releasing it.
- There are no explicit DRC exclusions. The project's configured rules and reports are included.

This is an unbuilt prototype. The motor-terminal footprint, wheel/coupling clearance and battery mounting still require a physical fit check. Charging, temperatures, camera/Wi-Fi, firmware behavior and carpet performance have not been tested. This download does not include production-release Gerbers or finished rover firmware.

The PCB chassis is nominally 100 mm across; wheel/coupling hardware extends beyond it. Printed motor clamps, a battery cradle and a camera bracket remain separate mechanical work.

ChatGPT can revise these files and provide updated copies. This package does not establish a live connection to your desktop KiCad installation. To collaborate, open the board locally and return the edited project or relevant screenshots when you make changes.

Read `README.md` for the hardware choices, power settings, battery requirements and first-assembly checks. `BOM.csv` is the engineering component list; generic passive entries require procurement choices meeting their stated ratings.
