from pathlib import Path
s=Path('work/rev-e/router.py').read_text().replace('r+.18','r+.155');s+='''
for ref,pin,pt in [('U7',7,(122.675,130.6)),('Q8',4,(112.8,136.1)),('R41',1,(117.2,134))]:
 addtrack('PROT_DSG',pad(ref,pin)['at'],pt,.15,'B.Cu');addvia('PROT_DSG',pt)
route('PROT_DSG',(122.675,130.6,'In2.Cu'),(112.8,136.1,'In2.Cu'),.15,False,12);save()
route('PROT_DSG',(117.2,134,'In2.Cu'),(112.8,136.1,'In2.Cu'),.15,False,8);save()
route('PROTECTED_RAW',(114.9,138.8,'B.Cu'),(117,136.3,'B.Cu'),.4,False,10);save()
''';Path('work/rev-e/dsg_tree_route.py').write_text(s)
