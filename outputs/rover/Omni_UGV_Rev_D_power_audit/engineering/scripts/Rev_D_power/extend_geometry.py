from pathlib import Path
s=Path('work/power-rev-d/export_geometry.py').read_text();s=s.replace("'side':f.GetLayerName()}","'side':f.GetLayerName(),'courtyard':[[line(f.GetCourtyard(l).COutline(i)) for i in range(f.GetCourtyard(l).OutlineCount())] for l in [p.F_Cu,p.B_Cu]]}")
Path('work/power-rev-d/export_geometry.py').write_text(s)
