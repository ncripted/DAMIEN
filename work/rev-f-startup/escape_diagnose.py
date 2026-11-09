from pathlib import Path
exec(Path("work/rev-f-startup/refine_routes.py").read_text().split('wide["CHG_BAT"]')[0])
for r,ns in (("U7",("1","5","6","7","8","9","10","11","12","14")),("U15",("5","6","8","9")),("C46",("2",))):
 for num in ns:
    d=pad(r,num); n=d["net"]; a=d["at"]; w=.16; l=endpoints(d)[0][2]
    directions=[(1,0),(-1,0),(0,1),(0,-1)]
    print(r,num,n,"escape:",[(dx,dy,length) for dx,dy in directions for length in [0.5,1,1.5,2,2.5] if straight(n,a,(a[0]+dx*length,a[1]+dy*length),w,l)])
    if r=="U15":
      for dy in [-1,1]:
        z=(a[0],a[1]+dy*1.6)
        line=LineString([a,z])
        print(dy,[(t.get("ref",t.get("layer")),t.get("num",""),t["net"],round(t["geo"].distance(line),3)) for t in pads+tracks if t["net"]!=n and (l in t.get("layers",[]) or l==t.get("layer") or t.get("via")) and t["geo"].distance(line)<.32])
