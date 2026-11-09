from pathlib import Path
import pcbnew as pcb
import json

root=Path("outputs/rover/Omni_UGV_Rev_F_left_candidate")
path=root/"omni_ugv.kicad_pcb"
settings=path.with_suffix(".kicad_pro").read_bytes()
board=pcb.LoadBoard(str(path))
site=json.loads(Path("work/rev-f-startup/efuse-left-site.json").read_text())
def point(x,y):
    return pcb.VECTOR2I(pcb.FromMM(x),pcb.FromMM(y))
footprint=board.FindFootprintByReference("U15")
footprint.SetPosition(point(*site["position"]))
for num,(a,b,c) in zip(("5","6"),site["legs"]):
    net=footprint.FindPadByNumber(num).GetNet()
    for start,end,width in ((a,b,.26),(b,c,.85)):
        track=pcb.PCB_TRACK(board)
        track.SetLayer(pcb.B_Cu)
        track.SetStart(point(*start))
        track.SetEnd(point(*end))
        track.SetWidth(pcb.FromMM(width))
        track.SetNet(net)
        board.Add(track)
pcb.ZONE_FILLER(board).Fill(board.Zones())
pcb.SaveBoard(str(path),board)
path.with_suffix(".kicad_pro").write_bytes(settings)
