import sys,json,math
from pathlib import Path
sys.path.insert(0,str(Path('work/protection/deps').resolve()))
from shapely.geometry import Polygon,Point,LineString,box
from shapely import affinity,unary_union
g=json.loads(Path('work/protection/geometry.json').read_text());new=json.loads(Path('work/protection/new_parts.json').read_text());refs={d['ref'] for d in new}
board=unary_union([Polygon(o,holes) for o,holes in g['outline']]);inside=board.buffer(-.32)
def padshape(d):
 w,h=d['size'];x,y=d['at']
 if d['shape']==0:return Point(x,y).buffer(w/2)
 return affinity.translate(affinity.rotate(box(-w/2,-h/2,w/2,h/2),-d['angle']),x,y)
def trshape(t):return (Point(t['a']) if t['via'] or t['a']==t['z'] else LineString([t['a'],t['z']])).buffer(t['width']/2)
ob=[]
for d in g['pads']:
 if d['ref'] in refs:continue
 if 'B.Cu' in d['layers']:ob.append(padshape(d).buffer(.17))
 if max(d['drill']):ob.append(Point(d['at']).buffer(max(d['drill'])/2+.27))
for t in g['tracks']:
 if t['via'] or t['layer']=='B.Cu':ob.append(trshape(t).buffer(.17 if not t['via'] else max(.17,.25+t['drill']/2-t['width']/2)))
fixed=unary_union(ob)
if '--place' in sys.argv:
 # Start with power FET pair facing their drain lands inward, keeping raw copper compact.
 targets={'Q7':(121,138),'Q8':(115,138),'R36':(113,127),'U7':(109,130),'R37':(110,133),'R38':(110,135),'R39':(106,130),'C24':(109,127),'R40':(122,134),'R41':(115,134),'J5':(126,91),'R42':(125,95),'R43':(129,95),'C25':(132,95)}
 placed=[];positions={}
 for ref in ['R36','Q7','Q8','U7','C24','R37','R38','R39','R40','R41','J5','R42','R43','C25']:
  d=next(x for x in new if x['ref']==ref);fp=next(x for x in g['footprints'] if x['ref']==ref);tx,ty=targets[ref];px,py=fp['at'];pads=[x for x in g['pads'] if x['ref']==ref and x['num']]
  candidates=sorted([(tx+dx*.25,ty+dy*.25) for dx in range(-24,25) for dy in range(-24,25)],key=lambda z:(z[0]-tx)**2+(z[1]-ty)**2)
  for x,y in candidates:
   shapes=[affinity.translate(padshape(a),x-px,y-py) for a in pads]
   cu=unary_union(shapes)
   # Courtyard-style body bounding envelope, used on B side. J5 remains F but no pad collisions permitted.
   body=box(*cu.bounds).buffer(.4)
   if not inside.covers(body) or cu.intersects(fixed) or any(body.intersects(b) for b in placed):continue
   positions[ref]=[x,y];placed.append(body);fixed=unary_union([fixed,cu.buffer(.17)])
   print(ref,positions[ref]);break
  else:raise RuntimeError('No legal location for '+ref)
 Path('work/protection/placements.json').write_text(json.dumps(positions,indent=2))
else:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.patches import Polygon as Patch
 fig,ax=plt.subplots(figsize=(12,10))
 for poly in (list(board.geoms) if hasattr(board,'geoms') else [board]):
  ax.plot(*poly.exterior.xy,c='black')
  for r in poly.interiors:ax.plot(*r.xy,c='black')
 for t in g['tracks']:
  if t['layer']=='B.Cu' or t['via']:
   sh=trshape(t);ax.add_patch(Patch(list(sh.exterior.coords),color='#4477aa',alpha=.5))
 for d in g['pads']:
  if 'B.Cu' in d['layers'] or max(d['drill']):
   sh=padshape(d);ax.add_patch(Patch(list(sh.exterior.coords),color='#cc5533' if d['ref'] in refs else '#777777',alpha=.8))
 for f in g['footprints']:
  if f['ref'] in refs:ax.text(*f['at'],f['ref'],fontsize=9)
 ax.set_xlim(70,135);ax.set_ylim(148,117);ax.set_aspect('equal');ax.grid(alpha=.2);ax.set_title('Bottom copper and proposed protection placement (viewed through board)')
 fig.savefig('work/protection/layout.png',dpi=150,bbox_inches='tight')
