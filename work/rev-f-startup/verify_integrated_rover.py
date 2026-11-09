"""Verify the merged power paths and export the Rev F integration BOM/pin map."""
from pathlib import Path
import csv
import json
import xml.etree.ElementTree as ET

rover = Path("outputs/rover")
base = rover / "Omni_UGV_Rev_E1_layout_candidate"
out = rover / "Omni_UGV_Rev_F_integration"

def read_netlist(folder):
    tree = ET.parse(folder / "schematic.net.xml")
    components = {c.get("ref"):c for c in tree.findall("./components/comp")}
    pins = {(n.get("ref"),n.get("pin")):(net.get("name"),n.get("pinfunction",""))
            for net in tree.findall("./nets/net") for n in net.findall("node")}
    return components,pins

parts,pins = read_netlist(out)
old_parts,old_pins = read_netlist(base)
expected = {
    "CHG_BAT":{("U5","2"),("U5","3"),("C16","1"),("D10","2")},
    "CHG_OUT":{("U5","10"),("U5","11"),("C17","1"),("D11","2")},
    "SYS_RAW":{("D11","1"),("D12","1"),("U4","10"),("R18","1"),("SW3","3"),("C18","1"),("TP5","1")},
    "VBAT":{("U15","6"),("D12","2"),("Q1","3"),("Q5","2"),("Q9","2"),("R31","1"),
            ("R48","1"),("C21","1"),("C43","1"),("TP3","1")},
    "PROT_CS_SENSE":{("R36","4"),("U7","6")},
    "PROT_VSS_SENSE":{("R36","3"),("U7","5"),("U7","15"),("C24","2"),("C39","2"),
                      ("SW4","2"),("J6","3"),("J7","2")},
    "EF_EN":{("U15","1"),("U18","5"),("R73","1")},
    "ARM_CLR_N":{("U17","1"),("U18","6")},
}
for net,members in expected.items():
    assert {key for key,(name,_) in pins.items() if name==net} == members, net
assert pins["D10","1"][0] == pins["U7","11"][0] == pins["U15","5"][0] == "PROTECTED_RAW"
assert pins["J2","1"][0] == "CELL_P" and pins["J2","2"][0] == "CELL_N"
assert pins["J7","1"][0] == pins["U7","1"][0] == "NTC_TH"
assert "Q13" not in parts and parts["U7"].findtext("value") == "MAX17301G+T"
for ref in ("TH1","TH2","J4","J5","U1","U2","U3","M1","M2","M3"):
    for pin,value in old_pins.items():
        if pin[0]==ref:
            assert pins[pin]==value,pin

erc = json.loads((out/"erc.json").read_text())
assert all(not sheet["violations"] for sheet in erc["sheets"])
with (out/"pin_map.csv").open("w",encoding="utf-8",newline="") as f:
    writer = csv.writer(f)
    writer.writerow(("Reference","Physical pin","Pin function","Net"))
    writer.writerows((ref,pin,function,net) for (ref,pin),(net,function) in sorted(pins.items()))
with (base/"BOM.csv").open(encoding="utf-8-sig",newline="") as f:
    source = {row[0]:row for row in list(csv.reader(f))[1:]}
specific = {"U7":"MAX17301G+T","U15":"TPS259474LRPWR","U16":"SN74LVC1G14DBVR","U17":"TPS3840PL31DBVR",
            "U18":"SN74LVC1G74DCUR","U19":"SN74LVC1G17DBVR","D10":"PMEG3020ER","D11":"PMEG3020ER","D12":"PMEG3020ER"}
with (out/"BOM.csv").open("w",encoding="utf-8",newline="") as f:
    writer = csv.writer(f)
    writer.writerow(("Reference","Value","Candidate MPN","Footprint","Status"))
    for ref,c in sorted(parts.items()):
        unchanged = ref in source and ref in old_parts and c.findtext("value")==old_parts[ref].findtext("value")
        mpn = specific.get(ref,source[ref][2] if unchanged else "")
        status = "Rev E1 baseline" if unchanged else "Rev F candidate"
        writer.writerow((ref,c.findtext("value"),mpn,c.findtext("footprint"),status))
print(f"ERC zero. Verified {len(expected)} complete net memberships and 9 retained interfaces. Exported {len(pins)} pin rows.")
