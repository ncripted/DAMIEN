from pathlib import Path
import json,sys
sys.path.insert(0,'work/humanize');from build import blocks
p=Path('outputs/rover/Omni_UGV_Rev_E_power_layout/omni_ugv.kicad_pcb');s=p.read_text();ids=json.loads(Path('work/rev-e/remove-pad-vias.json').read_text())
for a,b,t in reversed(list(blocks(s))):
 if t.startswith('(via') and any(i in t for i in ids):s=s[:a]+s[b:]
p.write_text(s)
