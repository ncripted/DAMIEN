from pathlib import Path
s=Path('work/rev-e/router.py').read_text().replace('r+.18','r+.16')
s+='''
# Three source leads feed broad offset buses, preserving gate clearance.
for ref,net,bx in [('Q7','CELL_P',124.0),('Q8','PROTECTED_RAW',113.2)]:
 for n in [1,2,3]:
  d=pad(ref,n);addtrack(net,d['at'],(bx,d['at'][1]),.4,'B.Cu')
 addtrack(net,(bx,137.025),(bx,138.325),.8,'B.Cu')
 save()
route('CELL_P',endpoint('J2',1),(124,137.025,'B.Cu'),1.5,True,12);save()
route('PROTECTED_RAW',(113.2,137.025,'B.Cu'),endpoint('Q13',1),1.0,True,14);save()
for n in [2,3]:rr('PROTECTED_RAW','Q13',n,'Q13',1,.4,False);save()
route('VBAT',endpoint('Q13',5),(114.2,141.0,'F.Cu'),1.5,True,12);save()
for net,r1,p1,r2,p2 in [('CELL_P','R37',1,'J2',1),('CELL_P','R38',1,'R37',1),('CELL_P','U10',2,'R37',1),('CELL_P','U10',4,'U10',2),('CELL_P','C30',1,'U10',2),('CELL_P','R46',1,'U10',2),('CELL_P','Q12',2,'Q7',1),('CELL_P','R66',1,'Q12',2),('CELL_P','R40',2,'Q7',1),('PROTECTED_RAW','R39',1,'Q8',1),('PROTECTED_RAW','R41',2,'Q8',1)]:
 rr(net,r1,p1,r2,p2,.15,True);save()
''';Path('work/rev-e/corrected_cutoff_route.py').write_text(s)
