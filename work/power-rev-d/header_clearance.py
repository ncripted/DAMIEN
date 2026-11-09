from pathlib import Path
import sys,re
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit')
for fn in ['cell_undervoltage.kicad_sch','charge_temperature.kicad_sch']:
 p=r/fn;s=p.read_text()
 for a,b,t in reversed(list(blocks(s))):
  if not t.startswith('(symbol'):continue
  m=re.search(r'\(property "Reference" "([^"]+)',t)
  if not m or m[1] not in ['U10','U11','U12','U13','U14','Q9','Q10','Q11','U14']:continue
  x,y,an=map(float,re.search(r'\(at ([^)]+)',t)[1].split());dx=16 if m[1] in ['U12','U13','U14','Q9'] else 0
  for k,dy in [('Reference',15),('Value',12.46)]:
   for aa,bb,v in reversed(list(blocks(t))):
    if v.startswith('(property "'+k+'"'):
     v=re.sub(r'\(at [^)]+\)',f'(at {x+dx} {y-dy} 0)',v,count=1);t=t[:aa]+v+t[bb:]
  s=s[:a]+t+s[b:]
 p.write_text(s)
