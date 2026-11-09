import json,math
from pathlib import Path
g=json.loads(Path('work/rev-e/geometry.json').read_text())
for n in ['CELL_P','CELL_N','VBAT','VMOTOR','SYS_RAW','+3V3']:
 ts=[t for t in g['tracks'] if t['net']==n]
 print(n,'vias',[(t['a'],t['width'],t['drill']) for t in ts if t['via']])
for ref in ['U2','U3','M1','M2','M3','Q1','Q2','J2','R36']:
 print(ref,[(p['num'],p['net'],p['at'],p['size']) for p in g['pads'] if p['ref']==ref])
