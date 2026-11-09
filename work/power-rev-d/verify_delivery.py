from pathlib import Path
import json,hashlib,zipfile
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');m=json.loads((r/'REV_D_SHA256.json').read_text());bad=[f for f,h in m.items() if hashlib.sha256((r/f).read_bytes()).hexdigest()!=h];assert not bad,bad
z=r.parent/'Omni_UGV_Rev_D_power_audit_review.zip'
with zipfile.ZipFile(z) as p:assert p.testzip() is None
print('Final manifest matched',len(m),'files; ZIP integrity passed')
