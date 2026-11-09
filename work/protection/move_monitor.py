from pathlib import Path
import json,re
root=Path('outputs/rover/Omni_UGV_Rev_B_protection');p=root/'omni_ugv.kicad_pcb';s=p.read_text()
src=Path('work/protection/dedup.py').read_text();exec(src[src.index('def blocks'):src.index('seen=set()')])
# Identify new +3V3 trace/via geometry from the last signal-routing record, not all rail copper.
routes=json.loads(Path('work/protection/signal-routes-final.json').read_text())
keys=set()
for t in routes:
 if t['net']=='+3V3':keys.add((t['via'],tuple(round(x,5) for x in t['a']),tuple(round(x,5) for x in t['z'])))
ed=[]
for a,z,t in blocks(s):
 if not t.startswith(('(segment','(via')):continue
 n=re.search(r'\(net "([^"]+)"',t)[1]
 pts=[tuple(round(float(x),5) for x in m) for m in re.findall(r'\((?:start|end|at)\s+([-\d.]+)\s+([-\d.]+)\)',t)]
 k=(t.startswith('(via'),pts[0],pts[-1])
 if n=='CELL_TEMP_DIV' or (n=='+3V3' and k in keys):ed.append((a,z))
for a,z in reversed(ed):s=s[:a]+s[z:]
p.write_text(s)
print('Detached',len(ed),'monitor-route objects')
