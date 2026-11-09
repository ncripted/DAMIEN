from pathlib import Path
import re,difflib
p=Path('work/humanize/board.pretty/RF_Module__ESP32-S3-WROOM-1.kicad_mod');q=Path('work/humanize/lib.pretty/RF_Module__ESP32-S3-WROOM-1.kicad_mod')
a=re.sub(r'\(uuid[^)]+\)','',p.read_text());b=re.sub(r'\(uuid[^)]+\)','',q.read_text());print(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True))))
