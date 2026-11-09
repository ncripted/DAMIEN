from pathlib import Path
import json,sys
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');rep=json.loads((r/'validation/current/drc.json').read_text());ids=set()
for v in rep['violations']:
 if v['type'] in ['clearance','shorting_items','solder_mask_bridge'] and any('CHG_DISABLE' in i['description'] for i in v['items']):
  ids.update(i['uuid'] for i in v['items'] if ('Track [GND]' in i['description'] or 'Via [GND]' in i['description']))
p=r/'omni_ugv.kicad_pcb';s=p.read_text();rm=[]
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(i in t for i in ids):rm.append(t);s=s[:a]+s[b:]
p.write_text(s);Path('work/power-rev-d/ce-isolation-removed.json').write_text(json.dumps(list(ids),indent=2));print('Isolated CE from',len(rm),'former ground copper objects')
