import pcbnew as p,json
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');fn=r/'omni_ugv.kicad_pcb';pr=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(fn));x,y=json.loads(Path('work/rev-e/c24-placement.json').read_text());next(f for f in b.GetFootprints() if f.GetReference()=='C24').SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));p.SaveBoard(str(fn),b);(r/'omni_ugv.kicad_pro').write_bytes(pr)
