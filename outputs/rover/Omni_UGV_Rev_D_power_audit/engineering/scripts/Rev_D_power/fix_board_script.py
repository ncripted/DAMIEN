from pathlib import Path
p=Path('work/power-rev-d/board_revision.py');s=p.read_text();a=s.index('b=p.LoadBoard');z=s.index("for ref in ['SW3'")
s=s[:a]+'''data=json.loads((r/'design_connections.json').read_text());dm={d['ref']:d for d in data};new=json.loads(Path('work/power-rev-d/new_parts.json').read_text())
g=json.loads(Path('work/power-rev-d/geometry.json').read_text());ce=next(d for d in g['pads'] if d['ref']=='U5' and d['num']=='4');x,y=ce['at'];w,h=ce['size'];removed=[]
for t in g['tracks']:
 hit=t['net'] in ['SYS_ON','BAT_NTC']
 if t['net']=='GND' and any(abs(pt[0]-x)<w/2+.03 and abs(pt[1]-y)<h/2+.03 for pt in [t['a'],t['z']]):hit=True
 if hit:removed.append(dict(uuid=t['uuid'],net=t['net']))
ids={d['uuid'] for d in removed};s=fn.read_text()
for a,z,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(i in t for i in ids):s=s[:a]+s[z:]
tmp=Path('work/power-rev-d/stripped.kicad_pcb');tmp.write_text(s);b=p.LoadBoard(str(tmp));nets={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()}
for name in {v for d in data for v in d['nets'].values() if v}:
 if name not in nets:n=p.NETINFO_ITEM(b,name);b.Add(n);nets[name]=n
fps={f.GetReference():f for f in b.GetFootprints()}
''' +s[z:];p.write_text(s)
