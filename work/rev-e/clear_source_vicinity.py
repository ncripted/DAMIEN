exec(open('work/rev-e/router.py').read().split('def route(')[0])
import sys
sys.path.insert(0,'work/humanize');from build import blocks
shapes=[pad('Q8',n)['geo'] for n in [1,2,3]]+[pad('R41',2)['geo'],pad('R39',1)['geo']];ids={t['uuid'] for t in tracks if t['net']=='VBAT' and any(t['geo'].distance(d)<.4 for d in shapes)}
p=Path('outputs/rover/Omni_UGV_Rev_E_power_layout/omni_ugv.kicad_pcb');s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(i in t for i in ids):s=s[:a]+s[b:]
p.write_text(s);print('Cleared former-source vicinity',len(ids))
