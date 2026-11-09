from pathlib import Path
import sys,re,collections,pymupdf
sys.path.insert(0,'work/humanize');from build import blocks
for name in ['cell_undervoltage','charge_temperature']:
 s=Path('outputs/rover/Omni_UGV_Rev_D_power_audit/'+name+'.kicad_sch').read_text();print(name,len(s),collections.Counter(re.match(r'\(([^\s()]+)',t)[1] for a,b,t in blocks(s)))
 print('refs',re.findall(r'\(property "Reference" "([^"]+)',s));print(s[-300:])
d=pymupdf.open('outputs/rover/Omni_UGV_Rev_D_power_audit/Schematic.pdf');print(d[8].get_text());print(d[9].get_text()[:2000])
