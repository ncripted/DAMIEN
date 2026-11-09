"""Conservative geometry-assisted routing; KiCad DRC remains the final clearance check."""
import sys,json,math,heapq,time
from pathlib import Path
sys.path.insert(0,str(Path('work/protection/deps').resolve()))
import numpy as np
from shapely.geometry import Polygon,Point,LineString,box
from shapely import affinity,unary_union,contains_xy
g=json.loads(Path('work/protection/geometry.json').read_text());tracks=g['tracks'];pads=g['pads'];out=[]
board=unary_union([Polygon(o,h) for o,h in g['outline']]);layers=['B.Cu','F.Cu','In2.Cu'];alllayers=layers+['In1.Cu']
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
 st=time.time();res=.1
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
def save():Path('work/protection/routes.json').write_text(json.dumps([{k:v for k,v in t.items() if k!='geo'} for t in out],indent=2))
try:
 if '--signals' not in sys.argv:
  # Power source pins share a wide bus; each lead has its own short neck.
  for ref,net in [('Q7','CELL_P'),('Q8','VBAT')]:
   pp=[pad(ref,i) for i in [1,2,3]];x=pp[0]['at'][0]+(.85 if ref=='Q7' else -.85);ys=[p['at'][1] for p in pp]
   for d in pp:addtrack(net,d['at'],(x,d['at'][1]),.45,'B.Cu')
   addtrack(net,(x,min(ys)),(x,max(ys)),.6,'B.Cu')
  # Drain lands face each other, with no gate or source copper in this bridge.
  rr('PROT_DRAIN','Q7',9,'Q8',9,1.6,False)
  rr('CELL_N','J2',2,'R36',1,1.2,False)
  route('CELL_P',endpoint('J2',1),(pad('Q7',2)['at'][0]+.85,pad('Q7',2)['at'][1],'B.Cu'),1.2,False)
 if '--initial' in sys.argv:
  save();sys.exit(0)
 # Reserve radial escapes before long paths can surround adjacent fine-pitch pins.
 fanouts={1:(117.2,124.0),2:(117.1,123.0),3:(117.1,122.0),5:(121.0,121.8),6:(121.8,122.9),7:(121.6,123.7),8:(119.0,124.5)}
 for pin in [2,6,1,7,3,5,8]:
  d=pad('U7',pin);net=d['net'];tx,ty=fanouts[pin];o=obs(net,'',.3,box(tx-2,ty-2,tx+2,ty+2),True)
  candidates=sorted([(tx+dx*.1,ty+dy*.1) for dx in range(-8,9) for dy in range(-8,9)],key=lambda p:(p[0]-tx)**2+(p[1]-ty)**2)
  dest=next((pt for pt in candidates if not o.intersects(Point(pt))),None)
  if dest is None:raise RuntimeError('No fanout via for U7.'+str(pin))
  route(net,endpoint('U7',pin),(*dest,'B.Cu'),.15,False,3);addvia(net,dest)
 # Kelvin traces, kept on the back copper until the sense-resistor pads.
 rr('GND','U7',4,'R36',2,.15,False)
 # Protection and analogue low-current nets.
 for net in ['PROT_CHG','PROT_DSG','PROT_VDD','PROT_BAT','PROT_PACK','CELL_TEMP_DIV','CELL_TEMP_ADC','LED_STATUS']:
  pts=[d for d in pads if d['net']==net and d['num']]
  connected=[pts.pop(0)]
  while pts:
   a,z=min(((a,z) for a in connected for z in pts),key=lambda pair:math.dist(pair[0]['at'],pair[1]['at']))
   rr(net,a['ref'],a['num'],z['ref'],z['num'],.15 if a['ref']=='U7' or z['ref']=='U7' else .2)
   connected.append(z);pts.remove(z)
 rr('CELL_N','U7',3,'R36',1,.15,True);rr('CELL_N','U7',5,'R36',1,.15,True)
 # Remaining raw-cell references join the shunt at its cell side.
 rr('CELL_N','C24',2,'R36',1)
 for ref,pin in [('R37',1),('R38',1),('R40',2)]:rr('CELL_P',ref,pin,'J2',1)
 rr('VBAT','R39',1,'R41',2);rr('VBAT','R41',2,'Q8',2)
 rr('+3V3','R42',1,'R4',1)
 # C25 ground ties to existing grounded through-hole J5 pin2.
 rr('GND','C25',2,'J5',2)
except Exception as e:
 save();print('ROUTING STOP:',e,flush=True);raise
save()
