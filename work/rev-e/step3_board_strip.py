from pathlib import Path
import json,sys,re
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');g=json.loads(Path('work/rev-e/geometry.json').read_text());bad=set()
for t in g['tracks']:
 pts=[t['a'],t['z']]
 if t['net']=='PROT_VDD':bad.add(t['uuid'])
 if t['net']=='CELL_N' and t['width']<=.65 and any(117.65<x<120.6 and 121.5<y<126.3 for x,y in pts):bad.add(t['uuid'])
 if t['net']=='GND' and any(118.5<x<119.5 and 121.65<y<122.75 for x,y in pts):bad.add(t['uuid'])
s=(r/'omni_ugv.kicad_pcb').read_text()
for a,b,t in reversed(list(blocks(s))):
 if (t.startswith('(footprint') and '(property "Reference" "R36"' in t) or (t.startswith(('(segment','(via')) and any(i in t for i in bad)):s=s[:a]+s[b:]
(r/'omni_ugv.kicad_pcb').write_text(s);Path('work/rev-e/step3-copper-removed.json').write_text(json.dumps(sorted(bad)));print('Stripped old shunt and',len(bad),'local supply/sense copper objects')
