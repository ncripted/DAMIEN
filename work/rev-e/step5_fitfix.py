import pcbnew as p,math
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');pr=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(r/'omni_ugv.kicad_pcb'));shifts=[]
for f in b.GetFootprints():
 if f.GetReference() in ['Q12','R66']:
  dx,dy=(1,0) if f.GetReference()=='Q12' else (2,-1)
  for pad in f.Pads():
   pt=pad.GetPosition();shifts.append((pt,p.VECTOR2I(pt.x+p.FromMM(dx),pt.y+p.FromMM(dy))))
  f.Move(p.VECTOR2I(p.FromMM(dx),p.FromMM(dy)))
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA):continue
 for method in ['Start','End']:
  pt=getattr(t,'Get'+method)()
  for a,z in shifts:
   if math.hypot(pt.x-a.x,pt.y-a.y)<3000:getattr(t,'Set'+method)(z);break
for f in b.GetFootprints():
 if f.GetReference()=='R67':f.Reference().SetPosition(p.VECTOR2I(p.FromMM(135),p.FromMM(133.5)))
p.SaveBoard(str(r/'omni_ugv.kicad_pcb'),b);(r/'omni_ugv.kicad_pro').write_bytes(pr)
