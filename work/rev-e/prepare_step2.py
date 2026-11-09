from pathlib import Path
s=Path('work/rev-e/router.py').read_text()
s+='''
# Reserve current-carrying pad escapes before long routing. Width changes outside pin row.
for ref,pin,net in [('U2',2,'M1_A'),('U2',4,'M1_B'),('U2',7,'M2_A'),('U2',5,'M2_B'),('U3',2,'M3_A'),('U3',4,'M3_B')]:
 d=pad(ref,pin);pt=(d['at'][0]-1.8,d['at'][1]);addtrack(net,d['at'],pt,.3,'F.Cu')
for ref,pin,net,m in [('U2',2,'M1_A','M1'),('U2',4,'M1_B','M1'),('U2',7,'M2_A','M2'),('U2',5,'M2_B','M2'),('U3',2,'M3_A','M3'),('U3',4,'M3_B','M3')]:
 d=pad(ref,pin);pt=(d['at'][0]-1.8,d['at'][1],'F.Cu');route(net,pt,endpoint(m,1 if net.endswith('A') else 2,'F.Cu'),.6,True,18);save()
for m,c in [('M1','C12'),('M2','C13'),('M3','C14')]:
 for pin in [1,2]:rr(pad(m,pin)['net'],m,pin,c,pin,.25,True);save()
'''
Path('work/rev-e/step2_motor_route.py').write_text(s)
