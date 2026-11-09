"""Generate the standalone, editable Rev F protection draft."""
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL
import csv
import json

OUT = Path("outputs/rover/Omni_UGV_Rev_F_protection_draft")
NAME = "rev_f_protection"
SOURCE = "https://www.analog.com/media/en/technical-documentation/data-sheets/max17300-max17313.pdf"
GRID = 1.27

def uid(key):
    return str(uuid5(NAMESPACE_URL, f"{NAME}/{key}"))

def mm(value):
    return f"{value * GRID:.2f}"

def xy(x, y):
    return f"{mm(x)} {mm(y)}"

def quote(value):
    return json.dumps(str(value), ensure_ascii=False)

def pin(number, name, kind, x, y, angle):
    return (str(number), name, kind, x, y, angle)

def line(points):
    return "(polyline (pts " + " ".join(f"(xy {xy(x,y)})" for x,y in points) + ") (stroke (width 0) (type default)) (fill (type none)))"

def box(x, y):
    return f"(rectangle (start {xy(-x,y)}) (end {xy(x,-y)}) (stroke (width 0) (type default)) (fill (type background)))"

left = [(3,"BATT","power_in"), (2,"CP","power_out"), (7,"REG","power_out"),
        (1,"TH","input"), (5,"CSP","power_in"), (6,"CSN","input"), (15,"EP","passive")]
right = [(14,"CHG","output"), (12,"DIS","output"), (11,"PCKP","passive"),
         (10,"ALRT/PIO","bidirectional"), (8,"SDA","bidirectional"), (9,"SCL","input"),
         (13,"ZVC","input"), (4,"PFAIL","output")]
max_pins = [pin(*p,-13,8-i*2,0) for i,p in enumerate(left)]
max_pins += [pin(*p,13,8-i*2,180) for i,p in enumerate(right)]
pair = [pin(1,"~","passive",-4,0,0),pin(2,"~","passive",4,0,180)]
shunt = pair + [pin(3,"K+","passive",-4,-2,0),pin(4,"K-","passive",4,-2,180)]
def fet(flipped):
    side = -1 if flipped else 1
    # Source pads and drain pads share a drawing point but remain individually netlisted.
    return ([pin(i,"S","passive",-5*side,0,0 if side==1 else 180) for i in (1,2,3)] +
            [pin(4,"G","input",0,-5,90)] +
            [pin(i,"D","passive",5*side,0,180 if side==1 else 0) for i in (5,6,7,8,9)])
def fet_art(flipped):
    side = -1 if flipped else 1
    return (box(3,2) + line([(-3,0),(-1,0)]) + line([(1,0),(3,0)]) +
            line([(0,-3),(0,-1),(-1.3,-1),(1.3,-1)]) +
            line([(-side,0),(-side,1),(side,1),(side,0)]) +
            line([(-0.5*side,0.5),(0.5*side,1),(-0.5*side,1.5),(-0.5*side,0.5)]) +
            line([(0.5*side,0.5),(0.5*side,1.5)]))

symbols = {
    "MAX17301": ("U",box(11,10),max_pins,False),
    "R": ("R",box(2,0.65),pair,True),
    "C": ("C",line([(-2,0),(-0.55,0)])+line([(-0.55,-1.5),(-0.55,1.5)])+
          line([(0.55,-1.5),(0.55,1.5)])+line([(0.55,0),(2,0)]),pair,True),
    "Shunt": ("R",box(2,0.7)+line([(-2,-2),(-2,0)])+line([(2,-2),(2,0)]),shunt,True),
    "FetCharge": ("Q",fet_art(False),fet(False),False),
    "FetDischarge": ("Q",fet_art(True),fet(True),False),
    "Switch": ("SW",line([(-2,0),(1,1)])+line([(1.5,0),(2,0)]),pair,True),
    "Conn2": ("J",box(2,3),[pin(i,"~","passive",4,3-2*i,180) for i in (1,2)],True),
    "Conn3": ("J",box(2,4),[pin(i,"~","passive",4,4-2*i,180) for i in (1,2,3)],True),
    "Flag": ("#FLG",line([(0,0),(0,1),(-0.5,1.5),(0,2),(0.5,1.5),(0,1)]),
             [pin(1,"~","power_out",0,0,90)],True),
}
parts = []
drawing = []
expected = {}

def effects(size=1, more=""):
    return f"(effects (font (size {size} {size})) {more})"

