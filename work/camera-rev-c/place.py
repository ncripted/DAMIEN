import sys,json,math
from pathlib import Path
sys.path.insert(0,'work/protection/deps')
from shapely.geometry import Polygon,Point,LineString,box
from shapely import affinity,unary_union
g=json.loads(Path('work/camera-rev-c/geometry.json').read_text());ds=json.loads(Path('work/camera-rev-c/new_parts.json').read_text());new={x['ref'] for x in ds}
board=unary_union([Polygon(o,h) for o,h in g['outline']]).buffer(-.4)
def pg(d):
 w,h=d['size'];return affinity.translate(affinity.rotate(box(-w/2,-h/2,w/2,h/2),-d['angle']),*d['at'])
pads=[(d,pg(d)) for d in g['pads']];obs=[v.buffer(.18) for d,v in pads if d['ref'] not in new]
for t in g['tracks']:obs.append((Point(t['a']) if t['via'] else LineString([t['a'],t['z']])).buffer(t['width']/2+.18))
fixed=unary_union(obs);bodies=[]
for f in g['footprints']:
 if f['ref'] in new:continue
 pp=[p for d,p in pads if d['ref']==f['ref']];bodies.append(box(*unary_union(pp).bounds).buffer(.35))
placed=[]
for ref in ['J3','U8','C26','C27','U9','C28','C29','R44','R45']:
 d=next(x for x in ds if x['ref']==ref);pp=[v for a,v in pads if a['ref']==ref];cu=unary_union(pp);old=next(f['at'] for f in g['footprints'] if f['ref']==ref);tx,ty=d['x'],d['y']
 # Place bypass capacitors near their regulator, adjusted by accepted regulator motion.
 if ref in ['C26','C27','C28','C29']:
  u='U8' if ref in ['C26','C27'] else 'U9';prev=next(x for x in ds if x['ref']==u);dx,dy=prev['shift'];tx+=dx;ty+=dy
 candidates=sorted([(tx+dx*.25,ty+dy*.25) for dx in range(-55,56) for dy in range(-55,56)],key=lambda v:math.dist(v,(tx,ty)))
 for x,y in candidates:
  cc=affinity.translate(cu,x-old[0],y-old[1]);body=box(*cc.bounds).buffer(.75)
  if not board.covers(body) or body.intersects(box(87,40.25,135,61.25)):continue
  if cc.intersects(fixed) or any(body.intersects(v) for v in bodies+placed):continue
  d['shift']=[x-d['x'],y-d['y']];d['x'],d['y']=x,y;placed.append(body);fixed=unary_union([fixed,cc.buffer(.18)]);print(ref,x,y);break
 else:raise RuntimeError('No legal placement '+ref)
Path('work/camera-rev-c/new_parts.json').write_text(json.dumps(ds,indent=2))
