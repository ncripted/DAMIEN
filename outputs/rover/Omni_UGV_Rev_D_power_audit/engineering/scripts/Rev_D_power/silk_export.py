import pcbnew as p,json
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');b=p.LoadBoard(str(r/'omni_ugv.kicad_pcb'));new={d['ref'] for d in json.loads(Path('work/power-rev-d/new_parts.json').read_text())}
def bb(o):
 z=o.GetBoundingBox();return [p.ToMM(z.GetX()),p.ToMM(z.GetY()),p.ToMM(z.GetRight()),p.ToMM(z.GetBottom())]
def xy(o):return [p.ToMM(o.GetPosition().x),p.ToMM(o.GetPosition().y)]
fixed=[];moving=[]
for f in b.GetFootprints():
 for pad in f.Pads():
  if pad.IsOnLayer(p.F_Cu):fixed.append(bb(pad))
 for v in f.GraphicalItems():
  if v.GetLayer()==p.F_SilkS:fixed.append(bb(v))
 if f.Reference().IsVisible() and f.Reference().GetLayer()==p.F_SilkS:
  if f.GetReference() in new:
   v=f.Reference();v.SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)));moving.append(dict(id=f.GetReference(),at=xy(v),bbox=bb(v),anchor=xy(f)))
  else:fixed.append(bb(f.Reference()))
for v in b.GetDrawings():
 if v.GetLayer()==p.F_SilkS:
  if hasattr(v,'GetText') and v.GetText()=='N. SANFORD':moving.append(dict(id='signature',at=xy(v),bbox=bb(v),anchor=xy(v)))
  else:fixed.append(bb(v))
Path('work/power-rev-d/silk-geometry.json').write_text(json.dumps(dict(fixed=fixed,moving=moving)));print('Exported',len(moving),'silkscreen labels')
