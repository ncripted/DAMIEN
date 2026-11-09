from pathlib import Path
p=Path('work/rev-e/auto_ports.py');s=p.read_text().replace("else:raise RuntimeError('no straight escape '+str(pin))",'''else:
  for pt in sorted([(round(x+dx*.1,3),round(y+dy*.1,3)) for dx in range(-60,61) for dy in range(-60,61)],key=lambda pt:math.dist(pt,(x,y))):
   if Point(pt).intersects(vo):continue
   try:route(net,(x,y,'B.Cu'),(*pt,'B.Cu'),.15,False,8)
   except RuntimeError:continue
   addvia(net,pt);ports[pin]=pt;print('Bent port',pin,pt,flush=True);break
  else:raise RuntimeError('no escape '+str(pin))''');p.write_text(s)
