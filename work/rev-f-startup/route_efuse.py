from pathlib import Path
import math
from itertools import product
exec(Path("work/rev-f-startup/refine_routes.py").read_text().split('wide["CHG_BAT"]')[0])
def save_power():
    (work/"power-routes.json").write_text(json.dumps([{k:v for k,v in t.items() if k!="geo"} for t in out]))
for pin in (5,6):
    d=pad("U15",pin)
    a=tuple(d["at"]); n=d["net"]
    pair=next((pair for pair in opens if d in pair),None)
    if pair is None:
        continue
    target=next(t for t in pair if t is not d)
    target_ends=endpoints(target)
    clear=obs(n,"",.3,Point(a).buffer(4),True)
    neck=.26
    candidates=[]
    for dx,dy in product(range(-12,13),range(-12,13)):
        pt=(round(a[0]+dx*.2,3),round(a[1]+dy*.2,3))
        if math.dist(a,pt)>2.55 or math.dist(a,pt)<1.5:
            continue
        if clear.intersects(Point(pt)):
            continue
        candidates.append((math.dist(a,pt)+.28*min(math.dist(pt,t[:2]) for t in target_ends),pt))
    print(n,len(candidates),"local transfer sites",flush=True)
    for _,pt in sorted(candidates)[:16]:
        resolution=.05
        pre=len(out)
        try:
            route(n,(*a,"B.Cu"),(*pt,"B.Cu"),neck,allow_via=False,margin=2)
        except RuntimeError:
            continue
        addvia(n,pt)
        success=False
        for end in sorted(target_ends,key=lambda e:math.dist(pt,e[:2]))[:2]:
            for lay in (end[2],"In2.Cu"):
                if route_pair(n,(*pt,lay),end,.75,5):
                    success=True
                    break
            if success:
                break
        if success:
            break
        del out[pre:]
        tracks[:]=original_tracks+out
    save_power()
