from pathlib import Path
s=Path('work/rev-e/router.py').read_text();s+="\nrr('SYS_ON','U4',1,'R54',2,.15,True);save()\n";Path('work/rev-e/step4_en_route.py').write_text(s)
