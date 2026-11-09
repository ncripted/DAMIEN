from pathlib import Path
s=Path('work/rev-e/router.py').read_text().replace('res=.1','res=.05')
s+='''
esc={}
for pin,net in [(7,'PROT_DSG'),(6,'PROT_PACK'),(8,'PROT_CHG')]:
 d=pad('U7',pin);px,py=d['at'];region=box(px-5,py-5,px+5,py+5);vo=obs(net,'',.3,region,True);attempt=0
 for pt in sorted([(round(px+dx*.1,3),round(py+dy*.1,3)) for dx in range(-40,41) for dy in range(-40,41)],key=lambda pt:math.dist(pt,(px,py))):
  if Point(pt).intersects(vo) or Point(pt).distance(d['geo'])<.4:continue
  attempt+=1
  try:route(net,endpoint('U7',pin,'B.Cu'),(*pt,'B.Cu'),.15,False,5)
  except Exception as e:
   print('Escape candidate failed',pin,str(e),flush=True)
   if attempt>=15:raise
   continue
  addvia(net,pt);esc[net]=pt;print('Reserved',net,pt,flush=True);break
 else:raise RuntimeError('No escape '+net)
 save()
for net,ref,pin in [('PROT_DSG','Q8',4),('PROT_CHG','Q7',4),('PROT_PACK','R39',2)]:
 route(net,(*esc[net],'In2.Cu'),endpoint(ref,pin,'B.Cu'),.15,True,12);save()
rr('PROT_DSG','R41',2,'Q8',4,.15,True);save()
rr('PROT_CHG','R40',1,'Q7',4,.15,True);save()
rr('CELL_N','U7',5,'R36',1,.15,True);save()
'''
Path('work/rev-e/step3_gate_finish.py').write_text(s)
