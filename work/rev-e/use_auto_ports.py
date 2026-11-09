from pathlib import Path
s=Path('work/rev-e/final_protect_route.py').read_text();a=s.index('for pin,x,y,ref,rpin');b=s.index("for net,r1,p1",a)
s=s[:a]+'''ports=json.loads(Path('work/rev-e/protect-ports.json').read_text())
for pin,ref,rpin in [(1,'R38',2),(2,'R37',2),(3,'R36',3),(4,'R36',4),(5,'R36',1),(6,'R39',2),(7,'Q8',4),(8,'Q7',4)]:
 x,y=ports[str(pin)];d=pad('U7',pin);route(d['net'],(x,y,'In2.Cu'),endpoint(ref,rpin),.15,True,15);save()
'''+s[b:];Path('work/rev-e/final_protect_route.py').write_text(s)
