from pathlib import Path
s=Path('work/rev-e/router.py').read_text().replace('r+.18','r+.16')
s+='''
removed=[];banks=[]
for net,origin,nnew,remove in [('PROTECTED_RAW',(129.5,134.5),3,True),('PROTECTED_RAW',(114.9,138.8),3,True),('VBAT',(125.2,137),2,False),('VBAT',(115.8,135.8),2,False)]:
 region=box(origin[0]-4,origin[1]-4,origin[0]+4,origin[1]+4);bo={l:obs(net,l,.2,region) for l in ['B.Cu','F.Cu']};chosen=[]
 for k in range(nnew):
  vo=obs(net,'',.3,region,True)
  for pt in sorted([(round(origin[0]+dx*.1,3),round(origin[1]+dy*.1,3)) for dx in range(-25,26) for dy in range(-25,26)],key=lambda pt:math.dist(pt,origin)):
   if Point(pt).intersects(vo) or math.dist(pt,origin)<.8 or any(math.dist(pt,u)<.8 for u in chosen):continue
   if any(d['geo'].distance(Point(pt))<.4 for d in pads if d['net']==net and d['layers']):continue
   line=LineString([origin,pt])
   if any(line.intersects(bo[l]) for l in bo) or not board.buffer(-.7).contains(Point(pt)):continue
   addvia(net,pt)
   for l in ['B.Cu','F.Cu']:addtrack(net,origin,pt,.4,l)
   chosen.append(pt);break
  else:raise RuntimeError('No bank room '+str((net,origin,k)))
 if remove:
  old=min((t for t in tracks if t['via'] and t['net']==net),key=lambda t:math.dist(t['a'],origin));assert math.dist(old['a'],origin)<.01;removed.append(old['uuid'])
 banks.append(dict(net=net,origin=origin,new_vias=chosen,old_via_removed=remove))
 save();Path('work/rev-e/final-via-banks.json').write_text(json.dumps(banks,indent=2));Path('work/rev-e/remove-pad-vias.json').write_text(json.dumps(removed))
''';Path('work/rev-e/final_via_banks.py').write_text(s)
