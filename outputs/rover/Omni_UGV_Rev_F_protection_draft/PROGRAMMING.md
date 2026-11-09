# MAX17301G+T programming worksheet

Draft settings for simulation and fixture qualification. Production limits depend on the cell specification and measured inrush and fault behavior.

| Function | Draft setting or action |
| --- | --- |
| Silicon ID | Read DevName at 0x021 before choosing the profile. MAX17301 revisions 0x4065 and 0x4074 have different reserved-word and thermistor requirements. Follow the datasheet tables for the detected revision. |
| Battery-only wake | nConfig at 0x1B0, PBen bit 10 set and COMMSH bit 6 cleared for the fixture-only bus. Verify both in the active Config register after recall. Keep ordinary low-power behavior separate from undervoltage-induced DeepShip2. |
| Current scaling | nRSense at 0x1CF set to 0x03E8 for 10 mΩ. This describes the shunt to host software. Current comparator thresholds are separate. |
| Fast current comparators | Enable nNVCfg1.enODSC. In nODSCTh at 0x1DD, candidate fields ODTH = 7, SCTH = 7 and OCTH = 2 produce nominal magnitudes of 60 mV, 120 mV and 36.25 mV. With 10 mΩ these are 6 A, 12 A and 3.625 A. The last is an emergency cutoff, separate from the charger's current regulation. |
| Comparator delay | nODSCCfg at 0x1DE candidate SCDLY = 3 gives 253 µs before additional latency. Candidate OCDLY = 14 gives approximately 13.75 ms. Confirm trip energy and immunity to insertion inrush before committing either. |
| Cell thermistor | Use the independent 103AT-2. For DevName below 0x4070, the published 103AT-2 coefficients are nTGain = 0xEE56, nTOff = 0x1DA4 and nTCurve = 0x0025. For DevName at or above 0x4070, use the supported nThermCfg = 0x91C3 path with nNVCfg1.enTherm enabled. Verify temperature selection and open/short responses. |
| Voltage and thermal trip profile | Qualify OV, UV, UV shutdown, temperature bands and recovery timing against the cell. Use the existing 4.25 V and 2.60 V primary thresholds only as comparison points. Keep zero-volt charging disabled in the draft. |

At 6 A the nominal shunt dissipation is 0.36 W. At the 12 A nominal short threshold it is 1.44 W, so check pulse energy and sustained fault behavior against the actual part. The 12 A choice is a candidate for testing. The previous 20 A nominal cutoff would require 200 mV across the shunt and exceeds this controller's 155 mV setting range.

For provisioning, use a current-limited cell simulator and an isolated fixture referenced to CSP_K. Supply pull-ups in the fixture and avoid an external ground path across the shunt. Read the device ID and baseline first. Build and check a complete revision-specific shadow RAM image before copying it to NVM. Follow ADI's power, timing and status requirements for the limited-write Copy NV Block operation. Reset, read back the configuration, and verify active protection before connecting a LiPo or motor load.

[Analog Devices datasheet, configuration and programming tables](https://www.analog.com/media/en/technical-documentation/data-sheets/max17300-max17313.pdf)
