from pathlib import Path
import json
s=Path('work/power-rev-d/route.py').read_text().split('errors=[]')[0]
s+='''# Restore the proven fine-pitch TS escape, now assigned to the fixed TS bias network.
addtrack('CHG_TS_BIAS',(94.5625,127.25),(94.5189,127.206),.2,'F.Cu')
addtrack('CHG_TS_BIAS',(94.5189,127.206),(94.5189,126.666),.2,'F.Cu')
addvia('CHG_TS_BIAS',(94.5189,126.666))
route('CHG_TS_BIAS',endpoint('R60',1),(94.5189,126.666,'B.Cu'),.15,True,15)
# The through-hole probe connector is reachable on the top side; use that escape.
route('CELL_CHG_TEMP',endpoint('R55',2),endpoint('J4',1,'F.Cu'),.15,True,18)
save()
'''
Path('work/power-rev-d/route_finish.py').write_text(s)
