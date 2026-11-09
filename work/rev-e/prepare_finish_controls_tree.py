from pathlib import Path
s=Path('work/rev-e/router.py').read_text().replace('r+.18','r+.155').replace("if d['net']!=net and (via or layer in d['layers'])","if (via or d['net']!=net) and (via or layer in d['layers'])")
s+='''
for ref,pin,pt in [('U7',8,(121,131.65)),('Q7',4,(123.5,140.1)),('R40',1,(124,134))]:
 addtrack('PROT_CHG',pad(ref,pin)['at'],pt,.15,'B.Cu');addvia('PROT_CHG',pt)
route('PROT_CHG',(121,131.65,'In2.Cu'),(123.5,140.1,'In2.Cu'),.15,True,10);save()
route('PROT_CHG',(124,134,'In2.Cu'),(123.5,140.1,'In2.Cu'),.15,True,8);save()
for net,r1,p1,r2,p2 in [('CELL_P','Q12',2,'Q7',1),('CELL_P','R66',1,'Q12',2),('CUT_PNP_B','R65',2,'Q12',1),('CUT_PNP_B','R66',2,'Q12',1),('CUT_GATE','Q12',3,'Q13',4),('CUT_GATE','R67',1,'Q13',4)]:
 rr(net,r1,p1,r2,p2,.15,True);save()
''';Path('work/rev-e/finish_controls_tree.py').write_text(s)
