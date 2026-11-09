"""Move conflicted reference labels without changing footprint locations."""
from pathlib import Path
from math import hypot
import json
import sys
import pcbnew as p
sys.path.insert(0,str(Path("work/protection/deps").resolve()))
from shapely import affinity
from shapely.geometry import box, Polygon
from shapely.ops import unary_union

root=Path("outputs/rover/Omni_UGV_Rev_F_integration")
path=root/"omni_ugv.kicad_pcb"
b=p.LoadBoard(str(path))
settings=path.with_suffix(".kicad_pro").read_bytes()
report=json.loads((root/"drc.json").read_text())
conflicts={i["uuid"] for d in report["violations"] if d["type"] in {"silk_overlap","silk_over_copper"}
           for i in d["items"] if i["description"].startswith("Reference field")}
def rect(obj):
    r=obj.GetBoundingBox()
    return box(*(p.ToMM(x) for x in (r.GetX(),r.GetY(),r.GetRight(),r.GetBottom())))
def xy(item):
    return p.ToMM(item.x),p.ToMM(item.y)
poly=p.SHAPE_POLY_SET()
assert b.GetBoardPolygonOutlines(poly,False)
def contour(line):
    return [xy(line.CPoint(i)) for i in range(line.PointCount())]
board=Polygon(contour(poly.COutline(0)),[contour(poly.CHole(0,i)) for i in range(poly.HoleCount(0))]).buffer(-.55)
offsets=sorted(((dx*.25,dy*.25) for dx in range(-28,29) for dy in range(-28,29)),key=lambda q:hypot(*q))
for silk,mask,courtyard in [(p.F_SilkS,p.F_Mask,p.F_CrtYd),(p.B_SilkS,p.B_Mask,p.B_CrtYd)]:
    fixed=[rect(d) for d in b.GetDrawings() if d.GetLayer()==silk]
    move=[]
    for f in b.GetFootprints():
        fixed.extend(rect(d) for d in f.GraphicalItems() if d.GetLayer() in {silk,courtyard})
        fixed.extend(rect(d) for d in f.Pads() if d.IsOnLayer(mask) or d.GetDrillSize().x)
        ref=f.Reference()
        if ref.GetLayer()!=silk or not ref.IsVisible():
            continue
        if ref.m_Uuid.AsString() in conflicts:
            move.append(ref)
        else:
            fixed.append(rect(ref))
    occupied=unary_union([r.buffer(.19) for r in fixed])
    for ref in move:
        x,y=xy(ref.GetPosition())
        ref.SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)))
        ref.SetTextThickness(p.FromMM(.13))
        body=rect(ref)
        for dx,dy in offsets:
            shifted=affinity.translate(body,dx,dy)
            if board.covers(shifted) and not occupied.intersects(shifted):
                ref.SetPosition(p.VECTOR2I(p.FromMM(x+dx),p.FromMM(y+dy)))
                occupied=occupied.union(shifted.buffer(.19))
                break
        else:
            print("No clear position",ref.GetText())
p.SaveBoard(str(path),b)
path.with_suffix(".kicad_pro").write_bytes(settings)
print("Checked",len(conflicts),"conflicting reference labels")
