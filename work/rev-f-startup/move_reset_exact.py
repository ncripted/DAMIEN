from pathlib import Path
import json,re
work=Path("work/rev-f-startup")
p=Path("outputs/rover/Omni_UGV_Rev_F_integration/omni_ugv.kicad_pcb")
x,y=json.loads((work/"reset-position.json").read_text())
parts=re.split(r"\n\t(?=\()",p.read_text(encoding="utf-8"))
for i,part in enumerate(parts):
    if part.startswith(("(via","(segment")) and '(net "RESET_CT")' in part:
        parts[i]=part.replace("88.52 108.48",f"{x:.4f} {y:.4f}")
p.write_text("\n\t".join(parts),encoding="utf-8")
