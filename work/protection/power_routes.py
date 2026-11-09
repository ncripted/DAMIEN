from pathlib import Path
exec(Path('work/protection/route.py').read_text().split('\ntry:\n')[0])
layers=['B.Cu','F.Cu']
def vias(net,preferred,count):
 o=obs(net,'',.3,box(preferred[0]-4,preferred[1]-4,preferred[0]+4,preferred[1]+4),True)
 candidates=sorted([(preferred[0]+dx*.8,preferred[1]+dy*.8) for dx in range(-5,6) for dy in range(-5,6)],key=lambda p:math.dist(p,preferred))
 selected=[]
 for pt in candidates:
  if o.intersects(Point(pt)):continue
  addvia(net,pt);selected.append(pt)
  if len(selected)==count:return selected
 raise RuntimeError('Insufficient legal power vias for '+net)
try:
 vp=vias('VBAT',(114.2,141.0),6)
 route('VBAT',(pad('Q8',1)['at'][0]-.85,pad('Q8',1)['at'][1],'B.Cu'),(*vp[0],'B.Cu'),1.2,False)
 for pt in vp[1:]:
  route('VBAT',(*vp[0],'B.Cu'),(*pt,'B.Cu'),.5,False,4)
  route('VBAT',(*vp[0],'F.Cu'),(*pt,'F.Cu'),.5,False,4)
 route('VBAT',(*vp[0],'F.Cu'),(120.67,125,'F.Cu'),1.0,True,13)
 route('VBAT',(120.67,125,'F.Cu'),(108,124.551,'F.Cu'),1.0,True,12)
 power_changes=[t['a'] for t in out if t['via'] and t['net']=='VBAT' and t['a'] not in [list(pt) for pt in vp]]
 for center in power_changes:
  extra=vias('VBAT',center,3)
  for pt in extra:
   for l in ['B.Cu','F.Cu']:route('VBAT',(*center,l),(*pt,l),.4,False,4)
 gp=vias('GND',(109.8,127.8),6)
 route('GND',endpoint('R36',2),(*gp[0],'B.Cu'),1.2,False,4)
 for pt in gp[1:]:route('GND',(*gp[0],'B.Cu'),(*pt,'B.Cu'),.5,False,4)
 # Drain thermal vias reside between the two FETs, outside their solder lands.
 for x in [118.2,118.9]:
  for y in [137,137.8,138.6,139.4]:
   o=obs('PROT_DRAIN','',.3,box(x-1,y-1,x+1,y+1),True)
   if not o.intersects(Point(x,y)):
    addvia('PROT_DRAIN',(x,y));route('PROT_DRAIN',endpoint('Q7',9),(x,y,'B.Cu'),.5,False,4)
except Exception:
 save();raise
save()
