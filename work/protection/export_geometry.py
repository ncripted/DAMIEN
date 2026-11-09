import pcbnew as p,json,sys
from pathlib import Path
root=Path('outputs/rover/Omni_UGV_Rev_B_protection');b=p.LoadBoard(str(root/'omni_ugv.kicad_pcb'))
def v(pt):return [p.ToMM(pt.x),p.ToMM(pt.y)]
def line(l):return [v(l.CPoint(i)) for i in range(l.PointCount())]
poly=p.SHAPE_POLY_SET();assert b.GetBoardPolygonOutlines(poly,False)
out={'outline':[[line(poly.COutline(i)),[line(poly.CHole(i,j)) for j in range(poly.HoleCount(i))]] for i in range(poly.OutlineCount())],'pads':[],'tracks':[],'footprints':[]}
for f in b.GetFootprints():
 out['footprints'].append({'ref':f.GetReference(),'at':v(f.GetPosition()),'side':f.GetLayerName()})
 for pad in f.Pads():
  out['pads'].append(dict(ref=f.GetReference(),num=pad.GetNumber(),net=pad.GetNetname(),at=v(pad.GetPosition()),size=v(pad.GetSize()),angle=pad.GetOrientationDegrees(),drill=v(pad.GetDrillSize()),layers=[b.GetLayerName(l) for l in pad.GetLayerSet().CuStack()],uuid=pad.m_Uuid.AsString(),shape=int(pad.GetShape())))
for t in b.GetTracks():
 out['tracks'].append(dict(net=t.GetNetname(),a=v(t.GetStart()),z=v(t.GetEnd()),width=p.ToMM(t.GetWidth(p.F_Cu) if isinstance(t,p.PCB_VIA) else t.GetWidth()),via=isinstance(t,p.PCB_VIA),drill=p.ToMM(t.GetDrill()) if isinstance(t,p.PCB_VIA) else 0,layer=t.GetLayerName(),uuid=t.m_Uuid.AsString()))
Path('work/protection/geometry.json').write_text(json.dumps(out))
print('Exported',len(out['pads']),'pads',len(out['tracks']),'tracks',len(out['outline']),'outlines')
