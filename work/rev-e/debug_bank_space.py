exec(open('work/rev-e/router.py').read().split('def route(')[0])
for pt in [(117,135.5),(117.8,136.3),(117.1,135.4),(117.5,135.5),(116.8,135.5)]:
 p=Point(pt);print('\nCandidate',pt)
 for d in pads:
  if d['net']!='PROTECTED_RAW' and d['geo'].distance(p)<.5:print('Pad',d['ref'],d['num'],d['net'],d['layers'],d['geo'].distance(p))
 for t in tracks:
  if t['net']!='PROTECTED_RAW' and t['geo'].distance(p)<.5:print('Track',t['net'],t['layer'],t['a'],t['z'],t['width'],t['geo'].distance(p))
