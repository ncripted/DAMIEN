from pathlib import Path
import urllib.request,json
root=Path('work/power-rev-d/sources');urls=json.loads((root/'urls.json').read_text())
urls.update(sn74lvc1g14='https://www.ti.com/lit/ds/symlink/sn74lvc1g14.pdf',dmp2035u='https://www.diodes.com/datasheet/download/DMP2035U.pdf')
for name in ['sn74lvc1g14','dmp2035u']:
 try:
  data=urllib.request.urlopen(urls[name],timeout=25).read();assert data[:4]==b'%PDF';(root/(name+'.pdf')).write_bytes(data)
  import fitz
  doc=fitz.open(stream=data,filetype='pdf');(root/(name+'.txt')).write_text('\n'.join(p.get_text() for p in doc),encoding='utf-8');print(name,len(data))
 except Exception as e:print(name,type(e).__name__,str(e))
(root/'urls.json').write_text(json.dumps(urls,indent=2))
