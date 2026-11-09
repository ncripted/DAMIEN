from pathlib import Path
import sys,re,json,csv
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');changes={'R24':'22k','R25':'56k'}
p=r/'design_connections.json';d=json.loads(p.read_text())
for z in d:
 if z['ref'] in changes:z['value']=changes[z['ref']]
p.write_text(json.dumps(d,indent=2))
p=r/'interlock.kicad_sch';s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 m=re.search(r'\(property "Reference" "([^"]+)',t)
 if t.startswith('(symbol') and m and m[1] in changes:t=re.sub(r'(\(property "Value" )"[^"]+"',lambda z:z[1]+json.dumps(changes[m[1]]),t,count=1);s=s[:a]+t+s[b:]
p.write_text(s)
with (r/'BOM.csv').open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
for d in rows:
 if d['Reference'] in changes:d['Value']=changes[d['Reference']]
with (r/'BOM.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
for fn in ['engineering/POWER_AUDIT.md','.pcba-workflow/circuit-review.md','CHANGELOG.md']:
 p=r/fn;s=p.read_text(encoding='utf-8').replace('R24 becomes 10 kΩ and R25 47 kΩ','R24 becomes 22 kΩ and R25 56 kΩ').replace('R24 to10k and R25 to47k','R24 to22k and R25 to56k');p.write_text(s,encoding='utf-8')
p=r/'engineering/POWER_CALCULATIONS.json';d=json.loads(p.read_text());d['drive_buffer']['max_static_output_load_A_using_VBE_0p4_R25_min_1pct']=(3.6-.4)/(56000*.99)+3.6/(1e6*.99)+32e-6;d['drive_buffer']['nSLEEP_input_current_engineering_envelope_A_each']=16e-6;d['drive_buffer']['gate_pull_current_A_bound']=4.2/(22000*.99)+20e-6;d['drive_buffer']['Q3_base_current_A_bound']=(2.9-.95)/(56000*1.01)-.95/(100000*.99);d['drive_buffer']['Q3_forced_beta_bound']=d['drive_buffer']['gate_pull_current_A_bound']/d['drive_buffer']['Q3_base_current_A_bound'];assert d['drive_buffer']['Q3_forced_beta_bound']<10;assert d['drive_buffer']['max_static_output_load_A_using_VBE_0p4_R25_min_1pct']<100e-6;p.write_text(json.dumps(d,indent=2));print('Final buffer/gate loading envelope',d['drive_buffer'])
