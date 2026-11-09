from pathlib import Path
s=Path('work/rev-e/router.py').read_text()
s+='''
layers=['F.Cu','B.Cu']
route('M3_A',(79.74,106.38,'B.Cu'),endpoint('M3',1,'F.Cu'),.4,True,24);save()
route('M3_B',(80.14,107.67,'B.Cu'),endpoint('M3',2,'F.Cu'),.4,True,24);save()
for m,c in [('M1','C12'),('M2','C13'),('M3','C14')]:
 for pin in [1,2]:rr(pad(m,pin)['net'],m,pin,c,pin,.25,True);save()
'''
Path('work/rev-e/step2_motor_finish.py').write_text(s)
