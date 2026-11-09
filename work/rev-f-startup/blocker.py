from pathlib import Path
exec(Path("work/rev-f-startup/refine_routes.py").read_text().split('wide["CHG_BAT"]')[0])
for n in (1,6,7,8,9,10,11,12,14):
 d=pad("U7",n); a=d["at"]; z=(a[0]+(1 if n>7 else -1),a[1]); line=LineString([a,z])
 print(n,[(t.get("ref",t.get("layer")),t.get("num",""),t["net"],round(t["geo"].distance(line),3)) for t in pads+tracks if t["net"]!=d["net"] and ("B.Cu" in t.get("layers",[]) or "B.Cu"==t.get("layer") or t.get("via")) and t["geo"].distance(line)<.232])
