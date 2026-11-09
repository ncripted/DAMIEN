from pathlib import Path
import math
from itertools import product
exec(Path("work/rev-f-startup/refine_routes.py").read_text().split('wide["CHG_BAT"]')[0])
d=next(t for t in tracks if t.get("via") and t["net"]=="RESET_CT" and math.dist(t["a"],(88.52,108.48))<.01)
a=d["a"]
region=Point(a).buffer(2)
tracks.remove(d)
keep=slow_obs("RESET_CT","",.3,region,True)
options=[(math.hypot(dx,dy),(a[0]+dx*.01,a[1]+dy*.01)) for dx,dy in product(range(-18,19),repeat=2)]
valid=[(di,p) for di,p in options if not keep.intersects(Point(p))]
if not valid:
    raise RuntimeError("Via corridor requires rip-up")
position=min(valid)[1]
print("Via",a,"to",position)
(work/"reset-position.json").write_text(json.dumps(position))

