from pathlib import Path
p=Path('work/rev-e/corrected_cutoff_route.py');s=p.read_text();a=s.index('# Three source leads');b=s.index('for n in [2,3]:rr',a)
s=s[:a]+'''for ref,net in [('Q7','CELL_P'),('Q8','PROTECTED_RAW')]:
 for n in [2,3]:rr(net,ref,n,ref,1,.4,False);save()
rr('CELL_P','J2',1,'Q7',1,.8,True);save()
rr('PROTECTED_RAW','Q8',1,'Q13',1,.8,True);save()
'''+s[b:];p.write_text(s)
