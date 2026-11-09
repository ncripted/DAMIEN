from pathlib import Path
import json,sys,math
sys.path.insert(0,'work/protection/deps')
from shapely.geometry import box,Polygon,LineString,Point
from shapely import affinity,unary_union
g=json.loads(Path('work/rev-e/geometry.json').read_text());f=next(f for f in g['footprints'] if f['ref']=='C24');old=f['at']
def padg(d):
 w,h=d['size'];return affinity.translate(affinity.rotate(box(-w/2,-h/2,w/2,h/2),-d['angle']),*d['at'])
cu=unary_union([padg(d) for d in g['pads'] if d['ref']=='C24']);obs=[padg(d).buffer(.18) for d in g['pads'] if d['ref']!='C24' and 'B.Cu' in d['layers']]
obs +=[(Point(t['a']) if t['via'] else LineString([t['a'],t['z']])).buffer(t['width']/2+.18) for t in g['tracks'] if t['via'] or t['layer']=='B.Cu'];ob=unary_union(obs)
body=unary_union([Polygon(p) for p in f['courtyard'][1]]);bodies=[unary_union([Polygon(p) for p in ff['courtyard'][1]]) for ff in g['footprints'] if ff['ref']!='C24' and ff['side']=='B.Cu']
for x,y in sorted([(old[0]+dx*.05,old[1]+dy*.05) for dx in range(-30,31) for dy in range(-30,31)],key=lambda v:math.dist(v,old)):
 moved=affinity.translate(cu,x-old[0],y-old[1]);bb=affinity.translate(body,x-old[0],y-old[1])
 if moved.intersects(ob) or any(bb.intersects(p) for p in bodies):continue
 print('C24 ->',x,y);p=Path('outputs/rover/Omni_UGV_Rev_E_power_layout/design_connections.json');ds=json.loads(p.read_text())
 for d in ds:
  if d['ref']=='C24':d.update(x=x,y=y)
 p.write_text(json.dumps(ds,indent=2));Path('work/rev-e/c24-placement.json').write_text(json.dumps([x,y]));break
else:raise RuntimeError('No local bypass-cap position')
