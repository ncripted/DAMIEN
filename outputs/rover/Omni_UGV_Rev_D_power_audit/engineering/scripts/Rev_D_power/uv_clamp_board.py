import pcbnew as p
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');fn=r/'omni_ugv.kicad_pcb';pro=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(fn));next(f for f in b.GetFootprints() if f.GetReference()=='R52').SetValue('3.3k');p.SaveBoard(str(fn),b);(r/'omni_ugv.kicad_pro').write_bytes(pro)
