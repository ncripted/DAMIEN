from pathlib import Path
import math
from itertools import product
exec(Path("work/rev-f-startup/rebuild_refine_routes.py").read_text().split('wide["CHG_BAT"]')[0])
wide["CHG_BAT"]=.3
wide["CHG_OUT"]=.35
def priority(pair):
    d,e=pair
    net=d["net"]
    return (net not in ("GND","CHG_BAT","CHG_OUT","VBAT","PROTECTED_RAW"),
            min((math.dist(a[:2],b[:2]) for a,b in product(endpoints(d),endpoints(e))),default=100))
def output():
    (work/"rebuild-routes.json").write_text(json.dumps([{k:v for k,v in t.items() if k!="geo"} for t in out]))
for d,e in sorted(opens,key=priority):
    n=d["net"]
    if n!=e["net"] or not n:
        continue
    if n not in {'EF_EN', 'PROT_DSG', 'EF_TIMER', 'PROT_CS_SENSE', 'EF_SLEW', 'BATT_F', 'REG_1V8', 'EF_ILM', 'PROT_CHG'}:
        continue
    refs={(t.get("ref"),t.get("num")) for t in (d,e)}
    if refs & {("U15","5"),("U15","6")}:
        continue
    w=wide.get(n,.16)
    if n=="GND":
        w=.2
    if n=="PROTECTED_RAW" and refs & {("U18","2"),("U18","8"),("U7","11"),("C46","1"),("D10","1")}:
        w=.2
    if n in ("CHG_BAT","CHG_OUT") and any(t.get("ref")=="U5" for t in (d,e)):
        w=.2
    candidates=[]
    for a,b in product(endpoints(d),endpoints(e)):
        if d.get("via") and a[2]=="F.Cu":
            continue
        if e.get("via") and b[2]=="F.Cu":
            continue
        candidates.append((a,b))
    candidates.sort(key=lambda q:math.dist(q[0][:2],q[1][:2])+.75*(q[0][2]!=q[1][2]))
    for a,b in candidates[:3]:
        if "ref" in e and "ref" not in d:
            a,b=b,a
        if route_pair(n,a,b,w,5):
            break
    output()
