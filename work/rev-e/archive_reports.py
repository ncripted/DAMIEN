from pathlib import Path
import shutil
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout').resolve();hist=r/'.history/rev-d-import';hist.mkdir(parents=True,exist_ok=True)
for name in ['engineering','preview','.pcba-workflow']:
 src=r/name;dst=hist/name
 assert src.is_relative_to(r) and dst.is_relative_to(r)
 if src.exists() and not dst.exists():shutil.move(str(src),str(dst))
 src.mkdir(exist_ok=True)
for name in ['REV_D_SHA256.json','validation_summary.json','README.md','START_HERE.md','CHANGELOG.md']:
 src=r/name;dst=hist/name
 if src.exists() and not dst.exists():shutil.copy2(src,dst)
val=r/'validation/current';dst=hist/'validation-current'
if val.exists() and not dst.exists():shutil.copytree(val,dst)
val.mkdir(parents=True,exist_ok=True)
for src,dest in [('work/rev-e/final-drc.json','drc.json'),('work/rev-e/final-erc.json','erc.json'),('work/rev-e/final.net.xml','schematic.net.xml')]:
 shutil.copy2(src,val/dest);shutil.copy2(src,r/dest)
shutil.copy2('work/rev-e/final-schematic.pdf',r/'Schematic.pdf')
print('Archived inherited reports; populated fresh Rev E validation')
