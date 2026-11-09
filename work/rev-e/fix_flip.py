from pathlib import Path
p=Path('work/rev-e/step3_board.py');s=p.read_text().replace(";f.Flip(f.GetPosition(),False);f.SetOrientationDegrees(0)",";b.Add(f);f.Flip(f.GetPosition(),False);f.SetOrientationDegrees(0)").replace(";f.Value().SetVisible(False);b.Add(f)",";f.Value().SetVisible(False)");p.write_text(s)
