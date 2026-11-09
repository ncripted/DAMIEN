from pathlib import Path
import json,re,uuid,sys,csv
sys.path.insert(0,'work/humanize');import build as h
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');p=r/'UGV.kicad_sym'
sym='''(symbol "WSK2512_Kelvin" (in_bom yes) (on_board yes)
(property "Reference" "R" (at 0 6.35 0) (effects (font (size 1 1))))
(property "Value" "WSK2512" (at 0 5.08 0) (effects (font (size 1 1))))
(symbol "WSK2512_Kelvin_0_1" (rectangle (start -2.54 2.54) (end 2.54 -2.54) (stroke (width .254) (type default)) (fill (type background))))
(symbol "WSK2512_Kelvin_1_1"
(pin passive line (at 0 3.81 270) (length 1.27) (name "I_CELL_N" (effects (font (size .6 .6)))) (number "1" (effects (font (size .9 .9)))))
(pin passive line (at 0 -3.81 90) (length 1.27) (name "I_GND" (effects (font (size .6 .6)))) (number "2" (effects (font (size .9 .9)))))
(pin passive line (at -5.08 1.27 0) (length 2.54) (name "S_CELL_N" (effects (font (size .6 .6)))) (number "3" (effects (font (size .9 .9)))))
(pin passive line (at 5.08 -1.27 180) (length 2.54) (name "S_GND" (effects (font (size .6 .6)))) (number "4" (effects (font (size .9 .9)))))))'''
s=p.read_text();assert '(symbol "WSK2512_Kelvin"' not in s;s=s.rstrip()[:-1]+sym+')';p.write_text(s)
data=json.loads((r/'design_connections.json').read_text());dm={d['ref']:d for d in data}
dm['R36'].update(value='10m 1% 1W KELVIN',mpn='WSK2512R0100FEA',key='WSK2512_Kelvin',symbol='UGV:WSK2512_Kelvin',fp='UGV:WSK2512_T1p19_Kelvin',localfp='UGV:WSK2512_T1p19_Kelvin',nets={'1':'CELL_N','2':'GND','3':'PROT_VSS_SENSE','4':'PROT_CS_SENSE'},note='4-terminal Vishay WSK2512 10mΩ. Current pads1/2, independent sense3/4. Native numbering explicitly mapped to manufacturer land drawing.')
dm['U7']['nets']['3']='PROT_VSS_SENSE';dm['U7']['nets']['4']='PROT_CS_SENSE';dm['C24']['nets']['2']='PROT_VSS_SENSE';dm['C24']['x']+=.5
(r/'design_connections.json').write_text(json.dumps(data,indent=2))
# Replace only the R36 symbol and add its two voltage terminals, retaining the component identity.
p=r/'battery_protection.kicad_sch';s=p.read_text();lb=next(t for a,b,t in h.blocks(s) if t.startswith('(lib_symbols'));s=s.replace(lb,lb[:-1]+sym.replace('(symbol "WSK2512_Kelvin"','(symbol "UGV:WSK2512_Kelvin"',1)+')',1)
for a,b,t in reversed(list(h.blocks(s))):
 if t.startswith('(symbol') and '(property "Reference" "R36"' in t:
  t=re.sub(r'\(lib_id "[^"]+"\)','(lib_id "UGV:WSK2512_Kelvin")',t,count=1)
  for key,val in [('Value',dm['R36']['value']),('Footprint',dm['R36']['localfp'])]:t=re.sub(r'(\(property "'+key+r'" )"[^"]*"',lambda m:m[1]+json.dumps(val),t,count=1)
  t=t.rstrip()[:-1]+''.join(f'(pin "{n}" (uuid {uuid.uuid4()}))' for n in [3,4])+')';s=s[:a]+t+s[b:]
