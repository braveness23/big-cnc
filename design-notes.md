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

### Multi-modal sensing: adding thermal (NOT a decision — exploratory, no hardware selected)

- Pairing the LiDAR (shape + grayscale) with a thermal/IR camera gives the scan head three channels instead of one: shape, texture, and heat. Most hobbyist machines have none of these; this one could have all three.
- **Cut safety monitoring**: thermal could catch scorching/char risk during laser work, or bearing/spindle overheating during routing, before it's visible optically — an early-warning layer on top of the fire/fume concern already flagged as a deferred multi-tool problem.
- **Material property inference**: thermal signatures can expose internal defects invisible to depth/RGB alone — delamination in plywood or composites, voids, moisture pockets.
- **Object/material classification**: feeding depth + grayscale + thermal into a vision model to identify *what* is on the bed, not just that something is — material type, defect flags, part ID for sorting/inventory. This is what upgrades "scanning" into genuinely automated inspection rather than a manual eyeball step.
- No specific thermal module researched or chosen yet — same open-exploration status as the LiDAR camera itself.

### Full sensor suite: add RGB and near-IR cameras (NOT a decision — exploratory, no hardware selected)

- **RGB camera**: true color imaging on top of the LiDAR's grayscale — enables color-based material/finish identification and normal documentation photos, which grayscale/depth alone can't do.
- **Near-IR camera** (distinct from the far-IR thermal module above): near-infrared can reveal material differences invisible in visible light (moisture content, certain dye/plastic distinctions) and can see through smoke/dust or bright cutting glare (laser flash, sparks) that would wash out or blind a visible-light camera.
- Candidate scan-head sensor stack is now five channels: depth, grayscale, color (RGB), near-IR, and thermal. No RGB/near-IR hardware researched or chosen yet.

### AI vision and control (NOT a decision — exploratory concept, no model/compute platform chosen)

- Feed the multi-channel scan data into a vision model to move past passive scanning into active decision-making: object/material classification, defect detection, automatic response.
- **Closed-loop control**: rather than only logging a scan for a human to review afterward, have the AI vision layer feed back into the machine controller in real time — e.g., auto-adjusting feed rate or toolpath when a defect or stock shift is detected, or triggering an automatic stop on a thermal safety anomaly.
- **Autonomous job setup**: AI interpretation of a stock scan (material type, boundaries, defects) to auto-generate or adjust a toolpath, instead of a human reviewing scan data before every job.
- Fully conceptual at this stage — depends on the electronics/controls design (currently TBD) having enough onboard or networked compute to run inference in real time.

### Photogrammetry, and usages beyond the shop (NOT a decision — exploratory)

- **Photogrammetry**: the RGB camera can do more than single shots — moving it to a series of precisely known gantry positions and combining the images (structure-from-motion / multi-view stereo) is exactly what photogrammetry needs, except normally that camera-position data has to be estimated from the images themselves. Here it's already known exactly, which could make reconstruction faster and more accurate than typical photogrammetry workflows, and gives a second, cross-checkable 3D reconstruction method alongside the LiDAR depth data.
- **Artistic usages**: digitizing sculpture or relief work for reproduction or archiving; scanning cosplay/costume pieces for pattern-making; digitizing terrain/dioramas for tabletop gaming or model railroading; capturing natural objects to reinterpret into a carved toolpath; **miniature cinematography** — the gantry's precise, repeatable X/Y/Z motion is the same thing a motion-control camera rig does, so the RGB camera could shoot programmable, perfectly repeatable dolly/pan/reveal moves over a tabletop miniature or diorama set — the kind of rig practical-effects and product shoots normally rent, running on a machine already built for precision motion.
- **Scientific usages**: specimen digitization (fossils, botanical samples, insects) using the combined depth/color/near-IR/thermal channels; material science documentation of composites/defects; a hands-on platform for demonstrating vision + robotics + AI integration.
- **Industrial usages**: reverse-engineering discontinued or broken parts; dimensional QA against CAD models; automated stock alignment and job setup; shop inventory/parts cataloging; machine self-calibration; a vision front end for a future pick-and-place head.
- All still open exploration — no builds, no hardware selections beyond the candidate LiDAR camera noted above.

### Sixth channel: UV / fluorescence imaging (NOT a decision — exploratory, no hardware selected)

