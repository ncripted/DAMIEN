from pathlib import Path
s=Path('work/camera-rev-c/place.py').read_text().replace('work/camera-rev-c','work/power-rev-d')
a=s.index("for ref in ['J3'");b=s.index(' candidates=',a)
s=s[:a]+'''order=['U11','C32','C33','U12','C34','R55','R56','R57','R58','R59','U13','C36','C35','R61','R62','R63','U10','C30','C31','R46','Q9','R47','R48','R49','Q10','R50','R51','Q11','R52','R53','R54','R60']
for ref in order:
 d=next(x for x in ds if x['ref']==ref);pp=[v for a,v in pads if a['ref']==ref];cu=unary_union(pp);old=next(f['at'] for f in g['footprints'] if f['ref']==ref);tx,ty=d['x'],d['y']
 if ref in ['C32','C33','C34','C36','C30','C31']:
  u={'C32':'U11','C33':'U11','C34':'U12','C36':'U13','C30':'U10','C31':'U10'}[ref];prev=next(x for x in ds if x['ref']==u);dx,dy=prev['shift'];tx+=dx;ty+=dy
''' +s[b:]
Path('work/power-rev-d/place.py').write_text(s)
