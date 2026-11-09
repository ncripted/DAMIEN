exec(open('work/rev-e/router.py').read().split('def route(')[0])
from shapely.strtree import STRtree
import sys
sys.path.insert(0,'work/humanize');from build import blocks
bad=set();report=json.loads(Path('work/rev-e/step3-routed.json').read_text())
for v in report['violations']:
 if v['type']=='hole_to_hole':bad.add(v['items'][1]['uuid'])
for net,seeds in [('GND',['08403ab3-696a-4337-a2f3-e4fb5cef3614','4d9e36ef-6315-43ad-b9ff-b5ee5de3a25f','705871b4-1b9f-4bf1-8ddf-b39b643121c4']),('CELL_N',['0393b2cb-a899-43e4-abf0-985bdee854d5','0c4948ed-e0dd-49f3-88ee-6c2f7a853fbc'])]:
 ts1=[t for t in tracks if t['net']==net];tree=STRtree([t['geo'] for t in ts1]);idx={t['uuid']:i for i,t in enumerate(ts1)}
 for seed in seeds:
  if seed not in idx:continue
  stack=[idx[seed]];seen=set(stack)
  while stack:
   i=stack.pop();t=ts1[i]
   for j in tree.query(t['geo'].buffer(.003)):
    j=int(j);u=ts1[j]
    if j not in seen and (t['via'] or u['via'] or t['layer']==u['layer']) and t['geo'].distance(u['geo'])<.003:seen.add(j);stack.append(j)
  touches=[d for d in pads if d['net']==net and any((ts1[i]['via'] or ts1[i]['layer'] in d['layers']) and ts1[i]['geo'].distance(d['geo'])<.003 for i in seen)]
  print(net,'component',len(seen),'pads',[(d['ref'],d['num']) for d in touches])
  if not touches:bad.update(ts1[i]['uuid'] for i in seen)
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');p=r/'omni_ugv.kicad_pcb';s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(i in t for i in bad):s=s[:a]+s[b:]
p.write_text(s);Path('work/rev-e/step3-orphans-removed.json').write_text(json.dumps(sorted(bad)));print('Removed',len(bad))