- Adding a UV light source + camera gives a sensing mode none of the other five channels (depth, grayscale, RGB, near-IR, thermal) can touch: many materials fluoresce or absorb differently under UV in ways invisible under normal light.
- **Artistic**: art/furniture restoration work commonly uses UV to reveal old varnish layers, prior repairs, or retouching invisible under visible light — directly useful if this platform is already being framed as a large-format digitizing/restoration tool.
- **Scientific**: mineral, botanical, and biological specimens often fluoresce distinctively under UV — another data channel for the specimen-digitization use case already noted, and a way to authenticate materials (certain dyes, inks, security features) that don't show up any other way.
- **Industrial**: UV can reveal adhesive/resin cure state and residue that's invisible optically — useful for QA on any bonded joint or composite lay-up before continuing a job.
- Ties directly into the AI vision/control concept above — one more channel for the classification model to reason over, not a separate standalone feature.

### Flagship use case: reproducing historical architectural fixtures (NOT a decision — aspirational, exploratory)

- The concrete story that ties the whole sensing + AI + fabrication stack together: take a molding profile, corbel, capital, baluster, or rosette from a historic building — damaged, missing a match, or the only surviving original — and reproduce it faithfully.
- **Scan it**: depth + RGB capture exact profile and proportions; UV reveals old varnish/prior repairs worth preserving or matching rather than guessing at the original finish; thermal/near-IR can flag rot or hidden damage in the original before it's trusted as a master.
- **Understand it**: the AI vision layer turns the scan into a clean model instead of a human tracing profiles by hand off a fragile original.
- **Remake it**: generate a toolpath (router for bulk profile, laser/drag knife for fine detail) and cut a faithful reproduction — a single replacement piece, or a full building's matching trim run from one surviving original.
- This is the anchor application for the "digitize-then-carve" and reverse-engineering ideas already logged above — historic preservation/restoration as the concrete case, not just an abstract capability list.
- Fully aspirational — no build, no scan-to-toolpath software pipeline written yet.

### Additional tool candidate: plasma cutter (NOT a decision — exploratory, no hardware selected)

- "Materials to support" already lists metal, but none of the four tools decided so far (router, laser, drag knife, pen) actually cut sheet metal well — a plasma cutter is the natural fit for that gap on the carriage.
- The 220V/60A single-phase power already available for this machine is in the right range for plasma cutter power draw, which is a good sign this fits the existing electrical plan rather than forcing a change to it.
- Same open problem as before, now with a third contributor: plasma adds sparks, UV flash, and molten spatter to the fume/dust/reflection conflict already flagged between the router and laser sharing the machine — still a deferred, unsolved multi-tool coexistence question.
- Tool-changing approach for plasma is subject to the same open question as the rest of the carriage: swap-in tool vs. simultaneously mounted.

### New usage: body scanning (NOT a decision — exploratory)

- The existing sensor stack (depth, RGB, near-IR, thermal, UV) applied to a person instead of a workpiece — a full-body scan pass, most naturally done with the bed pivoted vertical so a person can stand in front of it while the gantry sweeps.
- **Artistic**: custom costume/armor fitting — exact body geometry instead of a generic pattern, extending the cosplay/fabric-pattern use case already noted.
- **Scientific**: biometric documentation, posture/body-composition tracking over time.
- **Industrial**: custom ergonomic fixtures or furniture fitted to an actual body rather than standard sizing.
- **Safety note, distinct from object scanning**: scanning a person means a person standing near a machine that also carries a router, laser, and (candidate) plasma cutter. This needs a clearly separate "scan-only" mode with cutting tools mechanically or electrically disabled, not just a software safeguard — a real open safety question to resolve before this is anything more than a brainstorm item.

## 2026-08-06 — Electronics parts on hand (inventory, NOT a design decision)

Cataloged from a parts box; photos in `images/components/`. This is an inventory snapshot only — no controller architecture has been chosen, and nothing here is confirmed as the final motion-control electronics for the build.

