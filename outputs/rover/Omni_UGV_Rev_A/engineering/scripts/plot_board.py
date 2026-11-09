import json,sys
from pathlib import Path
import pcbnew as p
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle
root=Path('outputs/rover/Omni_UGV_Rev_A'); b=p.LoadBoard(str(root/'omni_ugv.kicad_pcb'))
fig,ax=plt.subplots(figsize=(12,10))
layers={p.F_Cu:'#c62e2e',p.B_Cu:'#2359c9',p.In1_Cu:'#b47018',p.In2_Cu:'#27933b'}
for t in b.GetTracks():
 x,y=p.ToMM(t.GetStart().x),p.ToMM(t.GetStart().y)
 if not(90<x<106 and 107<y<123):continue
 if type(t)==p.PCB_VIA:
  ax.add_patch(Circle((x,y),p.ToMM(t.GetWidth(p.F_Cu))/2,fill=False,color='black'));continue
 ex,ey=p.ToMM(t.GetEnd().x),p.ToMM(t.GetEnd().y)
 ax.plot([x,ex],[y,ey],color=layers.get(t.GetLayer(),'gray'),lw=max(.4,p.ToMM(t.GetWidth())*2),alpha=.65)
for f in b.GetFootprints():
 x,y=p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y)
 if not(90<x<106 and 107<y<123):continue
 ax.text(x,y-.8,f.GetReference(),fontsize=9,color='black')
 for q in f.Pads():
  x,y=p.ToMM(q.GetPosition().x),p.ToMM(q.GetPosition().y)
  w,h=p.ToMM(q.GetSize().x),p.ToMM(q.GetSize().y)
  if abs(f.GetOrientationDegrees())%180==90:w,h=h,w
  ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,facecolor='#e4be5c',edgecolor='black',lw=.5))
  ax.text(x,y,q.GetNumber(),fontsize=6,ha='center',va='center')
ax.set(xlim=(90,106),ylim=(123,107),xlabel='PCB X / mm',ylabel='PCB Y / mm',title='Regulator routing review — red front, blue back, green In2')
ax.set_aspect('equal'); ax.grid(alpha=.2);fig.tight_layout();fig.savefig(root/'preview/regulator-review.png',dpi=160)
