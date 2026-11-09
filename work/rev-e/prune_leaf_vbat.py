exec(open('work/rev-e/router.py').read().split('def route(')[0])
from shapely.strtree import STRtree
import sys
sys.path.insert(0,'work/humanize');from build import blocks
net='VBAT';ts1=[t for t in tracks if t['net']==net];ds=[d for d in pads if d['net']==net];centers=[Point(t['a']) if t['via'] else LineString([t['a'],t['z']]) for t in ts1];tree=STRtree(centers);gone=set()
for k in range(100):
 remove=set()
 for i,t in enumerate(ts1):
  if i in gone or t['via']:continue
  for end in [t['a'],t['z']]:
   pt=Point(end)
   if any(t['layer'] in d['layers'] and d['geo'].distance(pt)<t['width']/2+.003 for d in ds):continue
   connected=False
   for j in tree.query(pt.buffer(1)):
    j=int(j);u=ts1[j]
    if i==j or j in gone or (not u['via'] and u['layer']!=t['layer']):continue
    if centers[j].distance(pt)<(.3+t['width']/2+.003 if u['via'] else .003):connected=True;break
   if not connected:remove.add(i);break
 if not remove:break
 gone.update(remove)
ids={ts1[i]['uuid'] for i in gone};p=Path('outputs/rover/Omni_UGV_Rev_E_power_layout/omni_ugv.kicad_pcb');Path('work/rev-e/pre-leaf-prune.kicad_pcb').write_bytes(p.read_bytes());s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith('(segment') and any(i in t for i in ids):s=s[:a]+s[b:]
p.write_text(s);Path('work/rev-e/vbat-pruned.json').write_text(json.dumps(sorted(ids)));print('Pruned',len(ids),'centerline leaf segments')
