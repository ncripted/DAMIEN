# DAMIEN | Omni UGV

DAMIEN is a miniature omnidirectional camera rover with three independently driven omni wheels. The PCB doubles as the chassis. The design uses an ESP32-S3, a ribbon-connected camera, and a single-cell LiPo power system with USB charging and programming.

## Open the design

Open [the Rev F KiCad project](outputs/rover/Omni_UGV_Rev_F_power_rebuild/omni_ugv.kicad_pro) in KiCad. The project contains the editable schematics, board, and project-local footprint library. See the [routing checkpoint](outputs/rover/Omni_UGV_Rev_F_power_rebuild/START_HERE.md) and the [latest KiCad DRC report](outputs/rover/Omni_UGV_Rev_F_power_rebuild/drc.json).

## Prototype status

**Fabrication is on hold.** The saved Rev F rebuild has 19 open connections and 7 dangling traces. The remaining work includes charger, battery-protector, and eFuse routing, plus electrical review of the motor-current path, braking transients, and short-circuit recovery.

## Repository contents

- [Board revisions and review packages](outputs/rover/) include earlier designs and intermediate candidates.
- [Development and validation work](work/) includes layout experiments, routing scripts, and engineering checks.
