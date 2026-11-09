from pathlib import Path
import json,re,uuid,csv,sys,math
sys.path.insert(0,'work/humanize');import build as h
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout')
uid=lambda:str(uuid.uuid4())
q=lambda v:json.dumps(str(v))
def prop(k,v,x,y,hide=False):return f'(property {q(k)} {q(v)} (at {x} {y} 0) (effects (font (size 1 1))'+(' hide' if hide else '')+'))'
data=json.loads((r/'design_connections.json').read_text());dm={d['ref']:d for d in data}
libs={re.search(r'^\(symbol "([^"]+)',t)[1]:t for _,_,t in h.blocks((r/'UGV.kicad_sym').read_text()) if t.startswith('(symbol')}
sym='(symbol "PFET_3333" (in_bom yes) (on_board yes)'+prop('Reference','Q',0,10)+prop('Value','DMP2008UFG-7',0,8)
sym+='(symbol "PFET_3333_0_1" (rectangle (start -5.08 5.08) (end 5.08 -5.08) (stroke (width .254) (type default)) (fill (type background))))(symbol "PFET_3333_1_1"'
for n,name,x,y,a in [(1,'S [1-3]',-7.62,0,0),(2,'S',-7.62,0,0),(3,'S',-7.62,0,0),(4,'G',0,-7.62,90),(5,'D [5-8]',7.62,0,180)]:
 sym+=f'(pin passive line (at {x} {y} {a}) (length 2.54)'+(' hide' if n in [2,3] else '')+f'(name {q(name)} (effects (font (size .85 .85)))) (number "{n}" (effects (font (size .85 .85)))))'
sym+='))';libs['PFET_3333']=sym
p=r/'UGV.kicad_sym'
if '(symbol "PFET_3333"' not in p.read_text():p.write_text(p.read_text().rstrip()[:-1]+sym+')')
src=Path('C:/Program Files/KiCad/10.0/share/kicad/footprints/Package_SON.pretty/Diodes_PowerDI3333-8.kicad_mod').read_text()
src=src.replace('(footprint "Diodes_PowerDI3333-8"','(footprint "Discharge_PowerDI3333_8"',1)
(r/'UGV.pretty/Discharge_PowerDI3333_8.kicad_mod').write_text(src)
new=[]
def add(ref,val,key,fp,nets,x,y,mpn=''):
 d=dict(ref=ref,value=val,key=key,symbol='UGV:'+key,fp=fp,localfp='UGV:'+fp,nets={str(k):v for k,v in nets.items()},x=x,y=y,a=0,side='B',mpn=mpn,uuid=uid(),group='Independent discharge cutoff',note='Rev E 3.1V discharge-only cutoff. Prototype; transient and thermal qualification required.')
 new.append(d);return d
add('Q12','MMBT3906','PNP_123','Package_TO_SOT_SMD__SOT-23',{1:'CUT_PNP_B',2:'CELL_P',3:'CUT_GATE'},132,130,'MMBT3906-7-F')
add('Q13','DMP2008UFG-7','PFET_3333','Discharge_PowerDI3333_8',{1:'CELL_P',2:'CELL_P',3:'CELL_P',4:'CUT_GATE',5:'CELL_SWITCHED'},128,135.5,'DMP2008UFG-7')
for ref,val,n1,n2,x,y in [('R65','47k','CELL_UV_RESET_N','CUT_PNP_B',135,126),('R66','1M','CELL_P','CUT_PNP_B',135,129),('R67','56k','CUT_GATE','CELL_N',132,133.5)]:
 add(ref,val,'Device__R','Resistor_SMD__R_0603_1608Metric',{1:n1,2:n2},x,y)
for n in ['1','2','3']:dm['Q7']['nets'][n]='CELL_SWITCHED'
dm['R40']['nets']['2']='CELL_SWITCHED';dm['R46']['nets']['1']='CELL_P'
dm['R46']['note']='Raw-cell pullup is required to operate the independent discharge cutoff after protected VBAT collapses.'
data+=new;dm.update({d['ref']:d for d in new})
top=(r/'omni_ugv.kicad_sch').read_text();rootid=re.search(r'\(uuid "?([0-9a-f-]+)',top)[1];sid=next(re.search(r'\(uuid "?([0-9a-f-]+)',t)[1] for a,b,t in h.blocks(top) if t.startswith('(sheet') and 'discharge_cutoff.kicad_sch' in t)
sheet='(kicad_sch (version 20250114) (generator "eeschema") (uuid '+sid+') (paper "A3") (title_block (title "Independent discharge cutoff") (rev "E - prototype")) (lib_symbols '+''.join(libs[k].replace('(symbol "'+k+'"','(symbol "UGV:'+k+'"',1) for k in {d['key'] for d in new})+'))'
sheet=sheet[:-1]
for i,d in enumerate(new):
 x=50.8+i*60.96;y=63.5;d['sheet_uuid']=sid;d['sx']=x;d['sy']=y
 sheet+=f'(symbol (lib_id {q(d["symbol"])}) (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {d["uuid"]})'+prop('Reference',d['ref'],x,y-15.24)+prop('Value',d['value'],x,y-12.7)+prop('Footprint',d['localfp'],x,y,True)
 for n in d['nets']:sheet+=f'(pin "{n}" (uuid {uid()}))'
 sheet+=f'(instances (project "omni_ugv" (path "/{rootid}/{sid}" (reference {q(d["ref"])}) (unit 1)))))'
