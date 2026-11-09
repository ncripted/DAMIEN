import pcbnew as p,json,sys
from pathlib import Path
root=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');fn=root/'omni_ugv.kicad_pcb';pro=(root/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(fn));nets={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()}
def xy(v):return p.VECTOR2I(p.FromMM(v[0]),p.FromMM(v[1]))
ls={b.GetLayerName(i):i for i in [p.F_Cu,p.B_Cu,p.In1_Cu,p.In2_Cu]}
routes=json.loads(Path(sys.argv[1] if len(sys.argv)>1 else 'work/power-rev-d/routes.json').read_text())
for t in routes:
 if t['via']:
  o=p.PCB_VIA(b);o.SetPosition(xy(t['a']));o.SetViaType(p.VIATYPE_THROUGH);o.SetLayerPair(p.F_Cu,p.B_Cu);o.SetWidth(p.FromMM(t['width']));o.SetDrill(p.FromMM(t['drill']))
 else:
  o=p.PCB_TRACK(b);o.SetStart(xy(t['a']));o.SetEnd(xy(t['z']));o.SetWidth(p.FromMM(t['width']));o.SetLayer(ls[t['layer']])
 o.SetNet(nets[t['net']]);b.Add(o)
p.SaveBoard(str(fn),b);(root/'omni_ugv.kicad_pro').write_bytes(pro)
print('Applied',len(routes),'new copper objects')
