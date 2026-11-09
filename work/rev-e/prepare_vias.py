from pathlib import Path
s=Path('work/rev-e/router.py').read_text()
s+='''
reinforced=[]
for center in [(123.9375,119.2634),(133.65,116.2)]:
 net='VMOTOR';region=box(center[0]-4,center[1]-4,center[0]+4,center[1]+4);accepted=[]
 for k in range(2):
  vo=obs(net,'',.3,region,True);fo=obs(net,'F.Cu',.2,region);bo=obs(net,'B.Cu',.2,region)
  candidates=sorted([(round(center[0]+dx*.1,4),round(center[1]+dy*.1,4)) for dx in range(-25,26) for dy in range(-25,26) if .86<=math.hypot(dx*.1,dy*.1)<=2.5],key=lambda v:math.dist(v,center))
  for pt in candidates:
   line=LineString([center,pt])
   if Point(pt).intersects(vo) or line.intersects(fo) or line.intersects(bo):continue
   if not board.buffer(-.8).covers(Point(pt)):continue
   addvia(net,pt);addtrack(net,center,pt,.4,'F.Cu');addtrack(net,center,pt,.4,'B.Cu');accepted.append(pt);break
  else:break
 reinforced.append(dict(existing=center,added=accepted))
print('Power via reinforcements',reinforced,flush=True);save();Path('work/rev-e/step2-via-reinforcement.json').write_text(json.dumps(reinforced,indent=2))
'''
Path('work/rev-e/step2_vias.py').write_text(s)
