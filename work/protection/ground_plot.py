import sys,json
from pathlib import Path
sys.path.insert(0,str(Path('work/protection/deps').resolve()))
from shapely.geometry import Polygon,Point
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch
d=json.loads(Path('work/protection/ground-fill.json').read_text());fig,ax=plt.subplots(figsize=(9,7))
for i,v in enumerate(d):
 p=Polygon(v['outline'],v['holes']);col=plt.get_cmap('tab20')(i%20)
 ax.add_patch(Patch(v['outline'],fc=col,ec='none',alpha=.7))
 for h in v['holes']:ax.add_patch(Patch(h,fc='white',ec='none'))
 for label,pt in [('new',(109.8,127.8)),('old',(110.8,124))]:
  if p.covers(Point(pt)):print(label,'island',i,'area',p.area)
ax.scatter([109.8,110.8],[127.8,124],c='red');ax.set_xlim(104,123);ax.set_ylim(135,118);ax.set_aspect('equal');ax.grid(alpha=.2);fig.savefig('work/protection/ground.png',dpi=150)