- **Stepper motors (5x, NEMA 17 size)**: mixed lot, includes a labeled "Wantai 42BYGH610" (1.2A, 1.8°/step) and a "17HS08-1004S3" (dated 2014.05.21), plus three more unlabeled units of the same form factor, all with 4-wire leads (`nema17-stepper-motors-group.jpg`, `nema17-stepper-motors-labels.jpg`)
- **Stepper drivers**: one standalone microstep driver module (DC 9–42V, up to 3.5A, DIP-switch configurable — TB6600-style) (`stepper-driver-microstep-tb6600-style.jpg`), plus an Arduino Uno + CNC Shield populated with 4x A4988 driver modules, silkscreened for X/Y/Z/A axes (`arduino-cnc-shield-a4988-drivers-1.jpg`, `arduino-cnc-shield-a4988-drivers-2.jpg`) — **the Arduino is already flashed with GRBL**, confirmed, not just a GRBL-compatible shield
- **Limit switches**: 5x mechanical lever-arm microswitches, pre-wired with small connectors — for axis end-stops (`limit-switches-endstops.jpg`)
- **Connectors**: a bag of GX16-4 aviation connectors (16mm shell, 4-pin, panel-mount) for motor/cable disconnects (`gx16-4-aviation-connectors.jpg`); one small connector part still in its retail packaging, exact type not yet identified (`connector-part-packaged.jpg`)
- **Heatsinks**: small self-adhesive aluminum heatsinks, sized for driver ICs (`aluminum-heatsinks.jpg`)
- **Cabling**: one USB-A to USB-B cable, for Arduino programming/control (`usb-a-b-cable.jpg`)

Open question: whether the standalone higher-current driver module ends up driving the gantry, and what replaces the CNC Shield/GRBL stack for the controller — see follow-up below, this is no longer fully open.

### Follow-up: CNC Shield ruled out for big-cnc

- **Decision**: the Arduino Uno + CNC Shield (GRBL) from the inventory above will **not** be used for big-cnc. Firm decision, not a leaning.
- Leaves the standalone higher-current stepper driver module as the only motion-control hardware on hand so far.
- The 5x stepper motors, limit switches, connectors, heatsinks, and cabling cataloged above are unaffected by this — still on-hand parts, still unassigned to a specific role.

### Follow-up: controller firmware — grblHAL

- **Decision**: controller firmware is **grblHAL** — decided roughly a year prior to this entry (predates this journal), reaffirmed here. Firm decision, not a leaning.
- grblHAL is the modern 32-bit successor to classic GRBL: same G-code/workflow model, but runs on STM32/ESP32/RP2040-class boards instead of 8-bit Arduino, with room for more axes, networking, plugin drivers, and closed-loop stepper support as the design matures.
- This settles the earlier "GRBL on different hardware vs. LinuxCNC vs. something else" open question in favor of GRBL's lineage — just on genuinely modern hardware instead of the Arduino Uno + CNC Shield ruled out above.
- Not yet chosen: specific grblHAL board/MCU, and how it maps to the on-hand steppers/driver/limit-switches inventory.

### Follow-up: archived the original ChatGPT conversation this traces back to

- Recovered a shared ChatGPT conversation from **May 6–13, 2025**, "CNC Machine Design Options" — the year-prior source of the grblHAL decision above. Full transcript archived at `references/chatgpt-cnc-design-2025-05.md`. Captured for the record, not reconciled against current design state.

## 2026-08-09 — cnc-lathe: FreeCAD model of the existing wood lathe, as a foundation for a CNC addition

