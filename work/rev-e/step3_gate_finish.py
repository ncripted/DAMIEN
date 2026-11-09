"""Conservative geometry-assisted routing; KiCad DRC remains the final clearance check."""
import sys,json,math,heapq,time
from pathlib import Path
sys.path.insert(0,str(Path('work/protection/deps').resolve()))
import numpy as np
from shapely.geometry import Polygon,Point,LineString,box
from shapely import affinity,unary_union,contains_xy
g=json.loads(Path('work/rev-e/geometry.json').read_text());tracks=g['tracks'];pads=g['pads'];out=[]
board=unary_union([Polygon(o,h) for o,h in g['outline']]).difference(box(87,40.25,135,61.25));layers=['B.Cu','F.Cu','In2.Cu'];alllayers=layers+['In1.Cu']
def ps(d):
 w,h=d['size'];x,y=d['at']
 if d['shape']==0:return Point(x,y).buffer(w/2)
 return affinity.translate(affinity.rotate(box(-w/2,-h/2,w/2,h/2),-d['angle']),x,y)
def ts(t):return (Point(t['a']) if t['via'] or t['a']==t['z'] else LineString([t['a'],t['z']])).buffer(t['width']/2)
for d in pads:d['geo']=ps(d)
for t in tracks:t['geo']=ts(t)
def pad(ref,num):return next(p for p in pads if p['ref']==ref and p['num']==str(num))
def endpoint(ref,num,layer=None):
 d=pad(ref,num);return (*d['at'],layer or ('B.Cu' if 'B.Cu' in d['layers'] else 'F.Cu'))
def addtrack(net,a,z,width,layer):
 if math.dist(a,z)<1e-7:return
 t=dict(net=net,a=list(a),z=list(z),width=width,via=False,drill=0,layer=layer);out.append(t);t['geo']=ts(t);tracks.append(t)
def addvia(net,pt):
 if any(t['via'] and t['net']==net and math.dist(t['a'],pt)<.01 for t in tracks):return
 t=dict(net=net,a=list(pt),z=list(pt),width=.6,via=True,drill=.3,layer='F.Cu');out.append(t);t['geo']=ts(t);tracks.append(t)
def obs(net,layer,r,region,via=False):
 shapes=[]
 for d in pads:
  if d['net']!=net and (via or layer in d['layers']) and d['geo'].intersects(region):shapes.append(d['geo'].buffer(r+.18))
  if max(d['drill']) and d['geo'].intersects(region):
   # Same-net PTH copper may be joined by traces; via holes may not overlap existing holes.
   if via or d['net']!=net:shapes.append(Point(d['at']).buffer(max(d['drill'])/2+(.25+.15 if via else .27+r)))
 for t in tracks:
  if (via or t['via'] or t['layer']==layer) and t['geo'].intersects(region):
   if t['net']!=net:shapes.append(t['geo'].buffer(r+.18))
   if via and t['via']:shapes.append(Point(t['a']).buffer(.3+.25))
 return unary_union(shapes)
