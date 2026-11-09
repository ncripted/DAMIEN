from pathlib import Path
from itertools import product
from collections import Counter
import json

work=Path("work/rev-f-startup")
root=Path("outputs/rover/Omni_UGV_Rev_F_power_rebuild")
engine=Path("work/rev-e/router.py").read_text().split("removed=[]")[0]
engine=engine.replace("work/rev-e/geometry.json",(work/"rebuild-geometry.json").as_posix()).replace("r+.18","r+.155").replace("st=time.time();res=.1","st=time.time();res=.1")
engine=engine.replace("g['pads'];out=[]","[d for d in g['pads'] if d['layers']];out=[]")
engine=engine[:engine.index("  import matplotlib")] + engine[engine.index("  raise RuntimeError('No route"):]
exec(engine)
# Include the TI corner pad extensions in obstacle tests. Copper dimensions
# are exact in KiCad, which independently validates all candidate routes.
for d in pads:
    if d["ref"] == "U15" and d["num"] in {"1","4","7","10"}:
        x,y=d["at"]
        cx,cy=next(f["at"] for f in g["footprints"] if f["ref"]=="U15")
        sx=-1 if x<cx else 1
        sy=-1 if y<cy else 1
        d["geo"]=box(x-.125,y-.325,x+.125,y+.325).union(
            box(min(x,x+sx*.475),min(y+sy*.025,y+sy*.325),
                max(x,x+sx*.475),max(y+sy*.025,y+sy*.325)))

def dump():
    (work/"routes.json").write_text(json.dumps([{k:v for k,v in t.items() if k!="geo"} for t in out]))

items={d["uuid"]:d for d in pads+tracks}
report=json.loads((root/"drc.json").read_text())
opens=[tuple(items[i["uuid"]] for i in issue["items"]) for issue in report["unconnected_items"]
       if len(issue["items"])==2 and all(i["uuid"] in items for i in issue["items"])]
wide={"CELL_RAW":.85,"PROTECTED_RAW":.85,"VBAT":.85,"SYS_RAW":.55,
      "CHG_BAT":.4,"CHG_OUT":.5,"USB_5V":.5}
def endpoints(d):
    if "ref" in d:
        return [(*d["at"],l) for l in layers if l in d["layers"]]
    if d["via"]:
        return [(*d["a"],l) for l in layers]
    return [(*d[k],d["layer"]) for k in ("a","z")] if d["layer"] in layers else []

def ground(d):
    a=d["at"]
    l=endpoints(d)[0][2]
    x,y=a
    region=Point(a).buffer(4)
    veto=obs("","",.3,region,True)
    trace=obs("GND",l,.1,region)
    for dx,dy in sorted(product(range(-12,13),repeat=2),key=lambda q: math.hypot(*q)):
        pt=(round(x+dx*.2,4),round(y+dy*.2,4))
        if math.dist(a,pt)<.5 or not board.buffer(-.65).contains(Point(pt)) or veto.intersects(Point(pt)):
            continue
        if not trace.intersects(LineString([a,pt])):
            addtrack("GND",a,pt,.2,l)
            addvia("GND",pt)
            return True
    return False

seen=set()
for pair in opens:
    if pair[0]["net"]!="GND":
        continue
    for d in pair:
        if "ref" in d and d["uuid"] not in seen and endpoints(d):
            seen.add(d["uuid"])
            ground(d)
dump()

def rank(pair):
    a,b=pair
    near=min((math.dist(u[:2],v[:2]) for u,v in product(endpoints(a),endpoints(b))),default=100)
    return (a["net"] not in wide,near)

for a,b in sorted(opens,key=rank):
    n=a["net"]
    if n in {"GND",""} or b["net"]!=n:
        continue
    pairs=sorted(product(endpoints(a),endpoints(b)),key=lambda q:math.dist(q[0][:2],q[1][:2])+(q[0][2]!=q[1][2]))
    width=wide.get(n,.2)
    # Fanout from the eFuse input and output must clear the neighboring lands.
    efuse=next((d for d in (a,b) if d.get("ref")=="U15" and d.get("num") in {"5","6"}),None)
    if efuse:
        continue
    for start,end in pairs[:2]:
        try:
            route(n,start,end,width,margin=4)
            dump()
            break
        except RuntimeError as exc:
            print(exc,flush=True)



