from pathlib import Path
import re
for p in Path('outputs/rover/Omni_UGV_Rev_B_protection').glob('*.kicad_sch'):
 s=re.sub(r'"(?:[^"\\]|\\.)*"','',p.read_text())
 print(p.name,s.count('(')-s.count(')'))
