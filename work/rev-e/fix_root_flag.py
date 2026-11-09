from pathlib import Path
import sys,re
sys.path.insert(0,'work/humanize');from build import blocks
p=Path('outputs/rover/Omni_UGV_Rev_E_power_layout/omni_ugv.kicad_sch');s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith('(global_label "PROT_VSS_SENSE"'):s=s[:a]+re.sub(r'\(at [^)]+\)','(at 142.24 266.7 0)',t,count=1)+s[b:]
p.write_text(s)
