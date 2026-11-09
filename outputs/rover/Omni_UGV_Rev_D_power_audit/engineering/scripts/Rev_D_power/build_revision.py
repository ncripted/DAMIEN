from pathlib import Path
import sys,json,re,uuid,shutil,csv,math,hashlib
sys.path.insert(0,'work/humanize')
from build import blocks
base=Path('outputs/rover/Omni_UGV_Rev_C_flex_camera')
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit')
assert not r.exists(), 'Never overwrite an existing engineering revision'
shutil.copytree(base,r,ignore=shutil.ignore_patterns('.validation-runtime','*.lck','*.kicad_prl'))
(r/'validation/history/rev-c-before-power').mkdir(parents=True,exist_ok=True)
for fn in ['drc.json','erc.json']:
 shutil.copy2(base/'validation/current'/fn,r/'validation/history/rev-c-before-power'/fn)
manifest={str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest() for p in base.rglob('*') if p.is_file() and '.validation-runtime' not in p.parts}
Path('work/power-rev-d/rev-c-baseline-sha256.json').write_text(json.dumps(manifest,indent=2))
def uid():return str(uuid.uuid4())
def q(x):return json.dumps(str(x))
def prop(k,v,x,y,hide=False):return f'(property {q(k)} {q(v)} (at {x} {y} 0) (effects (font (size 1 1))'+(' hide' if hide else '')+'))'
def boxlib(name,pins):
 s=f'(symbol "{name}" (in_bom yes) (on_board yes)'+prop('Reference','U',0,9)+prop('Value',name,0,7)
 s+=f'(symbol "{name}_0_1" (rectangle (start -5.08 5.08) (end 5.08 -5.08) (stroke (width 0.254) (type default)) (fill (type background))))(symbol "{name}_1_1"'
 for n,pn,typ,x,y,a in pins:s+=f'(pin {typ} line (at {x} {y} {a}) (length 2.54) (name {q(pn)} (effects (font (size .85 .85)))) (number "{n}" (effects (font (size .85 .85)))))'
 return s+'))'
libsrc=(r/'UGV.kicad_sym').read_text();libs={re.search(r'^\(symbol "([^"]+)',t)[1]:t for _,_,t in blocks(libsrc) if t.startswith('(symbol')}
newlibs={
 'TPS3840_DL_DBV':boxlib('TPS3840_DL_DBV',[(1,'RESET_N','open_collector',7.62,2.54,180),(2,'VDD','power_in',-7.62,2.54,0),(3,'GND','power_in',0,-7.62,90),(4,'MR_N','input',-7.62,-2.54,0),(5,'CT','passive',7.62,-2.54,180)]),
 'TLV6700_DDC':boxlib('TLV6700_DDC',[(1,'OUTA','open_collector',7.62,2.54,180),(2,'GND','power_in',0,-7.62,90),(3,'INA+','input',-7.62,2.54,0),(4,'INB-','input',-7.62,-2.54,0),(5,'VDD','power_in',0,7.62,270),(6,'OUTB','open_collector',7.62,-2.54,180)]),
 'LVC1G14_DBV':boxlib('LVC1G14_DBV',[(1,'NC','no_connect',7.62,-2.54,180),(2,'A','input',-7.62,0,0),(3,'GND','power_in',0,-7.62,90),(4,'Y','output',7.62,0,180),(5,'VCC','power_in',0,7.62,270)]),
 'PNP_123':boxlib('PNP_123',[(1,'B','passive',-7.62,0,0),(2,'E','passive',0,7.62,270),(3,'C','passive',7.62,0,180)]),
 'NPN_123':boxlib('NPN_123',[(1,'B','passive',-7.62,0,0),(2,'E','passive',0,-7.62,90),(3,'C','passive',7.62,0,180)])}
libs.update(newlibs)
for s in newlibs.values():libsrc=libsrc.rstrip()[:-1]+s+')'
(r/'UGV.kicad_sym').write_text(libsrc)
data=json.loads((r/'design_connections.json').read_text());dm={d['ref']:d for d in data};new=[]
def add(ref,val,key,fp,nets,x,y,group,mpn=''):
 d=dict(ref=ref,value=val,key=key,symbol='UGV:'+key,fp=fp,localfp='UGV:'+fp,nets={str(k):v for k,v in nets.items()},x=x,y=y,a=0,side='F',mpn=mpn,uuid=uid(),group=group,note='Rev D power audit; engineering prototype, qualification required')
 new.append(d);return d
