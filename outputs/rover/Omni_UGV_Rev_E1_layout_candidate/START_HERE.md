# Omni rover Rev E1 layout candidate

2026-11-09 · **Manufacturing release blocked**

Open `omni_ugv.kicad_pro` in KiCad. This is the full Rev E rover with a local routing revision on PROTECTED_RAW. The board and design libraries are editable. E1 is a layout candidate, and the Rev F MAX17301 schematic is a separate circuit candidate.

## Change log

- Replaced the Q8 and Q13 source-pad vias with three off-pad through vias. Q8 has separate power and sense branches. Q13 has one short power escape. All three have 0.30 mm drills and 0.60 mm nominal copper diameter.
- Refilled the copper zones. All pre-existing tracks except the two removed vias, all pads, the four-layer stack count, the outline, motor slots and mounting holes were preserved. The added traces use F.Cu, In2.Cu and B.Cu. In1.Cu has no added signal tracks.
- Updated the Q8 and Q13 assembly notes in the local BOM. All schematic pin assignments match Rev E. The original PCB silkscreen still identifies the Rev E electrical baseline.

## Validation

KiCad 10.0.8 reported zero ERC violations, zero DRC violations, zero unconnected items and zero schematic parity issues under the existing project rules. The independent geometry check verified the new via annuli clear all SMD copper lands. `layout-proof.json` records the board hash, exact via coordinates and the drill count. The preview can omit parts whose 3D models are unavailable.

The main Q8 added escape uses approximately 3.34 mm of 0.65 mm bottom trace and 11.06 mm of 0.65 mm In2 trace. At assumed 35 µm outer and 17.5 µm inner copper, those traces alone add approximately 19 mΩ at room temperature in a simple series calculation. At 4 A this is about 0.31 W before the via barrel, temperature rise, or parallel copper effects. This is an estimate for routing tradeoffs. Validate voltage drop and temperature or shorten and widen that path before freezing the stackup.

## Release holds

1. **Battery protection.** E1 still has Rev E's startup defect with a fully charged cell. The Rev F schematic uses a dedicated wake input, but charger-driven fault recovery needs verification before integration. See `REV_F_CHARGER_INTERFACE.md` for the analysis and `PROTECTION_GATE_TEST.md` for the fixture and acceptance criteria.
2. **Fabricator and assembly.** Confirm the J1-specific 0.19 mm hole-to-copper rule, the final stackup, exposed-pad stencil and remaining thermal-via process. Lock the parts and footprint evidence before generating the order package.
3. **Prototype scope.** No physical measurements are claimed. Once the circuit is frozen, release the exact revision with Gerber and drill files, an assembly BOM and placement data if needed, and a current-limited first-power procedure. The first unit should be tested with a simulated cell before connecting a real battery or motors.

No order archive is supplied for this candidate.