def prop(name,value,x,y,more=""):
    return f"(property {quote(name)} {quote(value)} (at {xy(x,y)} 0) {effects(1,more)})"

def symbol(key, embedded):
    prefix, art, pins, hide_names = symbols[key]
    lib_id = "RevF:" + key if embedded else key
    hide = "(pin_names hide)" if hide_names else "(pin_names (offset 0.508))"
    if key.startswith("Fet") or key == "Flag":
        hide = "(pin_names hide) (pin_numbers hide)"
    power = "(power)" if key == "Flag" else ""
    draw_pins = []
    for number,name,kind,x,y,angle in pins:
        length = 0 if key == "Flag" else 2
        draw_pins.append(f'(pin {kind} line (at {xy(x,y)} {angle}) (length {mm(length)})'
                         f' (name {quote(name)} {effects(0.9)}) (number {quote(number)} {effects(0.9)}))')
    return (f'(symbol {quote(lib_id)} {power} {hide} (in_bom yes) (on_board yes)'
            f' {prop("Reference",prefix,0,0)} {prop("Value",key,0,0)}'
            f' (symbol "{key}_0_1" {art}) (symbol "{key}_1_1" {" ".join(draw_pins)}))')

def wire(x1,y1,x2,y2):
    drawing.append(f'(wire (pts (xy {xy(x1,y1)}) (xy {xy(x2,y2)})) (stroke (width 0) (type default)) (uuid "{uid(len(drawing))}"))')

def label(net,x,y):
    drawing.append(f'(label {quote(net)} (at {xy(x,y)} 0) {effects(1,"(justify left bottom)")} (uuid "{uid(len(drawing))}"))')

def note(value,x,y,size=1.25):
    drawing.append(f'(text {quote(value)} (at {xy(x,y)} 0) {effects(size,"(justify left)")} (uuid "{uid(len(drawing))}"))')

def instance(key,ref,value,x,y,nets,footprint="",datum="",stubs=None):
    pins = symbols[key][2]
    flag = key == "Flag"
    hide = "(hide yes)" if flag else ""
    text_offset = {"MAX17301":12, "TPS259474L":10, "Conn2":5, "Conn3":6, "Conn4":7,
                   "TPS3840PL31":6, "LVC1G74":7, "LVC1G14":6, "LVC1G17":6}.get(key,3)
    drawing.append(f'(symbol (lib_id "RevF:{key}") (at {xy(x,y)} 0) (unit 1)'
                   f' (in_bom {"no" if flag else "yes"}) (on_board {"no" if flag else "yes"}) (dnp no)'
                   f' (uuid "{uid(ref)}") {prop("Reference",ref,x,y-text_offset-2,hide)}'
                   f' {prop("Value",value,x,y-text_offset,hide)}'
                   f' {prop("Footprint",footprint,x,y,"(hide yes)")}'
                   f' {prop("Datasheet",datum,x,y,"(hide yes)")}'
                   f' {" ".join(f"(pin {quote(num)} (uuid {quote(uid(ref+num))}))" for num,*_ in pins)}'
                   f' (instances (project "{NAME}" (path "/{uid("root")}" (reference "{ref}") (unit 1)))))')
    if not flag:
        parts.append((ref,value,footprint,datum))
    seen = set()
    for num,_,_,px,py,angle in pins:
        net = nets[int(num)-1]
        if not flag and net is not None:
            expected[(ref,num)] = net
        at = (x+px,y-py)
        if at in seen:
            continue
        seen.add(at)
        if net is None:
            drawing.append(f'(no_connect (at {xy(*at)}) (uuid "{uid(ref+num+"nc")}"))')
        elif stubs is None or int(num) in stubs:
            if angle == 90:
                wire(*at,at[0],at[1]+2)
                label(net,at[0],at[1]+2)
            else:
                wide_label = key in {"MAX17301","TPS259474L","Schottky"} or NAME == "rev_f_usb_power_path"
                label_x = at[0]-(12 if wide_label else 6) if angle == 0 else at[0]+3
                wire(*at,label_x,at[1])
                label(net,label_x,at[1])

cap = "Capacitor_SMD:C_0603_1608Metric"
res = "Resistor_SMD:R_0603_1608Metric"
# The FET and shunt land patterns remain deliberately unassigned pending footprint review.
note("1. Cell and protection power path",18,16,1.8)
instance("Conn2","J1","1S raw cell",23,29,["CELL_P","CELL_N"])
instance("FetCharge","Q1","CSD17308Q3",66,28,
         ["CELL_P"]*3+["CHG_GATE"]+["FET_DRAIN"]*5,stubs={1,4})
