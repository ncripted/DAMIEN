"""Reserve local escape channels before completing inter-block routing."""
from pathlib import Path
import math
from itertools import product
exec(Path("work/rev-f-startup/refine_routes.py").read_text().split('wide["CHG_BAT"]')[0])
def persist():
    (work/"fanout-routes.json").write_text(json.dumps([{k:v for k,v in t.items() if k!="geo"} for t in out]))

def fanout(d,directions,w=.16,min_length=.55):
    a=tuple(d["at"])
    layer=endpoints(d)[0][2]
    net=d["net"]
    region=Point(a).buffer(5)
    drill_keepout=obs("","",.3,region,True)
    trace_keepout=obs(net,layer,w/2,region)
    candidates=[]
    for dx,dy in directions:
        for i in range(21):
            length=min_length+i*.125
            x,y=a[0]+dx*length,a[1]+dy*length
            pt=(round(x,4),round(y,4))
            if (not drill_keepout.intersects(Point(pt))
                and not trace_keepout.intersects(LineString([a,pt]))
                and board.buffer(-.65).contains(Point(pt))):
                candidates.append((length,pt))
    if not candidates:
        print("No local via",d["ref"],d["num"],net,flush=True)
        return None
    _,pt=min(candidates)
    addtrack(net,a,pt,w,layer)
    addvia(net,pt)
    print("Local via",d["ref"],d["num"],net,pt,flush=True)
    return pt

def direct_pin_pair(ref,i,j,w):
    a,b=pad(ref,i),pad(ref,j)
    if straight(a["net"],a["at"],b["at"],w,endpoints(a)[0][2]):
        addtrack(a["net"],a["at"],b["at"],w,endpoints(a)[0][2])

def get_directions(dx,dy):
    return [(dx,dy),(dx-.3*dy,dy+.3*dx),(dx+.3*dy,dy-.3*dx),
            (dx-.55*dy,dy+.55*dx),(dx+.55*dy,dy-.55*dx)]
for ref,i,j in [("U5",2,3),("U5",10,11),("U18",7,8)]:
    direct_pin_pair(ref,i,j,.2)

todo = [
    ("U15",5,0,-1,.26,1.52),("U15",6,0,1,.26,1.52),
    ("U15",8,1,0,.16,.75),("U15",9,1,0,.16,.75),
    ("U5",2,-1,0,.20,.85),("U5",10,1,0,.20,.85),
    ("U7",1,-1,0,.16,.8),("U7",14,1,0,.16,.8),
    ("U7",6,-1,0,.16,.8),("U7",7,-1,0,.16,.8),
    ("U7",8,1,0,.16,.8),("U7",9,1,0,.16,.8),
    ("U7",10,1,0,.16,.8),("U7",11,1,0,.16,.8),
    ("U7",12,1,0,.16,.8),("U7",3,-1,0,.16,.8),
    ("U18",2,-1,0,.18,.55),("U18",8,1,0,.18,.55),
    ("U17",3,1,0,.18,.55),("C46",2,0,1,.20,.55),
]
for ref,num,dx,dy,width,length in todo:
    d=pad(ref,num)
    if not any(d is item for pair in opens for item in pair):
        continue
    directions=get_directions(dx,dy)
    if ref=="U15" and num in (5,6):
        directions=[(0,dy),(0,-dy)]
    fanout(d,directions,width,length)
    persist()
