import pcbnew as p,json
from pathlib import Path
b=p.LoadBoard('outputs/rover/Omni_UGV_Rev_B_protection/omni_ugv.kicad_pcb')
z=next(z for z in b.Zones() if z.GetNetname()=='GND');ps=z.GetFilledPolysList(p.In1_Cu)
def xy(v):return [p.ToMM(v.x),p.ToMM(v.y)]
data=[]
for i in range(ps.OutlineCount()):
 l=ps.COutline(i);data.append({'outline':[xy(l.CPoint(j)) for j in range(l.PointCount())],'holes':[[xy(ps.CHole(i,h).CPoint(j)) for j in range(ps.CHole(i,h).PointCount())] for h in range(ps.HoleCount(i))]})
Path('work/protection/ground-fill.json').write_text(json.dumps(data))
print('ground islands',len(data))
