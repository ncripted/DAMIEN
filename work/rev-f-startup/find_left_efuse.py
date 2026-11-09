from pathlib import Path
exec(Path("work/rev-f-startup/left_route_integrated.py").read_text().split("def dump")[0])
from shapely import STRtree
from shapely.geometry import Polygon
fixed=[d["geo"] for d in pads if d["ref"]!="U15" and "B.Cu" in d["layers"]]
fixed += [t["geo"] for t in tracks if t["via"] or t["layer"]=="B.Cu"]
tree=STRtree(fixed)
court=[Polygon(f["courtyard"][1][0]).buffer(.15) for f in g["footprints"]
       if f["ref"]!="U15" and f["side"]=="B.Cu" and f["courtyard"][1]]
ct=STRtree(court)
region=board.buffer(-.6)
def clear(geometry):
    return region.covers(geometry) and not len(tree.query(geometry,predicate="intersects"))
sites=[]
for x in np.arange(104,143,.5):
    for y in np.arange(108,145,.5):
        body=box(x-1.47,y-1.47,x+1.47,y+1.47)
        if not clear(body.buffer(.16)) or len(ct.query(body,predicate="intersects")):
            continue
        for sign in (-1,1):
            legs=[]
            for offset,direction in ((-.25,sign),(.25,-sign)):
                a=(x+offset,y+direction*1.05)
                b=(x+offset,y+direction*1.80)
                c=(x+offset,y+direction*3.6)
                if not clear(LineString([b,c]).buffer(.425+.16)):
                    break
                legs.append((a,b,c))
            if len(legs)==2:
                score=math.dist((x,y),(122.5,126))+.5*math.dist((x,y),(123,133))
                sites.append((score,x,y,legs))
assert sites, "No short power escapes in the search area"
score,x,y,legs=min(sites)
print(len(sites),"options; selected",x,y,legs)
(work/"efuse-left-site.json").write_text(json.dumps({"position":[x,y],"legs":legs}))