def route(net,start,end,width=.2,allow_via=True,margin=8):
 print('Route',net,start,end,width,flush=True)
 st=time.time();res=.05
 x0=math.floor((min(start[0],end[0])-margin)/res)*res;y0=math.floor((min(start[1],end[1])-margin)/res)*res
 x1=max(start[0],end[0])+margin;y1=max(start[1],end[1])+margin
 xx=np.arange(x0,x1+res,res);yy=np.arange(y0,y1+res,res);X,Y=np.meshgrid(xx,yy);ny,nx=X.shape;region=box(x0,y0,x1,y1)
 ls=layers if allow_via else [start[2]]
 free=[];geos=[]
 for l in ls:
  o=obs(net,l,width/2,region);geos.append(o);free.append(contains_xy(board.buffer(-.33-width/2),X,Y)&~contains_xy(o,X,Y))
 free=np.array(free)
 vf=None
 if allow_via:
  vo=obs(net,'',.3,region,True);vf=contains_xy(board.buffer(-.65),X,Y)&~contains_xy(vo,X,Y)
  for t in tracks:
   if t['via'] and t['net']==net:
    ix=round((t['a'][0]-x0)/res);iy=round((t['a'][1]-y0)/res)
    if 0<=ix<nx and 0<=iy<ny:vf[iy,ix]=True
 def idx(pt):return (ls.index(pt[2]),round((pt[1]-y0)/res),round((pt[0]-x0)/res))
 def coord(n):return (float(xx[n[2]]),float(yy[n[1]]))
 a=idx(start);z=idx(end)
 # Exact pad centers can have narrow valid escape channels; don't override obstacle masks.
 for n,pt in [(a,start),(z,end)]:
  if not free[n]:raise RuntimeError('Blocked endpoint '+str((net,pt)))
 def heur(n):return math.hypot(n[1]-z[1],n[2]-z[2])+(0 if n[0]==z[0] else 12)
 heap=[(heur(a),0,a)];cost={a:0};parent={};directions=[(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(1,1,1.4142),(1,-1,1.4142),(-1,1,1.4142),(-1,-1,1.4142)];found=False
 while heap:
  _,c,n=heapq.heappop(heap)
  if c>cost[n]+1e-9:continue
  if n==z:found=True;break
  l,iy,ix=n
  cand=[]
  for dy,dx,dc in directions:
   j,k=iy+dy,ix+dx
   if 0<=j<ny and 0<=k<nx and free[l,j,k] and (not dx or not dy or (free[l,iy,k] and free[l,j,ix])):cand.append(((l,j,k),dc))
  if allow_via and vf[iy,ix]:
   for ll in range(len(ls)):
    if ll!=l and free[ll,iy,ix]:cand.append(((ll,iy,ix),22))
  for m,dc in cand:
   nc=c+dc
   if nc<cost.get(m,float('inf')):
    cost[m]=nc;parent[m]=n;heapq.heappush(heap,(nc+heur(m)*1.02,nc,m))
  if len(cost)>1200000:break
 if not found:
  import matplotlib;matplotlib.use('Agg')
  import matplotlib.pyplot as plt
  fig,ax=plt.subplots(figsize=(10,7));ax.imshow(free[0],extent=[xx[0],xx[-1],yy[-1],yy[0]],interpolation='nearest',cmap='gray');ax.scatter([start[0],end[0]],[start[1],end[1]],c='red');ax.set_xlim(start[0]-3,start[0]+3);ax.set_ylim(start[1]+3,start[1]-3)
  for d in pads:
   if math.dist(d['at'],start[:2])<4:ax.text(*d['at'],d['ref']+'.'+d['num'],fontsize=8,color='orange')
  fig.savefig('work/protection/route-failure.png');plt.close(fig)
  raise RuntimeError('No route '+str((net,start,end,width,len(cost))))
 path=[z]
 while path[-1]!=a:path.append(parent[path[-1]])
 path.reverse();addtrack(net,start[:2],coord(a),width,ls[a[0]])
 # Merge collinear grid steps, preserving layer transitions.
 prev=path[0];corner=prev;lastdir=None
 for n in path[1:]:
  if n[0]!=prev[0]:
   addtrack(net,coord(corner),coord(prev),width,ls[prev[0]]);addvia(net,coord(n));corner=n;lastdir=None
  else:
   dr=(n[1]-prev[1],n[2]-prev[2])
   if lastdir is not None and dr!=lastdir:addtrack(net,coord(corner),coord(prev),width,ls[prev[0]]);corner=prev
   lastdir=dr
  prev=n
 addtrack(net,coord(corner),coord(prev),width,ls[prev[0]]);addtrack(net,coord(z),end[:2],width,ls[z[0]])
 print('  done',round(time.time()-st,2),'s',len(cost),'nodes',flush=True)
def rr(net,r1,p1,r2,p2,w=.2,via=True):route(net,endpoint(r1,p1),endpoint(r2,p2),w,via)
def save():Path('work/rev-e/routes.json').write_text(json.dumps([{k:v for k,v in t.items() if k!='geo'} for t in out],indent=2))


esc={}
for pin,net in [(8,'PROT_CHG'),(6,'PROT_PACK'),(7,'PROT_DSG')]:
 d=pad('U7',pin);px,py=d['at'];region=box(px-5,py-5,px+5,py+5);vo=obs(net,'',.3,region,True);attempt=0
 for pt in sorted([(round(px+dx*.1,3),round(py+dy*.1,3)) for dx in range(-40,41) for dy in range(-40,41)],key=lambda pt:math.dist(pt,(px,py))):
  if Point(pt).intersects(vo) or Point(pt).distance(d['geo'])<.4:continue
  attempt+=1
  try:route(net,endpoint('U7',pin,'B.Cu'),(*pt,'B.Cu'),.15,False,5)
  except Exception as e:
   print('Escape candidate failed',pin,str(e),flush=True)
   if attempt>=15:raise
   continue
  addvia(net,pt);esc[net]=pt;print('Reserved',net,pt,flush=True);break
 else:raise RuntimeError('No escape '+net)
 save()
for net,ref,pin in [('PROT_DSG','Q8',4),('PROT_CHG','Q7',4),('PROT_PACK','R39',2)]:
 route(net,(*esc[net],'In2.Cu'),endpoint(ref,pin,'B.Cu'),.15,True,12);save()
rr('PROT_DSG','R41',2,'Q8',4,.15,True);save()
rr('PROT_CHG','R40',1,'Q7',4,.15,True);save()
rr('CELL_N','U7',5,'R36',1,.15,True);save()



