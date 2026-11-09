# Omni rover Rev F layout checkpoint

**Open `omni_ugv.kicad_pro` in KiCad. Fabrication is on hold while routing is open.**

This is the full rover project for a single lab prototype. Rev F integrates the MAX17301, charge isolation, eFuse and hardware rearm into the existing hierarchy. It retains the round board with three motor cutouts, the E1 mechanical mounting locations and the ribbon-camera connector. The E1 project remains in its original directory.

## Layout changes

- All 33 Rev F footprints are placed. J7 is on the underside toward the left on the front view. It accepts the external cell-mounted thermistor for the protector. TH1 and TH2 retain charger inhibit and firmware measurement functions.
- U15 uses the project-local TI RPW0010A footprint. Its two inner lands carry the eFuse input and output. The four corner pads use the extended geometry in the TI drawing. The stencil geometry is provisional and needs assembler review.
- The new route work uses F.Cu, B.Cu and In2.Cu. In1.Cu remains free of signal traces. Silkscreen was adjusted for readability and copper clearance.
- U5 BAT and OUT have separate nets CHG_BAT and CHG_OUT. D10 feeds charge toward PROTECTED_RAW. D11 and D12 join the USB and battery logic feeds at SYS_RAW. U15 feeds the original motor power path through VBAT. The USB data connection and separate motor interlock remain.
- U16–U19 implement USB and brownout disarm and a fresh press to rearm. J8 exposes the open-drain fault input.

## Files

- `drc.json` lists every open endpoint pair and board warning. `layout_validation.json` summarizes the latest checks.
- `erc.json`, `BOM.csv` and `pin_map.csv` are generated from the current schematic.
- `board-top.png` and `board-bottom.png` are placement previews. Several component bodies are missing 3D models, including the custom eFuse and J7. The renders do not establish assembly clearance.
- `LAYOUT_NOTES.md` records remaining layout and release work.

## Single-board lab sequence after release

Begin with a current-limited, source/sink cell simulator, with the LiPo and motors disconnected. Program the MAX17301 over J6. Verify cold startup, USB transitions, charge and drive current paths, fault behavior and rearm. Use differential probing across the cell-side and system-side returns to avoid bypassing R36. Test ESP32 programming, 3.3 V startup, camera streaming and the motor interlock. Add dummy loads before installing the motors. Use the real cell after the lab checks verify charging and protection.
