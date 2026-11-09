from pathlib import Path
import urllib.request
p=Path('work/rev-e/sources');p.mkdir(exist_ok=True)
try:
 d=urllib.request.urlopen('https://www.vishay.com/docs/30108/wsk2512.pdf',timeout=15).read();assert d[:4]==b'%PDF';(p/'wsk2512.pdf').write_bytes(d)
 import pymupdf
 doc=pymupdf.open(stream=d,filetype='pdf');doc[1].get_pixmap(matrix=pymupdf.Matrix(2.3,2.3)).save(p/'wsk2512-dimensions.png');print('Downloaded and rendered official shunt drawing')
except Exception as e:print(type(e).__name__,str(e))
