# Engineering audit — 3 November 2026

Status: unbuilt prototype, first corrective pass. Not a fabrication release.

The supplied native board/schematics determine the implementation. Attached prose was read as design history and factual claims, not as instructions overriding Nate's request. The original ZIP is preserved separately and unchanged. The working project is under `outputs/rover/Omni_UGV_Rev_A`.

## Actual editing and validation workflow

Installed KiCad: 10.0.8, versus 9.0.9 in supplied reports. `kicad-cli.exe` and the bundled Python 3.11 `pcbnew` API work. The native schematics and board can also be edited as S-expressions, then parsed and checked with KiCad. Changes in this pass used native file edits and the installed API for inventory and previews. No live IPC/editor connection has been established. Desktop PCB Editor was opened and the rover board was observed. Do not assume its in-memory document automatically reloads external file edits. Its starred title may include conversion/unsaved edits; do not overwrite or discard those casually.

CLI validation uses workspace-local `KICAD_DOCUMENTS_HOME` and `KICAD_CONFIG_HOME`. KiCad prints denied HKCU registry-setting messages in the sandbox, but produces valid reports and exports. Only installed 10.0.8 was reproduced; 9.0.9 results were not independently rerun. No external PCB editor plugin or running IPC server has been verified. OpenSCAD/FreeCAD and a C/C++ embedded toolchain were not found on PATH; parametric support sources are provisional, not validated prints.

Baseline: ERC 0 violations; DRC 4 errors, 4 warnings; 0 unconnected items; 0 schematic parity issues. The 4 additional errors are J1 contact-land to alignment-bore clearance, 0.1944 mm against the project's 0.25 mm global minimum. They are new findings with KiCad 10, not proof the older report was fraudulent. Reports list ignored rule categories; a zero count applies to configured checks, not every imaginable check.

## Changes actually implemented

1. R25: 10k to 100k; R27: 10k to 1k; R29: 47k to 10k. Updated interlock schematic, board values, BOM and design_connections.json. This reduces Q3 base loading and preserves Q4 USB override drive.
2. Removed dangling copper branches, iterating DRC and checking connectivity/parity after removal. Three warning markers represented chains of small segments, not only three isolated segments. UUID changes are recorded separately.
3. Replaced the REG_L1 and REG_L2 tracks/vias with six 0.4 mm front-copper segments. Each route is approximately 4.71 mm. The former REG_L1 network had 11.46 mm of copper and two vias; part was a redundant branch. Neither switch node now changes layers. The improvement does not establish complete converter layout approval: C18/C19/C20 proximity and current returns still need work.
4. Added an explicit J1-only hole_clearance rule of 0.19 mm, retaining the GCT drawing's alignment holes and land pattern. All other holes retain the 0.25 mm rule. This is a documented fabrication capability exception requiring fab acceptance; it is not an exclusion or a general relaxation. Do not shrink locator holes to make DRC green.
5. Exported U1's current board footprint to the bundled library while investigating its mismatch. The warning persists; no rule was disabled and the difference is not signed off. Resolve the normalized footprint comparison before release.
6. Added pin-map/inventory reports, provisional editable OpenSCAD supports and a mechanical review. No board outline or motor terminal geometry was changed.

## Motor-enable calculation

