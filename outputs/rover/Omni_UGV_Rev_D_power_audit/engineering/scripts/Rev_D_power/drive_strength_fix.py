from pathlib import Path
import json,re,csv,sys
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');changes={'R24':'10k','R25':'47k','R47':'22k','R50':'33k','R52':'4.7k'}
for fn in ['design_connections.json']:
 ds=json.loads((r/fn).read_text())
 for d in ds:
  if d['ref'] in changes:d['value']=changes[d['ref']]
 (r/fn).write_text(json.dumps(ds,indent=2))
p=Path('work/power-rev-d/new_parts.json');ds=json.loads(p.read_text())
for d in ds:
 if d['ref'] in changes:d['value']=changes[d['ref']]
p.write_text(json.dumps(ds,indent=2))
for fn in ['interlock.kicad_sch','cell_undervoltage.kicad_sch']:
 p=r/fn;s=p.read_text()
 for a,b,t in reversed(list(blocks(s))):
  if not t.startswith('(symbol'):continue
  m=re.search(r'\(property "Reference" "([^"]+)',t)
  if m and m[1] in changes:
   t=re.sub(r'(\(property "Value" )"[^"]*"',lambda z:z[1]+json.dumps(changes[m[1]]),t,count=1);s=s[:a]+t+s[b:]
 p.write_text(s)
with (r/'BOM.csv').open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
for d in rows:
 if d['Reference'] in changes:d['Value']=changes[d['Reference']]
with (r/'BOM.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print('Checked forced-beta and gate-leakage corner; strengthened gate pullup and inhibit base drives')
