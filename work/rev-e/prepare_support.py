from pathlib import Path
s=Path('work/rev-e/router.py').read_text()+'''\nrr('PROT_VDD','R37',2,'U7',2,.15,True);save()
rr('PROT_VDD','C24',1,'U7',2,.15,True);save()
rr('PROT_DSG','U7',7,'Q8',4,.15,True);save()
rr('PROT_DSG','R41',2,'Q8',4,.15,True);save()
rr('CELL_N','U7',5,'R36',1,.15,True);save()
'''
Path('work/rev-e/step3_support_finish.py').write_text(s)
