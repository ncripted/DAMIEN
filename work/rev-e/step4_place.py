import pcbnew as p,json
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');pr=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(r/'omni_ugv.kicad_pcb'))
for f in b.GetFootprints():
 if f.GetReference()=='L1':f.SetPosition(p.VECTOR2I(p.FromMM(99.75),p.FromMM(114)))
 if f.GetReference() in ['C18','C19','C20']:f.SetValue('22u/10V X5R 20%')
p.SaveBoard(str(r/'omni_ugv.kicad_pcb'),b);(r/'omni_ugv.kicad_pro').write_bytes(pr)
