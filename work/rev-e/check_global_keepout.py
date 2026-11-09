from pathlib import Path
import sys,re,json
sys.path.insert(0,'work/humanize');from build import blocks
paths=[Path('outputs/rover/Omni_UGV_Rev_D_power_audit/omni_ugv.kicad_pcb'),Path('outputs/rover/Omni_UGV_Rev_E_power_layout/omni_ugv.kicad_pcb')];zones=[]
for p in paths:zones.append([re.sub(r'\s+','',t) for a,b,t in blocks(p.read_text()) if t.startswith('(zone') and '(keepout' in t])
assert zones[0] and zones[0]==zones[1];print('Global antenna keepout preserved:',len(zones[1]))
p=paths[1].parent/'validation/current/preservation-and-layout-proof.json';j=json.loads(p.read_text());j['global_antenna_keepout_exactly_preserved']=True;j['global_rule_area_count']=len(zones[1]);p.write_text(json.dumps(j,indent=2))
