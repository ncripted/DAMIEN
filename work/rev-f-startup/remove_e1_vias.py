from pathlib import Path
import pcbnew as p
root=Path("outputs/rover/Omni_UGV_Rev_E1_layout_candidate")
fn=root/"omni_ugv.kicad_pcb"
pro=root/"omni_ugv.kicad_pro"
settings=pro.read_bytes()
b=p.LoadBoard(str(fn))
ids={"2187a600-0b00-458c-bf8c-aea0675c044a","16b9183a-32ab-48a7-88be-f34b132c3188"}
for t in list(b.GetTracks()):
    if t.m_Uuid.AsString() in ids:
        assert isinstance(t,p.PCB_VIA) and t.GetNetname()=="PROTECTED_RAW"
        print("Remove",t.m_Uuid.AsString(),p.ToMM(t.GetPosition()))
        ids.remove(t.m_Uuid.AsString())
        b.Remove(t)
assert not ids
p.ZONE_FILLER(b).Fill(b.Zones())
p.SaveBoard(str(fn),b)
pro.write_bytes(settings)
