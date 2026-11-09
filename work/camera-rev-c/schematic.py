from pathlib import Path
import re,json,uuid,csv,sys,shutil
sys.path.insert(0,'work/humanize')
from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_C_flex_camera')
def uid():return str(uuid.uuid4())
def q(s):return json.dumps(str(s))
def prop(k,v,x,y,hide=False):return f'(property {q(k)} {q(v)} (at {x} {y} 0) (effects (font (size 1 1))'+(' hide' if hide else '')+'))'
libsrc=(r/'UGV.kicad_sym').read_text();libs={re.search(r'^\(symbol "([^"]+)',t)[1]:t for _,_,t in blocks(libsrc) if t.startswith('(symbol ')}
def boxlib(name,pins):
 s=f'(symbol "{name}" (in_bom yes) (on_board yes)'+prop('Reference','U',0,8)+prop('Value',name,0,6)
 s+=f'(symbol "{name}_0_1" (rectangle (start -5.08 5.08) (end 5.08 -5.08) (stroke (width 0.254) (type default)) (fill (type background))))'
 s+=f'(symbol "{name}_1_1"'
 for n,pn,typ,x,y,a in pins:s+=f'(pin {typ} line (at {x} {y} {a}) (length 2.54) (name {q(pn)} (effects (font (size 0.9 0.9)))) (number "{n}" (effects (font (size 0.9 0.9)))))'
 return s+'))'
names=['STROBE','AGND','SDA','AVDD','SCL','RESET','VSYNC','PWDN','HREF','DVDD','DOVDD','Y9','XCLK','Y8','DGND','Y7','PCLK','Y6','Y2','Y5','Y3','Y4','Y1','Y0']
cam=boxlib('Camera_FPC24',[(i+1,n,'passive',-7.62,29.21-i*2.54,0) for i,n in enumerate(names)])
cam=cam.replace('(start -5.08 5.08) (end 5.08 -5.08)','(start -5.08 31.75) (end 12.7 -31.75)')
ldo=boxlib('TLV755P_DBV',[(1,'IN','power_in',-7.62,2.54,0),(2,'GND','power_in',0,-7.62,90),(3,'EN','input',-7.62,-2.54,0),(4,'NC','no_connect',7.62,-2.54,180),(5,'OUT','power_out',7.62,2.54,180)])
libs.update(Camera_FPC24=cam,TLV755P_DBV=ldo)
for v in [cam,ldo]:libsrc=libsrc.rstrip()[:-1]+v+')'
(r/'UGV.kicad_sym').write_text(libsrc)
# Remove only the old header's presentation island, leaving MCU and support networks intact.
s=(r/'controller.kicad_sch').read_text()
for a,b,t in reversed(list(blocks(s))):
 remove=t.startswith('(symbol') and '(lib_id' in t and '(property "Reference" "J3"' in t
 if t.startswith(('(wire','(global_label','(junction','(no_connect')):
  pts=re.findall(r'\((?:xy|at) ([-\d.]+) ([-\d.]+)',t)
  remove=bool(pts) and all(265<float(x)<325 and 65<float(y)<112 for x,y in pts)
 if remove:s=s[:a]+s[b:]
(r/'controller.kicad_sch').write_text(s)
top=(r/'omni_ugv.kicad_sch').read_text();topid=re.search(r'\(uuid ([^)]+)',top)[1].strip(chr(34));sid=uid()
data=json.loads((r/'design_connections.json').read_text());old=next(x for x in data if x['ref']=='J3');data=[x for x in data if x['ref']!='J3'];new=[]
map24={1:None,2:'GND',3:'CAM_SDA',4:'CAM_2V8',5:'CAM_SCL',6:'CAM_RESET',7:'CAM_VSYNC',8:'GND',9:'CAM_HREF',10:'CAM_1V3',11:'+3V3',12:'CAM_D7',13:'CAM_XCLK',14:'CAM_D6',15:'GND',16:'CAM_D5',17:'CAM_PCLK',18:'CAM_D4',19:'CAM_D0',20:'CAM_D3',21:'CAM_D1',22:'CAM_D2',23:None,24:None}
def add(ref,val,key,fp,nets,sx,sy,x,y,mpn=''):
 new.append(dict(ref=ref,value=val,key=key,symbol='UGV:'+key,fp=fp,localfp='UGV:'+fp,nets={str(k):v for k,v in nets.items()},sx=sx,sy=sy,x=x,y=y,a=0,side='F',mpn=mpn,uuid=uid(),group='Flex camera',note='Rev C camera redesign; qualification pending'))
add('J3','M0031 CAMERA FPC24','Camera_FPC24','Camera_FH12_24',map24,90.17,90.17,132,76,'FH12-24S-0.5SH(55)')
add('U8','TLV75513PDBVR','TLV755P_DBV','Camera_SOT23_5',{1:'+3V3',2:'GND',3:'+3V3',4:None,5:'CAM_1V3'},180.34,50.8,122,74,'TLV75513PDBVR')
add('U9','TLV75528PDBVR','TLV755P_DBV','Camera_SOT23_5',{1:'+3V3',2:'GND',3:'+3V3',4:None,5:'CAM_2V8'},180.34,101.6,122,82,'TLV75528PDBVR')
for ref,net,sx,sy,x,y in [('C26','+3V3',144.78,76.2,118,72),('C27','CAM_1V3',215.9,76.2,126,72),('C28','+3V3',144.78,127,118,80),('C29','CAM_2V8',215.9,127,126,80)]:
 add(ref,'2.2u/10V X7R','Device__C','Capacitor_SMD__C_0603_1608Metric',{1:net,2:'GND'},sx,sy,x,y)
