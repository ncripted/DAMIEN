from pathlib import Path
import json,sys
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');rep=json.loads((r/'validation/current/drc.json').read_text());ids={i['uuid'] for v in rep['violations'] if v['type']=='track_dangling' for i in v['items']};p=r/'omni_ugv.kicad_pcb';s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith('(segment') and any(i in t for i in ids):s=s[:a]+s[b:]
p.write_text(s);Path('work/power-rev-d/dangling-removed.json').write_text(json.dumps(list(ids)));print('Removed',len(ids),'dangling stubs; connectivity recheck required')
