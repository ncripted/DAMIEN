from pathlib import Path
import json,re,sys,uuid
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');p=r/'design_connections.json';d=json.loads(p.read_text())
for z in d:
 if z['ref']=='R36':z.update(x=113.15,a=0,side='B')
 if z['ref']=='C24':z['x']=120.0
p.write_text(json.dumps(d,indent=2))
# Manufacturer-correct extended sense pads require new silk markers clear of all mask openings.
p=r/'UGV.pretty/WSK2512_T1p19_Kelvin.kicad_mod';s=p.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith('(fp_line') and '(layer "F.SilkS")' in t:s=s[:a]+s[b:]
for y in [-1.95,1.95]:s=s.rstrip()[:-1]+f'(fp_line (start -1.5 {y}) (end 1.5 {y}) (stroke (width .12) (type default)) (layer "F.SilkS") (uuid {uuid.uuid4()})))'
p.write_text(s)
p=r/'omni_ugv.kicad_pcb';s=p.read_text();bad={'ad546fd6-b19f-43df-a0bb-f60ca7fe9e16','25ddd1d7-a43f-4516-a7a4-f3d2eae399ea'}
for a,b,t in reversed(list(blocks(s))):
 if (t.startswith('(footprint') and '(property "Reference" "R36"' in t) or (t.startswith(('(segment','(via')) and ('(net "PROT_DSG")' in t or any(i in t for i in bad))):s=s[:a]+s[b:]
p.write_text(s)
p=Path('work/rev-e/step3_board.py');s=p.read_text().replace(" n=p.NETINFO_ITEM(b,name);b.Add(n);nets[name]=n"," if name not in nets:n=p.NETINFO_ITEM(b,name);b.Add(n);nets[name]=n");p.write_text(s)