DRV8833 nSLEEP requires VIH >=2.5 V and VIL <=0.5 V. It is not the same 2.0 V threshold as the motor input pins. Its input current can be 13 uA per driver at 3.3 V. [TI DRV8833, electrical characteristics](https://www.ti.com/lit/ds/symlink/drv8833.pdf).

Using Q3 VBE=0.7 V, two nominal 500k sleep pulldowns, R28=100k, and a 3.3 V GPIO:

`(Vgpio - Ven)/R27 = Ven/R28 + (Ven - VBE)/R25 + 2*Ven/500k`.

Old values give Ven approximately 1.87 V. New values give approximately 3.23 V. At GPIO=2.64 V, R27=1.01k, R25=99k, R28=99k, VBE=0.55 V, and 26 uA total driver input current, Ven is approximately 2.57 V. This is a DC corner estimate, not a SPICE/transient or hardware test. It does not guarantee wake-up if the 3.3 V rail droops to 3.0 V; brownout behavior remains a bring-up requirement.

With USB present, Q4 must sink about 3.3 mA through R27. At USB=4.35 V and VBE=0.95 V, R29=10k and R30=100k provide approximately 0.33 mA base current, approximately forced beta 10. Q3 only needs to sink the 100k motor-gate pullup and gate charge. [Diodes MMBT3904](https://www.diodes.com/datasheet/download/MMBT3904.pdf). Choose a concrete transistor vendor/MPN and verify saturation over temperature; do not treat generic MMBT3904 as procurement-complete.

USB Q4 clamps the same signal that wakes both drivers and pulls down the motor PFET gates via Q3. On reset, R28 and R26 default that signal low. This is a USB-presence inhibit, not a mechanical emergency brake, independent watchdog or guaranteed instantaneous rail discharge. Test USB insertion at full PWM, reset, bootloader, dead battery and logic power off. Ensure retained motor input GPIO states cannot back-power an unpowered driver.

## Pin/package audit

The generated PIN_MAP.csv derives physical pins, signal names and functions from the fresh KiCad-exported native schematic netlist, with board pad comparison. There are 302 functional net-assigned pins and 11 explicitly unconnected pins in the 313-pin total used by the old report. No functional net mismatch was found. Duplicate package ground/paste pads are not counted as extra functional pins.

U1 is ESP32-S3-WROOM-1-N8R8. Physical pins 28/29/30 (GPIO35/36/37) are unconnected, correctly reserving them for octal PSRAM. GPIO0 has BOOT pullup/switch; EN has 10k/1u RC and RESET switch. GPIO19/20 are native USB D-/D+. GPIO3,45,46 are unconnected strap pins. GPIO44 is charger EN1, not an available UART RX signal. [Espressif module datasheet, pin table/PSRAM footnote](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf).

U2/U3 physical pin assignments match the DRV8833 **PWP HTSSOP**, not the QFN pin order. Pin17 is grounded PowerPAD. VCP capacitors are 10n to VM, VINT capacitors 2.2u to GND, VM bypass 10u to GND. These match nominal support values; effective capacitance and placement are separate checks. U3's unused B bridge has inputs grounded, BISEN grounded, and outputs no-connected. Pullups on individual active-low faults permit independent fault handling.

TPS63802 **DLA** pin order matches: EN1/MODE2/AGND3/FB4/PG5/VOUT6/L2-7/GND8/L1-9/VIN10. The custom 10-pad asymmetric footprint has no invented central thermal pad. Its exact land dimensions and inductor land overlap still require a drawing-overlay review. BQ24074 **RGT** has TS1, BAT2/3, CE4 low, EN2-5 low, EN1-6 GPIO44, PGOOD7, VSS8, CHG9, OUT10/11, ILIM12, IN13, TMR14, ITERM15 NC, ISET16, exposed pad17 ground. Leaving ITERM open intentionally selects the internal termination setting. The USBLC6-2SC6 and connector pin tables still require their own exact package drawing overlay.

J3's 18-pin interface is 3V3, GND, SCL, SDA, VSYNC, HREF, PCLK, XCLK, D7..D0, RESET, PWDN. Here D7..D0 correspond to sensor Y9..Y2, not Y7..Y0. RESET has pullup R4; PWDN is tied low. The Waveshare board supplies sensor regulators and SCCB pullups. Cable pin-1 orientation and male/female mirroring must be verified. [Waveshare schematic](https://files.waveshare.com/upload/9/99/OV2640-Camera-Board-Schematic.pdf).

## Power system review

The motor-current path is J2/VBAT -> Q1/Q2 -> VMOTOR -> drivers/motors -> battery GND. It does **not** pass through the charger OUT power-path transistor. Logic power is BQ24074 OUT/SYS_RAW -> TPS63802 -> 3V3; on battery the charger BAT-to-OUT path still carries logic current. Charging-current settings do not limit motor current.

R14=3.57k gives nominal 890/3570=249 mA charge current. R16=46.4k gives nominal fast-charge timer 10*48*46.4=22272 s, or 6.19 h; real tolerance and DPPM timer behavior matter. EN2 is grounded, so EN1 low/high selects USB100/USB500; the 3.24k ILIM resistor does not override those selected modes. Keep GPIO44 low until a valid USB power policy permits USB500. USB100 is insufficient for many Wi-Fi/camera loads: the battery may supplement, so a depleted/absent battery can prevent startup. R14 must be revisited for the selected cell's specified maximum charge current. [TI BQ24074](https://www.ti.com/lit/ds/symlink/bq24074.pdf).

The external 10k 103AT-2 NTC is required. TS nominal 75 uA gives hot/cold resistance thresholds near 4k/28k from 0.3/2.1 V. These are not exact temperatures without the thermistor curve and tolerances. The linked batteries provide no confirmed cell-mounted NTC. Test open/short/ambient/hot/cold behavior; do not replace it with a fixed resistor for unattended charging.

TPS63802 divider gives `0.5*(1+511/91)=3.3077 V`. Startup needs VIN >1.8 V until PG, with running input range down to1.3 V; this is not permission to deeply discharge a LiPo. MODE is grounded for power-save operation. TI specifies >=4uF effective input and >=7uF effective output at 3.3 V. C18=10u and C19/C20=22u each have no selected MPN/DC-bias curves, so effective values are unproven. Two 22u parts improve nominal margin but cannot substitute for qualification. [TI TPS63802 sections 8.3,10,12](https://www.ti.com/lit/ds/symlink/tps63802.pdf).

Each 0.25-ohm shunt sets nominal 0.8 A winding regulation. TI's 160–240mV threshold means 0.64–0.96 A before shunt tolerance; short transients can exceed that because of blanking time. Nominal shunt heating is 0.16 W, about0.23 W at0.96 A, below the stated0.5W rating before thermal derating. This is not an aggregate battery limiter. Motor rated stall is1.5A at6V; approximate resistance scaling gives1.05A at4.2V before losses. Sustained stalls remain unacceptable. The Pololu motor guidance generally favors operating currents well below stall. [Motor data](https://www.pololu.com/product/3065).

At2.4A total, two AO3401A devices at maximum85mOhm each for VGS=-2.5V dissipate about0.98W together, before hot-resistance increase. A5A transient would produce4.25W total at that resistance; do not infer an acceptable duty cycle from the headline transistor current rating. Their100k turn-off pullup is also slow enough that switching-energy measurements matter. [AO3401A datasheet](https://www.aosmd.com/pdfs/datasheet/AO3401A.pdf).

Back-to-back PFET isolation blocks a discharged/isolated battery from absorbing motor-rail regeneration when off. The220uF bulk capacitor stores only9.06mJ between4.2V and10V. A hypothetical10mJ returned into220uF initially at4.2V raises it to about10.42V, exceeding the capacitor rating. This is an energy example, not a measured braking event. Rail clamp strategy, winding inductance, rotating inertia, USB-disable and battery protection opening must be resolved experimentally/design-wise before motor operation. Do not assume a10V capacitor or driver OCP protects against this.

## Battery candidates supplied during review

The Rokland1100mAh candidate is listed as49×28×7.8mm, ±2mm,19g,1C, with1.5A working current,3C maximum and1.8–2.1A overcurrent cutoff. These descriptions are not mutually sufficient for a verified discharge specification.1C at1100mAh is1.1A. Three nominal0.8A bridges total2.4A before logic; cutoff is likely during heavy startup. Its Micro JST1.25 connector is not J2's Micro-Fit. It is **not adopted as the driving battery**. Keep the existing >=5A peak pack requirement pending a concrete qualified cell/protection/contact/wire combination. No protection board bypass or connector substitution was made. [Supplier listing](https://store.rokland.com/products/3-7v-1100mah-lithium-rechargeable-battery-1s-1c-lipo-battery-with-protection-board-with-micro-jst-1-25-plug).

A second Amazon candidate, ASIN B0FR8XSXX6, is listed as3000mAh,65×36×10mm,49g with Micro JST1.25. Its own feature bullets explicitly limit maximum operating current to approximately1.5A, despite the1C label, and advise against high-current vehicle use. This lower explicit current limit disqualifies it for the present motor budget. The65mm length also exceeds the inherited55mm tray assumption. It is not adopted; no protection bypass or arbitrary paralleling is proposed. [Amazon seller listing](https://www.amazon.com/dp/B0FR8XSXX6). Exact protection cutoff and charge-current certification remain unavailable.

## PCB electrical/structural review

The primary ground reference is In1. Its local M2_A route has20 segments at0.2mm, from around(107,102.05) to(111.6,109.6). It is a real switching motor conductor cutting the return plane, not an innocuous naming issue. It is outside the ESP32 antenna region but needs rerouting or a demonstrated continuous return path around it. It remains open; do not describe In1 as an uninterrupted plane.

Inventory reports minimum0.2mm portions on VBAT/VMOTOR/SYS_RAW/3V3. Some are low-current branches, so minimum width alone does not identify every bottleneck; trace the shared battery trunk, connector pads and vias before resizing. For scale, a10mm×0.2mm trace in35um copper is about24.6mOhm at20C: at2.4A it drops59mV and heats142mW. Copper thickness/stackup has not been selected, so this is an illustrative calculation, not a temperature certification.

Sense resistor active connections are3.1375mm long and0.3mm wide; there is no separate Kelvin net. Keep shunt-ground return away from motor-switch and logic return impedance. PowerPAD grounding exists electrically; thermal-via counts, solder-wicking, driver/charger temperature rise and plane spreading resistance are not signed off. No thermal simulation was run.

USB_DM and USB_DP networks contain approximately85.1/65.6mm of copper respectively. Those totals include branches and are not a rigorously extracted differential flight-time skew. Multi-layer routing and the reference path require cleanup; full-speed USB passing ERC does not establish signal integrity. No impedance simulation or eye test was performed. Camera parallel lines similarly require short cabling and scope checks at intended XCLK/PCLK.

The antenna keepout is defined across all four copper layers, with tracks/vias/pours prohibited. DRC found no antenna-area prohibited copper. The carrier has an antenna opening; nearby batteries, screws, clamps and camera metal still require assembled clearance and RF testing. Copper keepout does not imply mechanical RF clearance. [Espressif module layout guidance](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html).

The1.6mm FR-4 chassis has open radial slots; flex, corner stress and motor torque must be checked with the mounted battery and wheel loads. No structural FEA or drop test was performed. Maintain the100mm outline until terminal height, hub engagement, battery choice and clamp clearances close. Shrinking empty-looking copper regions first can remove useful load paths and fastener space.

## Mechanical facts and unresolved dimensions

M1/M2/M3 terminal reference positions are(122,100),(89,80.9474),(89,119.0526), with orientations0,+120,-120 degrees in KiCad. In robot coordinates x=PCB_X-100,y=100-PCB_Y, these are22mm radius at0,120,240 degrees. Clamp hole pairs are at34mm radius with ±10mm tangential offset. This determines wheel order geometrically; electrical motor sign still depends on terminal marking, motor roll and wheel mounting.

The native terminal pads are on6mm centers, each plated slot0.8×2.2mm. The actual Pololu HPCB dimension drawing is **0J949**, page3, not the older README's0J1487 performance-document link. It labels the HPCB terminal spacing6.2mm, so the draft6mm datum needs an overlay and physical fit check before moving pads. Do not present the product-page's approximate6mm prose as a tolerance drawing. The terminals are2mm wide; final plated slot clearance, lead thickness, bend radius and board height remain measurements. [Official dimension drawing](https://www.pololu.com/file/0J949/micro-metal-gearmotors-dimensions.pdf).

The motor gearbox cross section is10×12mm, shaft3mm D-shaped and9mm long. Nexus18036 is compatible with14184,18mm total length,10mm hex length,8mm across flats,6.5g. Total coupling length is not shaft engagement: measure bore depth, setback, grub screw position and wheel axial thickness. [Nexus coupling](https://www.nexusrobot.com/product/3mm-brass-hex-coupling-for-38mm-plastic-omni-wheel-18036.html).

For radial axle orientation, wheel circles lie in vertical tangent planes. If wheel midplane radius is R and axial width is w, a conservative top-view circumscribed radius is `sqrt((R+w/2)^2+19^2)` mm, combined with the50mm PCB radius. This is not `R+19`: wheel radius extends tangentially and vertically. R cannot yet be established from terminal-pad location without the bent-terminal datum, motor-body setback and hub insertion. Therefore an exact overall robot diameter is not yet confirmed. The supplied envelope view uses explicit provisional R/w assumptions; overall height additionally depends on axle height, battery and camera position. A smaller diameter cannot be justified yet.

Carpet is a test item. Measure sideways breakout force, roller sinking, wheel slip, motor current, battery sag, temperatures and video/control dropout on the actual carpet. Encoderless PWM controls applied voltage, not verified wheel speed; no accurate odometry is implied.

## Firmware and Vita stages

Stage0: preserve this pin map, mechanical wheel order and default-disabled policy. Stage1: bench bring-up, faults/ADC/USB override and calibrated motor signs with wheels off the ground. Stage2: limited omni drive, explicit arm/deadman, monotonic sequence numbers,250ms command deadline, acceleration limits, low-battery response and fault latching. Stage3: OV2640 JPEG capture and bounded streaming buffers. Stage4: Vita network/decode/display integration and measured latency; camera failures must not block the control watchdog.

For wheel angle theta_i and radial contact distance R_i, positive tangential wheel speed is `u_i=-sin(theta_i)*vx+cos(theta_i)*vy+R_i*wz`; wheel angular speed is `u_i/0.019`. Positive rotation convention and each motor's electrical sign must be calibrated. Never enable with an unknown sign or arbitrary assumed wheel order. Limit the wheel vector uniformly to preserve direction, then apply per-wheel slew and PWM limits. Fault/USB/link-loss paths must override ramps and drop DRIVE_REQ.

VitaSDK exposes BSD-style networking and JPEG/MJPEG decode APIs. This supports evaluating JPEG frames over TCP/HTTP and independent sequenced UDP commands; it does **not** establish that every OV2640 JPEG sampling format decodes on a Vita2000. Decode a captured sensor frame with the Vita API, validate subsampling/buffer alignment/color conversion, then benchmark latency before freezing the wire protocol. [VitaSDK samples](https://github.com/vitasdk/samples), [JPEG API](https://docs.vitasdk.org/group__SceJpegUser.html), [network API](https://docs.vitasdk.org/group__SceNetUser.html).

No firmware binary was built/flashed and no Vita compatibility hardware test was performed in this pass. The hardware audit remains open, so firmware deployment is deliberately not represented as ready.

## Release blockers

1. Qualified battery/protection/current path and connector; both supplied candidates require assessment.
2. Regenerative/USB-disable transients and PFET thermal/switching behavior.
3. Remaining converter capacitor placement/returns, power trunks and ground-plane motor route.
4. Motor terminal6.2mm drawing overlay, terminal bend/height, hub engagement and clamp axial restraint.
5. U1 footprint mismatch, exact package overlays, capacitor/inductor/connector procurement qualification.
6. Camera physical board/optics, battery attachment and full mechanical interference check.
7. Built/tested firmware, motor signs and Vita JPEG/control compatibility.

These are open engineering work, not DRC exclusions. No boards or components were ordered and the project was not published.
