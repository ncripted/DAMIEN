from pathlib import Path
import json
import re

root=Path("outputs/rover/Omni_UGV_Rev_F_left_candidate")
path=root/"omni_ugv.kicad_pcb"
report=json.loads((root/"drc.json").read_text())
ids={i["uuid"] for d in report["violations"] if d["type"] in {"track_dangling","via_dangling"} for i in d["items"]}
s=path.read_text(encoding="utf-8")
parts=re.split(r"\n\t(?=\()",s)
before=len(parts)
parts=[part for part in parts if not (part.startswith(("(segment","(via")) and any(f'(uuid "{u}")' in part for u in ids))]
s="\n\t".join(parts)
s=re.sub(r'(\(gr_text "PROTO - VERIFY FIT"\s*\(at )[^)]+',r'\g<1>68 102',s)
path.write_text(s,encoding="utf-8")
print("Removed",before-len(parts),"dangling items from the previous report")
