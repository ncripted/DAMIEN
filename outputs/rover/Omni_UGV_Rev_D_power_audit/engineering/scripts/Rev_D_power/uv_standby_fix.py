from pathlib import Path
import re,json
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit')
p=r/'cell_undervoltage.kicad_sch';s=p.read_text()
# Q9 emitter and its reset pullups run from protected VBAT, not the raw cell.
# Keep only U10/MR/C30 on raw CELL_P so the supervisor does not bypass the emergency cutoff with 100uA loads.
# These labels are at known individual pin stubs in the generated sheet.
for x,y in [(142.24,33.02),(50.8,134.62),(233.68,134.62)]:
 pass
import sys
sys.path.insert(0,'work/humanize');from build import blocks
parts=json.loads(Path('work/power-rev-d/new_parts.json').read_text())
# Compute label coordinates from native symbol pin direction and locate exact labels.
libtext=(r/'UGV.kicad_sym').read_text();libs={re.search(r'^\(symbol "([^"]+)',t)[1]:t for a,b,t in blocks(libtext) if t.startswith('(symbol')}
changes=[]
for d in parts:
 if d['ref'] not in ['Q9','R46','R48']:continue
 n='2' if d['ref']=='Q9' else '1';d['nets'][n]='VBAT'
 pdef=next(p for a,b,u in blocks(libs[d['key']]) if u.startswith('(symbol') for a,b,p in blocks(u) if p.startswith('(pin ') and f'(number "{n}"' in p)
 import math
 x,y,ang=map(float,re.search(r'\(at ([^)]+)',pdef)[1].split());lx=round(d['sx']+x-5.08*math.cos(math.radians(ang)),5);ly=round(d['sy']-y+5.08*math.sin(math.radians(ang)),5)
 for a,b,t in blocks(s):
  if t.startswith('(global_label "CELL_P"') and f'(at {lx} {ly} ' in t:changes.append((a,b,t.replace('"CELL_P"','"VBAT"',1)))
for a,b,t in sorted(changes,reverse=True):s=s[:a]+t+s[b:]
assert len(changes)==3,len(changes);p.write_text(s)
Path('work/power-rev-d/new_parts.json').write_text(json.dumps(parts,indent=2))
d=json.loads((r/'design_connections.json').read_text());nd={x['ref']:x for x in parts}
for x in d:
 if x['ref'] in ['Q9','R46','R48']:x['nets']=nd[x['ref']]['nets']
(r/'design_connections.json').write_text(json.dumps(d,indent=2))
print('UV pullups moved to protected VBAT; raw-cell standby is supervisor only')
