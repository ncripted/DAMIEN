from pathlib import Path
import pymupdf
from PIL import Image,ImageDraw
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');doc=pymupdf.open(r/'preview/layers/copper-layers.pdf');atlas=Image.new('RGB',(1600,1700),'white');draw=ImageDraw.Draw(atlas)
for i,(page,name) in enumerate(zip(doc,['F.Cu','In1.Cu — primary GND','In2.Cu','B.Cu'])):
 pix=page.get_pixmap(matrix=pymupdf.Matrix(2.6,2.6),clip=pymupdf.Rect(135,135,435,435));img=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);x=(i%2)*800;y=(i//2)*850;atlas.paste(img,(x,y+40));draw.text((x+20,y+10),name,fill='black');pix.save(r/f'preview/layers/copper-{i+1}.png')
atlas.save(r/'preview/copper-layer-overview.png')
