from pathlib import Path
s=Path('work/rev-e/router.py').read_text().replace('r+.18','r+.16')
s+='''
rr('CELL_P','J2',1,'Q13',1,1.5,True);save()
rr('CELL_SWITCHED','Q13',5,'Q7',1,1.5,True);save()
for ref,net in [('Q13','CELL_P'),('Q7','CELL_SWITCHED')]:
 for n in [2,3]:rr(net,ref,n,ref,1,.4,False);save()
rr('CELL_SWITCHED','R40',2,'Q7',1,.2,True);save()
for ref,pin in [('R37',1),('R38',1),('U10',2),('U10',4),('C30',1),('R46',1),('Q12',2),('R66',1)]:
 rr('CELL_P',ref,pin,'J2',1,.15,True);save()
for net,r1,p1,r2,p2 in [('CELL_UV_RESET_N','R65',1,'R46',2),('CUT_PNP_B','R65',2,'Q12',1),('CUT_PNP_B','R66',2,'Q12',1),('CUT_GATE','Q12',3,'Q13',4),('CUT_GATE','R67',1,'Q13',4),('CELL_N','R67',2,'R36',1)]:
 rr(net,r1,p1,r2,p2,.15,True);save()
''';Path('work/rev-e/step5_route.py').write_text(s)
