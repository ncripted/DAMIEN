from pathlib import Path
import zipfile, hashlib, json, difflib
p=Path("outputs/rover/Omni_UGV_Rev_E_power_layout")
m=json.loads((p/"REV_E_SHA256.json").read_text())
for n in m:
 if (p/n).is_file() and hashlib.sha256((p/n).read_bytes()).hexdigest()!=m[n]: print(n)
with zipfile.ZipFile(p.with_name(p.name+"_review.zip")) as z:
 n="omni_ugv.kicad_pcb"
 old=z.read(p.name+"/"+n).decode()
 new=(p/n).read_text(encoding="utf-8")
 print("old/new lengths",len(old),len(new))
 for line in list(difflib.unified_diff(old.splitlines(),new.splitlines(),n=1))[:80]: print(line)
