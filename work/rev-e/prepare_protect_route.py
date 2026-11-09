from pathlib import Path
s=Path('work/rev-e/router.py').read_text().replace('r+.18','r+.16')
s+='''
for pin,x,y,ref,rpin in [(1,119.5,130.5,'R38',2),(2,118.5,130,'R37',2),(3,119.5,129.5,'R36',3),(4,121,128.5,'R36',4),(5,122.5,129.5,'R36',1),(6,123.5,130,'R39',2),(7,122.5,130.5,'Q8',4),(8,121,131.5,'Q7',4)]:
 d=pad('U7',pin);route(d['net'],(x,y,'In2.Cu'),endpoint(ref,rpin),.15,True,15);save()
for net,r1,p1,r2,p2 in [('PROT_DSG','R41',1,'Q8',4),('PROT_CHG','R40',1,'Q7',4),('PROT_VSS_SENSE','C24',2,'R36',3),('PROT_VDD','C24',1,'R37',2)]:
 rr(net,r1,p1,r2,p2,.15,True);save()
'''
Path('work/rev-e/final_protect_route.py').write_text(s)