A separate, smaller sub-project alongside the main 4'×8' machine documented above: converting an existing benchtop wood lathe into a CNC lathe. Files live under `cnc-lathe/` (workshop photos, owner's manual, exploded parts diagram, and now a scripted 3D model in `cnc-lathe/cad/`).

- **Machine identified**: Central Machinery (Harbor Freight) SKU# S36066, "14" x 40" Wood Lathe w/7" Disc", from its nameplate and 14 workshop photos. Owner's manual and exploded parts diagram recovered and added to `cnc-lathe/manual/`.
- **CNC addition scope** (Dave's answer, drives what the model prioritizes): a powered Z carriage riding the bed rails, a spindle encoder for C-axis/indexing, and a full X/Z cross-slide — not just one of these. That means the bed rails, headstock/spindle (front and rear), tailstock, and banjo/tool-rest mount are the parts worth getting right; the sanding-disc/worktable/miter-gauge subsystem is out of scope and was modeled at low fidelity on purpose.
- **`cnc-lathe/cad/lathe.py`** builds a rough FreeCAD model (Part workbench, not Arch — this is a machine, not a building) with every dimension source-tagged in one table: manual specs and nameplate values are exact, several "unknown" dimensions turned out to be derivable from published standards instead of guessed (bearing 6201/6203/6204 bore/OD/width from the parts list, MT2 Morse taper geometry, 3/4"-10 UNC spindle nose thread — confirmed via forum sources, not in the manual itself), and the rest (bed-rail cross-section, headstock/tailstock/banjo casting envelopes) are proportioned from the reference photos with **no scale reference in any of them** — flagged `photo-est`, given an `_EST` label suffix in the model tree, and tinted orange in the rendered preview so they're never mistaken for real measurements.
- The build script asserts the `photo-est` sub-lengths sum back to the manual's overall envelope (63-3/4" length, 15" height, 40" between centers) within a few inches, as a guard against an estimate being not just imprecise but wrong.
- (NOT a decision — pending measurement) `cnc-lathe/cad/README.md` has the full prioritized measurement list: bed-rail channel profile and spacing (highest priority — it's the Z-carriage's travel surface), banjo/tool-rest-holder geometry (likely X cross-slide mount point), headstock and tailstock casting envelopes, whether the spindle is through-bored, and any bench-mounting bolt pattern.
- Rebuild with `freecadcmd cad/lathe.py` (writes `lathe.FCStd` + `lathe.step`) and `freecadcmd cad/_isosvg.py` (headless isometric preview, since this machine has no working offscreen GL context — same constraint documented in `basement-remodel/cad/README.md`).

### Follow-up: exploded-view part #22, reconstructed as sheet metal in FreeCAD

`PXL_20260808_133251586.jpg` shows exploded-view part #22 (a bracket beside the tailstock upright, mislabeled "Headstock" in the manual's own parts list — see `cnc-lathe/cad/part22_bracket.py`'s docstring) in enough detail to tell it's folded sheet steel, not solid tube: visible bend radius on the outer corners, constant wall thickness, a mitered seam at the end panel. An earlier pass (`cnc-lathe/cad/part22_bracket.py`, Blender) modeled it as a solid box-section bar and flagged its own uncertainty about this. This follow-up answers the "can FreeCAD do sheet metal" question and redoes the part properly.

- **Yes, FreeCAD can do sheet metal** — not out of the box, but via the community [SheetMetal workbench](https://github.com/shaise/FreeCAD_SheetMetal) (parametric wall/bend/flange/unfold tools with real thickness and bend-radius geometry, not just a solid modeled to look thin).
- **`cnc-lathe/cad/part22_sheetmetal.py`** rebuilds part #22 as an actual bent-sheet solid: an open-top U-channel trough (matching the rails' own folded-channel profile) closed at the far end by a wall folded up from all three open edges in one auto-mitered bend, with two bolt holes cut through the raised end face. Same non-measured status as the Blender attempt — pixel-scaled off the M8 bolt heads in the photo, every dimension source-tagged `photo-est` or `assumption` in the script's dimension table. Kept `part22_bracket.py` rather than deleting it (see `cnc-lathe/cad/README.md`).
- The environment this was built in had no working `freecad`/`freecadcmd` and no path to the AppImage this account's `freecad` skill normally uses (no snap, no FUSE-backed AppImage mount available), so FreeCAD itself came from conda-forge (`micromamba`, FreeCAD 1.1.3 / OCCT 7.9.3) as a fallback — and that build turned out to have its own quirk, `Part::Cut` silently not cutting against a SheetMetal object (worked around with a direct shape-level boolean instead). Both fully written up in `cnc-lathe/cad/README.md` so the next session doesn't have to rediscover either one.
- Left out: a third fastener visible low in the trough in the photo (probably item 48) — not legible enough to reconstruct with confidence, so it's absent rather than guessed.

### Follow-up: reorganized into one folder per reverse-engineered part, and a paper-tracing capture protocol

Dave's assessment of the part #22 sheet-metal attempt above: FreeCAD's SheetMetal workbench clearly works, but reconstructing a part from a single angled, unscaled reference photo is not a reliable way to get real dimensions — agreed, and expected: no scale reference, perspective distortion, and bend angles are essentially unrecoverable from one photo. Going forward, parts get measured properly (paper tracings + calipers/angle-gauge/radius-gauge readings) instead of estimated from photos.

- **New convention**: `cnc-lathe/parts/<N>/` holds *everything* for one exploded-view part — worksheet, scanned tracings, every build-script attempt, FreeCAD documents, exports, renders, and part-specific notes — instead of splitting build scripts into `cad/` and measurement worksheets into a separate `manual/measurements/` folder the way the first pass did it. `cnc-lathe/cad/` is now reserved for the whole-machine assembly model (`lathe.py`) only. Part #22's files (`part22_bracket.*`, `part22_sheetmetal.*`, and the new `worksheet.md`) all moved into `cnc-lathe/parts/part22/` — moved with `git mv`, history preserved; nothing deleted.
- **Capture protocol** (`cnc-lathe/parts/README.md`): trace each panel on paper (letter panels A/B/C… on the part first), scan at 1:1 (no "fit to page") or photograph strictly straight-on with a ruler in-frame if no scanner is available. Bends, thickness, and hole diameters aren't recoverable from a flat tracing, so those get measured separately — bend angle with an angle finder/bevel gauge, bend-line fillet radius with a radius gauge (or the sagitta trick off calipers if no gauge on hand: chord length `c` and midpoint height `h`, radius = `h/2 + c²/(8h)`), hole diameter and material thickness with calipers. A rounded/chamfered corner *within* a single panel's own outline is different from a bend-line fillet between two panels — that one's just part of the panel's traced outline, no separate gauge needed, trace the true contour rather than squaring it off.
- Once real data comes in for a part, each scan gets imported into a FreeCAD Sketcher background image and traced directly, and the model's dimension table gets rebuilt with everything tagged `"measured"` instead of `"photo-est"`/`"assumption"` — same source-tag convention `lathe.py` already uses.
- `cnc-lathe/parts/TEMPLATE.md` is the blank worksheet to copy for any new part; `cnc-lathe/parts/part22/worksheet.md` is the first instance, currently empty pending tracings.

### Follow-up: part #22's first tracing came in, and it corrected the model's *shape*, not just its numbers

First real capture-protocol data: fastener photos and a paper tracing of one of part #22's side walls ("panel B"), shot on a mat with a printed ruler (proper scale calibration, unlike the original angled reference photo). Reading it made clear `part22_sheetmetal.py`'s rectangular open-top box was wrong in kind, not just in dimensions — panel B is a tapered wedge (flat top flange with 2 holes → tapered web, wider at top → flat, narrower bottom flange with 2 holes, the two flanges folded to opposite sides), nothing like a flat rectangular wall.

- Rebuilt as `cnc-lathe/parts/part22/part22_panelB.py` — a third attempt, kept alongside (not replacing) the Blender box and the FreeCAD rectangular-box attempt, following this project's "supersede in spirit, keep for history" convention. The rendered isometric now visibly resembles the photographed part; the old box render did not.
- **Still photo-est, not measured** — same caveat as always, now compounded: fold direction/angle, exact hole positions, and whether the other side wall (panel C) mirrors panel B are all unconfirmed guesses layered on top of a photo reading. Explicitly a "does the silhouette look right now" pass, not a build-ready model.
- Both `part22_sheetmetal.py` and the new `part22_panelB.py` were rebuilt to be spreadsheet-parametric per Dave's request: every dimension lives in a `Dimensions` spreadsheet inside the `.FCStd` (name/value/source/note), with the sketch and SheetMetal wall/bend features expression-bound to those cells — open the file in the FreeCAD GUI, edit a cell, recompute, no Python required. Verified by round-trip test (reopen saved file, edit a cell, recompute, geometry updates). The one exception is bolt holes, still a raw shape boolean due to the `Part::Cut` quirk already logged in `cnc-lathe/parts/part22/README.md` — now confirmed not SheetMetal-specific (a plain `Part::Feature` built from the same shape has the identical problem).
- Dave will start including calipers in future part photos, which should resolve the standing M6-vs-M8 ambiguity on the tailstock-end hardware (the bolt shank read closer to M6, the head reading closer to M8 — the two disagreed, likely photo parallax on the raised head).
