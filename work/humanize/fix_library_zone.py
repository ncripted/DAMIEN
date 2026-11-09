from pathlib import Path
import re,sys
sys.path.insert(0,str(Path('work/humanize').resolve()))
from build import blocks
p=Path('outputs/rover/Omni_UGV_Rev_B_protection/UGV.pretty/RF_Module__ESP32-S3-WROOM-1.kicad_mod');s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if not t.startswith('(zone'):continue
 pts=[tuple(map(float,m)) for m in re.findall(r'\(xy ([-\d.]+) ([-\d.]+)\)',t)]
 if min(x for x,y in pts)>50:
  t=re.sub(r'\(xy ([-\d.]+) ([-\d.]+)\)',lambda m:f'(xy {float(m[1])-111:g} {float(m[2])-68:g})',t)
  s=s[:a]+t+s[b:]
p.write_text(s)
print('Library keepout converted from board coordinates to local coordinates; board geometry unchanged.')
