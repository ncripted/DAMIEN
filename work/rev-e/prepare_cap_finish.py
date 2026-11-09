from pathlib import Path
s=Path('work/rev-e/router.py').read_text()+"\nroute('M3_B',endpoint('M3',2,'F.Cu'),endpoint('C14',2),.2,True,18)\nsave()\n"
Path('work/rev-e/step2_cap_finish.py').write_text(s)
