# Change log

## 2026-11-03 — first independent audit and corrective pass

- Preserved original supplied ZIP, SHA256 b98c896f4cad7e2c9cc6c30c1111b8cb07aa9229da0994c1721cee39b67e5380.
- Reproduced checks with installed KiCad10.0.8. Baseline:4DRC errors/4warnings,0unconnected,0parity,0ERC. Older9.0.9 check was not rerun.
- Fixed loaded motor-enable network: R25=100k,R27=1k,R29=10k. Native schematic, PCB, BOM and connection JSON agree.
- Removed19dangling branch segments. Replaced62converter switch-node tracks/vias with6front-layer0.4mm segments. Complete copper UUID delta is in engineering/COPPER_CHANGE_MANIFEST.json.
- Added J1-only0.19mm alignment-hole clearance rule matching manufacturer land geometry. Fabricator approval is still required; global0.25mm rule remains.
- Exported board U1 footprint to local library while investigating mismatch; warning persists and remains enabled.
- Added pin map, actual board inventory, detailed engineering audit, candidate battery assessments and provisional parametric support sources.
- Current:0DRC errors,1footprint warning,0unconnected,0parity,0ERC under configured rules. No explicit DRC exclusions.
- No outline/motor pad geometry changes, production Gerbers, firmware binary, print-ready supports or hardware performance claims.
