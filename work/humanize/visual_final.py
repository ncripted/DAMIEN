from pathlib import Path
p=Path('work/humanize/build.py');s=p.read_text().replace("just='(justify left)'\n   else:","just='(justify right)' if ang==180 else '(justify left)'\n   else:")
s=s.replace("if ref=='U7':tx,ty=x+5,y-(18 if name=='Reference' else 15.46)","if ref=='U7':tx,ty=x+5,y-(18 if name=='Reference' else 15.46)\n   if ref=='Q8':tx,ty=x+20,y-(18 if name=='Reference' else 15.46)")
s=s.replace("Open/short probe or stale readings.',20,225)","Open/short probe or stale readings.',20,215)")
s=s.replace("open/short probe or stale readings.',20,225)","open/short probe or stale readings.',20,215)")
p.write_text(s)
