exec(open('work/rev-e/router.py').read().split('def route(')[0])
import sys
sys.path.insert(0,'work/humanize');from build import blocks
ids={t['uuid'] for t in tracks if t['net']=='PROT_CHG'}
for t in tracks:
 if t['net']=='VBAT' and ((t['via'] and any(math.dist(t['a'],pt)<.003 for pt in [(115.2,135.2),(115,136)])) or (not t['via'] and t['width']==.3 and any(math.dist(t['a'],pt)<.003 or math.dist(t['z'],pt)<.003 for pt in [(115.2,135.2),(115,136)]))):ids.add(t['uuid'])
p=Path('outputs/rover/Omni_UGV_Rev_E_power_layout/omni_ugv.kicad_pcb');s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(i in t for i in ids):s=s[:a]+s[b:]
p.write_text(s);print('Removed unused bank trial and charge-gate fanout',len(ids))
banks=json.loads(Path('work/rev-e/final-via-banks.json').read_text());Path('work/rev-e/final-via-banks.json').write_text(json.dumps(banks[:3],indent=2))
