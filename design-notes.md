# Design Notes

Running log of design thoughts, decisions, and ideas. Newest at bottom.

## 2026-07-19 — Initial concept

- **Bed size**: handles 4' x 8' sheet material
- **Tooling**: multi-tool — router, laser, drag knife, pen (plotter-style)
- **Frame**: welded steel tubing
- **Base frame ("truck")**: welded steel frame with lifting casters; supports the pivoting bed — not the tool carriage. Nothing fancy, just a mobile base + pivot support.
- **Bed orientation**: pivots — horizontal, vertical, and everywhere in between
- **Gantry**: dual rails along the 8' Y axis
- **Z axis travel**: 4–6"
- **Electronics**: TBD — Dave has a collection of electronics on hand already; controls/electronics design to be discussed later
- **X/Y drive**: belt drive — priority is precision over speed
- **Base frame footprint**: relatively small floor footprint
- **Bed pivot actuation**: manual at first, motorized actuator later
- **Materials to support**: wood, metal, composite, fabric, paper, vinyl
- **Additional tooling (sensing)**: lidar, camera, 3D scanner

### Q&A round 1

- **Tool changing**: likely multiple tools live on the carriage simultaneously (vs. one-at-a-time manual swap) — approach still unknown/open
- **Laser + other tools sharing the machine** (dust, fumes, reflections with router/metal work) — deferred, later problem
- **Bed pivot mechanics**: pivots on a center axis (not an edge trunnion). Material held to bed via clamps, adhesives, or plastic/blind nails (method depends on material/job)
- **"Truck" clarified**: it's the mobile base frame with lifting casters + pivot supports for the bed — not a carriage for the router. Nothing fancy — base + pivot support only
- **Precision target**: unknown/TBD so far
- **Power**: 220V, 60A, single phase available
- **Footprint target**: as small as reasonably possible — rough target ~4' x 3' floor space for the base

### Scope clarification

- Not designing around specific tools right now — the goal is a **versatile foundation/platform** for unknown future CNC tooling, not a tool-specific machine
- Precision goal: wants "high precision" capability, but no quantified target yet (no tolerance number in mind)

### Rough steel tube sizing estimate (NOT a decision — no load calcs, tool weights, or precision target yet)

Ballpark starting points only, to be refined once real loads (tools, electronics, total moving mass) and a precision target are known:

- **Gantry rails** (8' Y span, dual rail + tool carriage): 2"×4" or 3"×3" tube, 0.1875"–0.25" wall. Biggest deflection risk in the machine — gantry sag over an 8' span directly hurts cut accuracy. Orient rectangular tube long-axis vertical for max bending resistance.
- **Fixed main frame** (holds pivot bearings/shaft + gantry ends): 3"×3" square tube, 0.1875"–0.25" wall. The backbone — err thick here.
- **Pivoting bed frame** (torsion box holding the 4x8 sheet): lighter — 1.5"×1.5" or 2"×2" square tube, ladder/torsion-box pattern with cross bracing. Stiff in torsion, not heavy, since it swings through the full horizontal-to-vertical range.
- **Base ("truck") frame + casters**: 3"×3" or 4"×4" square tube, 0.25" wall. Easy to underestimate — bed going vertical creates a cantilevered tipping moment on the base, so a wide stance + heavier-than-expected base is the safer bet.
- **Pivot shaft**: its own component, not structural tube — likely a solid shaft or schedule 40 pipe through pillow-block bearings, sized once swinging mass is known.
- **Key open variable**: precision target drives this the most. True high-precision work pushes toward thicker wall / smaller cross-section tube over cheaper big-thin tube, since gantry deflection under load is the limiting factor.

## 2026-07-22 — Platform reframe: LiDAR scanning as a core capability

### Candidate hardware (NOT a decision — one candidate part, not yet purchased or tested)

- **Onion Tau LiDAR Camera (TA-L10)**: USB-C depth + grayscale camera. 160×60 depth stream @ 30fps, 0.1–4.5m range, 81°×30° FOV, 5V/500mA, OpenCV-compatible Python SDK, ~90×41×20mm.

### Brainstorm: gantry-mounted LiDAR scanning (open exploration, no decisions made)

- **Reframe**: the machine isn't "a CNC that also scans" — it's a general-purpose precision XY(Z) motion platform, with router/laser/drag-knife/pen/scanner as interchangeable heads on the same platform. This is the same "versatile foundation" framing as the original scope clarification, made concrete by a first non-cutting head.
- **Why this matters**: the gantry knows its own camera position exactly (vs. SLAM/feature-tracking drift in handheld or turntable consumer scanners), at a physical scale (4'x8') most affordable scanners can't reach. That combination — known-position + large-format — is genuinely uncommon.
- **Scanning as a job step**: pre-job stock/fixture mapping and auto-alignment (compensating for warped or skewed stock); pre/post-cut scans for QA (verify actual material removed vs. intended toolpath); digitize-then-carve workflow (scan an irregular object, generate a toolpath to reproduce or modify it).
- **Bed pivot as an extra scan axis**: combining gantry X/Y sweep with the bed's horizontal-to-vertical pivot could capture angled surfaces, not just a flat overhead view.
- **Self-calibration**: using the scanner to measure the machine's own gantry squareness, rail straightness, and bed flatness — directly relevant to the still-open precision target question above.
- **Non-cutting uses for the same platform**: large-format 3D digitizing of arbitrary objects (furniture, parts, costume/fabric pieces); a DIY coordinate-measuring-machine-style dimensional check against CAD models; reverse-engineering broken or discontinued parts; shop inventory/parts cataloging; a bin-picking vision front end for a possible future pick-and-place head.
- **Open questions**: whether the scanner is a permanent carriage fixture or a tool-changed head like the others; USB-C cable management through carriage wiring; lens protection from chips/fumes if it shares carriage space with the router/laser.
