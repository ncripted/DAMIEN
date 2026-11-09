from pathlib import Path
import pymupdf
r=Path('outputs/rover/Omni_UGV_Rev_B_protection');o=r/'preview/schematics';o.mkdir(exist_ok=True)
d=pymupdf.open(r/'Schematic.pdf')
for i,p in enumerate(d):
 p.get_pixmap(matrix=pymupdf.Matrix(1.2,1.2)).save(o/f'sheet-{i+1}.png')
# Dense inspection crops: PDF points from millimetres.
for name,i,box in [('controller',1,(20,35,180,115)),('regulator',2,(20,40,325,175)),('drivers',3,(25,35,190,245)),('interlock',4,(120,40,380,250)),('usb-charge',5,(20,30,300,250)),('protection',6,(20,30,375,250))]:
 rect=pymupdf.Rect(*(v*72/25.4 for v in box));d[i].get_pixmap(matrix=pymupdf.Matrix(2,2),clip=rect).save(o/f'detail-{name}.png')
