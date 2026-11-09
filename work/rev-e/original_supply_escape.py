from pathlib import Path
import json,math
x=json.loads(Path('outputs/rover/Omni_UGV_Rev_D_power_audit/engineering/board_inventory.json').read_text())
for t in x['tracks']:
 if t['net'] in ['PROT_VDD','PROT_BAT'] and (t['via'] or min(math.dist(p,(118.325,123)) for p in [t['a'],t['z']])<2):print(t['net'],t['layer'],t['width'],t['via'],t['a'],t['z'])
