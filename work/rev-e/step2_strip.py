from pathlib import Path
import json,sys,re
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');p=r/'omni_ugv.kicad_pcb';s=p.read_text();nets={f'M{i}_{x}' for i in [1,2,3] for x in ['A','B']};removed=[]
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(f'(net "{n}")' in t for n in nets):removed.append(t);s=s[:a]+s[b:]
p.write_text(s);Path('work/rev-e/step2-motor-removed.json').write_text(json.dumps(removed));print('Removed',len(removed),'old motor output copper objects for replacement')