SOT='Package_TO_SOT_SMD__SOT-23';RFP='Resistor_SMD__R_0603_1608Metric';CFP='Capacitor_SMD__C_0603_1608Metric'
def resistor(ref,val,n1,n2,x,y,grp):return add(ref,val,'Device__R',RFP,{1:n1,2:n2},x,y,grp)
def cap(ref,val,n1,n2,x,y,grp):return add(ref,val,'Device__C',CFP,{1:n1,2:n2},x,y,grp)
uv='Cell undervoltage shutdown';temp='Independent charging temperature'
add('U10','TPS3840DL31DBVR','TPS3840_DL_DBV','Camera_SOT23_5',{1:'CELL_UV_RESET_N',2:'CELL_P',3:'CELL_N',4:'CELL_P',5:'CELL_UV_CT'},80,110,uv,'TPS3840DL31DBVR')
add('Q9','MMBT3906','PNP_123',SOT,{1:'CELL_UV_PNP_B',2:'CELL_P',3:'CELL_UV_FAULT'},85,110,uv,'MMBT3906-7-F')
add('Q10','MMBT3904','NPN_123',SOT,{1:'CELL_UV_EN_B',2:'CELL_N',3:'SYS_ON'},87,116,uv,'MMBT3904-7-F')
add('Q11','MMBT3904','NPN_123',SOT,{1:'CELL_UV_MOTOR_B',2:'CELL_N',3:'DRIVE_ENABLE'},92,110,uv,'MMBT3904-7-F')
for a in [('R46','100k','CELL_P','CELL_UV_RESET_N',78,106),('R47','47k','CELL_UV_RESET_N','CELL_UV_PNP_B',83,106),('R48','100k','CELL_P','CELL_UV_PNP_B',85,103),('R49','1M','CELL_UV_FAULT','CELL_N',88,106),('R50','47k','CELL_UV_FAULT','CELL_UV_EN_B',84,116),('R51','1M','CELL_UV_EN_B','CELL_N',87,120),('R52','47k','CELL_UV_FAULT','CELL_UV_MOTOR_B',89,110),('R53','1M','CELL_UV_MOTOR_B','CELL_N',92,114),('R54','10k','SYS_ON_REQ','SYS_ON',90,120)]:resistor(*a,uv)
cap('C30','100n/10V X7R','CELL_P','CELL_N',77,110,uv);cap('C31','100n/10V X7R','CELL_UV_CT','CELL_N',80,114,uv)
add('U11','TLV75533PDBVR','TLV755P_DBV','Camera_SOT23_5',{1:'USB_5V',2:'GND',3:'USB_5V',4:None,5:'CHG_3V3'},75,99,temp,'TLV75533PDBVR')
add('U12','TLV6700DDCR','TLV6700_DDC','Power_SOT23_6',{1:'CHG_TEMP_OK_OD',2:'GND',3:'CHG_HOT_SENSE',4:'CHG_COLD_SENSE',5:'USB_5V',6:'CHG_TEMP_OK_OD'},84,94,temp,'TLV6700DDCR')
add('U13','SN74LVC1G14DBVR','LVC1G14_DBV','Camera_SOT23_5',{1:None,2:'CHG_TEMP_ALLOW_RC',3:'GND',4:'CHG_DISABLE',5:'USB_5V'},90,98,temp,'SN74LVC1G14DBVR')
for a in [('R55','10k 1%','CHG_3V3','CELL_CHG_TEMP',77,94),('R56','200k 1%','CELL_CHG_TEMP','CHG_HOT_SENSE',81,91),('R57','100k 1%','CHG_HOT_SENSE','GND',81,97),('R58','442k 1%','CELL_CHG_TEMP','CHG_COLD_SENSE',85,91),('R59','100k 1%','CHG_COLD_SENSE','GND',85,97),('R60','10k 1%','CHG_TS_BIAS','GND',93,125),('R61','100k','USB_5V','CHG_TEMP_ALLOW_RC',91,94),('R62','1k','CHG_TEMP_OK_OD','CHG_TEMP_ALLOW_RC',88,94),('R63','100k','USB_5V','CHG_DISABLE',93,98)]:resistor(*a,temp)
for a in [('C32','2.2u/10V X7R','USB_5V','GND',72,99),('C33','2.2u/10V X7R','CHG_3V3','GND',78,99),('C34','100n/10V X7R','USB_5V','GND',84,101),('C35','220n/10V X7R','CHG_TEMP_ALLOW_RC','GND',90,102),('C36','100n/10V X7R','USB_5V','GND',93,102)]:cap(*a,temp)
dm['SW3']['nets']['2']='SYS_ON_REQ';dm['J4']['nets']['1']='CELL_CHG_TEMP';dm['U5']['nets']['1']='CHG_TS_BIAS';dm['U5']['nets']['4']='CHG_DISABLE'
dm['J4']['note']='Independent insulated 103AT-2 bonded to actual cell. Analog U12 window controls U5 CE; pin1 CELL_CHG_TEMP, pin2 GND. Never attach to raw CELL_N.'
for ref in ['Q1','Q2']:dm[ref].update(value='DMP2035U-7',mpn='DMP2035U-7',note='Lower-loss P-FET, same G1/S2/D3 SOT23. Thermal/braking qualification remains required.')
dm['R24']['value']='47k'
def editprops(s,ref,values):
 for a,b,t in reversed(list(blocks(s))):
  if t.startswith('(symbol') and f'(property "Reference" "{ref}"' in t:
   for k,v in values.items():t=re.sub(r'(\(property "'+k+r'" )"[^"]*"',lambda m:m[1]+q(v),t,count=1)
   s=s[:a]+t+s[b:]
 return s
