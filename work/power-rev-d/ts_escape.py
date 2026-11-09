from pathlib import Path
import json
p=json.loads(Path('work/camera-rev-c/geometry.json').read_text())
for t in p['tracks']:
 if t['net']=='BAT_NTC' and min(__import__('math').dist(pt,(94.5625,127.25)) for pt in [t['a'],t['z']])<3:print(t)
