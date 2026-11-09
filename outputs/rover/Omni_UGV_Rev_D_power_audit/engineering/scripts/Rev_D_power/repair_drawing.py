from pathlib import Path
for name in ['cell_undervoltage','charge_temperature']:
 p=Path('outputs/rover/Omni_UGV_Rev_D_power_audit/'+name+'.kicad_sch');s=p.read_text().replace(' 0)) (effects',' 0) (effects');p.write_text(s)
p=Path('work/power-rev-d/drawing_cleanup.py');s=p.read_text().replace("r'\\(at ([^ ]+) ([^ ]+) ([^)]+)'","r'\\(at ([^ ]+) ([^ ]+) ([^)]+)\\)'");p.write_text(s)
