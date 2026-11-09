from pathlib import Path
import json,sys
sys.path.insert(0,'work/humanize');from build import blocks
g=json.loads(Path('work/rev-e/geometry.json').read_text());ids={t['uuid'] for t in g['tracks'] if t['net']=='SYS_ON' and any(97<x<100 and 111<y<113 for x,y in [t['a'],t['z']])};p=Path('outputs/rover/Omni_UGV_Rev_E_power_layout/omni_ugv.kicad_pcb');s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(i in t for i in ids):s=s[:a]+s[b:]
p.write_text(s);print('Local EN objects removed',len(ids))
