"""Presentation-only native KiCad rewrite; input is the preserved pre-cleanup snapshot.
Run from workspace root. PCB and electrical metadata are not modified.
"""
from pathlib import Path
import re,json,math,uuid,hashlib
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'engineering/presentation_baseline'
def blocks(s):
 depth=0;quoted=False;esc=False;start=0
 for i,c in enumerate(s):
  if quoted:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c=='(':
   if depth==1:start=i
   depth+=1
  elif c==')':
   if depth==2:yield start,i+1,s[start:i+1]
   depth-=1
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'rover-readable/'+s))
def q(s):return json.dumps(s)
def mm(v):return round(v*1.27,5)
def xy(p):return f'{p[0]:.5f} {p[1]:.5f}'
data={d['ref']:d for d in json.loads((ROOT/'design_connections.json').read_text())}
data.update(TH1={'nets':{'1':'BAT_NTC','2':'GND'}},TH2={'nets':{'1':'CELL_TEMP_DIV','2':'GND'}})
class Sheet:
 def __init__(self,name,title):
  self.name=name;self.title=title;self.s=(BASE/(name+'.kicad_sch')).read_text();self.items=list(blocks(self.s))
  self.lib=next(t for a,b,t in self.items if t.startswith('(lib_symbols'))
  self.libs={re.search(r'^\(symbol "([^"]+)',t)[1]:t for a,b,t in blocks(self.lib)}
  if name=='battery_protection':
   key='UGV:CSD17308Q3';v=self.libs[key];changes=[]
   for a,b,u in blocks(v):
    if not u.startswith('(symbol'):continue
    pu=[]
    for aa,bb,p in blocks(u):
     if not p.startswith('(pin '):continue
     n=int(re.search(r'\(number "([^"]+)',p)[1])
     pos='-12.7 0 0' if n<4 else '0 -10.16 90' if n==4 else '12.7 0 180'
     p=re.sub(r'\(at [^)]+\)',f'(at {pos})',p,count=1)
     if n not in [1,4,5]:p=p.replace('(length 2.54)','(length 2.54) hide',1)
     if n==1:p=p.replace('(name "S"','(name "S [1-3]"')
     if n==5:p=p.replace('(name "D"','(name "D [5-9]"')
     pu.append((aa,bb,p))
    for aa,bb,p in reversed(pu):u=u[:aa]+p+u[bb:]
    u=re.sub(r'\(start -10.16 [^)]+\) \(end 10.16 [^)]+\)','(start -10.16 7.62) (end 10.16 -7.62)',u)
    changes.append((a,b,u))
   for a,b,u in reversed(changes):v=v[:a]+u+v[b:]
   self.lib=self.lib.replace(self.libs[key],v);self.libs[key]=v
   lp=ROOT/'UGV.kicad_sym';ls=lp.read_text()
   for a,b,u in blocks(ls):
    if u.startswith('(symbol "CSD17308Q3"'):
     ls=ls[:a]+v.replace('"UGV:CSD17308Q3"','"CSD17308Q3"',1)+ls[b:];break
   lp.write_text(ls)
  self.orig={re.search(r'\(property "Reference" "([^"]+)',t)[1]:t for a,b,t in self.items if t.startswith('(symbol ')}
  self.out=[];self.pins={};self.covered=set();self.placed=set();self.seq=0;self.segments=[];self.labels=[]
 def id(self):self.seq+=1;return uid(self.name+str(self.seq))
 def text(self,s,x,y,size=1.27):
  self.out.append(f'(text {q(s)} (at {mm(x)} {mm(y)} 0) (effects (font (size {size} {size})) (justify left)) (uuid {self.id()}))')
 def place(self,ref,x,y,ang=0):
  t=self.orig[ref];self.placed.add(ref);x,y=mm(x),mm(y)
  libid=re.search(r'\(lib_id "([^"]+)',t)[1]; lib=self.libs[libid];pins=[]
  for a,b,u in blocks(lib):
   if u.startswith('(symbol'):
    pins.extend(p for aa,bb,p in blocks(u) if p.startswith('(pin '))
  c=round(math.cos(math.radians(ang)));sn=round(math.sin(math.radians(ang)))
  coords=[]
  for p in pins:
   n=re.search(r'\(number "([^"]+)',p)[1];px,py,pa=map(float,re.search(r'\(at ([^)]+)',p)[1].split())
   pos=(round(x+c*px-sn*py,5),round(y-sn*px-c*py,5)); direction=(pa+ang)%360
   self.pins[(ref,n)]=(pos,direction);coords.append(pos)
  t=re.sub(r'\(at [-\d.]+ [-\d.]+ [-\d.]+\)',f'(at {x} {y} {ang})',t,count=1)
  edits=[]
  passive=ref.startswith(('R','C','L','TH'))
  for a,b,u in blocks(t):
   if not u.startswith('(property '):continue
   name=re.search(r'\(property "([^"]+)',u)[1]
   if name not in ['Reference','Value']:continue
   if passive and ang in [0,180]: tx,ty=x+4.0,y+(-1.27 if name=='Reference' else 1.27);just='(justify right)' if ang==180 else '(justify left)'
   else:tx,ty=x,min(p[1] for p in coords)-(5.08 if name=='Reference' else 2.54);just=''
   if ref in ['Q7','Q8']:tx,ty=x-4,y-(14 if name=='Reference' else 11.46)
   if ref=='U7':tx,ty=x+5,y-(18 if name=='Reference' else 15.46)
   if ref=='Q8':tx,ty=x+20,y-(18 if name=='Reference' else 15.46)
   if ref=='U1':tx=x-20
   if ref=='U4':tx,ty=x,y-(15 if name=='Reference' else 12.46)
   if ref=='J1':ty=min(p[1] for p in coords)-(10.16 if name=='Reference' else 7.62)
   if ref in ['U2','U3']:tx=x-7
   if ref in ['Q1','Q2','Q3','Q4','Q5','Q6','U6']:tx=x-12
   u=re.sub(r'\(at [^)]+\)',f'(at {tx} {ty} {ang%180})',u,count=1)
   u=re.sub(r'\(effects[\s\S]*',f'(effects (font (size 1.0 1.0)) {just}))',u)
   edits.append((a,b,u))
  for a,b,u in reversed(edits):t=t[:a]+u+t[b:]
  self.out.append(t)
 def p(self,ref,pin):return self.pins[(ref,str(pin))][0]
 def wire(self,*points):
  for a,b in zip(points,points[1:]):
   if a==b:continue
   assert a[0]==b[0] or a[1]==b[1],(self.name,a,b)
   self.segments.append((a,b))
   self.out.append(f'(wire (pts (xy {xy(a)}) (xy {xy(b)})) (stroke (width 0) (type default)) (uuid {self.id()}))')
 def label(self,net,p,angle=0,local=False):
  self.labels.append((net,p,len(self.out)))
  kind='global_label';shape='(shape bidirectional)'
  just='right bottom' if angle in [180,270] else 'left bottom'
  self.out.append(f'({kind} {q(net)} {shape} (at {xy(p)} {angle}) (effects (font (size 0.9 0.9)) (justify {just})) (uuid {self.id()}))')
 def join(self,net,refs,axis='h',rail=None):
  # A shared straight rail and short orthogonal branches. Explicit junctions are added at finalization.
  keys=[(r,str(n)) for r,n in refs];pts=[self.p(*k) for k in keys]
  assert all(data.get(r,{}).get('nets',{}).get(n,net)==net for r,n in keys)
  self.covered.update(keys)
  if axis=='h':
   v=mm(rail) if rail is not None else pts[0][1]; taps=sorted(set((p[0],v) for p in pts))
   for p in pts:self.wire(p,(p[0],v))
  else:
   v=mm(rail) if rail is not None else pts[0][0];taps=sorted(set((v,p[1]) for p in pts),key=lambda p:p[1])
   for p in pts:self.wire(p,(v,p[1]))
  self.wire(*taps)
  anchor=taps[0]
  self.label(net,anchor,0,True)
 def link(self,net,a,b,via=None):
  a=(a[0],str(a[1]));b=(b[0],str(b[1]));self.covered.update([a,b]);p=self.p(*a);z=self.p(*b)
  pts=[p]+([(mm(x),mm(y)) for x,y in via] if via else ([(z[0],p[1])] if p[0]!=z[0] and p[1]!=z[1] else []))+[z]
  self.wire(*pts);self.label(net,pts[1] if len(pts)>2 else p,0,True)
 def finish(self):
  # Preserve and relocate ERC power flags into an explicit small block.
  flags=[r for r in self.orig if r.startswith('#')]
  for i,r in enumerate(flags):
   self.place(r,25+i*35,205)
   old=self.orig[r];oldpt=tuple(map(float,re.search(r'\(at ([\d.]+) ([\d.]+)',old).groups()))
   oldlabels=[t for a,b,t in self.items if t.startswith('(global_label') and tuple(map(float,re.search(r'\(at ([-\d.]+) ([-\d.]+)',t).groups()))==oldpt]
   if oldlabels:self.label(re.search(r'\(global_label "([^"]+)',oldlabels[0])[1],self.p(r,1))
   self.covered.add((r,'1'))
  assert set(self.orig)==self.placed,(self.name,set(self.orig)-self.placed)
  used=set()
  for k,(p,ang) in self.pins.items():
   if k in self.covered:continue
   net=data.get(k[0],{}).get('nets',{}).get(k[1])
   if (p,net) in used:continue
   used.add((p,net))
   if net is None:
    self.out.append(f'(no_connect (at {xy(p)}) (uuid {self.id()}))');continue
   a=math.radians(ang);end=(round(p[0]-5.08*math.cos(a),5),round(p[1]+5.08*math.sin(a),5))
   self.wire(p,end);self.label(net,end,int((ang+180)%360))
  # T branches and shared endpoints are explicitly dotted. No unrelated crossings are joined.
  ends=set(p for seg in self.segments for p in seg)
  for p in ends:
   rays=set()
   for a,b in self.segments:
    if (a[0]==b[0]==p[0] and min(a[1],b[1])<=p[1]<=max(a[1],b[1])) or (a[1]==b[1]==p[1] and min(a[0],b[0])<=p[0]<=max(a[0],b[0])):
     for z in [a,b]:
      if z!=p:rays.add((0 if z[0]==p[0] else (1 if z[0]>p[0] else -1),0 if z[1]==p[1] else (1 if z[1]>p[1] else -1)))
   if len(rays)>=3:self.out.append(f'(junction (at {xy(p)}) (diameter 0) (color 0 0 0 0) (uuid {self.id()}))')
  # Remove redundant labels only when they belong to the same visible wire component.
  parent={p:p for p in ends|{p for n,p,i in self.labels}}
  def find(p):
   while parent[p]!=p:parent[p]=parent[parent[p]];p=parent[p]
   return p
  for a,b in self.segments:
   for p in parent:
    if (a[0]==b[0]==p[0] and min(a[1],b[1])<=p[1]<=max(a[1],b[1])) or (a[1]==b[1]==p[1] and min(a[0],b[0])<=p[0]<=max(a[0],b[0])):parent[find(p)]=find(a)
  seen=set()
  geometric_nets={}
  for net,p,i in self.labels:
   key=(net,find(p))
   geometric_nets.setdefault(find(p),set()).add(net)
   if key in seen:self.out[i]=''
   seen.add(key)
  assert not [v for v in geometric_nets.values() if len(v)>1],(self.name,[v for v in geometric_nets.values() if len(v)>1])
  rootid=re.search(r'\(uuid ([^)]+)',self.s)[1]
  self.text(self.title,15,14,2.0)
  result=f'(kicad_sch (version 20230121) (generator eeschema) (uuid {rootid}) (paper "A3") (title_block (title {q(self.title)}) (rev "B - prototype") (company "Nate | Omni camera rover"))\n{self.lib}\n'+ '\n'.join(self.out)+')'
  (ROOT/(self.name+'.kicad_sch')).write_text(result)

