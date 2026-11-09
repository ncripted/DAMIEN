from pathlib import Path
p=Path('work/rev-e/final_via_banks.py');s=p.read_text();s=s.replace("region=box(origin[0]-4,origin[1]-4,origin[0]+4,origin[1]+4);bo={l:obs(net,l,.2,region) for l in ['B.Cu','F.Cu']};chosen=[]","region=box(origin[0]-4,origin[1]-4,origin[0]+4,origin[1]+4);chosen=[]")
s=s.replace("vo=obs(net,'',.3,region,True)","anchor=chosen[0] if chosen else origin;bo={l:obs(net,l,.2,region) for l in ['B.Cu','F.Cu']};vo=obs(net,'',.3,region,True)")
s=s.replace("line=LineString([origin,pt])","line=LineString([anchor,pt])").replace("(*origin,l),(*pt,l)","(*anchor,l),(*pt,l)").replace("addtrack(net,origin,pt,.4,l)","addtrack(net,anchor,pt,.4,l)")
s=s.replace('except RuntimeError:', 'except RuntimeError as e:').replace("del out[olen:];del tracks[tlen:];continue", "del out[olen:];del tracks[tlen:];continue")
s=s.replace("chosen.append(pt);break","chosen.append(pt);print('Bank',net,origin,pt,flush=True);break")
p.write_text(s)
