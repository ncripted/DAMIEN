from pathlib import Path
import re,json,csv,uuid,shutil
root=Path('outputs/rover/Omni_UGV_Rev_B_protection')
base=Path('outputs/rover/Omni_UGV_Rev_A')
def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,'nate-rover-protection/'+s))
def blocks(s):
 depth=0; quoted=False; escape=False; start=0
 for i,c in enumerate(s):
  if quoted:
   if escape: escape=False
   elif c=='\\': escape=True
   elif c=='"': quoted=False
  elif c=='"': quoted=True
  elif c=='(':
   if depth==1:start=i
   depth+=1
  elif c==')':
   if depth==2:yield start,i+1,s[start:i+1]
   depth-=1
def q(s):return json.dumps(str(s))
def prop(name,val,x,y,hide=False):return f'(property {q(name)} {q(val)} (at {x} {y} 0) (effects (font (size 1.0 1.0))'+(' hide' if hide else '')+'))'
def note(s,x,y):return f'(text {q(s)} (at {x} {y} 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid {uid(s)}))'
data=json.loads((base/'design_connections.json').read_text())
by={d['ref']:d for d in data}
top=(base/'omni_ugv.kicad_sch').read_text(); topid=re.search(r'\(uuid ([^)]+)',top)[1]; sid=uid('sheet')
# Relabel ONLY the connector's two local wire labels on the charging sheet.
s=(base/'charging.kicad_sch').read_text()
s=s.replace('(global_label "VBAT" (shape bidirectional) (at 459.74 195.58','(global_label "CELL_P" (shape bidirectional) (at 459.74 195.58')
s=s.replace('(global_label "GND" (shape bidirectional) (at 459.74 198.12','(global_label "CELL_N" (shape bidirectional) (at 459.74 198.12')
s=s.replace('1S BATTERY 4.2V MAX','RAW 1S CELL 4.2V MAX').replace('PACK NTC 10k','CELL NTC - CHARGER')
s=s.rstrip()[:-1]+note('J2 is RAW CELL: no ground connection except through R36. J4 uses an electrically isolated two-wire sensor bonded to the CELL.',30,310)+')'
(root/'charging.kicad_sch').write_text(s)
by['J2']['nets']={'1':'CELL_P','2':'CELL_N'};by['J2']['value']='RAW 1S CELL 4.2V MAX'
by['J2']['note']='Raw cell input, pin1 positive; protection now onboard. Cell itself must support >=4A continuous / >=5A peak. No CELL_N-to-GND bypass.'
by['J4']['value']='CELL NTC - CHARGER';by['J4']['note']='Independent 103AT-2 probe bonded to cell; both leads isolated from cell terminals. Pin1 TS, pin2 system GND. Do not share with J5.'
# GPIO1/ADC1 becomes temperature input; LED moves to GPIO43, formerly UART TX.
s=(base/'controller.kicad_sch').read_text()
for a,z,t in reversed(list(blocks(s))):
 if t.startswith('(global_label "LED_STATUS"'):
  # Only the label at the ESP32 pin; R3 retains LED_STATUS.
  at=re.search(r'\(at ([\d.]+) ([\d.]+)',t)
  print('LED label location',at.groups())
# Find pin 38 world coordinate from embedded symbol then its attached wire/label.
syms=[t for a,z,t in blocks(s) if t.startswith('(symbol (lib_id') and '(property "Reference" "U1"' in t]
u=syms[0]; ux,uy=map(float,re.search(r'\(at ([\d.]+) ([\d.]+)',u).groups())
libblock=next(t for a,z,t in blocks(s) if t.startswith('(lib_symbols'))
lib=next(t for a,z,t in blocks(libblock) if t.startswith('(symbol "UGV:RF_Module__ESP32-S3-WROOM-1"'))
pin=re.search(r'\(pin bidirectional line \(at ([-\d.]+) ([-\d.]+) [\d]+\).*?\(number "38"',lib,re.S)
# Parse individual pin blocks rather than matching across pins.
pins=[]
for a,z,t in blocks(lib):
 if t.startswith('(symbol'):
  pins += [b for aa,zz,b in blocks(t) if b.startswith('(pin ')]
p38=next(b for b in pins if '(number "38"' in b);px,py=map(float,re.search(r'\(at ([-\d.]+) ([-\d.]+)',p38).groups());pt=(round(ux+px,2),round(uy-py,2))
ends=[]
for a,z,t in blocks(s):
 if t.startswith('(wire'):
  xy=[tuple(map(float,m)) for m in re.findall(r'\(xy ([-\d.]+) ([-\d.]+)\)',t)]
  if pt in xy:ends+=xy
ed=[]
for a,z,t in blocks(s):
 if t.startswith('(global_label "LED_STATUS"'):
  xy=tuple(map(float,re.search(r'\(at ([-\d.]+) ([-\d.]+)',t).groups()))
  if xy in ends:ed.append((a,z,t.replace('"LED_STATUS"','"CELL_TEMP_ADC"')))
