exec(open('work/rev-e/router.py').read().split('def route(')[0])
import sys
sys.path.insert(0,'work/humanize');from build import blocks
ps1=[pad('Q8',i)['geo'] for i in [1,2,3]]+[pad('R41',2)['geo'],pad('R39',1)['geo']];ids={t['uuid'] for t in tracks if t['net'] in ['CELL_P','CELL_SWITCHED'] or (t['net']=='VBAT' and any(t['geo'].intersects(d) for d in ps1))}
p=Path('outputs/rover/Omni_UGV_Rev_E_power_layout/omni_ugv.kicad_pcb');s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(i in t for i in ids):s=s[:a]+s[b:]
p.write_text(s);Path('work/rev-e/corrected-cutoff-strip.json').write_text(json.dumps(sorted(ids)));print('Rebuilding',len(ids),'raw/protected power objects')
