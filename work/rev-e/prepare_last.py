from pathlib import Path
s=Path('work/rev-e/router.py').read_text().replace('res=.1','res=.05').replace('r+.18','r+.155')
s+='''
for net,r1,p1,r2,p2 in [('PROT_DSG','R41',2,'Q8',4),('PROT_CHG','R40',1,'Q7',4),('CELL_N','U7',5,'R36',1),('PROT_VSS_SENSE','U7',3,'R36',3),('PROT_VSS_SENSE','C24',2,'R36',3),('PROT_VDD','R37',2,'U7',2),('PROT_VDD','C24',1,'U7',2)]:
 rr(net,r1,p1,r2,p2,.15,True);save()
'''
Path('work/rev-e/step3_last.py').write_text(s)
