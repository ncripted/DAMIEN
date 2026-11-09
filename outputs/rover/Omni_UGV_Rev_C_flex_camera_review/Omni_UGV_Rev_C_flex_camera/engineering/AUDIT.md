# Current engineering audit — Rev B

Read STEP_1_REVIEW.md for the completed November 5 cleanup and UNRESOLVED.md for remaining gates. The prior Rev A audit is preserved at history/Rev_A_AUDIT.md and is historical where Rev B conflicts.

Rev B replaces the assumption of external-only protection with onboard BQ298217RUGR, common-drain CSD17308Q3 Q7/Q8, WSL2512R0100FEA 10 mΩ R36 and support components. It adds J5 plus R42/R43/C25 for an independent cell-temperature ADC input. J4 remains the charger's independent cell probe. Both TH1 and TH2 are off-board cell-bonded 103AT-2 sensors. GPIO1 becomes CELL_TEMP_ADC and GPIO43 becomes LED_STATUS.

The protection's nominal overcurrent disconnect is approximately 60 mV / 10 mΩ = 6 A, not a regulated current limit. This threshold does not qualify the cell or connector for that current. Detailed electrical/thermal review and bench qualification remain open. Do not treat the emergency undervoltage cutoff as the normal firmware stopping threshold.

Charging and motor paths differ: protected VBAT feeds the motor switch directly and also the charger BAT pins. Charger OUT/SYS_RAW feeds logic regulation. Motor-current qualification cannot be inferred from the charger's approximately 249 mA charging setting.

Rule checks currently pass with zero violations; no thermal, transient, physical-fit, carpet or firmware claim follows from that result. Native schematic and PCB are authoritative over older notes.
