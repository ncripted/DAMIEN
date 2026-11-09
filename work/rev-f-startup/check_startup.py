import hashlib
import json
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

revision = Path("outputs/rover/Omni_UGV_Rev_E_power_layout")
evidence = Path("work/rev-f-startup")
netlist = ET.parse(evidence / "rev-e.xml")
pins = {
    (node.attrib["ref"], node.attrib["pin"]): net.attrib["name"]
    for net in netlist.findall("./nets/net")
    for node in net.findall("node")
}
expected = {
    ("U5", "2"): "VBAT", ("U5", "3"): "VBAT",
    ("U5", "10"): "SYS_RAW", ("U5", "13"): "USB_5V",
    ("U7", "1"): "PROT_BAT", ("U7", "2"): "PROT_VDD",
    ("U7", "3"): "PROT_VSS_SENSE", ("U7", "6"): "PROT_PACK",
    ("R38", "1"): "CELL_P", ("R38", "2"): "PROT_BAT",
    ("R39", "1"): "PROTECTED_RAW", ("R39", "2"): "PROT_PACK",
    ("Q13", "1"): "PROTECTED_RAW", ("Q13", "5"): "VBAT",
    ("J2", "1"): "CELL_P", ("J2", "2"): "CELL_N",
}
for key, net in expected.items():
    assert pins[key] == net, (key, pins[key], net)
values = {comp.attrib["ref"]: comp.findtext("value")
          for comp in netlist.findall("./components/comp")}
assert values["U7"] == "BQ298217RUGR"
assert values["U5"] == "BQ24074RGT"
assert values["Q13"] == "DMP2008UFG-7"
assert values["R39"] == "1k 1%"

drc = json.loads((evidence / "rev-e-drc.json").read_text())
erc = json.loads((evidence / "rev-e-erc.json").read_text())
assert not any(drc[key] for key in ("violations", "unconnected_items", "schematic_parity"))
assert not any(sheet["violations"] for sheet in erc["sheets"])
manifest = json.loads((revision / "REV_E_SHA256.json").read_text())
for file in ("omni_ugv.kicad_sch", "battery_protection.kicad_sch",
             "charging.kicad_sch", "discharge_cutoff.kicad_sch"):
    assert hashlib.sha256((revision / file).read_bytes()).hexdigest() == manifest[file], file

with zipfile.ZipFile(revision.with_name(revision.name + "_review.zip")) as archive:
    def original(filename):
        return archive.read(revision.name + "/" + filename).decode("utf-8")

    def without_model_paths(contents):
        return [line for line in contents.splitlines() if not line.lstrip().startswith('(model "')]

    board = "omni_ugv.kicad_pcb"
    assert without_model_paths(original(board)) == without_model_paths(
        (revision / board).read_text(encoding="utf-8"))
    project = "omni_ugv.kicad_pro"
    saved_settings = json.loads(original(project))
    live_settings = json.loads((revision / project).read_text(encoding="utf-8"))
    for key in ("board", "net_settings", "schematic"):
        assert saved_settings[key] == live_settings[key], key

print("Native pin connections, component values and rule checks verified.")
print("PCB differs from archived release only in 3D model path lines.")
print("Board rules, net settings and schematic settings match the archive.")
print("Voltage headroom in V, optimistic zero-drop charger path")
print("Cell   BAT=4.16    BAT=4.20    BAT=4.23")
for cell in (2.60, 3.00, 3.10, 3.50, 3.70, 4.00, 4.20):
    print(f"{cell:4.2f} " + " ".join(f"{v - cell:+11.3f}" for v in (4.16, 4.20, 4.23)))
assert 4.23 - 4.20 < .70
print("Full-cell typical wake comparison fails even at the maximum regulated BAT voltage.")
print(f"6 V isolated fixture, 1 kOhm and modeled 100 kOhm UV pull: {6*100/101:.3f} V at PACK")
