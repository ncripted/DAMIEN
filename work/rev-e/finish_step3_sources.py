from pathlib import Path
import re,json,csv
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');dm={d['ref']:d for d in json.loads((r/'design_connections.json').read_text())};s=Path('work/rev-e/step3_schematic.py').read_text();exec(s[s.index("fp=Path('C:/Program"):])
