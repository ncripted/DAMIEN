import math,itertools,json
from pathlib import Path
# Numerical corner calculation includes both comparator input branches, input bias, LDO,
# all divider resistor tolerances and thermistor R25/B tolerance. Beta-model approximation.
def calc(ah=200e3,bh=100e3,ac=442e3,bc=100e3):
 out={}
 for mode in ['hot','cold']:
  vv=[]
  for s in itertools.product([-1,1],repeat=11):
   vs=3.3*(1+s[0]*.015);rt=1e4*(1+s[1]*.015)
   a,b,c,d=[v*(1+e*.015) for v,e in zip([ah,bh,ac,bc],s[2:6])]
   ih=s[6]*25e-9;ic=s[7]*15e-9
   th=([.387,.400] if mode=='hot' else [.396,.404])[s[8]>0]
   vt=th*(1+(a/b if mode=='hot' else c/d))+(ih*a if mode=='hot' else ic*c)
   # KCL at probe node: (Vs-Vt)/Rt=Vt/Rntc+Vt/(a+b)+Vt/(c+d)+bias loads
   inv=((vs-vt)/rt-vt/(a+b)-vt/(c+d)-ih*b/(a+b)-ic*d/(c+d))/vt
   rn=1/inv;r25=1e4*(1+s[9]*.01);beta=3435*(1+s[10]*.01)
   temp=1/(1/298.15+math.log(rn/r25)/beta)-273.15
   vv.append(temp)
  out[mode]=[min(vv),max(vv)]
 return out
print(calc())
Path('work/power-rev-d/temperature-corners.json').write_text(json.dumps(calc(),indent=2))

