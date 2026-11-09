from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Polygon,Rectangle
import numpy as np
r=Path('outputs/rover/Omni_UGV_Rev_A')
fig,ax=plt.subplots(figsize=(9,9))
ax.add_patch(Circle((0,0),50,fill=False,color='#287960',lw=2,label='100 mm nominal PCB boundary'))
R=60.;w=10.
for i,theta in enumerate([0,120,240]):
 a=np.deg2rad(theta);e=np.array([np.cos(a),np.sin(a)]);t=np.array([-np.sin(a),np.cos(a)])
 corners=[R*e+sx*w/2*e+sy*19*t for sx,sy in [(-1,-1),(1,-1),(1,1),(-1,1)]]
 ax.add_patch(Polygon(corners,color='#777777',alpha=.6))
 ax.plot([22*e[0],50*e[0]],[22*e[1],50*e[1]],color='#8b6d32',lw=6,alpha=.6)
 for sign in [-1,1]:
  h=34*e+sign*10*t;ax.plot(*h,'o',color='#2862aa')
 ax.plot(*(22*e),'s',color='#bd3e31');ax.text(*(37*e),f'M{i+1}',ha='center',va='center')
 ax.arrow(*(R*e),*(10*t),width=.3,color='#c43e31',length_includes_head=True)
ax.add_patch(Circle((0,0),np.hypot(R+w/2,19),fill=False,ls='--',color='#aa4848',label='Example circumscribed envelope: 135.4 mm'))
ax.set(xlim=(-78,78),ylim=(-78,78),xlabel='Robot X (PCB X − 100) / mm',ylabel='Robot Y (100 − PCB Y) / mm',title='PROVISIONAL wheel envelope and actual motor/clamp datums\nWheel midplane R=60 mm and axial width=10 mm are assumptions')
ax.set_aspect('equal');ax.grid(alpha=.2);ax.legend(loc='lower center',fontsize=8)
fig.tight_layout();fig.savefig(r/'preview/mechanical-envelope-provisional.png',dpi=150)
