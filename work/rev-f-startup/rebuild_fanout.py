from pathlib import Path
from itertools import product
exec(Path("work/rev-f-startup/rebuild_refine_routes.py").read_text().split('wide["CHG_BAT"]')[0])
for pin in (7,9,10,1):
    d=pad("U15",pin)
    n=d["net"]; a=tuple(d["at"]); layer="B.Cu"
    matches=[b if a0 is d else a0 for a0,b in opens if a0 is d or b is d]
    if not matches:
        continue
    keep=obs(n,layer,.08,Point(a).buffer(6))
    drill=obs("","",.3,Point(a).buffer(6),True)
    region=board.buffer(-.65)
    sites=[]
    for dx,dy in product(range(-14,15),repeat=2):
        v=(round(a[0]+dx*.2,4),round(a[1]+dy*.2,4))
        if math.dist(a,v)<.7 or drill.intersects(Point(v)) or not region.contains(Point(v)):
            continue
        if not keep.intersects(LineString([a,v])):
            sites.append((math.dist(a,v),v))
    found=False
    for _,v in sorted(sites)[:8]:
        for end in endpoints(matches[0])[:2]:
            count=len(out)
            addtrack(n,a,v,.16,layer)
            addvia(n,v)
            if route_pair(n,(*v,"In2.Cu"),end,.16,5):
                found=True
                break
            del out[count:]
            tracks[:]=original_tracks+out
        if found:
            break
    print(n, "routed" if found else "open",len(sites),"escape sites",flush=True)
(work/"rebuild-fanout.json").write_text(json.dumps([{k:v for k,v in t.items() if k!="geo"} for t in out]))
