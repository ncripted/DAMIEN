from pathlib import Path
import pcbnew as p
src=Path("outputs/rover/Omni_UGV_Rev_E_power_layout")
dst=Path("outputs/rover/Omni_UGV_Rev_E1_layout_candidate")
fn="omni_ugv.kicad_pcb"
b=p.LoadBoard(str(src/fn))
settings=(dst/"omni_ugv.kicad_pro").read_bytes()
raw=b.FindNet("PROTECTED_RAW")
def pt(x,y): return p.VECTOR2I(round(x*1e6),round(y*1e6))
def segment(start,end,layer,width):
    t=p.PCB_TRACK(b)
    t.SetStart(pt(*start)); t.SetEnd(pt(*end)); t.SetLayer(layer)
    t.SetWidth(p.FromMM(width)); t.SetNet(raw); b.Add(t)
def via(position):
    v=p.PCB_VIA(b)
    v.SetPosition(pt(*position)); v.SetViaType(p.VIATYPE_THROUGH)
    v.SetLayerPair(p.F_Cu,p.B_Cu); v.SetWidth(p.FromMM(.6)); v.SetDrill(p.FromMM(.3))
    v.SetNet(raw); b.Add(v)
removed={
 "2187a600-0b00-458c-bf8c-aea0675c044a",
 "16b9183a-32ab-48a7-88be-f34b132c3188",
}
for t in list(b.GetTracks()):
    if t.m_Uuid.AsString() in removed:
        assert isinstance(t,p.PCB_VIA) and t.GetNetname()=="PROTECTED_RAW"
        removed.remove(t.m_Uuid.AsString()); b.Remove(t)
assert not removed
import json,sys
layers={b.GetLayerName(n):n for n in (p.F_Cu,p.In2_Cu,p.B_Cu)}
for route in json.loads(Path(sys.argv[1]).read_text()):
    assert route["net"]=="PROTECTED_RAW"
    if route["via"]: via(route["a"])
    else: segment(route["a"],route["z"],layers[route["layer"]],route["width"])
p.ZONE_FILLER(b).Fill(b.Zones())
p.SaveBoard(str(dst/fn),b)
(dst/"omni_ugv.kicad_pro").write_bytes(settings)


