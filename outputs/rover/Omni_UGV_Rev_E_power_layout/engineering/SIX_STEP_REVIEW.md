# Rev E — six-step electrical and PCB revision

2026-11-07. Native KiCad 10.0.8 sources are authoritative. The six design-side steps have been implemented and checked in order. Fabrication remains **BLOCKED** by the issues below. No physical hardware tests were performed.

## 1. Restore the primary ground reference

Removed the inherited M2_A route from In1.Cu and rerouted the motor connections on F.Cu, B.Cu and In2.Cu. The final saved board has **zero non-ground track segments on In1.Cu**. Its ground zone was refilled and saved. This removes a local interruption in the reference plane; it does not eliminate the antipads around signal vias.

## 2. Improve current paths

Rerouted all six motor outputs. Main M1/M2 routes use 0.6 mm copper, with short narrower driver escapes. M3 routes use 0.4 mm on the outside layers where larger routes could not be placed cleanly. Motor suppression-capacitor branches are narrower than the main motor routes. Added two parallel vias at each of two motor-power transitions. Existing VBAT via-bank copper remains.

The final board retains **363 widened existing segments** relative to Rev D, in addition to replacement routes. Wide battery/motor trunks were increased toward 1.5 mm where clearance allowed. The new protected-output path has clearance-limited widths; the inventory records the actual widths instead of assigning one width to the entire rail. Driver sense-current traces were also widened where possible. See power-layout-inventory.json and validation/current.

For scale, 10 mm of 0.8 mm wide, 35 µm copper is about 6.16 mΩ at room temperature: 24.6 mV and 98.5 mW at 4 A. A 1.5 mm route is about 3.28 mΩ per 10 mm. These are conductor calculations, **not ampacity ratings**. Actual copper thickness, temperature, serial necks, via plating and current sharing still require qualification.

**Assembly exception:** Q8 source pad 1 and Q13 source pad 1 intersect 0.6/0.3 mm through-vias. Standard unfilled open vias are not an approved assembly process here. SOURCE_PAD_VIAS.csv gives their exact coordinates and UUIDs. Require filled, copper-capped processing with the assembler's acceptance, or move these vias in a subsequent layout revision. This requirement is explicit; no DRC rule was weakened to conceal it. Other thermal-pad via arrays also need a reviewed stencil/tenting/voiding process.

## 3. Make the primary protection shunt genuinely Kelvin

Replaced the two-terminal WSL2512 10 mΩ resistor with **Vishay WSK2512R0100FEA**, a four-terminal 10 mΩ, 1%, 1 W part. The manufacturer drawing, rather than the original footprint name, defines the new land pattern. The local footprint corrects the voltage-contact width to 1.70 mm for this resistance range. The package has no manufacturer terminal numbers; the project explicitly assigns them:

| Project pad | Connection | Purpose |
|---|---|---|
| 1 | CELL_N | Current terminal |
| 2 | GND | Current terminal |
| 3 | PROT_VSS_SENSE | Cell-side voltage contact: U7 VSS and C24 return only |
| 4 | PROT_CS_SENSE | Ground-side voltage contact: U7 CS only |

U7/C24 were repositioned to accommodate the new footprint and independent sensing. The native netlist verifies those memberships. No motor current is intentionally routed through either voltage-contact trace. The motor drivers' 0.25 Ω current-setting resistors remain two-terminal parts; they are not being described as four-terminal Kelvin shunts.

The nominal primary-protector thresholds remain 6 A discharge overcurrent, 3.6 A charge overcurrent and 20 A short detection. Including the IC threshold limits and 1% resistance tolerance gives approximately 5.45–6.57 A, 3.27–3.94 A and 18.6–21.4 A respectively. Temperature coefficient, self-heating, detection delays and current overshoot must be included in physical fault testing. At 5 A the shunt dissipates 0.25 W; a 1 W label does not establish its temperature on this PCB.

## 4. Improve regulator locality and decoupling

Moved L1 1.25 mm closer to U4. Each F.Cu switching connection shortened from **4.706 mm to 3.456 mm**, about 26.6%. The switching nodes remain on the outside layer. Their short narrow pin escapes preserve clearance at the IC. Added a ground-return via at each of C18, C19 and C20, and rebuilt the enable routing around the tighter power placement.

