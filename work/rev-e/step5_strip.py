from pathlib import Path
import json,sys
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');g=json.loads(Path('work/rev-e/geometry.json').read_text());ids={t['uuid'] for t in g['tracks'] if t['net']=='CELL_P'}
# Detach just the old protected-rail pullup terminal, then reconnect it on raw cell supply.
d=next(p for p in g['pads'] if p['ref']=='R46' and p['num']=='1');x,y=d['at'];w,h=d['size']
ids.update(t['uuid'] for t in g['tracks'] if t['net']=='VBAT' and any(abs(px-x)<w/2+.02 and abs(py-y)<h/2+.02 for px,py in [t['a'],t['z']]))
p=r/'omni_ugv.kicad_pcb';s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(i in t for i in ids):s=s[:a]+s[b:]
p.write_text(s);Path('work/rev-e/step5-removed.json').write_text(json.dumps(sorted(ids)));print('Isolated',len(ids),'raw-cell/pullup copper objects')
