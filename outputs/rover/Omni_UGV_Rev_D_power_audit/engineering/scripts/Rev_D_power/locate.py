import sys,re
from pathlib import Path
sys.path.insert(0,'work/humanize');from build import blocks
for name in ['regulator','charging']:
 s=Path('outputs/rover/Omni_UGV_Rev_C_flex_camera/'+name+'.kicad_sch').read_text();bs=list(blocks(s))
 lib=next(t for a,b,t in bs if t.startswith('(lib_symbols'))
 libs={re.search(r'^\(symbol "([^"]+)',t)[1]:t for a,b,t in blocks(lib)}
 for ref,num in ([('SW3','2')] if name=='regulator' else [('U5','4')]):
  t=next(t for a,b,t in bs if t.startswith('(symbol') and f'(property "Reference" "{ref}"' in t)
  x,y,ang=map(float,re.search(r'\(at ([^)]+)',t)[1].split());key=re.search(r'\(lib_id "([^"]+)',t)[1]
  pp=[p for a,b,u in blocks(libs[key]) if u.startswith('(symbol') for a,b,p in blocks(u) if p.startswith('(pin ') and f'(number "{num}"' in p]
  px,py,pa=map(float,re.search(r'\(at ([^)]+)',pp[0])[1].split());pt=(x+px,y-py);print(name,ref,num,pt)
  for a,b,u in bs:
   if u.startswith('(wire'):
    pts=[tuple(map(float,v)) for v in re.findall(r'\(xy ([^ ]+) ([^)]+)',u)]
    if pt in pts:print('wire',pts)

