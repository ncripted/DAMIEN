# Rev F layout notes

## Changes in this checkpoint

Placed J7, C47 and U15, closing the three schematic-to-board mismatches. Routed part of the charger, protection, regulator feed and interlock wiring. Removed obsolete copper stubs, merged two overlapping same-net vias and corrected overlapping reference designators. Preserved the Rev E1 outline, motor pads, mount locations and four-layer construction. The baseline project and layout checkpoints are retained.

U15 uses a local footprint derived from the TI RPW0010A example land pattern. Signal lands are 0.60 × 0.30 mm. The IN and OUT lands are 0.30 × 2.40 mm on 0.50 mm centers. Their solder mask and separate paste apertures need assembly signoff. The KiCad proposal was used as a cross-check for the corner geometry. [TI drawing](https://www.ti.com/lit/ds/symlink/tps25947.pdf#page=73) · [KiCad footprint proposal](https://gitlab.com/kicad/libraries/kicad-footprints/-/merge_requests/4677/diffs)

## Remaining work before fabrication

1. Rework the local placement around U15 so both power lands can transition into broad copper and via arrays within a short distance. The trial input escape added approximately 5.1 mm of 0.26 mm copper before widening. It was rejected and is absent from the board. Connect the U15 ground and ILM branches and verify C42/C43 bypass loop lengths.
2. Close the charger BAT connection and the remaining VBAT and PROTECTED_RAW connections. Audit the entire cell, shunt, FET, eFuse and motor current loop for copper cross-section, voltage drop, thermal limits and via capacity. Include the charging return separately.
3. Route U7's remaining local support and sense nets. Keep the two R36 Kelvin paths independent of load-current copper. Finish the wake, thermistor and programming lines and the U16–U19 reset and clock lines. Verify the U7 land and paste pattern against ADI before assembly. [MAX17301 manufacturer page](https://www.analog.com/en/products/MAX17301.html)
4. Check antenna clearance, final ground returns, connector access from the assembled chassis, and under-board battery cradle clearance. The 3D render only represents component bodies that have models.
5. Close the hard-short detection and motor regeneration questions. The fault header is an injection point. Qualification requires confirming the response when a hard short leaves PROTECTED_RAW powered, and measuring the motor rail during braking.
6. Re-run ERC and DRC with parity after changes. Confirm zero opens and review each warning. Then generate one fabrication package for the lab prototype.

Refer to `drc.json` for the exact locations. The separate ERC check validates schematic rules and does not establish electrical or thermal performance.
