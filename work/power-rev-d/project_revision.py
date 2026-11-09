from pathlib import Path
import json
p=Path('outputs/rover/Omni_UGV_Rev_D_power_audit/omni_ugv.kicad_pro');d=json.loads(p.read_text());print(d.get('text_variables'));d.setdefault('text_variables',{})['REVISION']='D-PROTOTYPE';p.write_text(json.dumps(d,indent=2)+'\n')
p=Path('outputs/rover/Omni_UGV_Rev_D_power_audit/omni_ugv.kicad_sch');p.write_text(p.read_text().replace('Omni UGV / Rev C','Omni UGV / Rev D'))
