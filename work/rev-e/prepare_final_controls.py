from pathlib import Path
s=Path('work/rev-e/router.py').read_text().replace('r+.18','r+.16');s+='''
for net,pin,pt in [('PROT_DSG',7,(122.675,130.6)),('PROT_CHG',8,(121,131.65))]:
 addtrack(net,pad('U7',pin)['at'],pt,.15,'B.Cu');addvia(net,pt)
for net,pt,ref,pin in [('PROT_DSG',(122.675,130.6),'Q8',4),('PROT_CHG',(121,131.65),'Q7',4)]:
 route(net,(*pt,'In2.Cu'),endpoint(ref,pin),.15,True,12);save()
for net,r1,p1,r2,p2 in [('PROT_DSG','R41',1,'Q8',4),('PROT_CHG','R40',1,'Q7',4),('CELL_P','Q12',2,'Q7',1),('CELL_P','R66',1,'Q12',2),('CUT_PNP_B','R65',2,'Q12',1),('CUT_PNP_B','R66',2,'Q12',1),('CUT_GATE','Q12',3,'Q13',4),('CUT_GATE','R67',1,'Q13',4)]:
 rr(net,r1,p1,r2,p2,.15,True);save()
''';Path('work/rev-e/final_controls.py').write_text(s)
