# part22/ — exploded-view part #22

The bracket beside the tailstock upright. The manual's own parts list
mislabels this item "Headstock" on p.10 — the diagram's own leader line for
#22 actually points at this bracket, not the headstock casting (see
`manual/exploded-view.png`, and either build script's docstring in this
folder). Both models here follow the diagram's leader line, not its label.

## Files

| File | What |
|---|---|
| `worksheet.md` | Measurement worksheet — fill in as tracings/measurements come in. See `../README.md` for the capture protocol. |
| `traces/` | Scanned/photographed panel tracings back the worksheet. |
| `part22_bracket.py`, `.blend`, `.stl`, `_iso.png` | First attempt, done in Blender as a solid box-section bar — kept for history, superseded in spirit (not deleted) by the SheetMetal version once the reference photo made clear the part is folded sheet, not solid tube. |
| `part22_sheetmetal.py` | Second attempt: a rectangular open-top box (trough + folded end cap) — kept for history, now also believed to have the wrong *topology* (not just unmeasured dimensions), see Status below. |
| `part22_sheetmetal.FCStd` / `.step` | The FreeCAD document and STEP export for that attempt. |
| `part22_sheetmetal_iso.svg` / `.png` | Headless isometric preview for that attempt. |
| `part22_panelB.py` | Current attempt: a single tapered-wedge panel (flat top flange → tapered web → flat, narrower bottom flange, folded flanges opposite senses), matching the 2026-08-09 tracing/photos of panel B. Same dimension-table + spreadsheet convention. |
| `part22_panelB.FCStd` / `.step` | The FreeCAD document and STEP export for panel B. |
| `part22_panelB_iso.svg` / `.png` | Headless isometric preview (see `part22_panelB_isosvg.py`). |

## Status: photo-est reconstruction, not yet measured

Three attempts so far, in order, each superseding the last in *shape*
understanding, not just dimensions — none deleted, all kept for history:

1. **`part22_bracket.py`** (Blender): a solid box-section bar. Flagged its
   own uncertainty about this ("a hint of a second fold line ... suggesting
   it may actually be an open C-channel").
2. **`part22_sheetmetal.py`** (FreeCAD): a rectangular open-top box —
   U-channel trough closed at the far end by a folded, mitered end cap —
   built from a single angled, unscaled reference photo
   (`PXL_20260808_133251586.jpg`). Answered "is this sheet metal" (yes) but
   the box *topology* is now believed wrong too, not just its numbers —
   see next point.
3. **`part22_panelB.py`** (current): a single tapered-wedge panel — flat
   top flange (2 holes) → tapered web, wider at top → flat, narrower bottom
   flange (2 holes), the two flanges folded to opposite sides. This is what
   the 2026-08-09 tracing + photos of the real part (`worksheet.md`,
   `traces/part22_panelB_trace_*.jpg`) actually show — nothing like
   `part22_sheetmetal.py`'s flat rectangular side wall. Render now visibly
   resembles the photographed part (a stepped/"Z" bracket), unlike the box.

**Still not a measured part** — every number in `part22_panelB.py` is the
photo-est reading logged in `worksheet.md` (pixel-measured off the mat's
printed grid in the tracing photos, calibrated properly this time via a
real ruler, but still a photo reading, not a 1:1 scan or calipers). Treat
this as "does the silhouette now look right," not "ready to cut metal from"
— see the caveats in `part22_panelB.py`'s own docstring (fold direction,
hole positions, and whether panel C mirrors panel B are all unconfirmed).
The M8 hole size carried over from `part22_sheetmetal.py` is also in
question — the fastener photos in `traces/` read closer to M6. Once
caliper-measured data comes in (calipers now in the photo rotation per
2026-08-09), the plan is to rebuild panel-by-panel from traced sketch
geometry and measured bend angles/radii, retagging the dimension table
`"measured"`.

## Parametric / tunable dimensions