assert len(ed)==1
for a,z,t in reversed(ed):s=s[:a]+t+s[z:]
s=s.replace('"UART_TX"','"LED_STATUS"')
(root/'controller.kicad_sch').write_text(s)
# UART TX test point is on the root schematic.
top=top.replace('"UART_TX"','"LED_STATUS"')
by['U1']['nets']['38']='CELL_TEMP_ADC';by['U1']['nets']['37']='LED_STATUS'
by['TP7']['nets']['1']='LED_STATUS';by['TP7']['value']='LED_STATUS'
by['TP7']['note']='GPIO43 status LED test point; UART0 TX no longer exposed. Programming remains native USB.'
# Custom pin-explicit semiconductor symbols. Passive components reuse supplied symbols.
libsrc=(base/'UGV.kicad_sym').read_text(); libs={re.search(r'^\(symbol "([^"]+)"',t)[1]:t for a,z,t in blocks(libsrc) if t.startswith('(symbol "')}
def chip(name,pins):
 n=len(pins);h=(n+1)*1.27
 out=f'(symbol {q(name)} (in_bom yes) (on_board yes) '+prop('Reference','U',0,h+3)+prop('Value',name,0,h+1)+f'(symbol {q(name+"_0_1")} (rectangle (start -10.16 {h}) (end 10.16 {-h}) (stroke (width 0.254) (type default)) (fill (type background)))) (symbol {q(name+"_1_1")}'
 for i,(num,pname,typ) in enumerate(pins):
  y=round((n-1)*1.27-i*2.54,2)
  out+=f'(pin {typ} line (at -12.7 {y} 0) (length 2.54) (name {q(pname)} (effects (font (size 1 1)))) (number {q(num)} (effects (font (size 1 1)))))'
 return out+'))'
libs['BQ298217']=chip('BQ298217',[(1,'BAT','input'),(2,'VDD','power_in'),(3,'VSS','power_in'),(4,'CS','input'),(5,'CTR','input'),(6,'PACK','input'),(7,'DSG','output'),(8,'CHG','output')])
libs['CSD17308Q3']=chip('CSD17308Q3',[(i,'S' if i<4 else 'G' if i==4 else 'D','input' if i==4 else 'passive') for i in range(1,10)])
libs['Cell_NTC']=libs['Device__R'].replace('Device__R','Cell_NTC')
for k in ['BQ298217','CSD17308Q3','Cell_NTC']:libsrc=libsrc.rstrip()[:-1]+libs[k]+')'
(root/'UGV.kicad_sym').write_text(libsrc)
new=[]
def add(ref,value,key,fp,nets,x,y,bx,by_,mpn='',note_=''):
 d=dict(ref=ref,value=value,symbol='UGV:'+key,localfp='UGV:'+fp,fp='UGV:'+fp,nets={str(k):v for k,v in nets.items()},x=bx,y=by_,a=0,side='B',group='Battery protection',uuid=uid(ref),mpn=mpn,note=note_,sx=round(round(x/1.27)*1.27,2),sy=round(round(y/1.27)*1.27,2),key=key)
 new.append(d);data.append(d)
R='Resistor_SMD__R_0603_1608Metric';C='Capacitor_SMD__C_0603_1608Metric'
add('U7','BQ298217RUGR','BQ298217','BQ298217_RUG0008A',{1:'PROT_BAT',2:'PROT_VDD',3:'CELL_N',4:'GND',5:'CELL_N',6:'PROT_PACK',7:'PROT_DSG',8:'PROT_CHG'},70,65,109,126,'BQ298217RUGR','4.25V OV / 2.6V UV / 60mV OCD; exact suffix required; zero-volt charging disabled')
new[-1]['a']=180
for ref,src,gate,x,bx,ang in [('Q7','CELL_P','PROT_CHG',145,115,0),('Q8','VBAT','PROT_DSG',220,121,180)]:
 add(ref,'CSD17308Q3','CSD17308Q3','CSD17308Q3_TI',{i:src if i<4 else gate if i==4 else 'PROT_DRAIN' for i in range(1,10)},x,65,bx,138,'CSD17308Q3','30V NFET; common-drain pair; source pins1-3 gate4 drain5-9')
 new[-1]['a']=ang
