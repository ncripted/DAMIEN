from pathlib import Path
s=Path('outputs/rover/Omni_UGV_Rev_D_power_audit/cell_undervoltage.kicad_sch').read_text();i=s.index('(symbol (lib_id');print(s[i:i+2600])
