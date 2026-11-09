from pathlib import Path
import json,math,sys
sys.path.insert(0,'work/protection/deps')
from shapely.geometry import Point,LineString,box,Polygon
from shapely import affinity,unary_union
p=Path('work/rev-e/geometry.json');g=json.loads(p.read_text())
# Identify narrow current paths and strengthen copper only where clearance permits.
def pg(d):
 w,h=d['size'];return affinity.translate(affinity.rotate(box(-w/2,-h/2,w/2,h/2),-d['angle']),*d['at'])
def tg(t):return (Point(t['a']) if t['via'] else LineString([t['a'],t['z']])).buffer(t['width']/2)
polys=[(d['net'],d['layers'],pg(d)) for d in g['pads']];polys +=[(t['net'],['F.Cu','B.Cu','In1.Cu','In2.Cu'] if t['via'] else [t['layer']],tg(t)) for t in g['tracks']]
out=[];targets={'CELL_P':1.5,'CELL_N':1.5,'VBAT':1.5,'VMOTOR':1.5,'MOTOR_MID':1.5,'SYS_RAW':.8}
for t in g['tracks']:
 if t['via'] or t['net'] not in targets:continue
 # Leave low-current sense/bias branches alone; examine wide trunks plus all VMOTOR pad escapes.
 if t['width']<.45 and t['net']!='VMOTOR':continue
 line=LineString([t['a'],t['z']]);clear=min((line.distance(v) for n,ls,v in polys if n!=t['net'] and t['layer'] in ls and v.distance(line)<2),default=10)
 width=min(targets[t['net']],math.floor(max(0,2*(clear-.18))/.05)*.05)
 if width>t['width']+.02:out.append(dict(uuid=t['uuid'],old=t['width'],new=round(width,3),net=t['net'],length_mm=math.dist(t['a'],t['z'])))
Path('work/rev-e/step2-width-changes.json').write_text(json.dumps(out,indent=2));print('Clearance-limited widening:',len(out),'segments;',round(sum(v['length_mm'] for v in out),2),'mm')
