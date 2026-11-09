from pathlib import Path
import re,sys,difflib
sys.path.insert(0,str(Path('work/humanize').resolve()))
from build import blocks
a=Path('outputs/rover/Omni_UGV_Rev_B_protection/UGV.pretty/RF_Module__ESP32-S3-WROOM-1.kicad_mod')
b=Path('work/humanize/inspect.pretty/RF_Module__ESP32-S3-WROOM-1.kicad_mod')
def norm(s):
 s=re.sub(r'\(uuid[^)]+\)','',s)
 return [' '.join(t.split()) for a,b,t in blocks(s) if not t.startswith(('(property','(path','(sheet','(at ','(uuid','(net '))]
out='\n'.join(difflib.unified_diff(norm(a.read_text()),norm(b.read_text()),fromfile='library',tofile='board export'))
Path('work/humanize/footprint-diff.txt').write_text(out)
print(out[:14000])

