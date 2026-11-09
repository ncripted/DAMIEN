# Provisional battery design basis — 2026-11-06

Nate authorized proceeding with assumptions. Selected candidate: Power Hobby PHB1S100020CJST (1S100020CJST), the **20C** model. This is a provisional design basis, not purchasing approval or a qualification pass.

## Evidence and assumptions

| Item | Working value | Evidence status |
|---|---|---|
| Configuration | 1S LiPo, 3.7 V, 1000 mAh | Advertised for this model |
| Continuous cell discharge | 20C = 20 A advertised | Not independently tested; does not rate wires/connectors |
| Maximum charge voltage | 4.2 V | Assumed conventional LiPo limit; confirm exact pack |
| Maximum charge current | 1C = 1 A | Assumption for this model |
| Minimum cell voltage | 3.0 V | Assumption; not a verified manufacturer limit |
| Charge temperature | 0 to 45 C | Assumption for cell temperature |
| Discharge temperature | -20 to 60 C | Assumption; does not establish full current across range |
| Pack envelope | 62 x 34 x 6 mm | Cross-model assumption from the separate 30C product; measure this pack |
| Connector and wire | Unspecified JST-style | Exact series, polarity, wire gauge and current rating unverified |
| Internal PCM and NTC | Unverified | Do not assume either is present |

Sources: [20C listing](https://www.hobbyrecreationproducts.com/products/phb1s100020cjst-1s-3-7v-1000mah-20c-lipo); [separate 30C model](https://www.powerhobby.com/products/powerhobby-1s-3-7v-1000mah-30c-lipo-battery-w-jst-connector). The latter's dimensions and charge guidance are not established specifications for the 20C pack.

## Decisions that can proceed

- Retain approximately 250 mA nominal charging (R14 = 3.57k), about 0.25C. This is a programmed target; USB input limiting, system load and thermal regulation can reduce it.
- Retain the onboard protection architecture and two independent insulated 103AT-2 probes bonded to the cell, on J4 and J5. A two-wire RC battery does not provide a thermistor signal. Do not open the pouch or bypass an internal PCM.
- Keep the PCB Micro-Fit battery connector. Design/qualify a mating harness after identifying the pack connector. No direct connector compatibility is claimed. Harness target remains 4 A continuous and 5 A peak with a defined duration and tested temperature rise.
- Use the 62 x 34 x 6 mm assumed envelope to continue provisional CAD. Allow 1 mm per side and 2 mm above the nominal cell, a soft liner, unobstructed lead exit, and straps that do not compress the pouch. Assembly placement and fastener fit remain unverified.

## Protection changes still required

The existing BQ298217 has a nominal 2.6 V UV threshold. It does **not** enforce the assumed 3.0 V cell minimum. Firmware cannot substitute for an independent hardware disconnect during firmware failure or storage. Select/review a different protection configuration or add an independent cutoff before release. Its nominal 6 A discharge overcurrent threshold is fault protection, not a 4 A current regulator.

Provisional operational targets for later firmware: stop driving at 3.4 V sustained for 1 s; latch until deliberate re-arm above 3.6 V. Validate under-load sag, ADC calibration, shunt/connector drops and remaining logic consumption. These targets are not implemented firmware and do not stop the powered logic from eventually depleting the cell.

Target charging permission at measured cell temperatures 5 to 40 C, with hardware tolerances inside the assumed 0 to 45 C limits. The current direct-NTC BQ24074 TS circuit has not been demonstrated to meet that window. It requires threshold/tolerance analysis and likely circuit adjustment; this authorization does not waive it. Drive-monitor target: stop at 55 C, with fault latching and open/short probe detection; firmware is still required.

## Release checks

Confirm actual pack dimensions/weight, label, 4.2 V chemistry, manufacturer voltage/temperature/current limits, connector identity/polarity and wire gauge. Check internal protection and NTC topology without opening the pack. Qualify harness, cell sag/temperature, cutoff and recovery, charger TS hot/cold/open/short behavior, USB inhibition and braking overshoot. No physical battery or thermal tests have been performed.

Status: **ASSUMPTIONS ADOPTED; HARDWARE QUALIFICATION BLOCKED**. Continue reversible design work; do not fabricate or describe the power system as qualified on this evidence alone.


## Rev D implementation update — 2026-11-06

U10 now shuts operating loads down around 3.1V independently of firmware; U7 retains its 2.6V emergency backstop. This does not close a strict 3.0V emergency/storage compatibility requirement. An independent USB-powered analog window now monitors TH1 at J4 and controls charger CE. The BQ TS input is intentionally fixed at 10k; it is no longer directly connected to TH1. The modeled tolerance envelope is 1.78–11.16C cold and 36.70–43.59C hot using a beta approximation; exact R-T and bonded-cell tests remain mandatory. Earlier paragraphs describe the pre-Rev-D state. POWER_AUDIT.md and UNRESOLVED.md govern current status.
