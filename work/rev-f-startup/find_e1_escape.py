exec(open('work/rev-e/router.py').read().split('removed=[]')[0])
from collections import deque
raw='PROTECTED_RAW'
ids={'2187a600-0b00-458c-bf8c-aea0675c044a','16b9183a-32ab-48a7-88be-f34b132c3188'}
assert ids <= {t['uuid'] for t in tracks}
tracks[:]=[t for t in tracks if t['uuid'] not in ids]
for ref,origin,branches in [
    ('Q8',(114.9,138.8),[('B.Cu',.65),('In2.Cu',.65),('F.Cu',.15)]),
    ('Q13',(129.5,134.5),[('B.Cu',.65),('In2.Cu',.75)]),
]:
 x,y=origin; reg=box(x-7,y-7,x+7,y+7)
 step=.1
 vals=np.arange(-55,56)*step
 X,Y=np.meshgrid(vals+x,vals+y)
 pad_block=unary_union([d['geo'].buffer(.37) for d in pads if d['geo'].intersects(reg) and d['layers']])
 candidates=contains_xy(board.buffer(-.65),X,Y)&~contains_xy(obs(raw,'',.3,reg,True),X,Y)&~contains_xy(pad_block,X,Y)
 for layer,width in branches:
    free=~contains_xy(obs(raw,layer,width/2,reg),X,Y)&contains_xy(board.buffer(-.33-width/2),X,Y)
    origin_index=(55,55)
    if not free[origin_index]:
        print(ref,layer,'endpoint blocks');free[origin_index]=True
    visited=np.zeros_like(free);visited[origin_index]=True;todo=deque([origin_index])
    while todo:
        i,j=todo.popleft()
        for a,z in ((i+1,j),(i-1,j),(i,j+1),(i,j-1)):
            if 0<=a<len(vals) and 0<=z<len(vals) and free[a,z] and not visited[a,z]:
                visited[a,z]=True;todo.append((a,z))
    candidates &= visited
 opts=sorted([(math.dist(origin,(X[i,j],Y[i,j])),round(X[i,j],2),round(Y[i,j],2)) for i,j in zip(*np.nonzero(candidates))])
 print(ref,opts[:10])
 if not opts: raise RuntimeError(ref)
 _,vx,vy=opts[0]
 addvia(raw,(vx,vy))
 for layer,width in branches:
    route(raw,(*origin,layer),(vx,vy,layer),width,False,margin=6)
Path('work/rev-f-startup/e1-routes.json').write_text(json.dumps([{k:v for k,v in t.items() if k!='geo'} for t in out],indent=2))
