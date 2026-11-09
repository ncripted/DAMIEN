import json
from pathlib import Path
s=Path('work/rev-e/router.py').read_text()
s+="\nroute('M2_A',(107.0,102.05,'B.Cu'),(111.6,109.6,'B.Cu'),.4,True,15)\nsave()\n"
Path('work/rev-e/step1_route.py').write_text(s)
