from pathlib import Path
import urllib.request, json
root=Path('work/power-rev-d/sources');url='https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf'
try:
 d=urllib.request.urlopen(url,timeout=15).read();assert d[:4]==b'%PDF';(root/'sn74lvc1g17.pdf').write_bytes(d);print('Saved official drive-buffer datasheet')
except Exception as e:print(type(e).__name__,str(e))
