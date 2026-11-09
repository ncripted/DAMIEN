from pathlib import Path
import json
r=Path('outputs/rover/Omni_UGV_Rev_C_flex_camera')
d=json.loads((r/'design_connections.json').read_text())
for ref in ['Q1','Q3','Q7','U7','SW3','J4','TH1','U5','R23','R24']:
 print(next((x for x in d if x['ref']==ref),None))
