from pathlib import Path
import zipfile, hashlib, json
p=Path("outputs/rover/Omni_UGV_Rev_E_power_layout")
m=json.loads((p/"REV_E_SHA256.json").read_text())
for n in m:
 if (p/n).is_file() and hashlib.sha256((p/n).read_bytes()).hexdigest()!=m[n]: print(n)
with zipfile.ZipFile(p.with_name(p.name+"_review.zip")) as z:
 n="omni_ugv.kicad_pcb"
 old=z.read(p.name+"/"+n).decode().splitlines()
 new=(p/n).read_text(encoding="utf-8").splitlines()
 print("old/new lines",len(old),len(new))
 for i,(a,b) in enumerate(zip(old,new)):
  if a!=b:
   print(i+1,repr(a),repr(b));print(new[i:i+8]);break
