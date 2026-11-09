# Provisional supports

`provisional_supports.scad` is editable parametric OpenSCAD source. It has not been rendered or collision checked in OpenSCAD on this host; OpenSCAD and a STEP-capable mechanical CAD kernel were not found. No new STL or STEP exports are represented as print-ready. The supplied `PCB_chassis_fit.step` remains a bare-board model of the original board; it predates the 2026-11-06 solid-perimeter change and is not the current outline.

Motor clamps use the actual 20 mm tangential hole spacing at radius 34 mm. The 9 mm axial width leaves access to the terminal region at radius 22 mm. Confirm clamp contact on the motor can rather than a fragile end cap, avoid brush vent obstruction, and provide axial retention against a gearbox shoulder. The current saddle study has no verified shoulder stop. M2 metal through-bolts, washers and nuts carry the clamp load; do not screw into FR-4 or rely on solder joints.

Motor roll, shaft-center height relative to PCB and bent terminal geometry are unresolved. The supplied footprint has slots through the PCB in the Z direction; the motor terminals extend axially. A bend or a verified right-angle terminal interface is necessary. Do not assume the native planar footprint proves direct insertion is possible. Measure terminal thickness, width, free length, root height and allowable bend location first.

Battery pack dimensions are provisionally 62 × 34 × 6 mm for PHB1S100020CJST. These dimensions are assumed from the separate 30C product, not verified for the selected 20C pack. The editable tray now has a 64 × 36 mm interior, with 1 mm per side clearance and a 2 mm top allowance parameter. This is a floating fit study, not a chassis attachment design. See ../engineering/BATTERY_ASSUMPTIONS.md. Add a smooth insulating liner, strain relief, cell-mounted NTC, swelling allowance and access to straps. Attachment feet must be designed after locating the actual pack around component bodies and clamp screws.

Camera board size, lens diameter and mounting holes in the source are conspicuously provisional placeholders. Verify header/cable handedness and lens center before finalizing. Check the field of view using the actual lens: at obstruction distance d, the opening half-width must exceed d*tan(horizontal_FOV/2), plus lens offset and tolerance. Keep bracket and battery away from the ESP32 antenna.

Rev C uses the Arducam M0031 flex camera. The universal 32 mm carrier-board bracket in provisional_supports.scad is a historical placeholder, not a verified mount for M0031. Measure the actual head/lens/flex before designing its retaining pocket and strain relief.

Current Rev C bare-board mechanical exchange file: Rev_C_board_only.step, exported by KiCad from the final saved board. This includes board outline and holes; it excludes components, camera/flex, supports and assembly clearance envelopes.
