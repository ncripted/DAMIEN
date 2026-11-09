"""Check the native KiCad export against the Rev F draft connectivity."""
from pathlib import Path
import csv
import json
import xml.etree.ElementTree as ET

draft = Path("outputs/rover/Omni_UGV_Rev_F_protection_draft")
with (draft / "pin_map.csv").open(encoding="utf-8") as file:
    expected = {(row["Reference"], row["Pin"]): row["Net"] for row in csv.DictReader(file)}
document = ET.parse(draft / "rev_f_protection.xml")
nets = {
    (pin.get("ref"), pin.get("pin")): net.get("name").lstrip("/")
    for net in document.findall("./nets/net")
    for pin in net.findall("node")
}
assert {pin: nets.get(pin) for pin in expected} == expected
assert {pin[1] for pin, name in nets.items() if pin[0] == "U1" and "unconnected" in name} == {"4", "13"}

def members(net):
    return {pin for pin, name in nets.items() if name == net}

assert members("WAKE") == {("U1", "10"), ("SW1", "1")}
assert members("PROTECTED_RAW") == {
    ("U1", "11"), ("Q2", "1"), ("Q2", "2"), ("Q2", "3"), ("J2", "1")
}
assert members("PACK_GND") == {("R1", "2"), ("J2", "2")}
assert members("CELL_N") == {("R1", "1"), ("J1", "2")}
assert members("CSN_K") == {("R1", "4"), ("U1", "6")}
assert members("NTC_TH") == {("J4", "1"), ("U1", "1")}
assert all(not sheet["violations"] for sheet in json.loads((draft / "erc.json").read_text())["sheets"])
print(f"{len(expected)} pin-to-net assignments matched. Six critical net memberships and two deliberate open pins verified. Zero ERC violations.")
