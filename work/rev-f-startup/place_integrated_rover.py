"""Create a placement draft from the integrated netlist. Power rerouting is open."""
from collections import Counter
from pathlib import Path
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
import pcbnew as pcb

sys.path.insert(0,str(Path("work/protection/deps").resolve()))
from shapely.geometry import LineString, Point, Polygon, box
from shapely import STRtree

rover = Path("outputs/rover")
base = rover / "Omni_UGV_Rev_E1_layout_candidate"
out = rover / "Omni_UGV_Rev_F_integration"
stock = Path("C:/Program Files/KiCad/10.0/share/kicad/footprints")
name = "omni_ugv.kicad_pcb"
settings = (out / "omni_ugv.kicad_pro").read_bytes()
root_id = re.search(r'\(uuid\s+"?([a-f0-9-]{36})',(out/"omni_ugv.kicad_sch").read_text())[1]
xml = ET.parse(out / "schematic.net.xml")
components = {c.get("ref"):c for c in xml.findall("./components/comp")}
pins = {(n.get("ref"),n.get("pin")):net.get("name")
        for net in xml.findall("./nets/net") for n in net.findall("node")}

def xy(v):
    return (pcb.ToMM(v.x),pcb.ToMM(v.y))

def point(x,y):
    return pcb.VECTOR2I(pcb.FromMM(x),pcb.FromMM(y))

def shape(rect):
    return box(pcb.ToMM(rect.GetLeft()),pcb.ToMM(rect.GetTop()),
               pcb.ToMM(rect.GetRight()),pcb.ToMM(rect.GetBottom()))

# Delete the original power nets whose topology is now divided. Their old routes
# must not bridge the new charger, regulator or motor rails.
changed_nets = {"PROT_VDD","PROT_BAT","PROT_PACK",
                "PROT_CHG","PROT_DSG","CUT_GATE","CELL_UV_RESET_N"}
split_rails = {"VBAT":("CHG_BAT",{"U5","C16"}),"SYS_RAW":("CHG_OUT",{"U5","C17"})}
source_board = pcb.LoadBoard(str(base/name))
isolated = set()
for rail,(new_rail,refs) in split_rails.items():
    changed_pads = [pad for fp in source_board.GetFootprints() if fp.GetReference() in refs
                    for pad in fp.Pads() if pins.get((fp.GetReference(),pad.GetNumber())) == new_rail]
    assert changed_pads
    for track in source_board.GetTracks():
        if track.GetNetname() != rail:
            continue
        via = isinstance(track,pcb.PCB_VIA)
        if not via and track.GetLayer() != pcb.F_Cu:
            continue
        path = Point(xy(track.GetPosition())) if via else LineString([xy(track.GetStart()),xy(track.GetEnd())])
        width = pcb.ToMM(track.GetWidth(pcb.F_Cu) if via else track.GetWidth())
        if any(path.distance(shape(pad.GetBoundingBox())) < width / 2 + .24 for pad in changed_pads):
            isolated.add(track.m_Uuid.AsString())
removed_tracks = Counter()
removed_footprints = []
source = (base / name).read_text(encoding="utf-8")
prefix, suffix = source.rsplit("\n)",1)
items = re.split(r'\n\t(?=\()',prefix)
kept = [items[0]]
for item in items[1:]:
    if item.startswith(("(segment","(via","(arc","(zone")):
        match = re.search(r'\(net "([^"]+)"\)',item)
        item_uuid = re.search(r'\(uuid "([^"]+)"\)',item)
        if match and (match[1] in changed_nets or (item_uuid and item_uuid[1] in isolated)
                      or (item.startswith("(zone") and match[1] in split_rails)):
            removed_tracks[match[1]] += 1
            continue
    if item.startswith("(footprint "):
        ref = re.search(r'\(property "Reference" "([^"]+)"',item)[1]
        if ref == "U7" or (ref not in components and not re.fullmatch(r"H\d+",ref)):
            removed_footprints.append(ref)
            continue
    kept.append(item)
assert removed_tracks["VBAT"] and removed_tracks["SYS_RAW"]
assert "Q13" in removed_footprints and "U7" in removed_footprints
(out/name).write_text("\n\t".join(kept).replace("OMNI / REV E","OMNI / REV F")+"\n)"+suffix,encoding="utf-8")
b = pcb.LoadBoard(str(out/name))

def net(name):
    item = b.FindNet(name)
    if item is None:
        item = pcb.NETINFO_ITEM(b,name)
        b.Add(item)
    return item

for footprint in b.GetFootprints():
    ref = footprint.GetReference()
    if ref not in components:
        assert re.fullmatch(r"H\d+",ref), ref
        continue
    footprint.SetValue(components[ref].findtext("value"))
    for pad in footprint.Pads():
        target = pins.get((ref,pad.GetNumber()))
        if target and target != pad.GetNetname():
            pad.SetNet(net(target))

poly = pcb.SHAPE_POLY_SET()
assert b.GetBoardPolygonOutlines(poly,False) and poly.OutlineCount() == 1
def polygon_points(line):
    return [xy(line.CPoint(i)) for i in range(line.PointCount())]
allowed = Polygon(polygon_points(poly.COutline(0)),
                  [polygon_points(poly.CHole(0,i)) for i in range(poly.HoleCount(0))]).buffer(-.6)
