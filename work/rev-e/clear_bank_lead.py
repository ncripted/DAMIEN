exec(open('work/rev-e/router.py').read().split('def route(')[0])
import sys
sys.path.insert(0,'work/humanize');from build import blocks
routes=json.loads(Path('work/rev-e/final-bank-routes.json').read_text());target=[t for t in routes if t['net']=='PROTECTED_RAW' and not t['via'] and t['layer']=='B.Cu' and max(t['a'][0],t['z'][0])<120 and not(math.dist(t['a'],(117,136.3))<.003 and any(math.dist(t['z'],pt)<.003 for pt in [(117.1,135.4),(118,135.3)]))]
ids={t['uuid'] for t in tracks if any(t['net']==u['net'] and t['layer']==u['layer'] and not t['via'] and math.dist(t['a'],u['a'])<.003 and math.dist(t['z'],u['z'])<.003 for u in target)}
p=Path('outputs/rover/Omni_UGV_Rev_E_power_layout/omni_ugv.kicad_pcb');s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith('(segment') and any(i in t for i in ids):s=s[:a]+s[b:]
p.write_text(s);print('Releasing power lead to preserve gate corridor',len(ids))
