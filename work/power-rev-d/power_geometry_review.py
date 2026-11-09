import json,collections,math
from pathlib import Path
g=json.loads(Path('work/power-rev-d/geometry.json').read_text())
for n in ['CELL_P','CELL_N','VBAT','VMOTOR','SYS_RAW','M2_A','REG_L1','REG_L2']:
 ts=[t for t in g['tracks'] if t['net']==n];print(n,'width mm/length mm',[(w,round(sum(math.dist(t['a'],t['z']) for t in ts if t['width']==w and not t['via']),2)) for w in sorted({t['width'] for t in ts if not t['via']})]);print('In1',[(t['width'],math.dist(t['a'],t['z'])) for t in ts if t['layer']=='In1.Cu'])
for ref in ['U7','R36','C24']:
 print(ref,[(d['num'],d['net'],d['at']) for d in g['pads'] if d['ref']==ref])
