from pathlib import Path
s=Path('work/rev-e/router.py').read_text().replace('res=.1','res=.05').replace('r+.18','r+.155')
s+='''
esc={}
for pin,dx,dy in [(1,-1.5,.5),(2,-2.2,0),(3,-1.5,-.5),(4,0,-1.5),(5,1.5,-.5),(6,2.2,0),(7,1.5,.5),(8,0,1.5)]:
 d=pad('U7',pin);pt=(127+dx,128+dy);net=d['net'];addtrack(net,d['at'],pt,.15,'B.Cu');addvia(net,pt);esc[pin]=pt
save()
'''
Path('work/rev-e/manual_ports.py').write_text(s)
