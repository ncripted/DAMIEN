from pathlib import Path
import shutil
source=Path("work/rev-f-startup/place_integrated_rover.py").read_text()
start=source.index("# Delete the original power nets")
end=source.index("def net(name)")
source=source[:start]+'''
refs={"U16","U17","U18","U19","C44","C45","C46","C47","C48","C49","R75","R76","R77","J8"}
original=out
out=rover/"Omni_UGV_Rev_F_left_candidate"
out.mkdir(exist_ok=True)
for file in original.iterdir():
    if file.suffix in {".kicad_pcb",".kicad_sch",".kicad_pro",".kicad_dru",".kicad_sym"} or file.name.endswith("lib-table"):
        shutil.copy2(file,out/file.name)
shutil.copytree(original/"UGV.pretty",out/"UGV.pretty",dirs_exist_ok=True)
b=pcb.LoadBoard(str(out/name))
old=[f for f in b.GetFootprints() if f.GetReference() in refs]
assert len(old)==len(refs)
for f in old:
    b.Remove(f)
removed_tracks={}
removed_footprints=[]
''' + source[end:]
start=source.index("placement = {")
end=source.index("placed = []",start)
source=source[:start]+'''
placement={
    "U18":(65,109,pcb.F_Cu), "J8":(63,104,pcb.F_Cu),
    "U16":(72,99,pcb.F_Cu), "U17":(77,99,pcb.F_Cu),
    "U19":(70,106,pcb.F_Cu),
    "C44":(77,96,pcb.F_Cu), "C45":(70,109,pcb.F_Cu),
    "C46":(72,96,pcb.F_Cu), "C47":(80,99,pcb.F_Cu),
    "C48":(77,109,pcb.F_Cu), "C49":(68,106,pcb.F_Cu),
    "R75":(66,110,pcb.F_Cu), "R76":(69,103,pcb.F_Cu), "R77":(66,107,pcb.F_Cu),
}
''' + source[end:]
import pcbnew
exec(source.replace('radius = 24 if ref in {"J7","D11","U17","C47","U15"} else 14', 'radius = 30'))


