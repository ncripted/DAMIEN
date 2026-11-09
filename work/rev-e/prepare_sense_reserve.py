from pathlib import Path
s=Path('work/rev-e/router.py').read_text()
s+='''
esc={}
for ref,pin,net in [('U7',4,'PROT_CS_SENSE'),('U7',3,'PROT_VSS_SENSE'),('R36',4,'PROT_CS_SENSE'),('R36',3,'PROT_VSS_SENSE')]:
 d=pad(ref,pin);px,py=d['at'];region=box(px-4,py-4,px+4,py+4);vo=obs(net,'',.3,region,True);attempts=0
 for pt in sorted([(round(px+dx*.1,2),round(py+dy*.1,2)) for dx in range(-30,31) for dy in range(-30,31)],key=lambda pt:math.dist(pt,(px,py))):
  if Point(pt).intersects(vo) or Point(pt).distance(d['geo'])<.4 or not board.buffer(-.8).covers(Point(pt)):continue
  attempts+=1
  try:route(net,endpoint(ref,pin,'B.Cu'),(*pt,'B.Cu'),.15,False,4)
  except Exception as e:
   print('Candidate',ref,pin,str(e),flush=True)
   if attempts>=30:raise
   continue
  addvia(net,pt);esc[(ref,pin)]=pt;print('Reserved sense escape',ref,pin,pt,flush=True);break
 else:raise RuntimeError('No sense escape '+str((ref,pin)))
 save()
for pin,upin,net in [(4,4,'PROT_CS_SENSE'),(3,3,'PROT_VSS_SENSE')]:
 route(net,(*esc[('R36',pin)],'In2.Cu'),(*esc[('U7',upin)],'In2.Cu'),.15,True,8);save()
rr('PROT_VSS_SENSE','C24',2,'U7',3,.15,True);save()
rr('PROT_VDD','R37',2,'U7',2,.2,True);save()
rr('PROT_VDD','C24',1,'U7',2,.2,True);save()
rr('PROT_DSG','U7',7,'Q8',4,.2,True);save()
rr('PROT_DSG','R41',2,'Q8',4,.15,True);save()
rr('CELL_N','U7',5,'R36',1,.15,True);save()
Path('work/rev-e/step3-sense-escapes.json').write_text(json.dumps({str(k):v for k,v in esc.items()},indent=2))
'''
Path('work/rev-e/step3_route_finish.py').write_text(s)
