from pathlib import Path
s=Path('work/rev-e/router.py').read_text()
s+='''
fanouts={}
order=[('U2',2,'M1_A','M1'),('U2',4,'M1_B','M1'),('U2',7,'M2_A','M2'),('U2',5,'M2_B','M2'),('U3',2,'M3_A','M3'),('U3',4,'M3_B','M3')]
for ref,pin,net,m in order:
 d=pad(ref,pin);px,py=d['at'];region=box(px-5,py-5,px+3,py+5);vo=obs(net,'',.3,region,True);wide=obs(net,'In2.Cu',.3,region)
 candidates=sorted([(round(px+dx*.1,2),round(py+dy*.1,2)) for dx in range(-40,-9) for dy in range(-30,31)],key=lambda pt:math.dist(pt,(px-1.4,py)))
 for pt in candidates:
  pp=Point(pt)
  if pp.intersects(vo) or pp.intersects(wide) or not board.buffer(-.8).covers(pp):continue
  try:route(net,endpoint(ref,pin),(*pt,'F.Cu'),.25,False,4)
  except Exception as e:print('Escape candidate failed',str(e),flush=True);continue
  addvia(net,pt);fanouts[net]=pt;print('Reserved',net,pt,flush=True);break
 else:raise RuntimeError('No legal motor fanout '+net)
 save()
for ref,pin,net,m in order:
 route(net,(*fanouts[net],'In2.Cu'),endpoint(m,1 if net.endswith('A') else 2,'F.Cu'),.6,True,18);save()
for m,c in [('M1','C12'),('M2','C13'),('M3','C14')]:
 for pin in [1,2]:rr(pad(m,pin)['net'],m,pin,c,pin,.25,True);save()
Path('work/rev-e/motor-fanouts.json').write_text(json.dumps(fanouts,indent=2))
'''
Path('work/rev-e/step2_motor_route.py').write_text(s)
