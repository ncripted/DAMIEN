exec(open('work/rev-e/router.py').read().split('def route(')[0])
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(10,8))
for d in pads:
 if 100<d['at'][0]<136 and 117<d['at'][1]<141:
  x,y=d['geo'].exterior.xy;ax.fill(x,y,color='red' if 'F.Cu' in d['layers'] else 'blue',alpha=.35);ax.text(*d['at'],d['ref']+':'+d['num'],fontsize=5)
for t in tracks:
 if t['via'] and 100<t['a'][0]<136 and 117<t['a'][1]<141:ax.plot(*t['a'],'.k',ms=3)
ax.set(xlim=(100,136),ylim=(141,117));ax.set_aspect('equal');fig.savefig('work/rev-e/local.png',dpi=130)
