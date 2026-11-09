from pathlib import Path
s=Path('work/rev-e/router.py').read_text().replace('res=.1','res=.05').replace('r+.18','r+.16')
s+='''
# Reserve straight fine-pitch escapes before selecting any through-via.
ends={};ports={}
for pin in range(1,9):
 d=pad('U7',pin);x,y=d['at'];dx,dy=((-1,0) if pin in [1,2,3] else (1,0) if pin in [5,6,7] else (0,-1) if pin==4 else (0,1));end=(x+dx*1.0,y+dy*1.0);ends[pin]=end;addtrack(d['net'],d['at'],end,.15,'B.Cu')
for pin in [4,8,1,3,5,7,2,6]:
 d=pad('U7',pin);net=d['net'];x,y=ends[pin];region=box(x-8,y-8,x+8,y+8);vo=obs(net,'',.3,region,True);bo=obs(net,'B.Cu',.075,region)
 for pt in sorted([(round(x+dx*.1,3),round(y+dy*.1,3)) for dx in range(-60,61) for dy in range(-60,61)],key=lambda pt:math.dist(pt,(x,y))):
  if Point(pt).intersects(vo) or LineString([(x,y),pt]).intersects(bo) or not board.buffer(-.7).contains(Point(pt)):continue
  addtrack(net,(x,y),pt,.15,'B.Cu');addvia(net,pt);ports[pin]=pt;print('Port',pin,pt,flush=True);break
 else:raise RuntimeError('no straight escape '+str(pin))
save();Path('work/rev-e/protect-ports.json').write_text(json.dumps(ports))
'''
Path('work/rev-e/auto_ports.py').write_text(s)
