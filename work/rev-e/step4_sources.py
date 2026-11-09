from pathlib import Path
import json,re,csv,sys
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');p=r/'omni_ugv.kicad_pcb';s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and ('"REG_L1"' in t or '"REG_L2"' in t):s=s[:a]+s[b:]
p.write_text(s)
data=json.loads((r/'design_connections.json').read_text());dm={d['ref']:d for d in data}
for ref in ['C18','C19','C20']:
 dm[ref].update(value='22u/10V X5R 20%',mpn='C2012X5R1A226M125AB',note='TDK production 0805, 22uF 10V +/-20% X5R. DC-bias/temperature/aging verification required; nominal capacitance is not effective capacitance.')
p=r/'regulator.kicad_sch';s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 for ref in ['C18','C19','C20']:
  if t.startswith('(symbol') and f'(property "Reference" "{ref}"' in t:t=re.sub(r'(\(property "Value" )"[^"]*"',lambda m:m[1]+json.dumps(dm[ref]['value']),t,count=1);s=s[:a]+t+s[b:]
p.write_text(s);(r/'design_connections.json').write_text(json.dumps(data,indent=2))
with (r/'BOM.csv').open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
for row in rows:
 if row['Reference'] in ['C18','C19','C20']:
  d=dm[row['Reference']];row.update(Value=d['value'],MPN=d['mpn'],Notes=d['note'])
with (r/'BOM.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
