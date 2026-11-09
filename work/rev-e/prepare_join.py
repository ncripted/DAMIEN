from pathlib import Path
s=Path('work/rev-e/router.py').read_text();s+="\nroute('VBAT',(115.6,136.4,'F.Cu'),(114.2,141,'F.Cu'),.8,True,8);save()\n";Path('work/rev-e/join_vbat.py').write_text(s)
