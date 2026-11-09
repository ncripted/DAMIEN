from pathlib import Path
s=Path('work/rev-e/router.py').read_text()
s+='''
net='PROT_VSS_SENSE';region=box(116,120,121,124)
for pt in [(118.3,122.3),(118.5,121.8),(118.3,122.5)]:
 print('POINT',pt)
 for d in pads:
  if d['net']!=net and d['geo'].distance(Point(pt))<.6:print('pad',d['ref'],d['num'],d['net'],d['at'],d['size'],d['geo'].distance(Point(pt)),d['layers'])
 for t in tracks:
  if t['net']!=net and t['geo'].distance(Point(pt))<.55:print('trace',t['net'],t['layer'],t['a'],t['z'],t['width'],t['geo'].distance(Point(pt)))
try:route(net,endpoint('U7',3,'B.Cu'),(118.3,122.3,'B.Cu'),.15,False,2)
except Exception as e:print(type(e).__name__,str(e))
'''
Path('work/rev-e/debug_sense.py').write_text(s)
