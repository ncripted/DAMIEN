from pathlib import Path
import pcbnew as p
import json
import sys

root = Path("outputs/rover/Omni_UGV_Rev_F_left_candidate")
path = root / "omni_ugv.kicad_pcb"
b = p.LoadBoard(str(path))
settings = path.with_suffix(".kicad_pro").read_bytes()
layers = {b.GetLayerName(n):n for n in (p.F_Cu,p.In2_Cu,p.B_Cu)}
def point(x,y):
    return p.VECTOR2I(p.FromMM(x),p.FromMM(y))

for route in json.loads(Path(sys.argv[1]).read_text()):
    if route["via"]:
        item = p.PCB_VIA(b)
        item.SetPosition(point(*route["a"]))
        item.SetViaType(p.VIATYPE_THROUGH)
        item.SetLayerPair(p.F_Cu,p.B_Cu)
        item.SetDrill(p.FromMM(route["drill"]))
    else:
        item = p.PCB_TRACK(b)
        item.SetStart(point(*route["a"]))
        item.SetEnd(point(*route["z"]))
        item.SetLayer(layers[route["layer"]])
    item.SetWidth(p.FromMM(route["width"]))
    item.SetNet(b.FindNet(route["net"]))
    b.Add(item)
p.ZONE_FILLER(b).Fill(b.Zones())
p.SaveBoard(str(path),b)
path.with_suffix(".kicad_pro").write_bytes(settings)
