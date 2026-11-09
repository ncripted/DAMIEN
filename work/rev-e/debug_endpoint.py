exec(open('work/rev-e/router.py').read().split('def route(')[0])
d=pad('R41',2);pt=Point(d['at']);print(d['at'])
for t in tracks:
 if t['net']!=d['net'] and (t['layer']=='B.Cu' or t['via']) and t['geo'].distance(pt)<.6:print(t['net'],t['a'],t['z'],t['width'],t['geo'].distance(pt),t['uuid'])
for t in pads:
 if t['net']!=d['net'] and 'B.Cu' in t['layers'] and t['geo'].distance(pt)<.6:print(t['ref'],t['num'],t['net'],t['geo'].distance(pt))
print('edge',board.boundary.distance(pt),'inside',board.contains(pt))
print('padnet',d['net']);print('obs',obs('PROT_DSG','B.Cu',.075,box(100,110,140,145)).distance(pt));print([(t['net'],t['a'],t['z'],t['width']) for t in tracks if t['net']!='PROT_DSG' and (t['layer']=='B.Cu' or t['via']) and t['geo'].distance(pt)<.3])
