from pathlib import Path
import sys,re,json,csv
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit')
# Increase UV clamp base current for a conservative forced-beta bound at the low rail.
for fn in ['design_connections.json']:
 p=r/fn;d=json.loads(p.read_text())
 for v in d:
  if v['ref']=='R52':v['value']='3.3k'
 p.write_text(json.dumps(d,indent=2))
p=r/'cell_undervoltage.kicad_sch';s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith('(symbol') and '(property "Reference" "R52"' in t:t=re.sub(r'(\(property "Value" )"[^"]+"',r'\1"3.3k"',t,count=1);s=s[:a]+t+s[b:]
p.write_text(s)
p=Path('work/power-rev-d/new_parts.json');ds=json.loads(p.read_text())
for d in ds:
 if d['ref']=='R52':d['value']='3.3k'
p.write_text(json.dumps(ds,indent=2))
with (r/'BOM.csv').open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
for d in rows:
 if d['Reference']=='R52':d['Value']='3.3k'
with (r/'BOM.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
