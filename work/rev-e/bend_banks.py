from pathlib import Path
p=Path('work/rev-e/final_via_banks.py');s=p.read_text().replace("if any(line.intersects(bo[l]) for l in bo) or not board.buffer(-.7).contains(Point(pt)):continue\n   addvia(net,pt)\n   for l in ['B.Cu','F.Cu']:addtrack(net,origin,pt,.4,l)","""if not board.buffer(-.7).contains(Point(pt)):continue
   olen,tlen=len(out),len(tracks)
   try:
    for l in ['B.Cu','F.Cu']:
     if line.intersects(bo[l]):route(net,(*origin,l),(*pt,l),.3,False,5)
     else:addtrack(net,origin,pt,.4,l)
   except RuntimeError:
    del out[olen:];del tracks[tlen:];continue
   addvia(net,pt)""")
p.write_text(s)