Both `part22_sheetmetal.py` and `part22_panelB.py` follow the same
convention: every dimension lives in a `Dimensions` spreadsheet inside the
respective `.FCStd` — name, value, source tag, and note, one row each — not
just as Python constants in the build script. The sketch geometry (fully
constrained, not just placed at starting coordinates) and the SheetMetal
wall/bend features' thickness/radius/length are expression-bound to those
cells (e.g. a sketch constraint's expression is literally
`Dimensions.box_width`, or `Dimensions.top_width` in panel B's case), so the
normal tuning loop is: open the `.FCStd` in the FreeCAD GUI, double-click
the `Dimensions` spreadsheet, edit a cell, recompute — no Python, no
re-running the script, and the shape updates live.

The one part of each model that **isn't** live this way is the bolt holes:
they're cut with a raw shape boolean, not a parametric `Part::Cut` (see
"Known quirk" below), so a bare GUI recompute won't move them. Editing the
hole-position cells in the spreadsheet and then re-running the script
(which reads the same cells) does. Both scripts sanity-check after cutting
that each hole actually removed the expected volume of material, and raise
an error instead of silently shipping an uncut hole if a big enough
dimension change moved one off solid material.

## Sheet metal workbench

FreeCAD's own install does *not* bundle a sheet-metal workbench — the one
used here is the community add-on
[shaise/FreeCAD_SheetMetal](https://github.com/shaise/FreeCAD_SheetMetal),
normally installed through FreeCAD's Addon Manager. The sandbox this was
first built in had no GUI Addon Manager available, so it was installed by
hand instead: clone the repo into FreeCAD's `Mod/` directory
(`~/.local/share/FreeCAD/v1-1/Mod/SheetMetal` on Linux) so `import
SheetMetalBaseCmd` / `SheetMetalCmd` resolve; `part22_sheetmetal.py` falls
back to a `sys.path` insert relative to itself if the normal import fails, in
case a future run has the same constraint. That same sandbox also had no
FreeCAD package in its Linux distro repos and no snap/AppImage+FUSE path, so
FreeCAD itself was installed from conda-forge (`micromamba create -n freecad
-c conda-forge freecad`, FreeCAD 1.1.3 / OCCT 7.9.3) rather than through this
account's usual `freecad` skill (AppImage-based) — if that skill is
available, prefer it; this is a fallback path, documented here so the next
person doesn't have to rediscover it.

**Known quirk in that conda-forge build**: `Part::Cut` (the parametric
boolean feature) silently no-ops against this part's shape — it recomputes
without error but removes no material, even though the identical boolean
succeeds when called directly on the shape geometry (`shape.cut(tool)`).
Confirmed it isn't specific to SheetMetal's `Part::FeaturePython` objects: a
plain `Part::Feature` built from the exact same shape (via `.Shape =
sheetMetalObj.Shape.copy()`, with or without stripping the element map, and
even round-tripped through a raw BREP export/import to rule out topological-
naming metadata) has the identical problem, while a shape built from
`Part.makeBox()` cuts fine through `Part::Cut` in the same session. So it's
some BRep property of SheetMetal's generated geometry (probably from the
`multiFuse` of offset faces `smBase()` uses internally) that this build's
`Part::Cut` recompute path chokes on — not chased further than that.
Both scripts' bolt holes are cut with the direct-geometry form for this
reason (see the comment at that point in each script) — correct, just not
parametric the way a `Part::Cut` tree node would be. Worth re-testing if
this is ever rebuilt against a different FreeCAD/OCCT build.

## Rebuild

```bash
# panel B (current best shape)
freecadcmd part22_panelB.py         # writes .FCStd + .step, prints the dimension table
freecadcmd part22_panelB_isosvg.py  # writes part22_panelB_iso.svg
rsvg-convert -b white part22_panelB_iso.svg -o part22_panelB_iso.png

# the older box attempt, kept for history
freecadcmd part22_sheetmetal.py
freecadcmd part22_sheetmetal_isosvg.py
rsvg-convert -b white part22_sheetmetal_iso.svg -o part22_sheetmetal_iso.png
```

(run from this directory; all scripts resolve paths relative to themselves)
