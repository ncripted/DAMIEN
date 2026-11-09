from pathlib import Path
import json,re,uuid,sys,csv
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');data=json.loads((r/'design_connections.json').read_text());dm={d['ref']:d for d in data};p=Path('work/power-rev-d/new_parts.json');new=json.loads(p.read_text());assert 'U14' not in dm
fn=r/'UGV.kicad_sym';s=fn.read_text();lib=next(t for a,b,t in blocks(s) if t.startswith('(symbol "LVC1G14_DBV"'));lib=lib.replace('LVC1G14_DBV','LVC1G17_DBV');s=s.rstrip()[:-1]+lib+')';fn.write_text(s)
sid=re.search(r'\(uuid "?([0-9a-f-]+)',(r/'cell_undervoltage.kicad_sch').read_text())[1];tid=re.search(r'\(uuid "?([0-9a-f-]+)',(r/'omni_ugv.kicad_sch').read_text())[1]
specs=[('U14','SN74LVC1G17DBVR','LVC1G17_DBV','Camera_SOT23_5',{1:None,2:'DRIVE_REQ_RAW',3:'GND',4:'DRIVE_REQ',5:'+3V3'},66,97,'SN74LVC1G17DBVR'),('R64','100k','Device__R','Resistor_SMD__R_0603_1608Metric',{1:'DRIVE_REQ_RAW',2:'GND'},63,94,''),('C37','100n/10V X7R','Device__C','Capacitor_SMD__C_0603_1608Metric',{1:'+3V3',2:'GND'},66,101,'')]
libs={re.search(r'^\(symbol "([^"]+)',t)[1]:t for a,b,t in blocks(s) if t.startswith('(symbol')}
sheet=(r/'cell_undervoltage.kicad_sch').read_text();lblock=next(t for a,b,t in blocks(sheet) if t.startswith('(lib_symbols'));sheet=sheet.replace(lblock,lblock[:-1]+lib.replace('(symbol "LVC1G17_DBV"','(symbol "UGV:LVC1G17_DBV"',1)+')',1)
def prop(k,v,x,y,hide=False):return f'(property "{k}" {json.dumps(v)} (at {x} {y} 0) (effects (font (size 1 1))'+(' hide' if hide else '')+'))'
for ref,val,key,fp,nets,x,y,mpn in specs:
 d=dict(ref=ref,value=val,key=key,symbol='UGV:'+key,fp=fp,localfp='UGV:'+fp,nets={str(k):v for k,v in nets.items()},x=x,y=y,a=0,side='F',mpn=mpn,uuid=str(uuid.uuid4()),sheet_uuid=sid,group='Cell undervoltage shutdown',note='Rev D drive-request buffer; input defaults low; USB/UV clamp remains after series resistor')
 new.append(d);data.append(d);sx,sy={'U14':(101.6,177.8),'R64':(38.1,177.8),'C37':(69.85,203.2)}[ref];d.update(sx=sx,sy=sy)
 pins=[p for a,b,u in blocks(libs[key]) if u.startswith('(symbol') for a,b,p in blocks(u) if p.startswith('(pin ')]
 ss=f'(symbol (lib_id "UGV:{key}") (at {sx} {sy} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {d["uuid"]})'+prop('Reference',ref,sx,sy-18)+prop('Value',val,sx,sy-15)+prop('Footprint','UGV:'+fp,sx,sy,True)
 for pp in pins:ss+=f'(pin "{re.search(chr(92)+chr(40)+"number "+chr(34)+"([^"+chr(34)+"]+)",pp)[1]}" (uuid {uuid.uuid4()}))'
 ss+=f'(instances (project "omni_ugv" (path "/{tid}/{sid}" (reference "{ref}") (unit 1)))))'
 import math
 for pp in pins:
  n=re.search(r'\(number "([^"]+)',pp)[1];px,py,ang=map(float,re.search(r'\(at ([^)]+)',pp)[1].split());px+=sx;py=sy-py;net=d['nets'][n]
  if net is None:ss+=f'(no_connect (at {px} {py}) (uuid {uuid.uuid4()}))';continue
  ex=round(px-5.08*math.cos(math.radians(ang)),5);ey=round(py+5.08*math.sin(math.radians(ang)),5);la=int((ang+180)%360) if ang in [0,180] else 0
  ss+=f'(wire (pts (xy {px} {py}) (xy {ex} {ey})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))(global_label {json.dumps(net)} (shape bidirectional) (at {ex} {ey} {la}) (effects (font (size 1 1)) (justify '+('right' if la==180 else 'left')+f' bottom)) (uuid {uuid.uuid4()}))'
 sheet=sheet.rstrip()[:-1]+ss+')'
(r/'cell_undervoltage.kicad_sch').write_text(sheet)
dm['U1']['nets']['35']='DRIVE_REQ_RAW';dm['R28']['value']='1M'
fn=r/'controller.kicad_sch';fn.write_text(fn.read_text().replace('(global_label "DRIVE_REQ"','(global_label "DRIVE_REQ_RAW"'))
fn=r/'interlock.kicad_sch';s=fn.read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith('(symbol') and '(property "Reference" "R28"' in t:t=re.sub(r'(\(property "Value" )"[^"]+"',r'\1"1M"',t,count=1);s=s[:a]+t+s[b:]
fn.write_text(s);(r/'design_connections.json').write_text(json.dumps(data,indent=2));p.write_text(json.dumps(new,indent=2))
with (r/'BOM.csv').open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
for d in rows:
 if d['Reference']=='R28':d['Value']='1M'
for d in new[-3:]:rows.append(dict(Reference=d['ref'],Value=d['value'],MPN=d['mpn'],Footprint=d['localfp'],Notes=d['note']))
with (r/'BOM.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print('Added buffered drive request and explicit default-low input')
