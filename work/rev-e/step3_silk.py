import pcbnew as p
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');pr=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(r/'omni_ugv.kicad_pcb'))
for f in b.GetFootprints():
 if f.GetReference() in ['R40','C24','U7']:
  x,y={'R40':(124.6,134),'C24':(125.7,132),'U7':(120,132)}[f.GetReference()];f.Reference().SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));f.Reference().SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)))
p.SaveBoard(str(r/'omni_ugv.kicad_pcb'),b);(r/'omni_ugv.kicad_pro').write_bytes(pr)

