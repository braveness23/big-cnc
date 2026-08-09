# parts/ — per-part reverse-engineering folders

Every individual part being reconstructed from the exploded-view diagram
gets one folder here, named after its exploded-view item number (e.g.
`part22/`). That folder holds *everything* for that part in one place:
measurement worksheet, scanned tracings, CAD build script(s), the FreeCAD
document, exports, renders, and notes — so there's one place to look, not
scattered across a `cad/` folder (build scripts) and a separate
`manual/measurements/` folder (worksheets) the way an earlier pass did it.
`cad/` (one level up) stays reserved for the whole-machine assembly model
(`lathe.py`/`lathe.FCStd`), which isn't part-specific.

## Folder contents (per part)

- `README.md` — part-specific build notes: what the part is, what's been
  tried, open questions, install/rebuild instructions for anything unusual
  that script needed. Optional for a part with nothing unusual to say.
- `worksheet.md` — the fillable measurement record (copy `TEMPLATE.md` from
  this directory to start a new one).
- `traces/` — scanned/photographed tracings, one file per panel, named
  `<part>_panel<Letter>_trace.<ext>` (e.g. `part22_panelA_trace.png`).
- `<part>_*.py` — build script(s). May be more than one if a part went
  through multiple reconstruction attempts (kept, not deleted, for history
  — see `part22/README.md` for an example: an earlier Blender-based attempt
  sits alongside the current FreeCAD SheetMetal one).
- `<part>_*.FCStd` / `.step` / `_iso.svg` / `_iso.png` — the FreeCAD
  document, STEP export, and rendered preview for each build script above.

## How a part gets measured (paper tracing protocol)

How to capture a sheet-metal part accurately enough to model in FreeCAD,
instead of guessing dimensions off angled reference photos (see
`part22/README.md` for why that failed on the first attempt: no scale
reference, perspective distortion, and bend angles are basically
un-recoverable from a single photo). Ranked by how directly each method
gives a *number* rather than something to interpret:

1. **Flatbed scan of a traced panel outline** — best. A scan is 1:1 and
   orthographic by construction, no parallax, no calibration needed. Gets
   imported straight into a FreeCAD sketch as a background image to trace
   exact geometry over.
2. **Direct numeric measurement** (calipers, tape, angle gauge, radius
   gauge) — unambiguous. Needed for thickness, bend angle, bend radius, and
   hole diameter, none of which a flat tracing captures on its own.
3. **Straight-on photo with a ruler in the same plane, camera perpendicular**
   — fallback for a panel too big or awkward to trace/scan. Noisier than a
   scan but still usable if genuinely shot square-on.
4. **Angled context photos** — identification and a sanity check against the
   assembled model only. Never used for a dimension.

### Tracing technique

1. **Letter each panel** on the part itself (tape or marker: A, B, C…) —
   the worksheet and file names refer back to these letters, so pick them
   before tracing anything.
2. **Trace each panel separately.** Hold paper flush against the panel and
   trace its outline. For a hole, poke a pencil or awl through from behind
   to mark the center on the paper — don't try to trace the hole's edge
   freehand.
3. **Scan at 1:1** — no "fit to page" or "auto-scale" option in the scanner
   driver. If no scanner is available, photograph straight-on: camera
   directly overhead (not angled), with a ruler laid flat in the same plane
   as the tracing, in-frame, right next to it.
4. **Bends aren't on the tracing** — a flat piece of paper can't record a
   dihedral angle. For every seam where two panels meet, separately:
   - measure the angle between them with an angle finder/bevel gauge
   - measure the inside corner radius with a radius gauge (aka fillet gauge
     — a cheap set of leaves with concave/convex arcs ground in; hold one
     against the curve until it sits flush with no light gap), or the
     sagitta trick if you don't have one: lay a straightedge across the
     curve to get a chord length `c`, measure the perpendicular height `h`
     from the chord's midpoint to the curve, radius = `h/2 + c^2/(8h)`
   - note which two panel letters that bend connects
   - a rounded or chamfered corner *within* a single panel's own outline
     (not a fold between two panels) is different — trace its true contour
     as part of that panel's tracing instead, it gets fit directly from the
     scan
5. **Thickness**: calipers at any exposed/cut edge of the actual material
   (not estimated from the tracing).
6. **Hole diameter**: calipers, separately from the traced center mark.
7. **Overall envelope** (L x W x H, tape measure) as a cross-check once
   everything is modeled — should match the assembled panels within a
   reasonable tolerance.

## How this gets used

Scanned/measured values go into the model's dimension table tagged
`"measured"` (see the source-tag convention already used in `cad/lathe.py`
and `part22/part22_sheetmetal.py`), replacing the old `"photo-est"` /
`"assumption"` tags. Each scan gets imported into a FreeCAD Sketcher
background image and traced directly, so panel geometry comes from your
tracing, not from re-estimating it.
