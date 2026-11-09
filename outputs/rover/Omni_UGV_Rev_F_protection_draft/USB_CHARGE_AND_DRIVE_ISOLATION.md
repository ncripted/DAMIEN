# Rev F USB charging and battery-only wake

**Status · Architecture candidate. Circuit and fabrication gates remain open.**

USB-C must program the ESP32, power its logic, and charge the installed 1S cell. A hardware path must inhibit battery discharge into the rover's load rail during USB use. The three motors require an explicit arm command after USB is removed. Preserve the charger and the cell-mounted temperature probes.

## Proposed changes at the rover interface

| Branch | From and to | Design intent |
| --- | --- | --- |
| USB programming and logic | USB data stays on the ESP32 interface. BQ24074 OUT supplies SYS_RAW through a one-way logic feed. | USB logic power remains available independently of the battery drive switch. Check the USB input limit against ESP32 startup demand and charger load. |
| USB charge | BQ24074 BAT → unidirectional charge branch → PROTECTED_RAW/PCKP → the MAX17301-controlled cell path. | The cell can charge while the discharge switch is open. The charge branch must limit reverse current into charger-side faults to a verified leakage bound. PCKP stays on the real protected node. |
| Battery drive | PROTECTED_RAW → hardware discharge switch → DRIVE_RAW → motor power switch and battery feed to SYS_RAW. | Default off until battery protection is awake and USB is absent. Use true reverse blocking so USB logic power cannot backfeed the battery or motor supply through this path. |
| Wake and fault controls | Momentary ALRT/PIO wake to the local protector reference. Separate hardware USB inhibit and a persistent discharge-fault latch on the downstream switch. | A wake press cannot clear the downstream fault latch. USB insertion/removal cannot reset it. A separate deliberate rearm after the fault is removed is required. |

The Rev E1 Q13 channel presently joins charger BAT and the load rail on the same path. The proposed branch split replaces that connection. The BQ24074, ESP32 USB data, motor-enable interlock, and cell temperature functions remain design inputs.

## Part screening and constraints

- **Startup.** Retain MAX17301G+T and its ALRT/PIO wake input. Program PBen and leave the ALRT pin FET-override option disabled for this application. ADI specifies the pushbutton path for supported sleep modes. A true battery insertion with USB and the programmer detached still needs a measured cold-start result. UV DeepShip2 uses charger recovery. [ADI MAX17301 datasheet, FET override and wakeup sections](https://www.analog.com/media/en/technical-documentation/data-sheets/max17300-max17313.pdf)
- **Charge-branch isolation.** A PMEG2010ER-class Schottky diode gives a simple first fixture with no enabled reverse channel. Its reverse leakage still needs a temperature limit. The BQ24074 regulates voltage at BAT ahead of the diode, so the cell sees less voltage while charging. Verify charge termination and top-off at temperature. An LM66100 with CE tied to VOUT is a lower-drop candidate, but TI gives a nonzero reverse turn-off threshold and delay. Its reverse pulse and fail modes need explicit qualification before replacing the diode. [Nexperia diode datasheet](https://assets.nexperia.com/documents/data-sheet/PMEG2010ER.pdf) · [TI BQ24074 datasheet](https://www.ti.com/lit/ds/symlink/bq24074.pdf) · [TI LM66100 datasheet, §8.3.2](https://www.ti.com/lit/ds/symlink/lm66100.pdf)
- **Discharge switch.** Screen TPS259474LRPW as a true reverse-blocking, latch-off circuit breaker. Its internal latch can reset if the enable is pulled into shutdown or its input cycles. USB must not be able to reset the fault and permit automatic discharge. The external latch/arming path needs a defined supply and fail-safe reset behavior before a schematic can be frozen. At 4 A and 28.3 mΩ typical the eFuse alone dissipates about 0.45 W, excluding temperature rise. Check low-cell inrush, hot resistance and continuous loss. [TI TPS25947 datasheet](https://www.ti.com/lit/ds/symlink/tps25947.pdf)
- **Motor regeneration.** Reverse blocking may keep regenerative current on DRIVE_RAW. Provide and verify a local clamp or braking strategy before the eFuse topology can drive the motors. Size from measured braking energy, switching conditions and driver ratings. The existing bulk capacitor does not establish this limit.

## Verification boundary

The browser simulator now checks the proposed control states, including healthy battery wake, UV wake rejection, USB insertion while driving, USB insertion during a held downstream fault, and explicit reset/rearm. It assumes accepted wake, functioning one-way elements, and independent latch retention. It does not model physical cold startup, the turn-off overlap when USB first rises, a short directly on PROTECTED_RAW, reverse leakage, or motor energy.

Add these cases to the existing fixture before release:

1. Record the battery-discharge switch, signed cell current and USB VBUS on the same acquisition during USB insertion under a pre-existing downstream fault. Confirm the switch stays off and never enables due to USB transitions or a wake press. Test unplugging USB with the fault held.
2. Repeat with a short at the charge-side BAT node and then directly on PROTECTED_RAW. The downstream switch does not cover the latter. Confirm the primary protection behavior separately.
3. Confirm USB powers logic and charges at its programmed limit with the discharge path open. Record full-cell insertion, charge restart and temperature cutoff, and check that the charge path can recover permitted undervoltage without enabling drive.
4. Check regen, load drop, thermal limits, switch turn-off delay, and the chosen latch implementation. A fixture result qualifies the tested configuration. It does not qualify later PCB or profile changes automatically.

The separate `rev_f_usb_power_path.kicad_pro` fixture implements the charge isolator, logic feeds, eFuse, USB inhibit and a hardware rearm latch. The rearm latch clears on a detected brownout, USB insertion or a fault signal at J12. A detector for a held hard short that does not collapse the protected rail remains outside this schematic. E1 remains the editable layout baseline.