s=(r/'interlock.kicad_sch').read_text()
for ref in ['Q1','Q2']:s=editprops(s,ref,{'Value':'DMP2035U-7'})
s=editprops(s,'R24',{'Value':'47k'});(r/'interlock.kicad_sch').write_text(s)
# Preserve regulator drawing, detach only SW3's short output lead from the SYS_ON graph.
s=(r/'regulator.kicad_sch').read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith('(wire') and '(xy 45.72 69.85)' in t:s=s[:a]+s[b:]
wire=lambda a,b:f'(wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]})) (stroke (width 0) (type default)) (uuid {uid()}))'
def label(net,x,y,ang=0):return f'(global_label {q(net)} (shape bidirectional) (at {x} {y} {ang}) (effects (font (size 1 1)) (justify '+('right' if ang in [180,270] else 'left')+f' bottom)) (uuid {uid()}))'
s=s.rstrip()[:-1]+wire((45.72,69.85),(40.64,69.85))+label('SYS_ON_REQ',40.64,69.85)+')';(r/'regulator.kicad_sch').write_text(s)
s=(r/'charging.kicad_sch').read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith('(global_label'):
  if '(at 365.76 184.15 ' in t:t=t.replace('"BAT_NTC"','"CELL_CHG_TEMP"',1)
  elif '(at 170.18 186.69 ' in t:t=t.replace('"BAT_NTC"','"CHG_TS_BIAS"',1)
  elif '(at 134.62 179.07 ' in t:t=t.replace('"GND"','"CHG_DISABLE"',1)
  s=s[:a]+t+s[b:]
