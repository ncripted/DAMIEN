from pathlib import Path
import sys
sys.path.insert(0,'work/humanize');from build import blocks
p=Path('outputs/rover/Omni_UGV_Rev_E_power_layout/omni_ugv.kicad_pcb');s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith('(segment') and '08403ab3-696a-4337-a2f3-e4fb5cef3614' in t:s=s[:a]+s[b:]
p.write_text(s)
