"""Compare mechanical and power split evidence for the Rev F placement."""
from pathlib import Path
from collections import Counter
import json
import pcbnew as pcb

root = Path("outputs/rover")
base = root / "Omni_UGV_Rev_E1_layout_candidate"
out = root / "Omni_UGV_Rev_F_integration"
old = pcb.LoadBoard(str(base / "omni_ugv.kicad_pcb"))
new = pcb.LoadBoard(str(out / "omni_ugv.kicad_pcb"))

def pos(point):
    return (point.x, point.y)

def outline(board):
    polygons = pcb.SHAPE_POLY_SET()
    assert board.GetBoardPolygonOutlines(polygons,False)
    def points(line):
        return [pos(line.CPoint(i)) for i in range(line.PointCount())]
    return [(points(polygons.COutline(i)),[points(polygons.CHole(i,j)) for j in range(polygons.HoleCount(i))])
            for i in range(polygons.OutlineCount())]

def motor_mount_geometry(board):
    return sorted((f.GetReference(), pad.GetNumber(), pos(pad.GetPosition()),
                   pos(pad.GetSize()),pos(pad.GetDrillSize()),pad.GetOrientationDegrees())
                  for f in board.GetFootprints() if f.GetReference().startswith(("M","H"))
                  for pad in f.Pads())

assert outline(old)==outline(new)
assert motor_mount_geometry(old)==motor_mount_geometry(new)
assert old.GetCopperLayerCount()==new.GetCopperLayerCount()==4
for ref,num,target in [("U5","2","CHG_BAT"),("U5","10","CHG_OUT"),
                       ("Q1","3","VBAT"),("U4","10","SYS_RAW"),("U7","11","PROTECTED_RAW")]:
    assert new.FindFootprintByReference(ref).FindPadByNumber(num).GetNetname()==target,ref
assert not new.FindFootprintByReference("Q13")
for track in new.GetTracks():
    if not isinstance(track,pcb.PCB_VIA) and track.GetLayer()==pcb.In1_Cu:
        assert track.GetNetname()=="GND"

drc = json.loads((out/"drc.json").read_text())
proof = {
    "status":"BLOCKED - placement and routing in progress",
    "outline_and_motor_mount_pads_match_E1":True,
    "board_layers":4,
    "board_pad_power_split_verified":True,
    "in1_signal_tracks":0,
    "drc_by_type":dict(Counter(item["type"] for item in drc["violations"])),
    "drc_errors":sum(item["severity"]=="error" for item in drc["violations"]),
    "unconnected_items":len(drc["unconnected_items"]),
    "schematic_parity_issues":len(drc["schematic_parity"]),
}
(out/"layout_validation.json").write_text(json.dumps(proof,indent=2)+"\n")
print(json.dumps(proof,indent=2))