instance("FetDischarge","Q2","CSD17308Q3",86,28,
         ["PROTECTED_RAW"]*3+["DIS_GATE"]+["FET_DRAIN"]*5,stubs={1,4})
wire(71,28,81,28)
label("FET_DRAIN",71,28)
note("Q1 source faces cell. Q2 source faces protected output. Drains are common.",52,21)
instance("Conn2","J2","Rev E interface",114,29,["PROTECTED_RAW","PACK_GND"])
instance("Shunt","R1","10m 1% Kelvin draft",42,43,
         ["CELL_N","PACK_GND","CSP_K","CSN_K"])
note("R1 carries all pack return current. CSP_K and CSN_K use separate Kelvin pads.",59,44)

note("2. MAX17301G+T and local supply",18,54,1.8)
instance("MAX17301","U1","MAX17301G+T",78,75,
         ["NTC_TH","CP","BATT_F",None,"CSP_K","CSN_K","REG_1V8",
          "PROG_SDA","PROG_SCL","WAKE","PROTECTED_RAW","DIS_GATE",None,"CHG_GATE","CSP_K"],
         datum=SOURCE)
instance("R","R2","10R",31,62,["CELL_P","BATT_F"],res)
instance("C","C1","100n X7R",31,72,["BATT_F","CSP_K"],cap)
instance("C","C2","100n X7R",31,82,["CP","BATT_F"],cap)
instance("C","C3","470n X7R",31,92,["REG_1V8","CSP_K"],cap)
instance("Flag","#FLG01","PWR_FLAG",54,91,["BATT_F"])
instance("Flag","#FLG02","PWR_FLAG",62,96,["CSP_K"])
note("ZVC open selects zero-volt charge inhibit. PFAIL open in this draft.",68,91)

note("3. Wake, provisioning and cell probe",121,54,1.8)
instance("Switch","SW1","Momentary wake",139,64,["WAKE","CSP_K"])
instance("Conn3","J3","Fixture I2C",137,76,["PROG_SDA","PROG_SCL","CSP_K"])
instance("Conn2","J4","Cell NTC 10k",137,88,["NTC_TH","CSP_K"])
note("J3 pull-ups supplied by isolated fixture.",157,76)
note("J4 sensor adheres to cell pouch.",150,88)
note("Separate from charger and monitor sensors.",150,91)
note("Integration review only. Confirm cold insertion and charger fault recovery before layout.",18,110,1.6)
note("See PROGRAMMING.md for settings and OPEN_ISSUES.md for integration gates.",18,114)

OUT.mkdir(parents=True,exist_ok=True)
project = OUT/(NAME+".kicad_pro")
if not project.exists():
    project.write_text("{}\n",encoding="utf-8")
library = "\n".join(symbol(key,False) for key in symbols)
(OUT/"RevF.kicad_sym").write_text(f'(kicad_symbol_lib (version 20231120) (generator kicad_symbol_editor)\n{library}\n)\n',encoding="utf-8")
(OUT/"sym-lib-table").write_text('(sym_lib_table (version 7) (lib (name "RevF") (type "KiCad") (uri "${KIPRJMOD}/RevF.kicad_sym") (options "") (descr "Rev F draft")))\n',encoding="utf-8")
def save_schematic(title,paper="A4"):
    embedded = "\n".join(symbol(key,True) for key in symbols)
    contents = "\n".join(drawing)
    (OUT/(NAME+".kicad_sch")).write_text(f'''(kicad_sch (version 20250114) (generator eeschema)
(uuid "{uid("root")}") (paper "{paper}")
(title_block (title {quote(title)}) (rev "F draft") (company "Nate"))
(lib_symbols {embedded})
{contents}
(sheet_instances (path "/" (page "1"))))
''',encoding="utf-8")
save_schematic("Omni rover | battery protection")
with (OUT/"BOM.csv").open("w",newline="",encoding="utf-8") as file:
    rows = csv.writer(file)
    rows.writerow(["Reference","Value","Candidate MPN","Draft footprint","Datasheet"])
    candidates = {"U1":"MAX17301G+T","Q1":"CSD17308Q3","Q2":"CSD17308Q3","R1":"WSK2512R0100FEA"}
    for ref,value,footprint,datum in parts:
        rows.writerow([ref,value,candidates.get(ref,""),footprint,datum])
    rows.writerow(["External NTC","10k at 25 C, cell mounted","103AT-2","",""])
