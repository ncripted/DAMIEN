# Omni UGV / Rev A

**Current audit and edits:** See `engineering/AUDIT.md` and `CHANGELOG.md`.
R25/R27/R29 are now100k/1k/10k. REG_L1/L2 are rerouted in front copper.
Updated checks and the pin map are under `validation/current/` and `engineering/`.
The original descriptions below remain useful context but their check counts
and completed-review implications are superseded. Neither battery candidate
Nate supplied meets the present documented motor current budget.

An editable four-layer PCB chassis for Nathaniel Sanford's three-wheel camera rover.

## Hardware implemented

- 100 mm nominal chassis diameter, 1.6 mm FR-4, three radial motor openings and an antenna opening.
- ESP32-S3-WROOM-1-N8R8; no separate STM32 in this revision.
- Three Pololu #3065 HPCB 6 V 100:1 motors operated from a 1S LiPo through two DRV8833PWP drivers.
- Soldered motor-terminal interfaces on 6 mm centers; separate printed clamps carry wheel and motor loads.
- Nexus #14184 38 mm omni wheels, with three #18036 3 mm couplings, purchased separately.
- Waveshare OV2640 Camera Board, using its documented 18-pin 2x9 interface. The camera board includes its sensor regulators. A raw 24-pin OV2640 flex camera is not pin-compatible with J3.
- TPS63802 3.3 V buck-boost converter, BQ24074 USB charger/power path, and a back-to-back PFET motor-power switch.
- Hardware USB-present override disables the motor drivers and motor power, including during programming.
- Battery voltage measurement, pack thermistor connector, BOOT/RESET controls, status/charge indicators and test pads.

## Files and use

Start with `START_HERE.md` for the KiCad opening instructions and current review status.

Open `omni_ugv.kicad_pro` in KiCad 9 or later. All used symbols and footprints are bundled. The root schematic links five functional sheets. `Schematic.pdf` is the six-page review copy; `BOM.csv` lists purchased PCB components and the motors. TP1-TP11 are bare copper test pads, not purchased components. Source pin-to-net assignments are in `design_connections.json`.

The latest validation result is recorded in `validation_summary.json`, with detailed `erc.json` and `drc.json` reports. Check the actual reports; a successful file export alone does not establish an electrically complete board. This is an unbuilt prototype, with mechanical fit and hardware behavior still to be verified.

## External parts and mechanical assumptions

| Item | Requirement |
|---|---|
| Battery | Protected standard 1S LiPo, 4.2 V maximum; 750-1000 mAh initial target; pack/protection/wiring capable of at least 5 A peak |
| Battery connection | J2 pin 1 positive, pin 2 ground; Molex Micro-Fit mating cable, rated contacts and wire |
| Pack temperature | External 10k 103AT-2 thermistor attached to the cell; J4 pin 1 TS, pin 2 ground |
| Battery cradle | Initial envelope 55 x 35 x 10 mm, mounted clear of solder joints and hot components; exact pack remains a procurement choice |
| Motor clamps | Six M2 mounting holes around the motor slots; screws and clamps carry torque |
| Motor pads | HPCB copper terminals, 6 mm spacing, 0.8 x 2.2 mm plated slots; check real terminals, height and orientation with a 1:1 print before ordering |
| Camera | Exact Waveshare OV2640 18-pin board; short cable to printed forward-facing bracket |
| Wheels | Check wheel-to-PCB clearance and coupling engagement with the actual wheel and motor |

The battery connector is keyed. The board does not provide a guarantee against a miswired pack or a reverse-polarity cable. Use the specified protected pack and correct cable polarity. No battery, motor, camera or radio hardware was available for physical testing during this design.

## Power and control settings

- Motor rail is the protected cell voltage, not a boosted 6 V rail. Motor speed and torque fall as the battery discharges.
- Each active bridge has a 0.25-ohm sense resistor: initial nominal winding-current limit 0.8 A. Check motor startup and sustained current on the actual carpet.
- Charger ISET is 3.57k, targeting approximately 250 mA. Input defaults to USB100. GPIO44 can request USB500 only after the connected USB source permits it; firmware must implement that policy.
- SW3 controls regulator enable; charging remains connected when logic power is off. The motor switch defaults off without logic drive.
- Use a current-limited bench supply for first bring-up. Verify 3.3 V regulation before fitting the ESP32 and camera if assembling by hand.
- Inspect driver/charger/FET temperatures, supply ripple, braking transients, charging termination, USB override, camera latency, radio range, and link-loss stopping on an assembled prototype.
- Motor and Vita firmware are separate work. The PCB does not yet provide a flashed application. Start with 320x240 JPEG, conservative speed ramps, and approximately 250 ms command timeout.
- GPIO44 is allocated to charger control. The debug pads provide UART TX only; use native USB plus BOOT/RESET for programming and recovery.

## Manufacturing and fit checks

Target four copper layers, 1.6 mm board thickness, and an inner ground reference. In1.Cu is the primary ground plane; a short local M2_A fanout route also occupies part of that layer near U2. Inspect that return-path region during review. Fine-pitch ICs and the module thermal-pad holes require a fabricator that supports the actual exported clearances and 0.2 mm minimum plated holes. Confirm the stackup with the fabricator before ordering; USB full-speed routing has not been impedance-simulated.

The custom motor footprint is based on manufacturer drawing dimensions and still needs a physical fit check. Verify the inductor's land overlap against the exact supplied part, camera cable orientation, battery clearance, wheel clearance and fastener lengths. 38 mm omni wheels have not been tested on carpet; thick pile may prevent useful sideways travel.

## Primary references

- ESP32-S3 module: https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf
- Espressif PCB guidance: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html
- DRV8833: https://www.ti.com/lit/ds/symlink/drv8833.pdf
- TPS63802: https://www.ti.com/lit/ds/symlink/tps63802.pdf
- BQ24074: https://www.ti.com/lit/ds/symlink/bq24074.pdf
- AO3401A: https://www.aosmd.com/pdfs/datasheet/AO3401A.pdf
- Motor: https://www.pololu.com/product/3065
- Motor drawing: https://www.pololu.com/file/0J1487/pololu-micro-metal-gearmotors.pdf
- Camera interface: https://files.waveshare.com/upload/9/99/OV2640-Camera-Board-Schematic.pdf
- Wheel coupling: https://www.nexusrobot.com/product/3mm-brass-hex-coupling-for-38mm-plastic-omni-wheel-18036.html
- Inductor: https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xfl/xfl4015/
- Bulk capacitor: https://na.industrial.panasonic.com/products/capacitors/lineup/aluminum-electrolytic-capacitors/series/88931/model/89218

Standard KiCad symbols and footprints are derived from the KiCad library contributors' libraries, distributed under CC-BY-SA 4.0 with the KiCad libraries exception. Custom design content in this project was generated for this build.
