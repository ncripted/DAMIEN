from pathlib import Path
exec(Path('work/protection/route.py').read_text().split('\ntry:\n')[0])
o=obs('GND','',.3,box(107,120,115,128),True)
candidates=sorted([(111.4+dx*.8,122.4+dy*.8) for dx in range(-3,4) for dy in range(-3,4)],key=lambda pt:math.dist(pt,(111.4,122.4)))
selected=[]
for pt in candidates:
 if o.intersects(Point(pt)) or any(p['geo'].buffer(.2).intersects(Point(pt)) for p in pads):continue
 route('GND',endpoint('C90',2),(*pt,'F.Cu'),.6,False,4);addvia('GND',pt);selected.append(pt)
 if len(selected)==4:break
assert len(selected)==4
save()
