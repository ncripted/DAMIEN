exec(open('work/rev-e/router.py').read().split('def route(')[0])
import sys
sys.path.insert(0,'work/humanize');from build import blocks
ids={t['uuid'] for t in tracks if t['net'] in ['CUT_GATE','CUT_PNP_B'] or (t['net']=='CELL_P' and t['width']<=.2 and any(x>124 and y>125 for x,y in [t['a'],t['z']]))}
p=Path('outputs/rover/Omni_UGV_Rev_E_power_layout/omni_ugv.kicad_pcb');s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(i in t for i in ids):s=s[:a]+s[b:]
p.write_text(s);print('Freed bias routing for power fanout:',len(ids))
