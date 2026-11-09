exec(open('work/rev-e/router.py').read().split('def route(')[0])
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(8,8))
colors={'PROTECTED_RAW':'orange','VBAT':'red','PROT_DRAIN':'purple','PROT_DSG':'cyan','PROT_CHG':'green'}
for d in pads:
 if 'B.Cu' in d['layers'] and 110<d['at'][0]<120 and 132<d['at'][1]<142:
  x,y=d['geo'].exterior.xy;ax.fill(x,y,color=colors.get(d['net'],'gray'),alpha=.5);ax.text(*d['at'],d['ref']+':'+d['num'],fontsize=6)
for t in tracks:
 if (t['layer']=='B.Cu' or t['via']) and t['geo'].intersects(box(110,132,120,142)):
  x,y=t['geo'].exterior.xy;ax.fill(x,y,color=colors.get(t['net'],'gray'),alpha=.6)
ax.set(xlim=(110,120),ylim=(142,132));ax.set_aspect('equal');fig.savefig('work/rev-e/gate-fanout.png',dpi=130)
