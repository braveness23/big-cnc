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
| `part22_sheetmetal.py` | Build script for the current SheetMetal-workbench reconstruction. Same dimension-table convention as `cad/lathe.py`. |
| `part22_sheetmetal.FCStd` / `.step` | The FreeCAD document and STEP export. |
| `part22_sheetmetal_iso.svg` / `.png` | Headless isometric preview (see `part22_sheetmetal_isosvg.py`). |

## Status: photo-est reconstruction, not yet measured

`PXL_20260808_133251586.jpg` (in `../../`) shows part #22 in the flesh: a
folded-sheet bracket (visible bend radius on the outer corners, constant
wall thickness, a mitered seam where the end panel meets the side walls)
that caps the tailstock end of the two bed rails and gives the tailstock
upright (item 24) its mounting face. `part22_bracket.py`, the original
Blender attempt, modeled it as a solid box-section bar and flagged its own
uncertainty about this ("a hint of a second fold line ... suggesting it may
actually be an open C-channel"). `part22_sheetmetal.py` resolves that by
rebuilding it as an actual bent-sheet solid in FreeCAD: an open-top
U-channel trough (the SheetMetal "base wall" feature, matching the rails'
own folded-channel profile) closed at the far end by a wall folded up from
all three open edges in one auto-mitered "Wall" (bend) feature, with two
bolt holes cut through the raised end face.

**Not a measured part** — pixel-scaled off the M8 bolt heads visible in the
photo and quantized to clean numbers, see the dimension table at the top of
`part22_sheetmetal.py` for the source tag on every number (`photo-est` vs
`assumption`). The third fastener visible low in the trough in the photo
(probably item 48) wasn't modeled; its geometry wasn't legible enough to
reconstruct with any confidence. `worksheet.md` in this folder is where real
measurements/tracings go once captured — once it's filled in, the plan is to
rebuild `part22_sheetmetal.py` panel-by-panel from traced sketch geometry
and measured bend angles/radii, retagging the dimension table `"measured"`.

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
boolean feature) silently no-ops against a SheetMetal `Part::FeaturePython`
Base — it recomputes without error but removes no material, even though the
identical boolean succeeds when called directly on the shape geometry
(`shape.cut(tool)`). `part22_sheetmetal.py`'s bolt holes are cut with the
direct-geometry form for this reason (see the comment at that point in the
script) — not parametric the way a `Part::Cut` tree node would be, but
correct. Not chased further; worth re-testing if this is ever rebuilt against
a different FreeCAD/OCCT build.

## Rebuild

```bash
freecadcmd part22_sheetmetal.py         # writes .FCStd + .step, prints the dimension table
freecadcmd part22_sheetmetal_isosvg.py  # writes part22_sheetmetal_iso.svg
rsvg-convert -b white part22_sheetmetal_iso.svg -o part22_sheetmetal_iso.png
```

(run from this directory; both scripts resolve paths relative to themselves)
