"""Validate independent pin expectations and the USB inhibit voltage budget."""
import json
from math import log
from pathlib import Path
import xml.etree.ElementTree as ET

draft = Path("outputs/rover/Omni_UGV_Rev_F_protection_draft")
netlist = ET.parse(draft / "usb_power_path.xml")
pins = {
    (node.get("ref"), node.get("pin")): net.get("name").lstrip("/")
    for net in netlist.findall("./nets/net")
    for node in net.findall("node")
}
expected = {
    ("U10","1"):"EF_EN", ("U10","2"):"USB_INHIBIT", ("U10","4"):"PACK_GND",
    ("U10","5"):"PROTECTED_RAW", ("U10","6"):"DRIVE_RAW", ("U10","7"):"EF_SLEW",
    ("U10","8"):"PACK_GND", ("U10","9"):"EF_ILM", ("U10","10"):"EF_TIMER",
    ("D10","1"):"PROTECTED_RAW", ("D10","2"):"CHG_BAT",
    ("D11","1"):"SYS_RAW", ("D11","2"):"CHG_OUT",
    ("D12","1"):"SYS_RAW", ("D12","2"):"DRIVE_RAW",
    ("R10","1"):"USB_5V", ("R10","2"):"USB_INHIBIT",
    ("R11","1"):"USB_INHIBIT", ("R11","2"):"PACK_GND",
    ("R13","1"):"EF_EN", ("R13","2"):"PACK_GND",
    ("U11","2"):"USB_5V", ("U11","3"):"PACK_GND", ("U11","4"):"USB_ABSENT",
    ("U11","5"):"PROTECTED_RAW",
    ("R15","1"):"USB_ABSENT", ("R15","2"):"ARM_RESET_N",
    ("U12","1"):"ARM_CLR_N", ("U12","2"):"PROTECTED_RAW",
    ("U12","3"):"PACK_GND", ("U12","4"):"ARM_RESET_N", ("U12","5"):"RESET_CT",
    ("U13","1"):"ARM_CLK", ("U13","2"):"PROTECTED_RAW", ("U13","4"):"PACK_GND",
    ("U13","5"):"EF_EN", ("U13","6"):"ARM_CLR_N", ("U13","7"):"PROTECTED_RAW",
    ("U13","8"):"PROTECTED_RAW",
    ("SW10","1"):"PROTECTED_RAW", ("SW10","2"):"ARM_SWITCH",
    ("U14","2"):"ARM_FILTER", ("U14","3"):"PACK_GND",
    ("U14","4"):"ARM_CLK", ("U14","5"):"PROTECTED_RAW",
    ("R16","1"):"ARM_SWITCH", ("R16","2"):"ARM_FILTER",
    ("R17","1"):"ARM_FILTER", ("R17","2"):"PACK_GND",
    ("C15","1"):"ARM_FILTER", ("C15","2"):"PACK_GND",
    ("J12","1"):"ARM_RESET_N", ("J12","2"):"PACK_GND",
}
assert {key: pins[key] for key in expected} == expected
assert "unconnected" in pins["U10", "3"]
assert {key for key, net in pins.items() if net == "USB_INHIBIT"} == {
    ("U10","2"), ("R10","2"), ("R11","1")
}
assert {key for key, net in pins.items() if net == "EF_EN"} == {
    ("U10","1"), ("U13","5"), ("R13","1")
}
assert not any(sheet["violations"] for sheet in
               json.loads((draft / "usb_power_path_erc.json").read_text())["sheets"])

def divider(source, top, bottom, leakage):
    return source * bottom / (top + bottom) + leakage * top * bottom / (top + bottom)

minimum = divider(4.35, 25200 * 1.001, 10000 * .999, -0.1e-6)
maximum = divider(5.25, 25200 * .999, 10000 * 1.001, 0.1e-6)
absent = divider(0, 25200 * 1.001, 10000 * 1.001, 0.1e-6)
assert minimum > 1.223 and maximum < 1.5
assert absent < 1.076
reset_minimum = -log(0.36) * 350_000 * 80e-9
# Engineering bound for a settled supply, 0.8 VCC target and +20% capacitance.
arm_upper = -log(1 - 0.8 / 0.9) * 10_100 * 120e-9
assert reset_minimum > 10 * arm_upper
print(f"{len(expected)} physical pin checks matched, with PG deliberately open. ERC zero.")
print(f"USB OVLO pin {minimum:.4f} to {maximum:.4f} V over 4.35 to 5.25 V. With VBUS at zero: <= {absent:.4f} V.")
print(f"Estimated reset delay lower bound {reset_minimum*1000:.1f} ms versus arm filter bound {arm_upper*1000:.1f} ms.")
print("Static bounds only. Hardware reset timing and qualification are open.")