layers = (pcb.F_Cu,pcb.B_Cu)
copper = {layer:[] for layer in layers}
courtyards = {layer:[] for layer in layers}
for layer in layers:
    for fp in b.GetFootprints():
        if fp.GetLayer() == layer:
            courtyard = fp.GetCourtyard(layer)
            if courtyard.OutlineCount():
                courtyards[layer].append(Polygon(polygon_points(courtyard.COutline(0))))
            else:
                courtyards[layer].append(shape(fp.GetBoundingBox(False,False)))
        for pad in fp.Pads():
            if pad.GetLayerSet().Contains(layer) or pad.GetDrillSize().x:
                copper[layer].append(shape(pad.GetBoundingBox()).buffer(.18))
    for track in b.GetTracks():
        if isinstance(track,pcb.PCB_VIA):
            copper[layer].append(Point(xy(track.GetPosition())).buffer(pcb.ToMM(track.GetWidth(layer))/2+.18))
        elif track.GetLayer() == layer:
            copper[layer].append(LineString([xy(track.GetStart()),xy(track.GetEnd())]).buffer(pcb.ToMM(track.GetWidth())/2+.18))
trees = {layer:STRtree(copper[layer]) for layer in layers}

placement = {
    "U15":(124,126,pcb.B_Cu), "C47":(96,98,pcb.B_Cu),
    "U7":(121,129.7,pcb.B_Cu), "C38":(120,126.8,pcb.B_Cu), "C39":(122,126.8,pcb.B_Cu),
    "J6":(83,104,pcb.B_Cu), "J7":(66,108,pcb.B_Cu), "SW4":(69,83,pcb.F_Cu),
    "SW5":(69,89,pcb.F_Cu), "J8":(84,94,pcb.B_Cu),
    "D10":(125,130,pcb.B_Cu), "D11":(96,129,pcb.F_Cu), "D12":(104,121,pcb.B_Cu),
    "U16":(91,101,pcb.B_Cu), "U17":(95,101,pcb.B_Cu), "U18":(100,101,pcb.B_Cu),
    "U19":(104,101,pcb.B_Cu), "R70":(128,127,pcb.B_Cu), "R71":(128,130,pcb.B_Cu),
    "R73":(127,132,pcb.B_Cu), "R74":(129,132,pcb.B_Cu), "R75":(94,104,pcb.B_Cu),
    "R76":(103,105,pcb.B_Cu), "R77":(106,105,pcb.B_Cu),
    "C40":(127,129,pcb.B_Cu), "C41":(130,129,pcb.B_Cu), "C42":(126,125,pcb.B_Cu),
    "C43":(130,130,pcb.B_Cu), "C44":(96,105,pcb.B_Cu), "C45":(105,107,pcb.B_Cu),
    "C46":(90,104,pcb.B_Cu), "C48":(100,98,pcb.B_Cu),
    "C49":(104,98,pcb.B_Cu),
}
placed = []
deferred = []
for ref,(x,y,layer) in placement.items():
    comp = components[ref]
    lib, land = comp.findtext("footprint").split(":")
    fp = pcb.FootprintLoad(str((out if lib == "UGV" else stock) / (lib+".pretty")),land)
    assert fp is not None, (ref,land)
    fp.SetReference(ref)
    fp.SetValue(comp.findtext("value"))
    datasheet = comp.findtext("datasheet")
    if datasheet:
        fp.GetField(pcb.FIELD_T_DATASHEET).SetText(datasheet)
    fp.SetFPID(pcb.LIB_ID(lib,land))
    sheet_path = comp.find("sheetpath").get("tstamps")
    fp.SetPath(pcb.KIID_PATH("/"+root_id+sheet_path+comp.findtext("tstamps")))
    fp.SetPosition(point(x,y))
    fp.SetParent(b)
    if layer == pcb.B_Cu:
        fp.Flip(fp.GetPosition(),False)
    fp.SetOrientationDegrees(0)
    through = any(pad.GetDrillSize().x for pad in fp.Pads())
    test_layers = layers if through else (layer,)
    radius = 24 if ref in {"J7","D11","U17","C47","U15"} else 14
    offsets = sorted((math.hypot(i,j),i,j) for i in range(-radius,radius+1) for j in range(-radius,radius+1))
    found = False
    for _,i,j in offsets:
        fp.SetPosition(point(x+.5*i,y+.5*j))
        body = shape(fp.GetBoundingBox(False,False)).buffer(.15)
        if not allowed.contains(body) or any(body.intersects(other) for other in courtyards[layer]):
            continue
        pad_shapes = [shape(pad.GetBoundingBox()) for pad in fp.Pads()]
        if any(len(trees[l].query(region,predicate="intersects")) for l in test_layers for region in pad_shapes):
            continue
        for pad in fp.Pads():
            target = pins.get((ref,pad.GetNumber()))
            if target:
                pad.SetNet(net(target))
        b.Add(fp)
        courtyards[layer].append(body)
        for l in test_layers:
            copper[l].extend(region.buffer(.18) for region in pad_shapes)
            trees[l] = STRtree(copper[l])
        placed.append((ref,*xy(fp.GetPosition()),b.GetLayerName(layer)))
        found = True
        break
    if not found:
        deferred.append(ref)


pcb.ZONE_FILLER(b).Fill(b.Zones())
pcb.SaveBoard(str(out/name),b)
(out/"omni_ugv.kicad_pro").write_bytes(settings)
result = {"status":"BLOCKED - placement draft",
          "placed":placed,"deferred":deferred,"obsolete_footprints_removed":sorted(removed_footprints),
          "old_routes_removed_by_net":dict(removed_tracks)}
(out/"placement.json").write_text(json.dumps(result,indent=2)+"\n")
print("Placed",len(placed),"footprints. Deferred:",", ".join(deferred))

