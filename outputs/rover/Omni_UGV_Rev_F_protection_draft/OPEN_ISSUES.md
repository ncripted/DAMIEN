# Rev F protection draft

Open `rev_f_protection.kicad_pro` in KiCad and select Schematic Editor. This standalone project is an integration candidate for the rover. The existing Rev E project is the baseline. The preview and native KiCad netlist are generated from this draft.

USB charging and programming are both required. See `USB_CHARGE_AND_DRIVE_ISOLATION.md` for the proposed charger and discharge branch separation and its remaining circuit gates.

The first implementation is the separate `rev_f_usb_power_path.kicad_pro` fixture. See `USB_POWER_PATH_FIXTURE.md` for what its OVLO inhibit covers and where independent fault memory still needs qualification.

## Changes from Rev E

- Replaced the BQ298217 topology in the draft with a MAX17301G+T, using the manufacturer's TDFN pinout, BATT filter, charge-pump bypass and regulator bypass.
- Added a dedicated momentary wake input. PCKP stays on the physical PROTECTED_RAW node so the wake switch does not impersonate an unplugged load.
- Kept the high-side charge/discharge FET arrangement and a four-terminal low-side shunt. CSP uses the battery-side Kelvin pad. CSN uses the pack-side Kelvin pad.
- Added fixture-only I²C and an independent 103AT-2 cell-pouch sensor interface. Retain the two existing Rev E cell-probe functions on their own circuits when integrating. J2 marks a logical boundary to the downstream schematic.

## Release gates

1. **Startup and USB recovery.** Verify cold start on a programmed device with simulated 4.20 V and 3.10 V cells and USB disconnected. Check recharge recovery after undervoltage, and repeat short-recovery tests with USB absent, attached and being inserted. Include a held wake button. Observe PCKP, VBAT, FET gate-to-source voltages and the USB drive inhibit. Ship/DeepShip pushbutton support by itself does not establish cold-start behavior.
2. **Physical integration.** Merge J1 and J2 boundaries with Rev E's cell connector, Q13, charger and system ground. Preserve a single high-current return through the shunt and check that charger presence cannot bias PCKP high during a real short. Confirm the local CELL_N versus PACK_GND reference strategy for wake, the sensor, and the programming fixture.
3. **Ratings and layout.** Qualify the final MAX17301 footprint against ADI land pattern 90-0063 and check FET resistance at the worst expected gate drive. Check inrush, shunt pulse energy, FET safe operating area, fault current and selected cell ratings. Resolve PFAIL and the secondary protection policy before release. Unassigned footprints in the draft identify unresolved placement work.
4. **Production programming.** Finalize the profile, validate it in shadow RAM, qualify the programmed unit over supply and temperature, and document the programming and readback fixture. The worksheet is preliminary and has no flashable image.

[Analog Devices datasheet and application schematic](https://www.analog.com/media/en/technical-documentation/data-sheets/max17300-max17313.pdf)