sheet+=')';(r/'discharge_cutoff.kicad_sch').write_text(sheet)
top=top.rstrip()[:-1]+f'(sheet (at 25.4 267.97) (size 165.1 12.7) (stroke (width .15) (type default)) (fill (color 0 0 0 0)) (uuid {sid}) (property "Sheetname" "Independent discharge cutoff" (at 25.4 266.7 0) (effects (font (size 1.27 1.27)) (justify left bottom))) (property "Sheetfile" "discharge_cutoff.kicad_sch" (at 25.4 281.94 0) (effects (font (size 1.27 1.27)) (justify left top))) (instances (project "omni_ugv" (path "/{rootid}" (page "11"))))) )'
# Root sheet was already created by the first run.
# Raw reset pullup: identify its previous direct VBAT terminal in the functional drawing.
p=r/'cell_undervoltage.kicad_sch';s=p.read_text();s=s.replace('(symbol\n','(symbol ');p.write_text(s)
h.ROOT=r;h.BASE=r;h.data=dm;h.data.update(TH1={'nets':{'1':'CELL_CHG_TEMP','2':'GND'}},TH2={'nets':{'1':'CELL_TEMP_DIV','2':'GND'}})
# Reuse the established UV diagram and replace its obsolete explanatory note.
sh=h.Sheet('cell_undervoltage','Independent cell undervoltage shutdown')
for ref,x,y,a in [('U14',80,140,0),('R64',30,140,0),('C37',55,160,0),('U10',50,65,0),('C30',20,65,0),('C31',80,90,0),('R46',95,45,0),('R47',115,63,90),('Q9',145,63,0),('R48',130,40,0),('R49',175,95,0),('R50',200,63,90),('Q10',235,63,0),('R51',225,95,0),('R52',200,130,90),('Q11',235,130,0),('R53',225,160,0),('R54',280,63,90)]:sh.place(ref,x,y,a)
sh.join('CELL_P',[('U10',2),('U10',4),('C30',1)],axis='v',rail=30)
sh.join('CELL_UV_RESET_N',[('U10',1),('R46',2),('R47',1)],rail=55)
sh.link('CELL_UV_CT',('U10',5),('C31',1),[(80,67)])
sh.join('CELL_UV_PNP_B',[('R47',2),('R48',2),('Q9',1)],rail=63)
sh.join('CELL_UV_FAULT',[('Q9',3),('R49',1),('R50',1),('R52',1)],axis='v',rail=180)
sh.join('CELL_UV_EN_B',[('R50',2),('Q10',1),('R51',1)],rail=63)
sh.join('CELL_UV_MOTOR_B',[('R52',2),('Q11',1),('R53',1)],rail=130)
sh.join('SYS_ON',[('Q10',3),('R54',2)],rail=80)
sh.join('DRIVE_REQ_RAW',[('U14',2),('R64',1)],axis='v',rail=60)
sh.text('3.1 V supervisor: load inhibits plus independent discharge cutoff on sheet 11',15,25)
sh.text('R46 now pulls RESET_N to raw CELL_P. Q12/Q13 remain effective after protected VBAT disappears.\nQ9/Q10/Q11 retain the existing logic and motor inhibits; R64 defaults the motor request low.\nU7 retains independent overvoltage/current/short protection and its factory 2.6 V UV threshold.\nThis is not a zero-leakage storage disconnect: the supervisor, protector and cutoff bias still use cell current.',20,190)
sh.finish()
sh=h.Sheet('discharge_cutoff','Discharge cutoff with charge recovery')
for ref,x,y,a in [('Q12',110,65,0),('Q13',190,65,0),('R65',65,65,90),('R66',90,35,0),('R67',150,105,0)]:sh.place(ref,x,y,a)
sh.covered.update([('Q13','2'),('Q13','3')])
sh.join('CUT_PNP_B',[('R65',2),('R66',2),('Q12',1)],axis='v',rail=90)
sh.join('CELL_P',[('Q12',2),('R66',1),('Q13',1)],rail=25)
sh.join('CUT_GATE',[('Q12',3),('Q13',4),('R67',1)],rail=90)
sh.text('Discharge: CELL_P -> Q13 -> CELL_SWITCHED -> Q7/Q8 -> VBAT',20,145)
sh.text('U10 RESET_N low turns Q12 on and raises Q13 gate to its source: discharge stops.\nTrip window 3.0535..3.1465 V (static, 3.1 V +/-1.5%); hysteresis permits recovery around 3.3 V.\nQ13 body diode points from CELL_SWITCHED to CELL_P, allowing recovery charging while Q13 is off.\nBQ24074 and the independent cell-mounted TH1 window still control charging. U7 protection is in series.\nDo not use the U7 CTR shutdown input for this function: its shutdown recovery must not be assumed.\nVerify dip response, recovery, standby draw and FET heating on the actual board before release.',20,170)
sh.finish()
# Change the existing Q7/R40 power labels by rebuilding their functional sheet from its previous adapter.
src=Path('work/rev-e/step3_schematic.py').read_text();start=src.index("sh=h.Sheet('battery_protection'");end=src.index('# Ground-side sense reference',start)
exec(src[start:end])
for p in r.glob('*.kicad_sch'):
 s=p.read_text().replace('B - prototype','E - prototype');p.write_text(s)
(r/'design_connections.json').write_text(json.dumps(data,indent=2));Path('work/rev-e/cutoff-new-parts.json').write_text(json.dumps(new,indent=2))
with (r/'BOM.csv').open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
for row in rows:
 if row['Reference']=='R46':row['Notes']=dm['R46']['note']
for d in new:rows.append(dict(Reference=d['ref'],Value=d['value'],MPN=d['mpn'],Footprint=d['localfp'],Notes=d['note']))
with (r/'BOM.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print('Added independent discharge cutoff: Q12/Q13/R65/R66/R67')
