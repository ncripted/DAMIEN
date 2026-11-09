from pathlib import Path
import json,sys,math
sys.path.insert(0,'work/protection/deps')
from shapely.geometry import Polygon,Point,LineString,box
from shapely import affinity,unary_union
p=Path('work/power-rev-d/new_parts.json');ds=json.loads(p.read_text());g=json.loads(Path('work/power-rev-d/geometry.json').read_text());moving={'Q11','R51','R54','R60'}
board=unary_union([Polygon(o,h) for o,h in g['outline']]).buffer(-.4)
def pg(d):
 w,h=d['size'];return affinity.translate(affinity.rotate(box(-w/2,-h/2,w/2,h/2),-d['angle']),*d['at'])
pads=[(d,pg(d)) for d in g['pads']];obs=[v.buffer(.18) for d,v in pads if d['ref'] not in moving]
for t in g['tracks']:obs.append((Point(t['a']) if t['via'] else LineString([t['a'],t['z']])).buffer(t['width']/2+.18))
fixed=unary_union(obs);bodies=[]
def cb(f):
 polys=[Polygon(v) for l in f.get('courtyard',[]) for v in l if len(v)>2]
 return unary_union(polys).buffer(.05) if polys else box(*unary_union([p for d,p in pads if d['ref']==f['ref']]).bounds).buffer(.5)
for f in g['footprints']:
 if f['ref'] not in moving:bodies.append(cb(f))
for ref in moving:
 d=next(x for x in ds if x['ref']==ref);f=next(f for f in g['footprints'] if f['ref']==ref);cu=unary_union([v for a,v in pads if a['ref']==ref]);body=cb(f);old=f['at'];tx,ty=old
 for x,y in sorted([(tx+dx*.25,ty+dy*.25) for dx in range(-120,121) for dy in range(-120,121)],key=lambda v:math.dist(v,old)):
  cc=affinity.translate(cu,x-old[0],y-old[1]);bb=affinity.translate(body,x-old[0],y-old[1])
  if not board.covers(bb) or bb.intersects(box(87,40.25,135,61.25)):continue
  if cc.intersects(fixed) or any(bb.intersects(v) for v in bodies):continue
  d['x'],d['y']=x,y;bodies.append(bb);fixed=unary_union([fixed,cc.buffer(.18)]);print(ref,x,y,flush=True);break
 else:raise Exception(ref)
p.write_text(json.dumps(ds,indent=2))
