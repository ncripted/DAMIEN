from pathlib import Path
import json,sys,math
sys.path.insert(0,'work/protection/deps')
from shapely.geometry import Polygon,box,Point
from shapely import unary_union,affinity
p=Path('work/power-rev-d/silk-geometry.json');g=json.loads(p.read_text());b=json.loads(Path('work/power-rev-d/geometry.json').read_text());outline=unary_union([Polygon(o,h) for o,h in b['outline']]).buffer(-.8)
fixed=unary_union([box(*v).buffer(.24) for v in g['fixed']]);results=[]
for d in sorted(g['moving'],key=lambda d:0 if d['id']=='signature' else 1):
 at=d['at'];body=box(*d['bbox']);found=False
 for x,y in sorted([(at[0]+dx*.25,at[1]+dy*.25) for dx in range(-64,65) for dy in range(-64,65)],key=lambda v:math.dist(v,at)):
  moved=affinity.translate(body,x-at[0],y-at[1])
  if not outline.covers(moved) or moved.intersects(fixed):continue
  results.append(dict(id=d['id'],at=[x,y]));fixed=unary_union([fixed,moved.buffer(.24)]);found=True;break
 if not found:raise Exception('No legal silkscreen position '+d['id'])
Path('work/power-rev-d/silk-positions.json').write_text(json.dumps(results,indent=2));print('Placed',len(results),'visible labels at >=0.8mm text height')
