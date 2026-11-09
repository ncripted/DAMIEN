from pathlib import Path
exec(Path("work/rev-f-startup/left_refine_routes.py").read_text().split('wide["CHG_BAT"]')[0])
site=json.loads((work/"efuse-left-site.json").read_text())
for pin,leg in zip(("5","6"),site["legs"]):
    d=pad("U15",pin)
    matches=[b if a is d else a for a,b in opens if a is d or b is d]
    start=(*leg[2],"B.Cu")
    found=False
    for other in matches:
        for end in endpoints(other):
            if route_pair(d["net"],start,end,.85,6):
                found=True
                break
        if found:
            break
    print(d["net"], "connected candidate" if found else "open",flush=True)
(work/"left-efuse-rails.json").write_text(json.dumps([{k:v for k,v in t.items() if k!="geo"} for t in out]))
