"""Merge verified Rev F battery fixture sheets into a copy of the full rover."""
from pathlib import Path
import re
import shutil
import uuid

rover = Path("outputs/rover")
base = rover / "Omni_UGV_Rev_E1_layout_candidate"
draft = rover / "Omni_UGV_Rev_F_protection_draft"
out = rover / "Omni_UGV_Rev_F_integration"
project = "omni_ugv"
out.mkdir(exist_ok=True)

def blocks(data):
    depth = 0
    quoted = escaped = False
    start = 0
    for index, char in enumerate(data):
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char == "(":
            if depth == 1:
                start = index
            depth += 1
        elif char == ")":
            if depth == 2:
                yield data[start:index + 1]
            depth -= 1

def first(data, kind):
    return next(item for item in blocks(data) if re.match(r"\(" + kind + r"(?:\s|\))", item))

def get_ref(item):
    return re.search(r'\(property "Reference" "([^"]+)"', item)[1]

def get_uuid(item):
    return re.search(r'\(uuid\s+"?([a-f0-9-]{36})', item)[1]

def instances(data):
    return {get_ref(item):item for item in blocks(data) if item.startswith("(symbol ")}

def read(directory, name):
    return (directory / name).read_text(encoding="utf-8-sig")

def save(name, contents):
    (out / name).write_text(contents, encoding="utf-8")

for item in base.iterdir():
    if item.suffix in {".kicad_sch",".kicad_pro",".kicad_dru",".kicad_sym"} or item.name in {
        "sym-lib-table","fp-lib-table","mechanical.json",
    }:
        shutil.copyfile(item, out / item.name)
shutil.copytree(base / "UGV.pretty", out / "UGV.pretty", dirs_exist_ok=True)
shutil.copyfile(draft / "RevF.kicad_sym", out / "RevF.kicad_sym")
table = read(base, "sym-lib-table").rstrip()
save("sym-lib-table", table[:-1] +
     '\n(lib (name "RevF") (type "KiCad") (uri "${KIPRJMOD}/RevF.kicad_sym") (options "") (descr "Rev F power symbols"))\n)\n')
# An immutable E1 board remains available in its own project. This copy is the placement baseline.
board = out / "omni_ugv.kicad_pcb"
if not board.exists():
    shutil.copyfile(base / board.name, board)

root = read(base, project + ".kicad_sch")
root_uuid = get_uuid(root)
original = read(base, "battery_protection.kicad_sch")
old_parts = instances(original)
protection_sheet = get_uuid(original)
power_sheet = "149847e2-56fb-4325-93ee-59d89adc0718"

# Convert the two standalone review drawings to the existing hierarchy.
def transplant(data, sheet_uuid, refs, nets, footprints, retained, remove):
    source_uuid = get_uuid(data)
    data = data.replace(source_uuid, sheet_uuid, 1)
    keep = []
    skip_points = set()
    for item in blocks(data):
        if not item.startswith("(symbol "):
            continue
        ref = get_ref(item)
        if ref not in remove:
            continue
        x, y, _ = map(float, re.search(r'\(at ([^)]+)', item)[1].split())
        offsets = {
            "J1":[1,-1],"J2":[1,-1],"J10":[3,1,-1,-3],
            "J11":[3,1,-1,-3],"#FLG02":[0],"#FLG11":[0],
        }[ref]
        for offset in offsets:
            px = x if ref.startswith("#") else x + 5.08
            skip_points.add((round(px,2),round(y - offset * 1.27,2)))
    skipped_labels = set()
    for item in blocks(data):
        if not item.startswith("(wire "):
            continue
        points = [tuple(map(float,p)) for p in re.findall(r'\(xy ([\d.]+) ([\d.]+)\)',item)]
        if points[0] in skip_points:
            skipped_labels.add(points[1])
    for item in blocks(data):
        if item.startswith("(symbol "):
            ref = get_ref(item)
            if ref in remove:
                continue
            new = refs[ref]
            item = item.replace(f'(property "Reference" "{ref}"',f'(property "Reference" "{new}"')
            item = item.replace(f'(reference "{ref}")',f'(reference "{new}")')
            item = item.replace(f'(path "/{source_uuid}"',f'(path "/{root_uuid}/{sheet_uuid}"')
            item = re.sub(r'\(project "[^"]+"',f'(project "{project}"',item,count=1)
            if ref in footprints:
                item = re.sub(r'\(property "Footprint" "[^"]*"',
                              f'(property "Footprint" "{footprints[ref]}"',item,count=1)
            if ref in retained:
                item = item.replace(get_uuid(item),get_uuid(old_parts[new]),1)
        elif item.startswith("(wire "):
            start = tuple(map(float,re.search(r'\(xy ([\d.]+) ([\d.]+)',item).groups()))
            if start in skip_points:
                continue
        elif item.startswith("(label "):
            pos = tuple(map(float,re.search(r'\(at ([\d.]+) ([\d.]+)',item).groups()))
            if pos in skipped_labels:
                continue
            net = re.search(r'\(label "([^"]+)"',item)[1]
            item = item.replace(f'(label "{net}"',f'(global_label "{nets.get(net,net)}" (shape bidirectional)',1)
        elif item.startswith("(sheet_instances "):
            continue
        keep.append(item)
    return keep

