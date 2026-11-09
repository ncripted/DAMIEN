from pathlib import Path
import re

path=Path("outputs/rover/Omni_UGV_Rev_F_integration/omni_ugv.kicad_pcb")
s=path.read_text(encoding="utf-8")
pairs=[("105.962499 108.999999","105.975 109","GND"),
       ("122.174999 131.999999","122.199999 131.999999","PROT_VSS_SENSE")]
items=re.split(r"\n\t(?=\()",s)
out=[]
for item in items:
    for first,second,net in pairs:
        if f'(net "{net}")' not in item:
            continue
        if item.startswith("(via") and f"(at {second})" in item:
            item=""
            break
        if item.startswith("(segment"):
            item=item.replace(f"(start {second})",f"(start {first})").replace(f"(end {second})",f"(end {first})")
    if item and not (item.startswith("(segment") and re.search(r"\(start ([^)]+)\).*?\(end \1\)",item,re.S)):
        out.append(item)
path.write_text("\n\t".join(out),encoding="utf-8")
