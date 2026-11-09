import pcbnew as p, math
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_E1_layout_candidate')
b=p.LoadBoard(str(r/'omni_ugv.kicad_pcb'))
def xy(v):return (round(v.x/1e6,4),round(v.y/1e6,4))
for ref in ('Q8','Q13'):
 f=b.FindFootprintByReference(ref)
 print(ref,[(d.GetNumber(),xy(d.GetPosition()),xy(d.GetSize()),d.GetNetname()) for d in f.Pads()])
 for t in b.GetTracks():
  if t.GetNetname()=='PROTECTED_RAW' and min(math.dist(xy(x),xy(f.GetPosition())) for x in (t.GetStart(),t.GetEnd()))<4:
   print(t.GetLayerName(),xy(t.GetStart()),xy(t.GetEnd()),round(t.GetWidth()/1e6,3),t.m_Uuid.AsString())
