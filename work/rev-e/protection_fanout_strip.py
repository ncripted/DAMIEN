from pathlib import Path
import sys,json
sys.path.insert(0,'work/humanize');from build import blocks
p=Path('outputs/rover/Omni_UGV_Rev_E_power_layout/omni_ugv.kicad_pcb');s=p.read_text();rm=[]
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(f'(net "{n}")' in t for n in ['PROT_PACK','PROT_CHG']):rm.append(t);s=s[:a]+s[b:]
p.write_text(s);Path('work/rev-e/step3-gate-fanout-removed.json').write_text(json.dumps(rm));print('Reserved protection gate/sense escape space:',len(rm),'copper objects')