protection_refs = {
    "Q1":"Q7","Q2":"Q8","R1":"R36","U1":"U7","R2":"R37",
    "C1":"C24","C2":"C38","C3":"C39","SW1":"SW4","J3":"J6","J4":"J7",
    "#FLG01":"#FLG31",
}
protection_fp = {
    "U1":"Package_DFN_QFN:TDFN-14-1EP_3x3mm_P0.4mm_EP1.78x2.35mm",
    "Q1":"UGV:CSD17308Q3_TI","Q2":"UGV:CSD17308Q3_TI",
    "R1":"UGV:WSK2512_T1p19_Kelvin","R2":"UGV:Resistor_SMD__R_0603_1608Metric",
    "C1":"UGV:Capacitor_SMD__C_0603_1608Metric",
    "SW1":"Button_Switch_SMD:SW_SPST_TL3342",
    "J3":"Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical_SMD_Pin1Left",
    "J4":"Connector_JST:JST_PH_S2B-PH-SM4-TB_1x02-1MP_P2.00mm_Horizontal",
}
common = {"PACK_GND":"GND"}
parts = transplant(read(draft,"rev_f_protection.kicad_sch"),protection_sheet,
                   protection_refs,{"FET_DRAIN":"PROT_DRAIN","CHG_GATE":"PROT_CHG",
                                    "DIS_GATE":"PROT_DSG","CSP_K":"PROT_VSS_SENSE",
                                    "CSN_K":"PROT_CS_SENSE",**common},
                   protection_fp,{"Q1","Q2","R1","R2","C1"},{"J1","J2","#FLG02"})
temp_refs = {"J5","R42","R43","C25","TH1","TH2","#FLG20"}
old_lib = first(original,"lib_symbols")
temp_instances = [old_parts[ref] for ref in sorted(temp_refs)]
library_ids = {re.search(r'\(lib_id "([^"]+)"',item)[1] for item in temp_instances}
temp_defs = [item for item in blocks(old_lib)
             if re.match(r'\(symbol "([^"]+)"',item)[1] in library_ids]
for index,item in enumerate(parts):
    if item.startswith("(lib_symbols"):
        parts[index] = item[:-1] + "\n" + "\n".join(temp_defs) + "\n)"
    if item.startswith("(paper"):
        parts[index] = '(paper "A3")'
# Existing temperature circuits occupy y >= 149.86 mm. Keep their native wiring
# and the original raw-cell ground flag. Exclude the old shunt pin at 149.86 mm.
for item in blocks(original):
    if item.startswith("(wire "):
        pts = [tuple(map(float,p)) for p in re.findall(r'\(xy ([\d.]+) ([\d.]+)\)',item)]
        if all(149.86 <= y <= 231.14 for _,y in pts) or pts == [(76.2,260.35),(76.2,260.35)]:
            parts.append(item)
    elif item.startswith("(global_label "):
        y = float(re.search(r'\(at [\d.]+ ([\d.]+)',item)[1])
        if 149.86 <= y <= 231.14 and not item.startswith('(global_label "PROT_VSS_SENSE"'):
            parts.append(item)
        elif y == 260.35 and item.startswith('(global_label "CELL_N"'):
            parts.append(item)
    elif item.startswith("(junction "):
        y = float(re.search(r'\(at [\d.]+ ([\d.]+)',item)[1])
        if 149.86 <= y <= 231.14:
            parts.append(item)
