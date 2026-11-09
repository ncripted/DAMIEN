import sys,re,uuid
from pathlib import Path
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');fn=r/'omni_ugv.kicad_sch';s=fn.read_text();tid=re.search(r'\(uuid "?([0-9a-f-]+)',s)[1]
flag=next(t for a,b,t in blocks(s) if t.startswith('(symbol') and '(lib_id "UGV:PWR_FLAG")' in t)
oldref=re.search(r'\(property "Reference" "([^"]+)',flag)[1];oldid=re.search(r'\(uuid "?([0-9a-f-]+)',flag)[1]
x,y,ang=map(float,re.search(r'\(at ([^)]+)',flag)[1].split());dx,dy=365.76-x,215.9-y
flag=re.sub(r'\((at|xy) ([-\d.]+) ([-\d.]+)',lambda m:f'({m[1]} {float(m[2])+dx} {float(m[3])+dy}',flag)
flag=flag.replace(oldref,'#FLGD01').replace(oldid,str(uuid.uuid4()))
s=s.rstrip()[:-1]+flag+f'(global_label "CELL_P" (shape bidirectional) (at 365.76 215.9 0) (effects (font (size 1 1)) (justify left bottom)) (uuid {uuid.uuid4()})))'
fn.write_text(s);print('Marked raw battery CELL_P as an actual external power source for ERC')
