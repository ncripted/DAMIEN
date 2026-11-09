from pathlib import Path
import difflib,re
p=Path('outputs/rover/Omni_UGV_Rev_B_protection/UGV.pretty/RF_Module__ESP32-S3-WROOM-1.kicad_mod');q=Path('work/humanize/inspect.pretty/RF_Module__ESP32-S3-WROOM-1.kicad_mod')
a=re.sub(r'\(uuid[^)]+\)','',p.read_text());b=re.sub(r'\(uuid[^)]+\)','',q.read_text());print(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True))))
