from pathlib import Path
s=Path('work/rev-e/router.py').read_text();s+='''
rr('REG_L1','U4',9,'L1',1,.4,False);save()
rr('REG_L2','U4',7,'L1',2,.4,False);save()
# Choose offset ground vias near each capacitor return, clear of all layers.
for ref in ['C18','C19','C20']:
 d=pad(ref,2);x,y=d['at'];vo=obs('GND','',.3,box(x-3,y-3,x+3,y+3),True);bo=obs('GND','F.Cu',.15,box(x-3,y-3,x+3,y+3))
 pts=sorted([(round(x+dx*.1,3),round(y+dy*.1,3)) for dx in range(-18,19) for dy in range(-18,19)],key=lambda pt:math.dist(pt,(x,y)))
 found=0
 for pt in pts:
  if Point(pt).intersects(vo) or Point(pt).distance(d['geo'])<.4 or LineString([(x,y),pt]).intersects(bo):continue
  addtrack('GND',(x,y),pt,.3,'F.Cu');addvia('GND',pt);found+=1;break
 print('Ground return via',ref,found,flush=True)
 save()
''';Path('work/rev-e/step4_route.py').write_text(s)
