from pathlib import Path
import json,sys,re
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');rep=json.loads((r/'validation/current/drc.json').read_text());changes={x['uuid']:x for x in json.loads(Path('work/rev-e/step2-width-changes.json').read_text())};bad={i['uuid'] for v in rep['violations'] if v['type'] in ['clearance','hole_clearance'] for i in v['items'] if i['uuid'] in changes};Path('work/rev-e/step2-width-rejected.json').write_text(json.dumps(sorted(bad)))
s=(r/'omni_ugv.kicad_pcb').read_text();rm='26f3229a-da86-4c6d-90bf-00b112878767'
for a,b,t in reversed(list(blocks(s))):
 if t.startswith('(via') and rm in t:s=s[:a]+s[b:]
(r/'omni_ugv.kicad_pcb').write_text(s)
Path('work/rev-e/step2-width-accepted.json').write_text(json.dumps([v for k,v in changes.items() if k not in bad],indent=2));print('Rejected',len(bad),'width increases; removed redundant overlapping motor via')
