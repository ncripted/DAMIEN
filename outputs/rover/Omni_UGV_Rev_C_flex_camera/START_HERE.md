# Omni rover — Rev C flex camera

Open **omni_ugv.kicad_pro** in KiCad 10.0.8. This is the new camera revision. Rev B remains preserved separately.

J3 now accepts the selected **Arducam M0031 24-pin DVP flex module**, via a Hirose FH12-24S-0.5SH(55). It is incompatible with the old 18-pin Waveshare carrier. See engineering/CAMERA_REV_C.md and engineering/PIN_MAP.md before connecting anything.

Eight-page Schematic.pdf, BOM.csv, design_connections.json and validation/current reflect Rev C. Final configured checks: ERC 0; DRC errors/warnings 0; unconnected items 0; schematic parity 0. Every existing non-J3 pin retains its Rev B net assignment. These checks do not establish camera operation or fabrication readiness.

Current board previews: preview/rev-c-top.png and preview/rev-c-bottom.png. Old renders and mechanical STEP are historical and must not be used as current assembly geometry. Custom 3D bodies and the attached camera head are not fully represented.

Camera bracket, exact flex fit/contact orientation, signal integrity and camera power/thermal behavior require validation. Battery assumptions, protection cutoff/temperature-window work, regulator/motor thermal/transient work, mechanical fit, RF testing, firmware and Vita integration remain open. No board order or fabrication release is authorized.
