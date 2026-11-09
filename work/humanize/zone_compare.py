from pathlib import Path
import sys,re
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_B_protection');s=(r/'omni_ugv.kicad_pcb').read_text();f=next(t for a,b,t in blocks(s) if t.startswith('(footprint ') and '(property "Reference" "U1"' in t)
for name,t in [('board',f),('lib',(r/'UGV.pretty/RF_Module__ESP32-S3-WROOM-1.kicad_mod').read_text())]:
 print(name)
 for a,b,z in blocks(t):
  if z.startswith('(zone'):print(z)