(OUT/"pin_map.csv").write_text("Reference,Pin,Net\n"+"".join(f"{ref},{pin},{net}\n" for (ref,pin),net in expected.items()),encoding="utf-8")

# A separate top-level sheet keeps the fixture design distinct from the rover board.
NAME = "rev_f_usb_power_path"
drawing.clear()
parts.clear()
expected.clear()
efuse_source = "https://www.ti.com/lit/ds/symlink/tps25947.pdf"
diode_source = "https://assets.nexperia.com/documents/data-sheet/PMEG3020ER.pdf"
symbols["TPS259474L"] = (
    "U", box(11,8),
    [pin(5,"IN","power_in",-13,6,0), pin(1,"EN/UVLO","input",-13,4,0),
     pin(2,"OVLO","input",-13,2,0), pin(9,"ILM","passive",-13,0,0),
     pin(8,"GND","power_in",-13,-2,0), pin(6,"OUT","power_out",13,6,180),
     pin(7,"DVDT","passive",13,4,180), pin(10,"ITIMER","passive",13,2,180),
     pin(4,"PGTH","input",13,0,180), pin(3,"PG","open_collector",13,-2,180)], False)
symbols["Schottky"] = (
    "D", line([(-2,0),(-1,0)]) + line([(-1,-1.2),(1,0),(-1,1.2),(-1,-1.2)]) +
    line([(1,1.25),(1,1),(1,-1),(1,-1.25)]) + line([(1,0),(2,0)]),
    [pin(2,"A","passive",-4,0,0), pin(1,"K","passive",4,0,180)], True)
symbols["Conn4"] = ("J",box(2,5),[pin(i,"~","passive",4,5-2*i,180) for i in (1,2,3,4)],True)
symbols["TPS3840PL31"] = (
    "U",box(9,4),
    [pin(2,"VDD","power_in",-11,2,0),pin(4,"MR_N","input",-11,0,0),
     pin(3,"GND","power_in",-11,-2,0),pin(1,"RESET_N","output",11,2,180),
     pin(5,"CT","passive",11,0,180)],False)
symbols["LVC1G74"] = (
    "U",box(9,5),
    [pin(8,"VCC","power_in",-11,3,0),pin(2,"D","input",-11,1,0),
     pin(1,"CLK","input",-11,-1,0),pin(4,"GND","power_in",-11,-3,0),
     pin(7,"PRE_N","input",11,3,180),pin(6,"CLR_N","input",11,1,180),
     pin(5,"Q","output",11,-1,180),pin(3,"Q_N","output",11,-3,180)],False)
for gate in ("LVC1G14","LVC1G17"):
    symbols[gate] = (
        "U",box(8,4),
        [pin(5,"VCC","power_in",-10,2,0),pin(2,"A","input",-10,0,0),
         pin(3,"GND","power_in",-10,-2,0),pin(4,"Y","output",10,2,180),
         pin(1,"NC","no_connect",10,0,180)],False)
diode_fp = "Diode_SMD:Nexperia_CFP3_SOD-123W"

note("1. Charge and logic paths",18,16,1.8)
note("USB_5V comes from the USB-C port. The existing BQ24074 and USB data path are external to this sheet.",18,20)
instance("Conn4","J10","Charger and USB",23,32,["USB_5V","CHG_BAT","CHG_OUT","PACK_GND"])
instance("Schottky","D10","PMEG3020ER",76,31,["PROTECTED_RAW","CHG_BAT"],diode_fp,diode_source)
instance("Schottky","D11","PMEG3020ER",123,31,["SYS_RAW","CHG_OUT"],diode_fp,diode_source)
instance("Schottky","D12","PMEG3020ER",164,31,["SYS_RAW","DRIVE_RAW"],diode_fp,diode_source)
note("Charge only",66,37)
note("USB logic feed",114,37)
note("Battery logic feed",155,37)

note("2. Battery discharge switch and USB inhibit",18,48,1.8)
instance("TPS259474L","U10","TPS259474LRPW",85,68,
         ["EF_EN","USB_INHIBIT",None,"PACK_GND","PROTECTED_RAW","DRIVE_RAW","EF_SLEW",
          "PACK_GND","EF_ILM","EF_TIMER"], datum=efuse_source)
