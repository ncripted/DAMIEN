# Provisional supports

`provisional_supports.scad` is editable parametric OpenSCAD source. It has not been rendered or collision checked in OpenSCAD on this host; OpenSCAD and a STEP-capable mechanical CAD kernel were not found. No new STL or STEP exports are represented as print-ready. The supplied `PCB_chassis_fit.step` remains a bare-board model of the original board; the outline has not changed.

Motor clamps use the actual 20 mm tangential hole spacing at radius 34 mm. The 9 mm axial width leaves access to the terminal region at radius 22 mm. Confirm clamp contact on the motor can rather than a fragile end cap, avoid brush vent obstruction, and provide axial retention against a gearbox shoulder. The current saddle study has no verified shoulder stop. M2 metal through-bolts, washers and nuts carry the clamp load; do not screw into FR-4 or rely on solder joints.

Motor roll, shaft-center height relative to PCB and bent terminal geometry are unresolved. The supplied footprint has slots through the PCB in the Z direction; the motor terminals extend axially. A bend or a verified right-angle terminal interface is necessary. Do not assume the native planar footprint proves direct insertion is possible. Measure terminal thickness, width, free length, root height and allowable bend location first.

Battery tray dimensions 55 × 35 × 10 mm are inherited assumptions, not a selected pack. Add a smooth insulating liner, strain relief, cell-mounted NTC, swelling allowance and access to straps. Attachment feet must be designed after locating the actual pack around component bodies and clamp screws.

Camera board size, lens diameter and mounting holes in the source are conspicuously provisional placeholders. Verify header/cable handedness and lens center before finalizing. Check the field of view using the actual lens: at obstruction distance d, the opening half-width must exceed d*tan(horizontal_FOV/2), plus lens offset and tolerance. Keep bracket and battery away from the ESP32 antenna.