C18 increased from nominal 10 µF to 22 µF. C18/C19/C20 now specify **TDK C2012X5R1A226M125AB**, 22 µF, 10 V, ±20%, X5R, 0805. TDK lists this M-tolerance part as Production; the K-tolerance variant is NRND. The selected part's guaranteed effective capacitance under bias, temperature and aging has **not** been established. Do not substitute nominal capacitance for the TPS63802 effective-capacitance requirements.

Reviewed the ground plane, regulator return vias, driver exposed-pad returns and the common-drain copper/via regions of Q7/Q8. The native views expose these paths for review; no thermal qualification or junction-temperature measurement is claimed. Several custom component bodies are absent from the 3D preview, so that preview cannot establish complete assembly clearance.

## 5. Add an independent operating discharge cutoff

The existing U10 supervisor previously disabled the main regulator and driving, while U7 retained a factory 2.6 V undervoltage threshold. Rev E adds Q12, Q13 and R65–R67 to interrupt the protected output independently of firmware:

`CELL_P → Q7/Q8 → PROTECTED_RAW → Q13 → VBAT → loads`

U10's active-low reset turns on PNP Q12 at undervoltage. Q12 raises the P-channel Q13 gate toward the raw cell voltage, turning off discharge. R46 now pulls reset up to raw CELL_P so this function survives loss of protected VBAT. Q13 is **DMP2008UFG-7**, with source contacts on PROTECTED_RAW and the merged drain contact on VBAT. The switch is downstream of Q7/Q8 so their gate-source reference is retained. Placing the cutoff ahead of Q7 would expose its gate to excessive voltage while its source was disconnected.

The 3.1 V supervisor's static falling window is **3.0535–3.1465 V**. Calculated recovery is 3.2285–3.3715 V, with approximately 62 ms nominal release delay from the existing capacitor. This is an operating cutoff, not a guarantee that a rapid cell dip can never cross 3.0 V.

Q13's body diode permits current from VBAT toward PROTECTED_RAW for recovery charging while discharge is off. Normal charging still passes through BQ24074 and the primary protection FETs. Its roughly 250 mA programmed charging current is separate from the motor-current path. TH1 still measures the **cell**, using the independent analog charging-temperature window. TH2 remains a separate cell-mounted ADC probe. USB motor-disable circuitry and default-low drive request are retained.

Q13's 25 °C maximum specified resistance at −2.5 V gate drive is 9.8 mΩ: about 0.157 W at 4 A or 0.245 W at 5 A. A simple 2× hot-resistance scenario doubles those losses; it is not a thermal simulation. Gate-off leakage, body-diode recovery charging and temperature require measurements. The raw supervisor, protector and cutoff bias still consume current after trip; a rough 0.15 mA budget is about 3.6 mAh/day. There is no indefinite-storage guarantee above 3.0 V.

**New release blocker:** U7's documented power-on state assumes undervoltage. With UV_SHUT enabled, entering normal operation requires charger detection. Its typical PACK-minus-BAT charger threshold is 700 mV. A 4.2 V charger output cannot supply that margin over an already full 4.2 V cell. The added cutoff avoids intentionally invoking U7 CTR shutdown, but does not resolve this inherited cold-start/wake issue. Verify the complete startup state machine on a cell simulator and revise the protector/wake architecture if necessary. Do not short the protection FETs or apply an unregulated activation voltage to the cell.

## 6. Regenerate evidence and views

Final configured results: **ERC 0; DRC errors 0; DRC warnings 0; unconnected items 0; schematic parity issues 0.** Native DRC refilled and saved zones. Re-exported the eleven-page schematic, native-netlist pin map, top/bottom 3D previews, every copper-layer SVG/PDF and bare-board STEP.

Verified the original ZIP and every preserved Rev D file against the starting hashes. The 100 mm outline, motor/mounting geometry and all-layer antenna keepout are unchanged. Board design settings and custom rules are unchanged. The inherited J1-specific 0.19 mm hole-clearance exception still requires fabricator acceptance. Configured ignored checks are disclosed in validation_summary.json; zero results do not mean every possible KiCad check was enabled.

The new overview page separates the functional sheets without overlapping boxes. The changed protection, undervoltage and cutoff drawings and the native board views were visually inspected. This is not a manufacturing release: no Gerber order, purchase, publication, thermal test, fault-injection test or physical fit test was performed. There is no live KiCad editor IPC connection.

See UNRESOLVED.md for the remaining gates, POWER_CALCULATIONS.json for assumptions and arithmetic, PIN_MAP.csv for physical pins, and SOURCES.md for primary documentation.
