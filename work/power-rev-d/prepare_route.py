from pathlib import Path
s=Path('work/camera-rev-c/route.py').read_text().split('errors=[]')[0].replace('work/camera-rev-c','work/power-rev-d')
s+='''errors=[]
report=json.loads(Path('work/power-rev-d/drc-placed.json').read_text());items={d['uuid']:d for d in pads+tracks}
def end(i):
 d=items[i['uuid']]
 if 'ref' in d:return (*d['at'],'B.Cu' if 'B.Cu' in d['layers'] else 'F.Cu')
 # Reports give a location on the disconnected copper; snap to its nearest end.
 pos=(i['pos']['x'],i['pos']['y']);pt=min([d['a'],d['z']],key=lambda v:math.dist(v,pos))
 return (*pt,'B.Cu' if d['via'] else d['layer'])
for v in sorted(report['unconnected_items'],key=lambda v:len(v['items'][0]['description'])):
 a,z=v['items'];net=items[a['uuid']]['net']
 try:route(net,end(a),end(z),.15,True,12)
 except Exception as e:print('FAILED',net,str(e),flush=True);errors.append([net,str(e)])
 save()
Path('work/power-rev-d/route-errors.json').write_text(json.dumps(errors,indent=2));print('Finished',len(out),'objects;',len(errors),'failures',flush=True)
'''
Path('work/power-rev-d/route.py').write_text(s)
s=Path('work/camera-rev-c/apply_routes.py').read_text().replace('Omni_UGV_Rev_C_flex_camera','Omni_UGV_Rev_D_power_audit').replace('work/camera-rev-c','work/power-rev-d');Path('work/power-rev-d/apply_routes.py').write_text(s)
