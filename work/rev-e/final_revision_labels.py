from pathlib import Path
import re,json,sys
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout')
p=r/'omni_ugv.kicad_sch';s=p.read_text();items=list(blocks(s));sheets=[t for a,b,t in items if t.startswith('(sheet')]
for i,t in enumerate(sheets):
 x=25.4+(i%3)*125.73;y=43.18+(i//3)*48.26
 u=re.sub(r'\(at [^)]+\)',f'(at {x} {y})',t,count=1);u=re.sub(r'\(size [^)]+\)','(size 105.41 30.48)',u,count=1)
 for a,b,v in reversed(list(blocks(u))):
  if v.startswith('(property "Sheetname"'):v=re.sub(r'\(at [^)]+\)',f'(at {x} {y-1.27} 0)',v,count=1)
  elif v.startswith('(property "Sheetfile"'):v=re.sub(r'\(at [^)]+\)',f'(at {x} {y+31.75} 0)',v,count=1)
  else:continue
  u=u[:a]+v+u[b:]
 s=s.replace(t,u,1)
flags=[t for a,b,t in blocks(s) if t.startswith('(symbol') and '(lib_id "UGV:PWR_FLAG")' in t];moves={}
for i,t in enumerate(flags):
 ox,oy=map(float,re.search(r'\(at ([^ ]+) ([^ ]+) ',t).groups());x=30.48+(i%4)*55.88;y=246.38+(i//4)*20.32;moves[(ox,oy)]=(x-ox,y-oy)
 u=re.sub(r'\((at|xy) ([-\d.]+) ([-\d.]+)',lambda m:f'({m[1]} {float(m[2])+x-ox:.5f} {float(m[3])+y-oy:.5f}',t);s=s.replace(t,u,1)
for a,b,t in reversed(list(blocks(s))):
 if t.startswith('(global_label'):
  ox,oy=map(float,re.search(r'\(at ([^ ]+) ([^ ]+) ',t).groups())
  if (ox,oy) in moves:
   dx,dy=moves[(ox,oy)];t=re.sub(r'\(at [^)]+\)',f'(at {ox+dx:.5f} {oy+dy:.5f} 0)',t,count=1)
   s=s[:a]+t+s[b:]
 elif t.startswith('(text') and 'Editable functional sheets' in t:
  t=re.sub(r'\(at [^)]+\)','(at 25.4 231.14 0)',t,count=1);s=s[:a]+t+s[b:]
s=s.replace('REV C PROTOTYPE','REV E PROTOTYPE');p.write_text(s)
for p in r.glob('*.kicad_sch'):
 s=p.read_text();s=re.sub(r'\(rev "[^"]*"\)','(rev "E - prototype")',s);s=s.replace('Omni UGV / Rev D','Omni UGV / Rev E');s=re.sub(r'\(date "[^\"]+"\)','(date "2026-11-07")',s);p.write_text(s)
# Project display revision only; all rules and stackup settings remain unchanged.
p=r/'omni_ugv.kicad_pro';j=json.loads(p.read_text());j.setdefault('text_variables',{})['REVISION']='E';p.write_text(json.dumps(j,indent=2))
print('Reflowed root overview and updated revision labels')
