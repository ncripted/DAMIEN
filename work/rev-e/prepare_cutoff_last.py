from pathlib import Path
s=Path('work/rev-e/router.py').read_text();s+="\nrr('CELL_P','R66',1,'Q12',2,.15,True);save()\nrr('VBAT','R48',1,'Q9',2,.15,True);save()\n";Path('work/rev-e/cutoff_last_route.py').write_text(s)
