from pathlib import Path
import re
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit')
for p in r.glob('*.kicad_sch'):
 s=p.read_text();s=re.sub(r'\(rev "[^"]*"\)','(rev "D - prototype")',s);s=s.replace('REV B PROTOTYPE','REV D PROTOTYPE');p.write_text(s)
