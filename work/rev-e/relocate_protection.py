import pcbnew as p
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');pr=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(r/'omni_ugv.kicad_pcb'))
for f in b.GetFootprints():
 if f.GetReference()=='U7':f.SetPosition(p.VECTOR2I(p.FromMM(121),p.FromMM(130)))
 if f.GetReference()=='C24':f.SetPosition(p.VECTOR2I(p.FromMM(123),p.FromMM(132)))
p.SaveBoard(str(r/'omni_ugv.kicad_pcb'),b);(r/'omni_ugv.kicad_pro').write_bytes(pr)

