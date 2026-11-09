from pathlib import Path
s=Path('work/rev-e/router.py').read_text()
s+='''
net='PROT_VSS_SENSE';fanouts={}
for ref,pin in [('U7',3),('R36',3)]:
 d=pad(ref,pin);px,py=d['at'];region=box(px-4,py-4,px+4,py+4);vo=obs(net,'',.3,region,True)
 candidates=sorted([(round(px+dx*.1,2),round(py+dy*.1,2)) for dx in range(-25,26) for dy in range(-25,26)],key=lambda pt:math.dist(pt,(px,py)))
 for pt in candidates:
  if Point(pt).intersects(vo) or not board.buffer(-.8).covers(Point(pt)):continue
  try:route(net,endpoint(ref,pin,'B.Cu'),(*pt,'B.Cu'),.15,False,4)
  except Exception:continue
  addvia(net,pt);fanouts[ref]=pt;print('Reserved sense escape',ref,pt,flush=True);break
 else:raise RuntimeError('No sense escape '+ref)
 save()
route(net,(*fanouts['R36'],'In2.Cu'),(*fanouts['U7'],'In2.Cu'),.15,True,8);save()
rr(net,'C24',2,'U7',3,.15,True);save()
rr('PROT_VDD','R37',2,'U7',2,.2,True);save()
rr('PROT_VDD','C24',1,'U7',2,.2,True);save()
rr('PROT_DSG','U7',7,'Q8',4,.2,True);save()
rr('PROT_DSG','R41',2,'Q8',4,.15,True);save()
rr('CELL_N','U7',5,'R36',1,.15,True);save()
'''
Path('work/rev-e/step3_route_finish.py').write_text(s)
