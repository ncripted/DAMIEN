import pcbnew as p
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');pr=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(r/'omni_ugv.kicad_pcb'))
next(f for f in b.GetFootprints() if f.GetReference()=='R66').Reference().SetPosition(p.VECTOR2I(p.FromMM(138.5),p.FromMM(130)))
p.SaveBoard(str(r/'omni_ugv.kicad_pcb'),b);(r/'omni_ugv.kicad_pro').write_bytes(pr)

