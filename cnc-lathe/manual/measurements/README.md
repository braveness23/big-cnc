# Measurement capture protocol (paper tracing)

How to capture a sheet-metal part accurately enough to model in FreeCAD,
instead of guessing dimensions off angled reference photos (see
`cnc-lathe/cad/README.md`'s part #22 writeup for why that failed: no scale
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

## Per-part folder

Each part gets its own folder here, named after its exploded-view item
number, e.g. `part22/`. Inside:

- `worksheet.md` — the fillable measurement record (copy `TEMPLATE.md` from
  this directory to start a new one).
- `<part>_panel<Letter>_trace.<ext>` — the scanned/photographed tracing for
  each panel (e.g. `part22_panelA_trace.png`).
- Any supporting context photos, named descriptively.

## Tracing technique

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
   - estimate or measure the inside corner radius (radius gauge, or "sharp"
     if there isn't a meaningful one)
   - note which two panel letters that bend connects
5. **Thickness**: calipers at any exposed/cut edge of the actual material
   (not estimated from the tracing).
6. **Hole diameter**: calipers, separately from the traced center mark.
7. **Overall envelope** (L x W x H, tape measure) as a cross-check once
   everything is modeled — should match the assembled panels within a
   reasonable tolerance.

## How this gets used

Scanned/measured values go into the model's dimension table tagged
`"measured"` (see the source-tag convention already used in `cad/lathe.py`
and `cad/part22_sheetmetal.py`), replacing the old `"photo-est"` /
`"assumption"` tags. Each scan gets imported into a FreeCAD Sketcher
background image and traced directly, so panel geometry comes from your
tracing, not from re-estimating it.
