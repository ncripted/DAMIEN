# Rev F left-side routing checkpoint

Open omni_ugv.kicad_pro. Fabrication remains on hold.

The 14 USB inhibit and rearm footprints occupy the front of the left crescent. U15 moved to board coordinates (127.0 mm, 117.5 mm) on B.Cu. Both power lands escape in opposite directions and transition from 0.26 mm to 0.85 mm traces 0.60 mm beyond the nominal ends of the lands. KiCad no longer reports opens at U15 pins 5 and 6. The wider traces are provisional pending an end-to-end review of current capacity, via capacity and return paths.

The latest DRC reports 20 open connections, 13 warnings, zero other board-rule errors and zero schematic parity issues. Complete the eFuse control routes, reposition and verify the eFuse bypass capacitors, and close the remaining charger and battery protection paths. Review the short recovery and motor braking behavior before releasing fabrication files. See drc.json for exact endpoints.

