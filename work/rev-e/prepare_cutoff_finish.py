from pathlib import Path
s=Path('work/rev-e/router.py').read_text().replace('r+.18','r+.16')
s+='''
for net,r1,p1,r2,p2 in [('CELL_P','C30',1,'U10',2),('CELL_P','R46',1,'U10',2),('CELL_P','Q12',2,'Q13',1),('CELL_P','R66',1,'Q12',2),('CELL_UV_RESET_N','R65',1,'R46',2),('CUT_PNP_B','R65',2,'Q12',1),('CUT_PNP_B','R66',2,'Q12',1),('CUT_GATE','Q12',3,'Q13',4),('CUT_GATE','R67',1,'Q13',4),('CELL_N','R67',2,'R36',1)]:
 rr(net,r1,p1,r2,p2,.15,True);save()
''';Path('work/rev-e/step5_finish.py').write_text(s)