for ref,net,sx,sy,x,y in [('R44','CAM_SDA',270.51,50.8,131,85),('R45','CAM_SCL',270.51,101.6,134,85)]:
 add(ref,'4.7k','Device__R','Resistor_SMD__R_0603_1608Metric',{1:'+3V3',2:net},sx,sy,x,y)
used=set(d['key'] for d in new);embedded=''.join(libs[k].replace('(symbol "'+k+'"','(symbol "UGV:'+k+'"',1) for k in used)
sheet=f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {sid}) (paper "A3") (title_block (title "OV2640 M0031 flex interface") (rev "C-DRAFT")) (lib_symbols {embedded})'
for d in new:
 x,y=d['sx'],d['sy'];pins=[p for _,_,u in blocks(libs[d['key']]) if u.startswith('(symbol') for _,_,p in blocks(u) if p.startswith('(pin ')]
 sheet+=f'(symbol (lib_id {q(d["symbol"])}) (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {d["uuid"]})'+prop('Reference',d['ref'],x+17.78,y-5.08)+prop('Value',d['value'],x+25.4,y-1.27)+prop('Footprint',d['localfp'],x,y,True)
 for p in pins:
  pin_num=re.search(r'\(number "([^"]+)',p)[1];sheet+=f'(pin {q(pin_num)} (uuid {uid()}))'
 sheet+=f'(instances (project "omni_ugv" (path "/{topid}/{sid}" (reference {q(d["ref"])}) (unit 1)))))'
 for p in pins:
  n=re.search(r'\(number "([^"]+)',p)[1];px,py,ang=map(float,re.search(r'\(at ([^ ]+) ([^ ]+) ([^)]+)',p).groups());px+=x;py=y-py;net=d['nets'][n]
  if net is None:sheet+=f'(no_connect (at {px} {py}) (uuid {uid()}))';continue
  import math
  ex=round(px-5.08*math.cos(math.radians(ang)),5);ey=round(py+5.08*math.sin(math.radians(ang)),5);la=int((ang+180)%360);just='right' if la in [180,270] else 'left'
  sheet+=f'(wire (pts (xy {px} {py}) (xy {ex} {ey})) (stroke (width 0) (type default)) (uuid {uid()})) (global_label {q(net)} (shape bidirectional) (at {ex} {ey} {la}) (effects (font (size 1 1)) (justify {just} bottom)) (uuid {uid()}))'
sheet+=f'(text "M0031 only. Verify flex contact side, thickness and pin-1 before assembly.\n1.3 V core / 2.8 V analog / 3.3 V I-O. No interchangeable generic OV2640 pinout." (at 30.48 172.72 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid {uid()})))'
(r/'camera.kicad_sch').write_text(sheet)
top=top.rstrip()[:-1]+f'(sheet (at 260.35 165.1) (size 88.9 20.32) (stroke (width 0.15) (type default)) (fill (color 0 0 0 0)) (uuid {sid}) (property "Sheetname" "Flex camera" (at 260.35 163.83 0) (effects (font (size 1.27 1.27)) (justify left bottom))) (property "Sheetfile" "camera.kicad_sch" (at 260.35 186.69 0) (effects (font (size 1.27 1.27)) (justify left top))) (instances (project "omni_ugv" (path "/{topid}" (page "8"))))) )'
(r/'omni_ugv.kicad_sch').write_text(top)
data+=new;(r/'design_connections.json').write_text(json.dumps(data,indent=2)+'\n');Path('work/camera-rev-c/new_parts.json').write_text(json.dumps(new,indent=2))
with (r/'BOM.csv').open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
rows=[d for d in rows if d['Reference']!='J3']
for d in new:rows.append(dict(Reference=d['ref'],Value=d['value'],MPN=d['mpn'],Footprint=d['localfp'],Notes=d['note']))
rows.append(dict(Reference='CAM1',Value='OV2640 24-pin DVP flex camera',MPN='Arducam M0031',Footprint='OFFBOARD',Notes='Manufacturer pinout basis; confirm supplied module revision/contact orientation; bracket dimensions require measurement.'))
with (r/'BOM.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=['Reference','Value','MPN','Footprint','Notes']);w.writeheader();w.writerows(rows)
for src,dst in [('Connector_FFC-FPC/Hirose_FH12-24S-0.5SH_1x24-1MP_P0.50mm_Horizontal','Camera_FH12_24'),('Package_TO_SOT_SMD/SOT-23-5','Camera_SOT23_5')]:
 folder,name=src.split('/');s=(Path('C:/Program Files/KiCad/10.0/share/kicad/footprints')/(folder+'.pretty')/(name+'.kicad_mod')).read_text();s=s.replace('(footprint "'+name+'"','(footprint "'+dst+'"',1);(r/'UGV.pretty'/(dst+'.kicad_mod')).write_text(s)
print('Created Rev C native camera sheet, symbols, BOM and connector library.')