p.write_text(s.replace('(symbol\n','(symbol '))
# Rebuild this one functional drawing with the established local-wiring adapter.
h.ROOT=r;h.BASE=r;h.data=dm;h.data.update(TH1={'nets':{'1':'CELL_CHG_TEMP','2':'GND'}},TH2={'nets':{'1':'CELL_TEMP_DIV','2':'GND'}})
sh=h.Sheet('battery_protection','Four-terminal cell protection and cell probes')
for ref,x,y,ang in [('U7',100,70,0),('Q7',185,60,0),('Q8',255,60,180),('R36',40,110,90),('R37',35,45,90),('R38',35,65,90),('R39',140,100,90),('C24',50,52,0),('R40',185,95,0),('R41',255,35,180),('J5',180,145,180),('R42',210,125,0),('R43',245,145,90),('C25',275,165,0),('TH1',50,175,0),('TH2',210,165,0)]:sh.place(ref,x,y,ang)
sh.link('PROT_DRAIN',('Q7',5),('Q8',5))
for ref in ['Q7','Q8']:sh.covered.update((ref,str(n)) for n in [6,7,8,9])
sh.link('PROT_CHG',('Q7',4),('R40',1));sh.link('PROT_DSG',('Q8',4),('R41',1))
sh.link('PROT_VDD',('R37',2),('C24',1),[(50,45)]);sh.link('PROT_VDD',('R37',2),('U7',2),[(75,45),(75,65)])
sh.link('PROT_BAT',('R38',2),('U7',1),[(70,65),(70,63)])
sh.join('CELL_TEMP_DIV',[('R42',2),('R43',1),('TH2',1)],rail=145);sh.link('CELL_TEMP_DIV',('J5',1),('R43',1));sh.join('CELL_TEMP_ADC',[('R43',2),('C25',1)],rail=155);sh.join('GND',[('TH2',2),('C25',2)],rail=180)
sh.text('Kelvin sense: no motor current in S_CELL_N / S_GND traces',20,25);sh.text('Common-drain high-side protection FET pair',165,25)
sh.text('TH1 -> J4 analog charging window',20,145);sh.text('TH2 -> J5 -> GPIO2 / ADC1',170,112)
sh.text('WSK2512 current pads1/2 replace WSL2512. Sense3 -> U7 VSS + C24 return; sense4 -> U7 CS.\nThe voltage contacts are internal Kelvin pickups, not ground-plane taps.\nTH1 and TH2 remain OFF-BOARD, insulated and bonded to the actual cell.',20,215)
sh.finish();p=r/'battery_protection.kicad_sch';p.write_text(p.read_text().replace('B - prototype','E - prototype'))
# Ground-side sense reference is supplied through the passive four-terminal shunt.
p=r/'omni_ugv.kicad_sch';s=p.read_text();flag=next(t for a,b,t in h.blocks(s) if t.startswith('(symbol') and '(lib_id "UGV:PWR_FLAG")' in t);oldref=re.search(r'\(property "Reference" "([^"]+)',flag)[1];oldid=re.search(r'\(uuid "?([0-9a-f-]+)',flag)[1];x,y,an=map(float,re.search(r'\(at ([^)]+)',flag)[1].split());flag=re.sub(r'\((at|xy) ([-\d.]+) ([-\d.]+)',lambda m:f'({m[1]} {float(m[2])+330.2-x} {float(m[3])+215.9-y}',flag);flag=flag.replace(oldref,'#FLGE01').replace(oldid,str(uuid.uuid4()));s=s.rstrip()[:-1]+flag+f'(global_label "PROT_VSS_SENSE" (shape bidirectional) (at 330.2 215.9 0) (effects (font (size .9 .9)) (justify left bottom)) (uuid {uuid.uuid4()})))';p.write_text(s)
# Manufacturer pad dimensions for the 0.005..0.2 ohm range, not the low-ohm variants.
fp=Path('C:/Program Files/KiCad/10.0/share/kicad/footprints/Resistor_SMD.pretty/R_Shunt_Vishay_WSK2512_6332Metric_T1.19mm.kicad_mod').read_text();fp=re.sub(r'^\(footprint "[^"]+"','(footprint "WSK2512_T1p19_Kelvin"',fp,count=1)
fp=fp.replace('(at -3.43 1.27)','(at -3.28 1.27)').replace('(at 3.43 -1.27)','(at 3.28 -1.27)').replace('(size 1.4 0.76)','(size 1.70 0.76)')
mapping={'1':'2','2':'4','3':'3','4':'1'}
fp=re.sub(r'\(pad "([1-4])"',lambda m:'(pad "'+mapping[m[1]]+'"',fp)
fp=re.sub(r'\(descr "[^"]+"\)','(descr "Vishay WSK2512, 10mΩ, T=1.19mm. Manufacturer30108 a2.29 b3.30 c0.76 d0.51 e1.70 l3.68mm. Pins1 CELL_N-current/right,2 GND-current/left,3 CELL_N-sense/right,4 GND-sense/left; package unnumbered.")',fp,count=1)
(r/'UGV.pretty/WSK2512_T1p19_Kelvin.kicad_mod').write_text(fp)
with (r/'BOM.csv').open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
for d in rows:
 if d['Reference']=='R36':d.update(Value=dm['R36']['value'],MPN=dm['R36']['mpn'],Footprint=dm['R36']['localfp'],Notes=dm['R36']['note'])
with (r/'BOM.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print('Created four-terminal shunt symbol/land pattern and independent CS/VSS nets')
