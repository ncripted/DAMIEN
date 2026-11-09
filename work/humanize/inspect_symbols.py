from pathlib import Path
import re
src=Path('work/protection/make_schematic.py').read_text()
exec(src[src.index('def blocks'):src.index('def q')])
for f in Path('work/humanize/before').glob('*.kicad_sch'):
 s=f.read_text(); lib=next(t for a,b,t in blocks(s) if t.startswith('(lib_symbols'))
 libs={re.search(r'^\(symbol "([^"]+)',t)[1]:t for a,b,t in blocks(lib)}
 print('\n',f.stem)
 seen=set()
 for a,b,t in blocks(s):
  if not t.startswith('(symbol '):continue
  name=re.search(r'\(lib_id "([^"]+)',t)[1]
  if name in seen:continue
  seen.add(name);pins=[]
  for aa,bb,u in blocks(libs[name]):
   if not u.startswith('(symbol'):continue
   for aaa,bbb,p in blocks(u):
    if p.startswith('(pin '):pins.append((re.search(r'\(number "([^"]+)',p)[1],re.search(r'\(at ([^)]+)',p)[1]))
  print(name,pins)
