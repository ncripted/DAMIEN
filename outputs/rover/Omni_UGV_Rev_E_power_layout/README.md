# Miniature omni camera rover — Rev E

Rev E implements the six-step electrical/layout revision in native KiCad: motor routing off In1, stronger current paths, a four-terminal protection shunt, shorter regulator switch connections, and an independent 3.1 V operating discharge cutoff.

Open omni_ugv.kicad_pro. Read START_HERE.md and engineering/SIX_STEP_REVIEW.md. The fresh board views are in preview; the eleven-page Schematic.pdf and engineering/PIN_MAP.csv come from the current native files.

Final configured ERC/DRC/unconnected/parity results are zero. **Fabrication remains BLOCKED:** primary-protector startup compatibility, source-pad via filling/capping, electrical/thermal/transient qualification and physical fit remain unresolved. See engineering/UNRESOLVED.md. No board order or publication was made.

The original ZIP and Rev D are preserved. Imported older reports/views are under .history/rev-d-import and are historical. Native files are authoritative. There is no live KiCad editor IPC connection; reopen/reload the saved Rev E file to inspect it.