(r/'charging.kicad_sch').write_text(s)
p=r/'battery_protection.kicad_sch';p.write_text(p.read_text().replace('"BAT_NTC"','"CELL_CHG_TEMP"').replace('TH1 -> J4 charger input','TH1 -> J4 analog charge window'))
top=(r/'omni_ugv.kicad_sch').read_text();rootid=re.search(r'\(uuid "?([0-9a-f-]+)',top)[1]
for page,(group,fn,title,note) in enumerate([(uv,'cell_undervoltage','Cell undervoltage load shutdown','Raw-cell supervisor: 3.1 V falling / about 3.3 V rising.\nClamps EN and driving; charger can recover cell while logic stays off.\nBQ298217 remains independent 2.6 V emergency backstop. Not a zero-leakage storage disconnect.'),(temp,'charge_temperature','Cell temperature charging window','TH1 is an insulated OFF-BOARD cell-mounted 103AT-2 probe at J4.\nU12 controls charging independently of ESP32 and main power switch.\nR60 intentionally biases the BQ TS input; U12/U13 replace its temperature decision.\nOpen or shorted probe disables charging. Beta-model tolerance envelope needs fixture verification.')],9):
 sid=uid();parts=[d for d in new if d['group']==group];used={d['key'] for d in parts}
 embedded=''.join(libs[k].replace('(symbol "'+k+'"','(symbol "UGV:'+k+'"',1) for k in used)
 sheet=f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {sid}) (paper "A3") (title_block (title {q(title)}) (rev "D-PROTOTYPE")) (lib_symbols {embedded})'
 for i,d in enumerate(parts):
  x=50.8+(i%4)*91.44;y=45.72+(i//4)*45.72;d.update(sx=x,sy=y,sheet_uuid=sid)
  pins=[p for _,_,u in blocks(libs[d['key']]) if u.startswith('(symbol') for _,_,p in blocks(u) if p.startswith('(pin ')]
  sheet+=f'(symbol (lib_id {q(d["symbol"])}) (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {d["uuid"]})'+prop('Reference',d['ref'],x,y-15.24)+prop('Value',d['value'],x,y-12.7)+prop('Footprint',d['localfp'],x,y,True)
  for p in pins:
   n=re.search(r'\(number "([^"]+)',p)[1];sheet+=f'(pin {q(n)} (uuid {uid()}))'
  sheet+=f'(instances (project "omni_ugv" (path "/{rootid}/{sid}" (reference {q(d["ref"])}) (unit 1)))))'
  for p in pins:
   n=re.search(r'\(number "([^"]+)',p)[1];px,py,ang=map(float,re.search(r'\(at ([^ ]+) ([^ ]+) ([^)]+)',p).groups());px=round(x+px,5);py=round(y-py,5);net=d['nets'][n]
   if net is None:sheet+=f'(no_connect (at {px} {py}) (uuid {uid()}))';continue
   ex=round(px-5.08*math.cos(math.radians(ang)),5);ey=round(py+5.08*math.sin(math.radians(ang)),5)
   sheet+=wire((px,py),(ex,ey))+label(net,ex,ey,int((ang+180)%360))
 sheet+=f'(text {q(note)} (at 25.4 238.76 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid {uid()})))'
 (r/(fn+'.kicad_sch')).write_text(sheet)
 # Root has room for these functional references below prior overview.
 xx=25.4+(page-9)*190.5;yy=241.3
 top=top.rstrip()[:-1]+f'(sheet (at {xx} {yy}) (size 165.1 15.24) (stroke (width 0.15) (type default)) (fill (color 0 0 0 0)) (uuid {sid}) (property "Sheetname" {q(title)} (at {xx} {yy-1.27} 0) (effects (font (size 1.27 1.27)) (justify left bottom))) (property "Sheetfile" {q(fn+".kicad_sch")} (at {xx} {yy+16.51} 0) (effects (font (size 1.27 1.27)) (justify left top))) (instances (project "omni_ugv" (path "/{rootid}" (page "{page}"))))) )'
(r/'omni_ugv.kicad_sch').write_text(top)
data+=new;(r/'design_connections.json').write_text(json.dumps(data,indent=2)+'\n');Path('work/power-rev-d/new_parts.json').write_text(json.dumps(new,indent=2))
with (r/'BOM.csv').open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
for d in rows:
 if d['Reference'] in dm:
  z=dm[d['Reference']];d.update(Value=z['value'],MPN=z.get('mpn',''),Notes=z.get('note',''))
for d in new:rows.append(dict(Reference=d['ref'],Value=d['value'],MPN=d['mpn'],Footprint=d['localfp'],Notes=d['note']+(' ; tolerance calculation uses resistor 1.5% envelope including TCR; exact passive MPN pending' if d['ref'].startswith('R') else '')))
for d in rows:
 if d['Reference']=='TH1':d['Notes']='Independent 103AT-2 bonded to cell and insulated; J4 analog charging window. Never PCB mounted.'
with (r/'BOM.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=['Reference','Value','MPN','Footprint','Notes']);w.writeheader();w.writerows(rows)
src=Path('C:/Program Files/KiCad/10.0/share/kicad/footprints/Package_TO_SOT_SMD.pretty/SOT-23-6.kicad_mod').read_text().replace('(footprint "SOT-23-6"','(footprint "Power_SOT23_6"',1)
(r/'UGV.pretty/Power_SOT23_6.kicad_mod').write_text(src)
print('Preserved Rev C; created Rev D native schematics and',len(new),'new parts')
