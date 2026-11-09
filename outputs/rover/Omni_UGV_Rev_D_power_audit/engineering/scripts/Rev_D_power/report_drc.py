from pathlib import Path
import json,collections
r=json.loads(Path('outputs/rover/Omni_UGV_Rev_D_power_audit/validation/current/drc.json').read_text())
for v in r['violations']:
 print(v['type'],v['severity'],v['description'],[i['description'] for i in v['items']])
