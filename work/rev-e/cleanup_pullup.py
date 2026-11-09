exec(open('work/rev-e/router.py').read().split('def route(')[0])
from shapely.strtree import STRtree
import sys
sys.path.insert(0,'work/humanize');from build import blocks
net='VBAT';ts1=[t for t in tracks if t['net']==net];tree=STRtree([t['geo'] for t in ts1]);idx={t['uuid']:i for i,t in enumerate(ts1)};bad=set()
for seed in ['f55c67d2-87a9-4f1b-a7ba-8765c9dde0be','fccf7362-bc2a-417f-a7e7-b4e8491cdd99']:
 stack=[idx[seed]];seen=set(stack)
 while stack:
  i=stack.pop();t=ts1[i]
  for j in tree.query(t['geo'].buffer(.003)):
   j=int(j);u=ts1[j]
   if j not in seen and (t['via'] or u['via'] or t['layer']==u['layer']) and t['geo'].distance(u['geo'])<.003:seen.add(j);stack.append(j)
 touches=[d for d in pads if d['net']==net and any((ts1[i]['via'] or ts1[i]['layer'] in d['layers']) and ts1[i]['geo'].distance(d['geo'])<.003 for i in seen)]
 print('VBAT',len(seen),'padcount',len(touches))
 if not touches:bad.update(ts1[i]['uuid'] for i in seen)
# Remove only dangling portion at former R46 pad; the other side belongs to the real VBAT network.
bad.update(['f55c67d2-87a9-4f1b-a7ba-8765c9dde0be','cdaedeac-f993-41ab-b77d-6e8cb71bf765'])
p=Path('outputs/rover/Omni_UGV_Rev_E_power_layout/omni_ugv.kicad_pcb');s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(i in t for i in bad):s=s[:a]+s[b:]
p.write_text(s);print('Removed',len(bad),'old pullup objects')
