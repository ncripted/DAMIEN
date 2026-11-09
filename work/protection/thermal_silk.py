from pathlib import Path
import pcbnew as p,json
root=Path('outputs/rover/Omni_UGV_Rev_B_protection');pro=(root/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(root/'omni_ugv.kicad_pcb'));nets={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()}
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
for l in [p.F_Cu,p.B_Cu]:
 z=p.ZONE(b);z.SetLayer(l);z.SetNet(nets['PROT_DRAIN']);z.SetLocalClearance(p.FromMM(.2));z.SetPadConnection(p.ZONE_CONNECTION_FULL);z.SetMinThickness(p.FromMM(.2));z.SetZoneName('Protection FET drain heat spreader')
 z.Outline().NewOutline()
 for x,y in [(115.6,135.8),(122,135.8),(122,140.4),(115.6,140.4)]:z.Outline().Append(xy(x,y))
 b.Add(z)
fps={f.GetReference():f for f in b.GetFootprints()}
for ref,pt in {'U7':(120.8,123),'C24':(119,126.7),'R41':(115,134.8),'C25':(133.25,93.4),'Q8':(116.05,135.9)}.items():fps[ref].Reference().SetPosition(xy(*pt))
p.SaveBoard(str(root/'omni_ugv.kicad_pcb'),b);(root/'omni_ugv.kicad_pro').write_bytes(pro)
print('Added drain heat-spreader zones on F/B and moved colliding reference text')
