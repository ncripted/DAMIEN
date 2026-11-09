from pathlib import Path
import urllib.request
for fn,url in [('tdk-c2012x5r1a226k125ab.pdf','https://product.tdk.com/system/files/dam/doc/product/capacitor/ceramic/mlcc/charasheet/c2012x5r1a226k125ab.pdf'),('dmp2008ufg.pdf','https://www.diodes.com/datasheet/download/DMP2008UFG.pdf')]:
 try:urllib.request.urlretrieve(url,Path('work/rev-e/sources')/fn);print(fn)
 except Exception as e:print(type(e).__name__,str(e))
