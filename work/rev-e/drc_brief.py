import json
from pathlib import Path
r=json.loads(Path('outputs/rover/Omni_UGV_Rev_E_power_layout/validation/current/drc.json').read_text())
for v in r['violations']:print(v['type'],v['description'],[(i['description'],i['uuid']) for i in v['items']])
