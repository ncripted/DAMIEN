from pathlib import Path
s=Path('work/rev-e/step5_lastfix.py').read_text();s=s.replace("['fccf7362-bc2a-417f-a7e7-b4e8491cdd99']","['57e88b9a-fda4-4ed7-9f6f-b734c56b8da7','09ffdb86-ab73-465b-93be-ab8001afba35']").replace("bad.update(['0227f5da-c08e-4746-838c-c458e91f7e39'])","pass");Path('work/rev-e/cleanup_current_islands.py').write_text(s)
