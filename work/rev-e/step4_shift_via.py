import pcbnew as p
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');pr=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(r/'omni_ugv.kicad_pcb'))
for t in b.GetTracks():
 if t.GetNetname()=='SYS_RAW':
  if isinstance(t,p.PCB_VIA):
   if abs(p.ToMM(t.GetPosition().x)-97.5)<.005 and abs(p.ToMM(t.GetPosition().y)-112.6)<.005:t.SetPosition(p.VECTOR2I(p.FromMM(97.3),p.FromMM(112.6)))
  else:
   for meth in ['Start','End']:
    pt=getattr(t,'Get'+meth)()
    if abs(p.ToMM(pt.x)-97.5)<.005 and abs(p.ToMM(pt.y)-112.6)<.005:getattr(t,'Set'+meth)(p.VECTOR2I(p.FromMM(97.3),p.FromMM(112.6)))
p.SaveBoard(str(r/'omni_ugv.kicad_pcb'),b);(r/'omni_ugv.kicad_pro').write_bytes(pr)
