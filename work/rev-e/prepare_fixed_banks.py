from pathlib import Path
s=Path('work/rev-e/router.py').read_text().replace('r+.18','r+.16');s+='''
banks=[('PROTECTED_RAW',(129.5,134.5),[(129.5,133.7),(130.3,134.5),(128.7,133.9)],True),('PROTECTED_RAW',(114.9,138.8),[(117,136.3),(117.1,135.4),(118,135.3)],True),('VBAT',(125.2,137),[(124.4,137),(125.2,137.8)],False),('VBAT',(115.8,135.8),[(115.2,135.2),(115,136)],False)]
removed=[]
for net,origin,pts,remove in banks:
 for i,pt in enumerate(pts):
  anchor=origin if i==0 else pts[0]
  for l in ['B.Cu','F.Cu']:
   if net=='PROTECTED_RAW' and origin[0]<120 and i==0:route(net,(*anchor,l),(*pt,l),.3,False,6)
   else:addtrack(net,anchor,pt,.3,l)
  addvia(net,pt)
 if remove:
  old=min((t for t in tracks if t['via'] and t['net']==net),key=lambda t:math.dist(t['a'],origin));removed.append(old['uuid'])
save();Path('work/rev-e/remove-pad-vias.json').write_text(json.dumps(removed));Path('work/rev-e/final-via-banks.json').write_text(json.dumps([dict(net=n,origin=o,new_vias=p,old_via_removed=r) for n,o,p,r in banks],indent=2))
''';Path('work/rev-e/fixed_banks.py').write_text(s)
