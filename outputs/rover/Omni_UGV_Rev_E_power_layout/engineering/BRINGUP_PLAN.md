# Rev E — required bench evidence

No tests below have been performed. Resolve/review the BQ298217 startup architecture and source-pad via assembly process before authorizing a prototype build.

Use a current-limited cell simulator capable of sinking charging current, plus an isolated USB source. CELL_N and GND are separated by R36: externally bonding them bypasses the current shunt. Use differential probing where needed; do not connect common scope grounds to both sides of R36.

1. Check assembly, polarity and every new protection pin against the native pin map. Inspect the four separate R36 contacts, source-pad via fill/caps, thermal-pad solder and actual NTC insulation/mounting. Begin without motors or a real LiPo.
2. Characterize cold start at several simulated cell voltages, especially 4.2 V, with USB absent/present. Record BAT, PACK, VDD, CHG, DSG, PROTECTED_RAW and VBAT. Do not assume U7 can wake from the available charger voltage. Do not bypass its FETs to make the test pass.
3. Once a valid primary-protector startup sequence is established, sweep raw cell voltage down/up. Record U10 RESET_N, Q13 gate/source, VBAT, SYS_ON and DRIVE_ENABLE. Measure static cutoff/recovery, release delay, transient dip response and residual current. Confirm that the switch remains effective after protected VBAT falls.
4. With the simulated cell below operating cutoff, verify controlled recovery charging through Q13's body diode, the diode's temperature, eventual switch turn-on and final charge regulation. Verify TH1 open/short/hot/cold inhibit independently of ESP32, and calibrate TH2 against cell temperature.
5. With suitable test firmware and powered logic, verify hardware USB motor disable even while the software drive request is asserted. Confirm default-disabled power-up, driver fault response and absence of unintended motor pulses during resets or cutoff recovery.
6. Apply staged electrical loads. Measure every supply, shunt error and temperature at the drivers, regulator, charger, FETs, shunt, connector and via transitions. Scope Wi-Fi/camera load steps, motor start/stall/reversal, coast/braking, USB insertion and fault recovery. Set measured operating limits; the 4 A/5 A harness targets are not a board rating.
7. Only after electrical gates pass, fit the actual motors, couplings, wheels, battery and camera. Validate clamps and under-board clearance, then perform RF/camera tests, link-loss stopping and carpet trials. Choose Vita streaming/network protocols only after a working compatibility experiment.

Record supply settings, probe locations, waveform files, ambient/cell temperatures and pass/fail limits. Update the circuit/layout if any required state depends on an undocumented component behavior.
