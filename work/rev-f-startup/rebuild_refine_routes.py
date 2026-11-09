"""Route remaining local fanouts and open nets with a finer grid."""
from pathlib import Path
import json

source=Path("work/rev-f-startup/rebuild_route_integrated.py").read_text().split("seen=set()")[0]
source=source.replace('exec(engine)', '''
engine=engine.replace("st=time.time();res=.1","st=time.time();res=resolution")
engine=engine.replace("math.floor((min(start[0],end[0])-margin)/res)*res","start[0]-math.ceil((start[0]-min(start[0],end[0])+margin)/res)*res")
engine=engine.replace("math.floor((min(start[1],end[1])-margin)/res)*res","start[1]-math.ceil((start[1]-min(start[1],end[1])+margin)/res)*res")
engine=engine.replace("r+.155","r+.151")
engine=engine.replace("if len(cost)>1200000","if len(cost)>180000")
resolution=.1
exec(engine)''')
source=source.replace('work/"routes.json"','work/"refine-routes.json"')
exec(source)
from shapely import STRtree
original_pads=pads[:]
original_tracks=tracks[:]
pad_tree=STRtree([d["geo"] for d in original_pads])
track_tree=STRtree([t["geo"] for t in original_tracks])
slow_obs=obs
def obs(net,layer,r,region,via=False):
    original=(pads[:],tracks[:])
    pads[:]=[original_pads[i] for i in pad_tree.query(region)]
    tracks[:]=[original_tracks[i] for i in track_tree.query(region)]
    tracks.extend(t for t in out if t["geo"].intersects(region))
    try:
        return slow_obs(net,layer,r,region,via)
    finally:
        pads[:],tracks[:]=original

def straight(net,a,b,w,l):
    if not board.buffer(-.33-w/2).covers(LineString([a,b])):
        return False
    return not obs(net,l,w/2,LineString([a,b]).buffer(1)).intersects(LineString([a,b]))

def escape(d,directions,neck,bulk):
    a=tuple(d["at"]); layer=endpoints(d)[0][2]; n=d["net"]
    options=[]
    for dx,dy in directions:
        for length in (.65,.8,1.0,1.2,1.5,1.7,1.9,2.2,2.5,3.0):
            pt=(round(a[0]+dx*length,5),round(a[1]+dy*length,5))
            if not straight(n,a,pt,neck,layer):
                continue
            if obs("","",.3,Point(pt).buffer(2),True).intersects(Point(pt)):
                continue
            options.append((a,pt,layer,neck,bulk))
    return options

def route_pair(n,start,end,width,margin):
    global resolution
    if start[2]==end[2] and straight(n,start[:2],end[:2],width,start[2]):
        addtrack(n,start[:2],end[:2],width,start[2])
        return True
    resolution=.05 if math.dist(start[:2],end[:2])<8 else .1
    try:
        route(n,start,end,width,margin=margin)
        return True
    except RuntimeError as exc:
        print(exc,flush=True)
        return False

def power_escape(d,other):
    n=d["net"]
    if d["ref"]=="U15":
        directions=[(0,1),(0,-1)] if d["num"]=="5" else [(0,-1),(0,1)]
        neck=.26
    elif d["ref"]=="U7":
        directions=[(1,0)]
        neck=.18
    else:
        directions=[(-1,0),(1,0),(0,1),(0,-1)]
        neck=.2
    for a,pt,layer,neck,width in escape(d,directions,neck,wide[n])[:5]:
        for end in endpoints(other)[:2]:
            for new_layer in ("In2.Cu","F.Cu","B.Cu"):
                if route_pair(n,(*pt,new_layer),end,width,4):
                    addtrack(n,a,pt,neck,layer)
                    addvia(n,pt)
                    return True
    return False

wide["CHG_BAT"]=.35
wide["CHG_OUT"]=.4
def rank(pair):
    n=pair[0]["net"]
    ref={d.get("ref") for d in pair}
    dist=min((math.dist(a[:2],b[:2]) for a,b in product(*(endpoints(d) for d in pair))),default=100)
    return (0 if n=="GND" else 1 if ref & {"U15","U5","U7"} else 2,dist)

for a,b in sorted(opens,key=rank):
    n=a["net"]
    if n!=b["net"] or not n:
        continue
    if n=="GND":
        for d in (a,b):
            if "ref" in d and endpoints(d):
                ground(d)
        dump()
        continue
    pairings=sorted(product(endpoints(a),endpoints(b)),
                    key=lambda q:math.dist(q[0][:2],q[1][:2])+(q[0][2]!=q[1][2]))
    width=wide.get(n,.16)
    if n in ("CHG_BAT","CHG_OUT") and any(d.get("ref")=="U5" for d in (a,b)):
        width=.2
    if n=="PROTECTED_RAW" and any(d.get("ref") in ("U18","D10","C46") for d in (a,b)):
        width=.22
    if n in wide:
        device=next((d for d in (a,b) if
                     (d.get("ref"),d.get("num")) in {("U15","5"),("U15","6"),("U7","11")}),None)
        if device:
            power_escape(device,b if a is device else a)
            dump()
            continue
    for start,end in pairings[:2]:
        if route_pair(n,start,end,width,6):
            dump()
            break
