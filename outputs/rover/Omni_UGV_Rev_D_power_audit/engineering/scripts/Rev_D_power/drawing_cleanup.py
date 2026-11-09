from pathlib import Path
import sys,re
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit')
for fn in ['cell_undervoltage.kicad_sch','charge_temperature.kicad_sch']:
 p=r/fn;s=p.read_text()
 for a,b,t in reversed(list(blocks(s))):
  if t.startswith('(global_label'):
   mm=re.search(r'\(at ([^ ]+) ([^ ]+) ([^)]+)\)',t)
   if int(mm[3]) in [90,270]:t=t[:mm.start()]+f'(at {mm[1]} {mm[2]} 0)'+t[mm.end():];t=t.replace('(justify right bottom)','(justify left bottom)')
  elif t.startswith('(symbol'):
   mm=re.search(r'\(at ([^ ]+) ([^ ]+) ([^)]+)\)',t);x,y=float(mm[1]),float(mm[2])
   for k,dy in [('Reference',20.32),('Value',17.78)]:
    t=re.sub(r'(\(property "'+k+r'" "[^"]+" \(at )[^)]+',lambda m:m[1]+f'{x} {y-dy} 0',t,count=1)
  s=s[:a]+t+s[b:]
 p.write_text(s)