parts.extend(temp_instances)
parts = [item.replace('"1S raw cell"','"Cell input is on Charging sheet"')
         .replace('Confirm cold insertion and charger fault recovery before layout.','Confirm cold insertion and charger fault recovery before lab bring-up.')
         .replace('See PROGRAMMING.md for settings and OPEN_ISSUES.md for integration gates.','Existing TH1 and TH2 circuits below remain cell-mounted.') for item in parts]
save("battery_protection.kicad_sch","(kicad_sch\n"+"\n".join(parts)+"\n)\n")

power_refs = {"U10":"U15","U11":"U16","U12":"U17","U13":"U18","U14":"U19",
              "J12":"J8","SW10":"SW5","#FLG10":"#FLG32"}
power_refs.update({f"D{i}":f"D{i}" for i in range(10,13)})
power_refs.update({f"R{i}":f"R{i+60}" for i in (10,11,13,14,15,16,17)})
power_refs.update({f"C{i}":f"C{i+30}" for i in range(10,20)})
power_fp = {"U10":"UGV:TI_RPW0010A", "U13":"Package_SO:VSSOP-8_2.3x2mm_P0.5mm",
            "SW10":"Button_Switch_SMD:SW_SPST_TL3342",
            "J12":"Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical_SMD_Pin1Left"}
parts = transplant(read(draft,"rev_f_usb_power_path.kicad_sch"),power_sheet,power_refs,
                   {"DRIVE_RAW":"VBAT",**common},power_fp,set(),{"J10","J11","#FLG11"})
# SYS_RAW is driven by the output of the diode OR, represented by a flag for ERC.
flag = next(item for item in parts if item.startswith("(symbol ") and get_ref(item) == "#FLG32")
flag = flag.replace("#FLG32","#FLG33")
flag = re.sub(r'\(uuid "([a-f0-9-]+)"\)',lambda _: f'(uuid "{uuid.uuid5(uuid.NAMESPACE_URL,"rover-f/sys"+_.group(1))}")',flag)
flag = re.sub(r'\(at [^)]+\)',"(at 210.82 114.30 0)",flag)
parts.extend([flag,'(global_label "SYS_RAW" (shape bidirectional) (at 210.82 114.30 0) (effects (font (size 1 1))) (uuid "6d140f78-3452-57b4-b489-bab589139628"))'])
parts = [item.replace("TPS259474LRPW\"", "TPS259474LRPWR\"").replace("DRIVE_RAW requires","VBAT motor feed requires")
         .replace("USB_5V comes from the USB-C port. The existing BQ24074 and USB data path are external to this sheet.",
                  "USB_5V, CHG_BAT and CHG_OUT connect to the Charging sheet. SYS_RAW powers the regulator.")
         for item in parts]
save("discharge_cutoff.kicad_sch","(kicad_sch\n"+"\n".join(parts)+"\n)\n")

charging = read(base,"charging.kicad_sch")
for item in blocks(charging):
    if item.startswith('(global_label "SYS_RAW"') and "95800c9d-dff2-5be5-9582-487c2d6cdb6d" in item:
        charging = charging.replace(item,item.replace('"SYS_RAW"','"CHG_OUT"',1),1)
    if item.startswith('(global_label "VBAT"'):
        charging = charging.replace(item,item.replace('"VBAT"','"CHG_BAT"',1),1)
save("charging.kicad_sch",charging)
save(project+".kicad_sch",root.replace('"Independent discharge cutoff"','"Rev F USB and drive power path"')
     .replace('(rev "E - prototype")','(rev "F - integration draft")'))

