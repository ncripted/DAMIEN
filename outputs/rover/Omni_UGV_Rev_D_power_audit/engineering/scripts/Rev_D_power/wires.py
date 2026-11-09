exec(open('work/power-rev-d/locate.py').read().split('for name')[0])
s=Path('outputs/rover/Omni_UGV_Rev_C_flex_camera/regulator.kicad_sch').read_text()
for a,b,t in blocks(s):
 if t.startswith('(wire'):
  pts=[tuple(map(float,v)) for v in re.findall(r'\(xy ([^ ]+) ([^)]+)',t)]
  if any(x<65 and y<115 for x,y in pts):print(pts)
