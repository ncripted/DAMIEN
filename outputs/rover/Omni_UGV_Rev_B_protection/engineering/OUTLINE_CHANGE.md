# Solid perimeter change — 2026-11-06

At Nate’s request, replaced the three edges forming the ESP32 antenna notch with the missing 50 mm radius perimeter, centered at (100,100) mm. The three motor openings, module placement, holes, electrical routing and four-layer antenna copper keepouts are unchanged. Original board saved in work/outline-change/before.kicad_pcb; the step-1 ZIP also preserves the previous revision.

This adds bare FR-4 beneath/around the module antenna. Espressif recommends removing substrate in this placement. Copper clearance alone does not establish equal RF performance. This is a user-selected mechanical shape, pending assembled Wi-Fi range/throughput and streaming tests, including motors running. Keep battery, screws, brackets and wires out of the antenna clearance region. Source: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html
