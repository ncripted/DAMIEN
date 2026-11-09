from pathlib import Path
import pcbnew as p
root=Path('outputs/rover/Omni_UGV_Rev_B_protection');pro=(root/'omni_ugv.kicad_pro').read_bytes();path=root/'omni_ugv.kicad_pcb';b=p.LoadBoard(str(path));f=next(f for f in b.GetFootprints() if f.GetReference()=='U1')
lp=root/'UGV.pretty/RF_Module__ESP32-S3-WROOM-1.kicad_mod';bak=Path('work/humanize/U1-library-before.kicad_mod')
if not bak.exists():bak.write_bytes(lp.read_bytes())
f.SetStackupMode(p.FOOTPRINT_STACKUP_CUSTOM_LAYERS);f.SetStackupLayers(p.LSET.AllCuMask(4))
for z in f.Zones():z.SetLayerSet(p.LSET.AllCuMask(4))
p.SaveBoard(str(path),b);(root/'omni_ugv.kicad_pro').write_bytes(pro)
p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str((root/'UGV.pretty').resolve()),f)
print('Explicit four-copper-layer footprint and keepout, board and bundled library.')
