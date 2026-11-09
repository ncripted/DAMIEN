import pcbnew as p,json
from pathlib import Path
b=p.LoadBoard('work/rev-e/pre-leaf-prune.kicad_pcb');out=[]
for t in b.GetTracks():
 if t.GetNetname()!='PROT_DSG':continue
 via=isinstance(t,p.PCB_VIA);v=lambda a:[p.ToMM(a.x),p.ToMM(a.y)];out.append(dict(net='PROT_DSG',a=v(t.GetStart()),z=v(t.GetEnd()),width=p.ToMM(t.GetWidth(p.F_Cu) if via else t.GetWidth()),via=via,drill=p.ToMM(t.GetDrill()) if via else 0,layer=t.GetLayerName()))
Path('work/rev-e/restore-dsg-routes.json').write_text(json.dumps(out));print(len(out),'gate copper objects recovered')
