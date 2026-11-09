from pathlib import Path
import sys
sys.path.insert(0,'work/humanize');from build import blocks
p=Path('outputs/rover/Omni_UGV_Rev_E_power_layout/omni_ugv.kicad_pcb');s=p.read_text();ids=['be3ce334-b42c-4f51-a455-720ef7b37e9b','e74e1d4f-4ee0-488f-8397-beee2e0cb94c','c7b3910f-0f4b-47ee-bac7-0619c76fc391','fc4fe004-6bea-4796-8543-cc702bf39c29']
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(i in t for i in ids):s=s[:a]+s[b:]
p.write_text(s)
