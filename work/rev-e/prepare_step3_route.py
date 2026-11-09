from pathlib import Path
s=Path('work/rev-e/router.py').read_text()
s+='''
# Reserve the battery return first; do not resolve this load-current connection as a signal.
layers=['F.Cu','B.Cu']
route('CELL_N',endpoint('J2',2,'F.Cu'),endpoint('R36',1,'B.Cu'),1.0,True,12);save()
layers=['B.Cu','F.Cu','In2.Cu']
# Independent sense contacts terminate only at the protection front end and its bypass return.
rr('PROT_CS_SENSE','R36',4,'U7',4,.15,True);save()
rr('PROT_VSS_SENSE','R36',3,'U7',3,.15,True);save()
rr('PROT_VSS_SENSE','C24',2,'U7',3,.15,True);save()
rr('PROT_VDD','R37',2,'U7',2,.2,True);save()
rr('PROT_VDD','C24',1,'U7',2,.2,True);save()
rr('PROT_DSG','U7',7,'Q8',4,.2,True);save()
rr('PROT_DSG','R41',2,'Q8',4,.15,True);save()
# Retain CTR's existing low state until the independent cutoff interface is implemented in step5.
rr('CELL_N','U7',5,'R36',1,.15,True);save()
'''
Path('work/rev-e/step3_route.py').write_text(s)
