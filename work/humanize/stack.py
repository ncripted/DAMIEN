from pathlib import Path
import pcbnew as p
r=Path('outputs/rover/Omni_UGV_Rev_B_protection');b=p.LoadBoard(str(r/'omni_ugv.kicad_pcb'));f=next(f for f in b.GetFootprints() if f.GetReference()=='U1');g=p.FootprintLoad(str((r/'UGV.pretty').resolve()),'RF_Module__ESP32-S3-WROOM-1')
for h in [f,g]:
 print('stack',h.GetStackupMode(),h.GetStackupLayers().FmtHex(),'layer',h.GetLayerSet().FmtHex(),'attribute',h.GetAttributes())
 print('zone',[(z.GetLayerSet().FmtHex(),z.GetLocalClearance(),z.GetDoNotAllowPads()) for z in h.Zones()])
