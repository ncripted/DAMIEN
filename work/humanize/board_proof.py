from pathlib import Path
import re,json,hashlib,sys
sys.path.insert(0,str(Path('work/humanize').resolve()))
from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_B_protection');a=Path('work/humanize/board-before.kicad_pcb').read_text();b=(r/'omni_ugv.kicad_pcb').read_text()
def sha(s):return hashlib.sha256((Path('work/humanize/board-before.kicad_pcb') if s is a else r/'omni_ugv.kicad_pcb').read_bytes()).hexdigest()
def select(s,prefix):return sorted(re.sub(r'\s+','',t) for aa,bb,t in blocks(s) if t.startswith(prefix))
def fps(s):return {re.search(r'\(property "Reference" "([^"]+)',t)[1]:t for aa,bb,t in blocks(s) if t.startswith('(footprint ')}
fa,fb=fps(a),fps(b)
changed=[k for k in fa if re.sub(r'\s+','',fa[k])!=re.sub(r'\s+','',fb[k])]
proof=dict(before_board_sha256=sha(a),after_board_sha256=sha(b),tracks_vias_unchanged=select(a,('(segment','(via'))==select(b,('(segment','(via')),board_graphics_outline_unchanged=select(a,('(gr_','(dimension'))==select(b,('(gr_','(dimension')),changed_footprints=changed,footprint_count_before=len(fa),footprint_count_after=len(fb),allowed_changes=['R42 position and associated fields translated -0.2 mm X','U1 explicit four-layer keepout/stackup; all pad blocks unchanged','Refilled zone data'],u1_pads_unchanged=select(fa['U1'],'(pad ')==select(fb['U1'],'(pad '))
assert proof['tracks_vias_unchanged'] and proof['board_graphics_outline_unchanged'] and proof['u1_pads_unchanged'] and set(changed)=={'R42','U1'},proof
(r/'validation/current/board-change-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
# Stale Rev A previews are preserved but removed from current-preview names.
h=r/'preview/history';h.mkdir(exist_ok=True)
for name in ['baseline.svg','board-current.png','PCB_review.png','PCB_review.svg','regulator-review.png']:
 p=r/'preview'/name
 if p.exists() and not (h/('Rev_A_'+name)).exists():p.rename(h/('Rev_A_'+name))
print(json.dumps(proof,indent=2))
