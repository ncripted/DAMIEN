from pathlib import Path
s=Path('work/rev-e/router.py').read_text().replace('r+.18','r+.155');s+="\nroute('PROTECTED_RAW',(114.9,138.8,'B.Cu'),(117,136.3,'B.Cu'),.4,False,10);save()\n";Path('work/rev-e/reroute_bank_lead.py').write_text(s)