instance("R","R10","25.2k 0.1%",34,56,["USB_5V","USB_INHIBIT"],res)
instance("R","R11","10k 0.1%",34,65,["USB_INHIBIT","PACK_GND"],res)
instance("R","R13","100k",34,78,["EF_EN","PACK_GND"],res)
instance("R","R14","750R 1%",130,57,["EF_ILM","PACK_GND"],res)
instance("C","C10","2.2n 25V",130,66,["EF_SLEW","PACK_GND"],cap)
instance("C","C11","1n 16V",130,75,["EF_TIMER","PACK_GND"],cap)
instance("C","C12","100n 16V",130,84,["PROTECTED_RAW","PACK_GND"],cap)
instance("C","C13","1u 16V",130,94,["DRIVE_RAW","PACK_GND"],cap)
instance("Conn4","J11","Rover loads",160,61,["SYS_RAW","DRIVE_RAW","PACK_GND","PROTECTED_RAW"])
instance("Flag","#FLG10","PWR_FLAG",61,89,["PROTECTED_RAW"])
instance("Flag","#FLG11","PWR_FLAG",61,95,["PACK_GND"])
note("EF_EN comes from the rearm latch below.",148,77)
note("Retain the separate motor-enable interlock.",148,81)
note("DRIVE_RAW requires a verified regen clamp.",148,85)

note("3. Hardware rearm after USB, undervoltage or external fault",18,109,1.8)
note("Wake the protector, then press SW10 after reset releases. A held button has no new rising edge.",18,113)
sot = "Package_TO_SOT_SMD:SOT-23-5"
instance("LVC1G14","U11","SN74LVC1G14DBVR",44,128,
         [None,"USB_5V","PACK_GND","USB_ABSENT","PROTECTED_RAW"],
         sot,"https://www.ti.com/lit/ds/symlink/sn74lvc1g14.pdf")
instance("TPS3840PL31","U12","TPS3840PL31DBVR",106,128,
         ["ARM_CLR_N","PROTECTED_RAW","PACK_GND","ARM_RESET_N","RESET_CT"],
         sot,"https://www.ti.com/lit/ds/symlink/tps3840.pdf")
instance("LVC1G74","U13","SN74LVC1G74DCUR",172,128,
         ["ARM_CLK","PROTECTED_RAW",None,"PACK_GND","EF_EN","ARM_CLR_N","PROTECTED_RAW","PROTECTED_RAW"],
         datum="https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf")
instance("R","R15","4.7k",44,141,["USB_ABSENT","ARM_RESET_N"],res)
instance("C","C14","100n X7R",106,141,["RESET_CT","PACK_GND"],cap)
instance("Conn2","J12","Open-drain fault input",165,147,["ARM_RESET_N","PACK_GND"])
note("J12 is a fault-injection port. The final hard-short detector is external.",135,155)

instance("Switch","SW10","Momentary rearm",31,166,["PROTECTED_RAW","ARM_SWITCH"])
instance("R","R16","10k",71,166,["ARM_SWITCH","ARM_FILTER"],res)
instance("LVC1G17","U14","SN74LVC1G17DBVR",126,167,
         [None,"ARM_FILTER","PACK_GND","ARM_CLK","PROTECTED_RAW"],
         sot,"https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf")
instance("R","R17","100k",71,178,["ARM_FILTER","PACK_GND"],res)
instance("C","C15","100n X7R",71,189,["ARM_FILTER","PACK_GND"],cap)
for i,x in enumerate((29,72,115,158),16):
    instance("C",f"C{i}","100n X7R",x,204,["PROTECTED_RAW","PACK_GND"],cap)
note("C16–C19 are local bypass capacitors for U11–U14 respectively.",18,211)
note("Fixture draft. Verify reset timing, held shorts, charge termination and motor transients before routing.",18,216)

project = OUT/(NAME+".kicad_pro")
if not project.exists():
    project.write_text("{}\n",encoding="utf-8")
library = "\n".join(symbol(key,False) for key in symbols)
(OUT/"RevF.kicad_sym").write_text(f'(kicad_symbol_lib (version 20231120) (generator kicad_symbol_editor)\n{library}\n)\n',encoding="utf-8")
save_schematic("Omni rover | USB and drive isolation","A3")
with (OUT/"usb_power_path_BOM.csv").open("w",newline="",encoding="utf-8") as file:
    rows = csv.writer(file)
    rows.writerow(["Reference","Value","Draft footprint","Datasheet"])
    rows.writerows(parts)
(OUT/"usb_power_path_pin_map.csv").write_text(
    "Reference,Pin,Net\n"+"".join(f"{ref},{pin},{net}\n" for (ref,pin),net in expected.items()),encoding="utf-8")