add('R36','10m 1% 1W','Device__R','Resistor_SMD__R_2512_6332Metric',{1:'CELL_N',2:'GND'},55,115,113,127,'WSL2512R0100FEA','Current shunt, Kelvin sense endpoints. Nominal6A OCD; do not substitute resistance.')
add('R37','100R 1%','Device__R',R,{1:'CELL_P',2:'PROT_VDD'},105,115,106,126)
add('R38','20R 1%','Device__R',R,{1:'CELL_P',2:'PROT_BAT'},150,115,106,123)
add('R39','1k 1%','Device__R',R,{1:'VBAT',2:'PROT_PACK'},195,115,109,130)
add('C24','100n/16V X7R','Device__C',C,{1:'PROT_VDD',2:'CELL_N'},240,115,109,123)
add('R40','10M','Device__R',R,{1:'PROT_CHG',2:'CELL_P'},55,155,113,135,'','Gate discharge path; <1uA loading at normal gate drive')
add('R41','10M','Device__R',R,{1:'PROT_DSG',2:'VBAT'},105,155,124,135)
add('J5','CELL NTC - DRIVE','Connector_Generic__Conn_01x02','Connector_JST__JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical',{1:'CELL_TEMP_DIV',2:'GND'},150,155,82,137,'B2B-PH-K-S','Second electrically isolated103AT-2 probe bonded to same cell; not shared with J4')
new[-1]['side']='F'
add('R42','10k 1%','Device__R',R,{1:'+3V3',2:'CELL_TEMP_DIV'},195,155,80,139)
add('R43','1k 1%','Device__R',R,{1:'CELL_TEMP_DIV',2:'CELL_TEMP_ADC'},240,155,84,139)
add('C25','100n/16V X7R','Device__C',C,{1:'CELL_TEMP_ADC',2:'GND'},240,185,87,137)
# Embedded library names must match lib_id while internal unit names remain unprefixed.
used=set(d['key'] for d in new)|{'Cell_NTC'}
embedded=''.join(libs[k].replace('(symbol "'+k+'"','(symbol "UGV:'+k+'"',1) for k in sorted(used))
flag='(symbol "UGV:PWR_FLAG" (power) (pin_names (offset 0)) (in_bom no) (on_board no) (property "Reference" "#FLG" (at 0 2 0) (effects (font (size 1 1)) hide)) (property "Value" "PWR_FLAG" (at 0 4 0) (effects (font (size 1 1)))) (symbol "PWR_FLAG_0_1" (polyline (pts (xy 0 0) (xy 0 1.27) (xy -1.27 1.9) (xy 0 2.54) (xy 1.27 1.9) (xy 0 1.27)) (stroke (width 0) (type default)) (fill (type none)))) (symbol "PWR_FLAG_1_1" (pin power_out line (at 0 0 90) (length 0) (name "pwr" (effects (font (size 1 1)))) (number "1" (effects (font (size 1 1)))))))'
flag=flag.replace('PWR_FLAG','PROTECTION_PWR_FLAG')
libsrc=libsrc.rstrip()[:-1]+flag.replace('"UGV:PROTECTION_PWR_FLAG"','"PROTECTION_PWR_FLAG"',1)+')';(root/'UGV.kicad_sym').write_text(libsrc)
sheet=f'(kicad_sch (version 20230121) (generator eeschema) (uuid {sid}) (paper "A3") (title_block (title "1S protection and CELL temperature") (rev "B-PROTOTYPE")) (lib_symbols {embedded}{flag})'
for i,net in enumerate(['CELL_N','PROT_VDD']):
 x=25.4+25.4*i;y=180.34;ref='#FLG'+str(20+i)
 sheet+=f'(symbol (lib_id "UGV:PROTECTION_PWR_FLAG") (at {x} {y} 0) (unit 1) (in_bom no) (on_board no) (uuid {uid(ref)})'+prop('Reference',ref,x,y,True)+prop('Value','PROTECTION_PWR_FLAG',x,y-4)+f'(pin "1" (uuid {uid(ref+"1")})) (instances (project "omni_ugv" (path "/{topid}/{sid}" (reference "{ref}") (unit 1)))))'
 sheet+=f'(global_label "{net}" (shape bidirectional) (at {x} {y} 0) (effects (font (size 0.9 0.9)) (justify left bottom)) (uuid {uid(ref+"label")}))'
