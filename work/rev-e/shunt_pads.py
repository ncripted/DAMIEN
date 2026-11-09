from pathlib import Path
import json
x=json.loads(Path('work/rev-e/geometry.json').read_text());print([(d['num'],d['at'],d['net']) for d in x['pads'] if d['ref']=='R36'])
