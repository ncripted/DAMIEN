import os,json,collections,xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew as p
root=Path('outputs/rover/Omni_UGV_Rev_B_protection')
b=p.LoadBoard(str(root/'omni_ugv.kicad_pcb'))
fps={f.GetReference():f for f in b.GetFootprints()}
def xy(v): return [round(p.ToMM(v.x),5),round(p.ToMM(v.y),5)]
report={'footprints':{},'tracks_by_net':{},'primary_plane_tracks':[]}
for ref,f in fps.items():
 report['footprints'][ref]={'value':f.GetValue(),'at':xy(f.GetPosition()),'angle':f.GetOrientationDegrees(),'pads':[{'number':q.GetNumber(),'net':q.GetNetname(),'at':xy(q.GetPosition()),'size':xy(q.GetSize()),'drill':xy(q.GetDrillSize())} for q in f.Pads()]}
for net in sorted(set(t.GetNetname() for t in b.GetTracks())):
 ts=[t for t in b.GetTracks() if t.GetNetname()==net and type(t)==p.PCB_TRACK]
 report['tracks_by_net'][net]={'length_mm':sum(p.ToMM(t.GetLength()) for t in ts),'min_width_mm':min([p.ToMM(t.GetWidth()) for t in ts],default=0),'layers':dict(collections.Counter(t.GetLayerName() for t in ts))}
for t in b.GetTracks():
 if t.GetLayer()==p.In1_Cu: report['primary_plane_tracks'].append({'uuid':t.m_Uuid.AsString(),'net':t.GetNetname(),'start':xy(t.GetStart()),'end':xy(t.GetEnd()),'width':p.ToMM(t.GetWidth())})
x=ET.parse(root/'schematic.net.xml')
expected={(n.attrib['ref'],n.attrib['pin']):net.attrib['name'] for net in x.findall('.//nets/net') for n in net.findall('node') if not net.attrib['name'].startswith('unconnected-')}
actual={(r,q.GetNumber()):q.GetNetname() for r,f in fps.items() for q in f.Pads() if q.GetNetname() and not q.GetNetname().startswith('unconnected-')}
report['parity']={'expected_pins':len(expected),'mismatches':[{'ref':k[0],'pin':k[1],'expected':v,'actual':actual.get(k)} for k,v in expected.items() if actual.get(k)!=v],'extras':[k for k in actual if k not in expected]}
(Path('work/power-audit/board_inventory.json')).write_text(json.dumps(report,indent=2))
print(json.dumps(report['parity'],indent=2))
for r in ['U2','U3','U4','U5','Q1','Q2','J1']:
 print(r,json.dumps(report['footprints'][r]))
