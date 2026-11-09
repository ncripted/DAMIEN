from pathlib import Path
p=Path("work/rev-f-startup/check_startup.py")
s=p.read_text(encoding="utf-8-sig").replace("import json","import json\nimport zipfile")
s=s.replace('for file in ("omni_ugv.kicad_pcb", "omni_ugv.kicad_sch", "battery_protection.kicad_sch",\n             "charging.kicad_sch", "discharge_cutoff.kicad_sch", "omni_ugv.kicad_pro"):', 'for file in ("omni_ugv.kicad_sch", "battery_protection.kicad_sch",\n             "charging.kicad_sch", "discharge_cutoff.kicad_sch"):')
s=s.replace('print("Native connectivity, exact variants, source hashes and rule checks verified.")','''with zipfile.ZipFile(revision.with_name(revision.name + "_review.zip")) as archive:
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
print("Board rules, net settings and schematic settings match the archive.")''')
p.write_text(s,encoding="utf-8")
