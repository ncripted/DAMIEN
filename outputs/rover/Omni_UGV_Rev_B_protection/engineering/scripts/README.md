# Editing workflow

The root native KiCad files are the current editable design. Open omni_ugv.kicad_pro in KiCad 10.
The PCB was edited using pcbnew and native text; schematics were regenerated with a presentation-only adapter and checked against XML netlists.

readable_schematic.py reconstructs the November 5 presentation from the explicitly archived presentation_baseline, not from arbitrary later electrical edits. It rewrites all seven schematic files and the CSD17308Q3 library symbol. Back up current files and update its input snapshot before using it after electrical changes. Do not run older protection construction scripts over the finished board: they reset routing.

validate.ps1 reruns the native configured checks. A CLI exit code alone is not the result; inspect violation counts. Saved reports apply to their hashed snapshot.

The KiCad GUI can display the same saved files, but there is no live IPC edit connection. Reload externally modified files; do not save an older open editor over a newer disk revision.
