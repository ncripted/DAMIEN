"""Verify the saved E1 layout against its unchanged Rev E circuit baseline."""
from collections import Counter
from hashlib import sha256
import csv
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

import pcbnew as pcb

root = Path("outputs/rover")
base = root / "Omni_UGV_Rev_E_power_layout"
candidate = root / "Omni_UGV_Rev_E1_layout_candidate"
board_file = "omni_ugv.kicad_pcb"
before = pcb.LoadBoard(str(base / board_file))
after = pcb.LoadBoard(str(candidate / board_file))

def xy(point):
    return (point.x, point.y)

def tracks(board):
    return {item.m_Uuid.AsString(): item for item in board.GetTracks()}

def track_shape(item):
    dimensions = (item.GetWidth(pcb.F_Cu), item.GetDrill()) if isinstance(item, pcb.PCB_VIA) else (item.GetWidth(),)
    return (item.GetNetname(), item.GetLayer(), xy(item.GetStart()), xy(item.GetEnd()), dimensions)

def outline(board):
    poly = pcb.SHAPE_POLY_SET()
    assert board.GetBoardPolygonOutlines(poly, False)
    def points(line):
        return [xy(line.CPoint(i)) for i in range(line.PointCount())]
    return [(points(poly.COutline(i)), [points(poly.CHole(i, j)) for j in range(poly.HoleCount(i))])
            for i in range(poly.OutlineCount())]

def pads(board):
    return {
        (part.GetReference(), pad.m_Uuid.AsString()):
        (pad.GetNumber(), pad.GetNetname(), xy(pad.GetPosition()), xy(pad.GetSize()),
         xy(pad.GetDrillSize()), pad.GetOrientationDegrees(), tuple(pad.GetLayerSet().Seq()))
        for part in board.GetFootprints() for pad in part.Pads()
    }

old, new = tracks(before), tracks(after)
removed, added = old.keys() - new.keys(), new.keys() - old.keys()
assert removed == {"2187a600-0b00-458c-bf8c-aea0675c044a", "16b9183a-32ab-48a7-88be-f34b132c3188"}
assert all(track_shape(old[key]) == track_shape(new[key]) for key in old.keys() & new.keys())
assert all(new[key].GetNetname() == "PROTECTED_RAW" for key in added)
assert all(new[key].GetLayer() != pcb.In1_Cu for key in added if not isinstance(new[key], pcb.PCB_VIA))
assert outline(before) == outline(after)
assert pads(before) == pads(after)
assert after.GetCopperLayerCount() == 4
new_vias = [new[key] for key in added if isinstance(new[key], pcb.PCB_VIA)]
assert len(new_vias) == 3
smd_pads = [pad for part in after.GetFootprints() for pad in part.Pads()
            if pad.GetAttribute() == pcb.PAD_ATTRIB_SMD]
for via in new_vias:
    pos = via.GetPosition()
    for pad in smd_pads:
        box = pad.GetBoundingBox()
        dx = max(box.GetLeft() - pos.x, pos.x - box.GetRight(), 0)
        dy = max(box.GetTop() - pos.y, pos.y - box.GetBottom(), 0)
        assert math.hypot(dx, dy) > via.GetWidth(pcb.F_Cu) / 2, (pos, pad.GetParent().GetReference())

native_drc = json.loads((candidate / "drc.json").read_text())
for key in ("violations", "unconnected_items", "schematic_parity"):
    assert not native_drc[key], key
assert all(not sheet["violations"] for sheet in json.loads((candidate / "erc.json").read_text())["sheets"])

def pin_map(filename):
    doc = ET.parse(filename)
    return {(n.get("ref"), n.get("pin")): net.get("name")
            for net in doc.findall("./nets/net") for n in net.findall("node")}

assert pin_map(base / "schematic.net.xml") == pin_map(candidate / "schematic.net.xml")
unchanged = [file.name for file in base.glob("*.kicad_sch")] + ["omni_ugv.kicad_dru", "omni_ugv.kicad_pro"]
for name in unchanged:
    assert (base / name).read_bytes() == (candidate / name).read_bytes(), name

diameters = Counter(round(pcb.ToMM(via.GetDrill()), 4)
                    for via in new.values() if isinstance(via, pcb.PCB_VIA))
proof = {
    "board_sha256": sha256((candidate / board_file).read_bytes()).hexdigest(),
    "removed_source_pad_vias": sorted(removed),
    "new_vias_mm": sorted([pcb.ToMM(c) for c in xy(via.GetPosition())] for via in new_vias),
    "new_vias_outside_smd_copper": True,
    "all_footprint_pads_and_board_outline_match_rev_e": True,
    "other_track_geometry_preserved": True,
    "new_in1_signal_tracks": 0,
    "via_drill_count_by_mm": dict(diameters),
    "native_netlist_pin_count": len(pin_map(candidate / "schematic.net.xml")),
    "native_drc": 0,
    "native_opens": 0,
    "schematic_parity_issues": 0,
    "native_erc": 0,
    "manufacturing_release": "BLOCKED",
}
(candidate / "layout-proof.json").write_text(json.dumps(proof, indent=2) + "\n")
with (base / "BOM.csv").open(encoding="utf-8-sig", newline="") as file:
    rows = list(csv.reader(file))
for row in rows[1:]:
    if row[0] == "Q8":
        row[-1] = "Primary discharge FET. E1 uses separate off-pad power and sense vias."
    elif row[0] == "Q13":
        row[-1] = "Cell undervoltage disconnect. E1 moves its source via outside the land."
with (candidate / "BOM.csv").open("w", encoding="utf-8", newline="") as file:
    csv.writer(file).writerows(rows)
print(json.dumps(proof, indent=2))
