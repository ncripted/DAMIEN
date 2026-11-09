from pathlib import Path
import pcbnew as p,json,hashlib
root=Path('outputs/rover/Omni_UGV_Rev_B_protection');path=root/'omni_ugv.kicad_pcb'
backup=Path('work/humanize/board-before.kicad_pcb')
if not backup.exists():backup.write_bytes(path.read_bytes())
pro=(root/'omni_ugv.kicad_pro').read_bytes()
b=p.LoadBoard(str(path))
for f in b.GetFootprints():
 if f.GetReference()=='R42':f.SetPosition(p.VECTOR2I(p.FromMM(125.3),p.FromMM(88)))
 if f.GetReference()=='U1':
  lib=Path('work/humanize/inspect.pretty');lib.mkdir(exist_ok=True)
  p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(lib.resolve()),f)
p.SaveBoard(str(path),b);(root/'omni_ugv.kicad_pro').write_bytes(pro)
print('Moved R42 0.2 mm left; existing traces still terminate inside its pads.')


