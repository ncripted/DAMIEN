from pathlib import Path
import pcbnew as p
import json

root=Path("outputs/rover/Omni_UGV_Rev_F_integration")
path=root/"omni_ugv.kicad_pcb"
settings=path.with_suffix(".kicad_pro").read_bytes()
b=p.LoadBoard(str(path))
def pt(x,y):
    return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
first=json.loads(Path("work/rev-f-startup/layout-checkpoints/pass1-routes.json").read_text())
def close(a,b):
    return (a-pt(*b)).EuclideanNorm()<5
for t in list(b.GetTracks()):
    n=t.GetNetname()
    is_via=isinstance(t,p.PCB_VIA)
    if n=="BATT_F" and any(r["net"]==n and r["via"]==is_via and close(t.GetStart(),r["a"]) and close(t.GetEnd(),r["z"]) for r in first):
        b.Remove(t)
    if n=="RESET_CT":
        if is_via:
            if close(t.GetPosition(),[88.55,108.5]):
                t.SetPosition(pt(88.52,108.48))
        else:
            if close(t.GetStart(),[88.55,108.5]):
                t.SetStart(pt(88.52,108.48))
            if close(t.GetEnd(),[88.55,108.5]):
                t.SetEnd(pt(88.52,108.48))
p.ZONE_FILLER(b).Fill(b.Zones())
p.SaveBoard(str(path),b)
path.with_suffix(".kicad_pro").write_bytes(settings)

