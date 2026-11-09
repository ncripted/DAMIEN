from pathlib import Path
import json,hashlib
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');m=json.loads((r/'REV_D_SHA256.json').read_text());bad=[f for f,h in m.items() if (r/f).exists() and hashlib.sha256((r/f).read_bytes()).hexdigest()!=h];print('Changed since delivery:',bad)
g=json.loads((r/'engineering/board_inventory.json').read_text())
print('In1 motor segments:')
for t in g['tracks']:
 if t['net']=='M2_A' and t['layer']=='In1.Cu' and not t['via']:print(t['a'],t['z'],t['uuid'])
print('Power ICs / passives:')
for ref in ['U4','L1','C18','C19','C20','R36','U7','R37','R38','R39','C24']:
 print(ref,[(p['num'],p['net'],p['at']) for p in g['pads'] if p['ref']==ref])