for d in new:
 x,y=d['sx'],d['sy'];lib=libs[d['key']];pblocks=[]
 for a,z,t in blocks(lib):
  if t.startswith('(symbol'):
   pblocks += [t2 for a2,z2,t2 in blocks(t) if t2.startswith('(pin ')]
 oy=18 if d['ref'][0] in 'UQ' else 6
 sheet+=f'(symbol (lib_id {q(d["symbol"])}) (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {d["uuid"]})'+prop('Reference',d['ref'],x+5,y-oy)+prop('Value',d['value'],x+5,y-oy+3)+prop('Footprint',d['localfp'],x,y,True)
 for pin in pblocks:
  num=re.search(r'\(number "([^"]+)"',pin)[1]
  sheet+=f'(pin {q(num)} (uuid {uid(d["ref"]+"pin"+num)}))'
 sheet+=f'(instances (project "omni_ugv" (path "/{topid}/{sid}" (reference {q(d["ref"])}) (unit 1)))))'
 for pin in pblocks:
  num=re.search(r'\(number "([^"]+)"',pin)[1];px,py,angle=map(float,re.search(r'\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)',pin).groups());px+=x;py=y-py
  import math
  ex=round(px-5.08*math.cos(math.radians(angle)),2);ey=round(py+5.08*math.sin(math.radians(angle)),2)
  sheet+=f'(wire (pts (xy {px} {py}) (xy {ex} {ey})) (stroke (width 0) (type default)) (uuid {uid(d["ref"]+"wire"+num)}))'
  # Simple labels attached to remote wire endpoints; all used nets are global across sheets.
  la=int(angle if angle in [0,180] else (angle+180)%360)
  sheet+=f'(global_label {q(d["nets"][num])} (shape bidirectional) (at {ex} {ey} {la}) (effects (font (size 0.9 0.9)) (justify left bottom)) (uuid {uid(d["ref"]+"label"+num)}))'
for ref,x,net in [('TH1',55.88,'BAT_NTC'),('TH2',154.94,'CELL_TEMP_DIV')]:
 y=228.6
 sheet+=f'(symbol (lib_id "UGV:Cell_NTC") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board no) (dnp no) (uuid {uid(ref)})'+prop('Reference',ref,x+10,y-2)+prop('Value','103AT-2 CELL-MOUNTED',x+27,y+2)+f'(pin "1" (uuid {uid(ref+"1")})) (pin "2" (uuid {uid(ref+"2")})) (instances (project "omni_ugv" (path "/{topid}/{sid}" (reference "{ref}") (unit 1)))))'
 for pin,dy,n,ang in [(1,-3.81,net,90),(2,3.81,'GND',270)]:
  yy=round(y+dy,2);ey=round(y+dy*2,2)
  sheet+=f'(wire (pts (xy {x} {yy}) (xy {x} {ey})) (stroke (width 0) (type default)) (uuid {uid(ref+"w"+str(pin))})) (global_label "{n}" (shape bidirectional) (at {x} {ey} {ang}) (effects (font (size 0.9 0.9)) (justify left bottom)) (uuid {uid(ref+"l"+str(pin))}))'
sheet+=note('OFF-BOARD harness components: TH1 -> J4; TH2 -> J5. Attach both sensing heads to the CELL, not the chassis PCB.',20,250)
sheet+=note('RAW CELL: J2 -> Q7/Q8 -> VBAT (charger + motors). R36 is the ONLY CELL_N-to-GND connection.\nU7 CS and VSS require Kelvin routing to opposite R36 pads. No bypass via sensor wires or USB.',20,20)
sheet+=note('J4: independent charger probe. J5: second 103AT-2 cell probe for GPIO1/ADC1.\nBoth probes contact the cell pouch through electrical insulation; neither mounts on this PCB.\nOpen/short J5 must disable driving. Charge temperature control remains hardware BQ24074 TS.',20,195)+')'
(root/'battery_protection.kicad_sch').write_text(sheet)
top=top.rstrip()[:-1]+f'(sheet (at 170 150) (size 70 20) (stroke (width 0.15) (type default)) (fill (color 0 0 0 0)) (uuid {sid}) (property "Sheetname" "Battery protection" (at 170 149 0) (effects (font (size 1.27 1.27)) (justify left bottom))) (property "Sheetfile" "battery_protection.kicad_sch" (at 170 171 0) (effects (font (size 1.27 1.27)) (justify left top))) (instances (project "omni_ugv" (path "/{topid}" (page "7"))))) )'
(root/'omni_ugv.kicad_sch').write_text(top)
if Path('work/protection/placements.json').exists():
 for ref,pos in json.loads(Path('work/protection/placements.json').read_text()).items():
  d=next(d for d in new if d['ref']==ref);d['x'],d['y']=pos
(root/'design_connections.json').write_text(json.dumps(data,indent=2)+'\n')
(Path('work/protection')/'new_parts.json').write_text(json.dumps(new,indent=2))
with (root/'BOM.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['Reference','Value','MPN','Footprint','Notes']);w.writeheader()
 for d in data:w.writerow(dict(Reference=d['ref'],Value=d['value'],MPN=d.get('mpn',''),Footprint=d['localfp'],Notes=d.get('note','')))
 for ref,note_ in [('TH1','Cell-bonded charger probe -> J4'),('TH2','Cell-bonded drive monitoring probe -> J5')]:w.writerow(dict(Reference=ref,Value='10k NTC 1% B25/85=3435K',MPN='103AT-2',Footprint='OFFBOARD',Notes=note_+'; separate insulated two-wire harness; strain relief; never attach to PCB as temperature proxy'))
print('Created native sheet, updated connector and GPIO connections, BOM and manifest.')