def build():
 s=Sheet('controller','Controller, camera and service points')
 for r,x,y,a in [('U1',85,65,0),('C2',125,42,0),('C3',145,42,0),('R1',30,48,0),('C1',30,70,0),('SW1',47,70,270),('R2',30,110,0),('SW2',30,130,270),('R3',135,105,90),('D1',160,105,180),('J3',230,65,0),('R4',205,110,0),('C4',205,130,0),('C5',260,110,0)]:s.place(r,x,y,a)
 s.join('+3V3',[('U1',2),('C2',1),('C3',1)],rail=33)
 s.join('GND',[('C2',2),('C3',2)],rail=52)
 s.join('ESP_EN',[('R1',2),('C1',1),('SW1',1)],rail=60)
 s.join('GND',[('C1',2),('SW1',2)],rail=80)
 s.link('ESP_EN',('U1',3),('R1',2),[(55,47),(55,60),(30,60)])
 s.join('ESP_BOOT',[('R2',2),('SW2',1)],rail=120)
 s.link('LED_A',('R3',2),('D1',2))
 s.join('CAM_RESET',[('R4',2),('C4',1)],rail=120)
 s.link('CAM_RESET',('J3',17),('R4',2),[(215,73),(215,120),(205,120)])
 s.text('RESET / enable RC',20,30);s.text('BOOT strap',20,96);s.text('Status indicator',120,90)
 s.text('Waveshare OV2640 | documented 2 x 9 interface',190,30)
 s.text('Camera reset RC',190,96);s.text('[SPEC] GPIO35 / 36 / 37 reserved for N8R8 PSRAM.',65,145)
 s.text('Service points (named nets continue on other sheets)',20,162)
 for i in range(1,12):s.place('TP'+str(i),25+(i-1)%6*43,180+(i-1)//6*25)
 s.finish()

 s=Sheet('regulator','3.3 V buck-boost supply')
 for r,x,y,a in [('U4',125,80,0),('L1',175,80,0),('C18',205,105,0),('C19',220,60,0),('C20',245,60,0),('R20',70,85,0),('R21',70,110,0),('R22',95,120,0),('R23',40,85,0),('SW3',40,55,0)]:s.place(r,x,y,a)
 s.link('REG_L2',('U4',7),('L1',2),[(160,78),(160,90),(175,90)])
 s.link('REG_L1',('U4',9),('L1',1),[(150,82),(150,70),(175,70)])
 s.join('+3V3',[('U4',6),('C19',1),('C20',1)],rail=48)
 s.join('GND',[('C19',2),('C20',2)],rail=70)
 s.join('REG_FB',[('R20',2),('R21',1)],rail=97)
 s.link('REG_FB',('U4',4),('R20',2),[(90,82),(90,97),(70,97)])
 s.link('REG_PG',('U4',5),('R22',2),[(105,84),(105,130),(95,130)])
 s.link('SYS_ON',('SW3',2),('U4',1),[(25,55),(25,70),(105,70),(105,76)])
 s.link('SYS_ON',('R23',1),('SW3',2),[(40,70),(25,70),(25,55)])
 s.text('System enable',20,30);s.text('Feedback divider',60,65);s.text('Output capacitors',205,30)
 s.text('[TARGET] Keep switching loops short. Place input/output capacitors at U4.\n[TBD-MEASURE] Verify startup, load transients and capacitor effective capacitance.',25,160)
 s.finish()

 s=Sheet('motors','Three independent motor channels')
 for r,x,y,a in [('U2',85,70,0),('C6',120,40,180),('C7',89,40,180),('C8',50,45,90),('R5',140,70,0),('R6',35,85,0),('R7',55,90,0),('M1',200,72,180),('C12',225,85,180),('M2',265,105,180),('C13',290,118,180),('U3',85,160,0),('C9',120,130,180),('C10',89,130,180),('C11',50,135,90),('R8',140,160,0),('R9',35,175,0),('M3',200,162,180),('C14',225,175,180),('C90',280,175,0)]:s.place(r,x,y,a)
 for u,c,vcp,r,base in [('U2','C7','C8','R5',0),('U3','C10','C11','R8',90)]:
  s.link(u+'_VINT',(u,14),(c,1))
  s.link(u+'_VCP',(u,11),(vcp,1),[(47,64+base)])
  s.join('VMOTOR',[(u,12),('C6' if u=='U2' else 'C9',1)],rail=50+base)
  s.link('FAULT_'+u,(u,8),(r,2),[(125,68+base),(125,80+base),(140,80+base)])
 s.link('M1_SENSE',('U2',3),('R6',1),[(35,66)])
 s.link('M2_SENSE',('U2',6),('R7',1),[(55,68)])
 s.link('M3_SENSE',('U3',3),('R9',1),[(35,156)])
 for n,y in [(1,72),(2,105),(3,162)]:
  x=200 if n!=2 else 265;c='C'+str(11+n);m='M'+str(n)
  s.join(m+'_A',[(m,1),(c,1)],rail=y+20)
  s.join(m+'_B',[(m,2),(c,2)],rail=y-7)
 s.text('U2: wheels 1 and 2',25,25);s.text('U3: wheel 3; unused bridge pins retained as designed',25,115)
 s.text('Motor terminal pads and suppression capacitors',180,30)
 s.text('[TARGET] Route motor current away from logic returns.\n[TBD-MEASURE] Braking overshoot, driver temperature and carpet load.',165,215)
 s.finish()

 s=Sheet('charging','USB input, charging and cell connections')
 for r,x,y,a in [('J1',35,60,0),('R10',65,38,0),('R11',85,38,0),('U6',115,62,0),('R12',155,62,90),('R13',180,64,90),('U5',120,145,0),('R14',60,170,0),('R15',80,165,0),('R16',60,135,0),('R17',45,145,0),('C15',160,120,0),('C16',190,145,0),('C17',215,120,0),('J2',280,45,180),('J4',280,145,180),('D2',200,185,180),('R18',175,185,90),('R19',155,170,0)]:s.place(r,x,y,a)
 s.link('USB_CC1',('J1','A5'),('R10',1),[(55,52),(55,30),(65,30)])
 s.link('USB_CC2',('J1','B5'),('R11',1),[(60,54),(60,25),(85,25)])
 s.join('GND',[('R10',2),('R11',2)],rail=45)
 s.join('USB_DM_EXT',[('J1','A7'),('J1','B7')],axis='v',rail=55)
 s.join('USB_DP_EXT',[('J1','A6'),('J1','B6')],axis='v',rail=60)
 s.link('USB_DM_EXT',('U6',6),('R12',1))
 s.link('USB_DP_EXT',('U6',4),('R13',1))
 s.link('USB_DM_EXT',('J1','A7'),('U6',1),[(95,58),(95,62)])
 s.link('USB_DP_EXT',('J1','B6'),('U6',3))
 s.link('CHG_ISET',('U5',16),('R14',1),[(60,153)])
 s.link('CHG_ILIM',('U5',12),('R15',1),[(80,151)])
 s.link('CHG_TIMER',('U5',14),('R16',1),[(95,143),(95,125),(60,125)])
 s.link('CHG_LED_A',('R18',2),('D2',2))
 s.join('VBAT',[('U5',2),('U5',3),('C16',1)],rail=145)
 s.join('SYS_RAW',[('U5',10),('U5',11),('C17',1)],rail=105)
 s.join('USB_5V',[('U5',13),('C15',1)],rail=100)
 s.text('USB data to ESP32 native USB',110,30);s.text('Raw cell -> protection sheet',250,25)
 s.text('Charge / system power path',25,100);s.text('Cell-bonded charger probe',245,125)
 s.text('[SPEC] J2 CELL_N is not system GND: R36 is the only intended return path.\nJ4: independent insulated two-wire 103AT-2 probe on the cell.\nMotor current uses protected VBAT, not charger SYS_RAW output.',25,215)
 s.finish()

 s=Sheet('interlock','USB motor interlock and battery measurement')
 for r,x,y,a in [('Q1',150,50,0),('Q2',200,50,0),('Q3',150,110,0),('Q4',65,100,0),('Q5',210,145,0),('Q6',210,180,0),('R24',170,72,0),('R25',125,110,90),('R26',138,130,0),('R27',40,80,90),('R28',80,115,0),('R29',35,100,90),('R30',50,120,0),('C21',250,45,0),('C22',280,45,0),('R31',180,150,0),('R32',180,180,90),('R33',195,195,0),('R34',255,145,0),('R35',255,175,0),('C23',285,175,0)]:s.place(r,x,y,a)
 s.join('MOTOR_MID',[('Q1',2),('Q2',2),('R24',1)],rail=65)
 s.link('MOTOR_GATE',('Q1',1),('Q2',1),[(140,50),(140,80),(190,80),(190,50)])
 s.join('MOTOR_GATE',[('Q3',3),('R24',2)],rail=80)
 s.link('MOTOR_BASE',('R25',2),('Q3',1))
 s.link('USB_DETECT_BASE',('R29',2),('Q4',1))
 s.link('MEAS_BASE',('R32',2),('Q6',1))
 s.join('VBAT_ADC',[('R34',2),('R35',1),('C23',1)],rail=160)
 s.join('GND',[('R35',2),('C23',2)],rail=185)
 s.link('MEAS_GATE',('Q5',1),('Q6',3),[(200,145),(200,163),(212,163)])
 s.link('MEAS_GATE',('R31',2),('Q6',3),[(180,163),(212,163)])
 s.link('VBAT_MEAS',('Q5',3),('R34',1),[(212,132),(255,132)])
 s.link('VBAT',('Q5',2),('R31',1),[(212,155),(170,155),(170,137),(180,137)])
 s.link('MEAS_BASE',('R33',1),('Q6',1),[(195,180)])
 s.link('MOTOR_BASE',('R26',1),('Q3',1),[(138,110)])
 s.link('USB_DETECT_BASE',('R30',1),('Q4',1),[(50,100)])
 s.join('DRIVE_ENABLE',[('R27',2),('Q4',3),('R28',1)],rail=87)
 s.text('USB presence clamps DRIVE_ENABLE',20,35);s.text('Back-to-back motor supply switch',100,25)
 s.text('Switched battery measurement',165,120)
 s.text('[TARGET] Reset / absent commands keep motors disabled.\n[TBD-MEASURE] Verify USB insertion/removal and motor braking transients.',20,165)
 s.finish()

 s=Sheet('battery_protection','1S protection and cell-temperature monitoring')
 for r,x,y,a in [('U7',100,70,0),('Q7',185,60,0),('Q8',255,60,180),('R36',40,110,90),('R37',35,45,90),('R38',35,65,90),('R39',140,100,90),('C24',50,52,0),('R40',185,95,0),('R41',255,35,180),('J5',180,145,180),('R42',210,125,0),('R43',245,145,90),('C25',275,165,0),('TH1',50,175,0),('TH2',210,165,0)]:s.place(r,x,y,a)
 s.link('PROT_DRAIN',('Q7',5),('Q8',5))
 for r in ['Q7','Q8']:
  s.covered.update((r,str(n)) for n in [6,7,8,9])
 s.link('PROT_CHG',('Q7',4),('R40',1))
 s.link('PROT_DSG',('Q8',4),('R41',1))
 s.link('PROT_VDD',('R37',2),('C24',1),[(50,45)])
 s.link('PROT_VDD',('R37',2),('U7',2),[(75,45),(75,65)])
 s.link('PROT_BAT',('R38',2),('U7',1),[(70,65),(70,63)])
 s.join('CELL_TEMP_DIV',[('R42',2),('R43',1),('TH2',1)],rail=145)
 s.link('CELL_TEMP_DIV',('J5',1),('R43',1))
 s.join('CELL_TEMP_ADC',[('R43',2),('C25',1)],rail=155)
 s.join('GND',[('TH2',2),('C25',2)],rail=180)
 s.text('Cell voltage / current sensing',20,25);s.text('Common-drain high-side protection FET pair',165,25)
 s.text('TH1 -> J4 charger input',20,145);s.text('TH2 -> J5 -> GPIO1 / ADC1',170,112)
 s.text('[SPEC] TH1 and TH2 are OFF-BOARD, bonded to the cell through electrical insulation.\nSeparate two-wire probes; do not connect either sensor to raw CELL_N.\n[TARGET] Firmware must stop driving on overtemperature, open/short probe or stale readings.',20,215)
 s.finish()

 # Root overview: move the overlapping seventh sheet and keep flags on page.
 p=BASE/'omni_ugv.kicad_sch';t=p.read_text();ed=[];index=0
 for a,b,u in blocks(t):
  if u.startswith('(sheet '):
   x=25+(index%3)*125;y=45+(index//3)*75;index+=1
   oldx,oldy=map(float,re.search(r'\(at ([\d.]+) ([\d.]+)',u).groups());dx=x-oldx;dy=y-oldy
   def move(m):return f'(at {float(m[1])+dx} {float(m[2])+dy}'+(f' {m[3]}' if m[3] else '')+')'
   u=re.sub(r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)',move,u);u=re.sub(r'\(size [^)]+\)','(size 100 35)',u,count=1)
   # Sheet file labels follow the smaller box.
   u=re.sub(r'(\(property "Sheetfile" "[^"]+" \(at )[-\d.]+ [-\d.]+',lambda m:m[1]+f'{x} {y+36}',u)
   ed.append((a,b,u))
  elif u.startswith('(text '):ed.append((a,b,''))
 for a,b,u in reversed(ed):t=t[:a]+u+t[b:]
 t=t.replace('Rev A','Rev B').replace('A-PROTOTYPE','B-PROTOTYPE')
 # Existing root flags are outside A3 bounds; translate their entire block row upward.
 # Translate only root symbols and their labels/wires, which are exclusively ERC flags.
 ed=[]
 for a,b,u in blocks(t):
  if u.startswith(('(symbol ','(global_label ','(wire ','(junction ')):
   coords=re.findall(r'\((?:at|xy) ([-\d.]+) ([-\d.]+)',u)
   if coords:
    oldy=float(coords[0][1]);dy=190.5-oldy
    u=re.sub(r'\((at|xy) ([-\d.]+) ([-\d.]+)',lambda m:f'({m[1]} {float(m[2])} {float(m[3])+dy}',u);ed.append((a,b,u))
 for a,b,u in reversed(ed):t=t[:a]+u+t[b:]
 t=t.rstrip()[:-1]+f'(text "OMNI CAMERA ROVER | REV B PROTOTYPE" (at 25 20 0) (effects (font (size 2 2)) (justify left)) (uuid {uid("root-title")}))'+f'(text "Editable functional sheets. Global net names link sheets.\\nPrototype: electrical, thermal and mechanical qualification remains open." (at 25 225 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid {uid("root-note")})))'
 (ROOT/'omni_ugv.kicad_sch').write_text(t)
if __name__=='__main__':build()

