from pathlib import Path
import pcbnew as p
import json

root=Path("outputs/rover/Omni_UGV_Rev_F_integration")
path=root/"omni_ugv.kicad_pcb"
settings=path.with_suffix(".kicad_pro").read_bytes()
b=p.LoadBoard(str(path))
old=p.VECTOR2I(p.FromMM(88.5),p.FromMM(108.5))
new=p.VECTOR2I(p.FromMM(88.55),p.FromMM(108.5))
for t in b.GetTracks():
    if t.GetNetname()!="RESET_CT":
        continue
    if isinstance(t,p.PCB_VIA):
        if (t.GetPosition()-old).EuclideanNorm()<5:
            t.SetPosition(new)
    else:
        if (t.GetStart()-old).EuclideanNorm()<5:
            t.SetStart(new)
        if (t.GetEnd()-old).EuclideanNorm()<5:
            t.SetEnd(new)
p.ZONE_FILLER(b).Fill(b.Zones())
p.SaveBoard(str(path),b)
path.with_suffix(".kicad_pro").write_bytes(settings)
