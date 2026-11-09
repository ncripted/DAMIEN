from pathlib import Path
import math,json
from itertools import product
exec(Path("work/rev-f-startup/refine_routes.py").read_text().split('wide["CHG_BAT"]')[0])
# Refine grid near fine pitch pins and try both search directions.
# Full-current rails require local placement work and are excluded here.
selected={"ARM_RESET_N","ARM_CLK","USB_ABSENT","EF_ILM","GND"}
for d,e in opens:
    n=d["net"]
    if n not in selected:
        continue
    for a,b in list(product(endpoints(d),endpoints(e)))[:3]:
        for start,end in ((a,b),(b,a)):
            resolution=.025
            try:
                route(n,start,end,.16 if n!="GND" else .2,margin=3)
                break
            except RuntimeError as exc:
                print(exc,flush=True)
        else:
            continue
        break
    (work/"order-signal-routes.json").write_text(json.dumps([{k:v for k,v in t.items() if k!="geo"} for t in out]))
