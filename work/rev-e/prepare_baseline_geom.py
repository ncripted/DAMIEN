from pathlib import Path
s=Path('work/rev-e/export_geometry.py').read_text().replace("Path('outputs/rover/Omni_UGV_Rev_E_power_layout')","Path('outputs/rover/Omni_UGV_Rev_D_power_audit')").replace("Path('work/rev-e/geometry.json')","Path('work/rev-e/baseline_geometry.json')");Path('work/rev-e/export_baseline_geometry.py').write_text(s)
