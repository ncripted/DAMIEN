from pathlib import Path
import pcbnew as pcb
exec(Path("work/rev-f-startup/left_refine_routes.py").read_text().split('wide["CHG_BAT"]')[0])
path=root/"omni_ugv.kicad_pcb"
b=pcb.LoadBoard(str(path))
settings=path.with_suffix(".kicad_pro").read_bytes()
def point(x,y):
    return pcb.VECTOR2I(round(x*1e6),round(y*1e6))
for ref,pin in [("C40",7),("C41",10),("R74",9)]:
    d=pad("U15",pin)
    n=d["net"]; a=tuple(d["at"])
    f=b.FindFootprintByReference(ref)
    center=next(fg["at"] for fg in g["footprints"] if fg["ref"]==ref)
    p1,p2=pad(ref,1),pad(ref,2)
    local=Point(a).buffer(10)
    keep=obs(n,"B.Cu",.08,local)
    bodykeep=obs("","B.Cu",.15,local)
    drill=obs("","",.3,local,True)
    allowed=board.buffer(-.65)
    for _,dx,dy in sorted((math.hypot(center[0]+i*.25-a[0],center[1]+j*.25-a[1]),i*.25,j*.25)
                          for i in range(-32,33) for j in range(-32,33)):
        dst=(center[0]+dx,center[1]+dy)
        if math.dist(a,dst)>5:
            break
        body=box(dst[0]-1.05,dst[1]-.65,dst[0]+1.05,dst[1]+.65)
        if not allowed.covers(body) or bodykeep.intersects(body):
            continue
        z=(p1["at"][0]+dx,p1["at"][1]+dy)
        q=(p2["at"][0]+dx,p2["at"][1]+dy)
        if keep.intersects(LineString([a,z])) or LineString([a,z]).distance(Point(q))<.67:
            continue
        via=None
        for vx,vy in [(0,.8),(0,-.8),(.95,0),(-.95,0),(0,1.1),(0,-1.1)]:
            trial=(q[0]+vx,q[1]+vy)
            if allowed.contains(Point(trial)) and not drill.intersects(Point(trial)) and straight("GND",q,trial,.2,"B.Cu") and Point(trial).distance(LineString([a,z]))>.55:
                via=trial
                break
        if via is None:
            continue
        f.SetPosition(point(*dst))
        for track in list(b.GetTracks()):
            if track.GetNetname()==n:
                b.Remove(track)
        for start,end,net,width in [(a,z,n,.16),(q,via,"GND",.2)]:
            t=pcb.PCB_TRACK(b)
            t.SetStart(point(*start)); t.SetEnd(point(*end)); t.SetWidth(pcb.FromMM(width))
            t.SetLayer(pcb.B_Cu); t.SetNet(b.FindNet(net)); b.Add(t)
        v=pcb.PCB_VIA(b)
        v.SetPosition(point(*via)); v.SetViaType(pcb.VIATYPE_THROUGH); v.SetLayerPair(pcb.F_Cu,pcb.B_Cu)
        v.SetWidth(pcb.FromMM(.6)); v.SetDrill(pcb.FromMM(.3)); v.SetNet(b.FindNet("GND")); b.Add(v)
        print("Moved",ref,dst,flush=True)
        # Check one placement at a time against the current native board.
        pcb.ZONE_FILLER(b).Fill(b.Zones())
        pcb.SaveBoard(str(path),b)
        path.with_suffix(".kicad_pro").write_bytes(settings)
        raise SystemExit(0)
print("No clear short placement found")
