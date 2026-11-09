import pcbnew as p,json
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');pr=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(r/'omni_ugv.kicad_pcb'))
for o in b.GetDrawings():
 if hasattr(o,'GetText'):o.SetText(o.GetText().replace('REV D','REV E'))
tb=b.GetTitleBlock();tb.SetRevision('E - prototype');tb.SetDate('2026-11-07');b.SetTitleBlock(tb)
p.SaveBoard(str(r/'omni_ugv.kicad_pcb'),b);(r/'omni_ugv.kicad_pro').write_bytes(pr)
