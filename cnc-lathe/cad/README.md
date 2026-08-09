# cad/ — FreeCAD model of the Central Machinery 36066 lathe

Rough 3D model of the existing benchtop wood lathe (Central Machinery /
Harbor Freight SKU# S36066, "14" x 40" Wood Lathe w/7" Disc"), built as the
foundation for designing a CNC addition (powered Z carriage, spindle
encoder / C-axis, X/Z cross-slide). Built with FreeCAD's Part workbench
(plain solids + booleans, not Arch/BIM — this is a machine, not a building).

**This is a rough-out, not a measured model.** See "What's real vs.
estimated" below before trusting any specific number.

## Files

| File | What |
|---|---|
| `lathe.py` | The build script — regenerates the whole model from the source-tagged dimension table at its top. Authoritative source. Prints the dimension table, envelope-closure checks, and the measurement request list every time it runs. |
| `lathe.FCStd` | The FreeCAD document (open this in the FreeCAD GUI). |
| `lathe.step` | STEP export of every part, for use in other CAD tools. |
| `lathe_iso.svg` / `lathe_iso.png` | Shaded isometric preview, rendered headlessly from the model geometry. |
| `_isosvg.py` | Helper that renders `lathe_iso.svg` from `lathe.FCStd` (adapted from `basement-remodel/cad/_isosvg.py`). |
| `part22_bracket.py`, `.blend`, `.stl`, `_iso.png` | First attempt at reconstructing exploded-view part #22 (see below), done in Blender as a solid box-section bar — kept for history, superseded in spirit (not deleted) by the SheetMetal version once the reference photo made clear the part is folded sheet, not solid tube. |
| `part22_sheetmetal.py` | Build script for the SheetMetal-workbench reconstruction of part #22. Same dimension-table convention as `lathe.py`. |
| `part22_sheetmetal.FCStd` / `.step` | The FreeCAD document and STEP export. |
| `part22_sheetmetal_iso.svg` / `.png` | Headless isometric preview (see `part22_sheetmetal_isosvg.py`). |

### Part #22 — sheet metal reconstruction

`PXL_20260808_133251586.jpg` (in `../`) shows the exploded-view's part #22 in
the flesh: a folded-sheet bracket (visible bend radius on the outer corners,
constant wall thickness, a mitered seam where the end panel meets the side
walls) that caps the tailstock end of the two bed rails and gives the
tailstock upright (item 24) its mounting face. `part22_bracket.py`, the
original Blender attempt, modeled it as a solid box-section bar and flagged
its own uncertainty about this ("a hint of a second fold line ... suggesting
it may actually be an open C-channel"). `part22_sheetmetal.py` resolves that
by rebuilding it as an actual bent-sheet solid in FreeCAD: an open-top
U-channel trough (the SheetMetal "base wall" feature, matching the rails' own
folded-channel profile) closed at the far end by a wall folded up from all
three open edges in one auto-mitered "Wall" (bend) feature, with two bolt
holes cut through the raised end face. Same epistemic status as
`part22_bracket.py`: **not a measured part** — pixel-scaled off the M8 bolt
heads visible in the photo and quantized to clean numbers, see the dimension
table at the top of `part22_sheetmetal.py` for the source tag on every
number (`photo-est` vs `assumption`). The third fastener visible low in the
trough in the photo (probably item 48) wasn't modeled; its geometry wasn't
legible enough to reconstruct with any confidence.

#### Sheet metal workbench

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

Rebuild:
```bash
freecadcmd cad/part22_sheetmetal.py         # writes .FCStd + .step, prints the dimension table
freecadcmd cad/part22_sheetmetal_isosvg.py  # writes part22_sheetmetal_iso.svg
rsvg-convert -b white cad/part22_sheetmetal_iso.svg -o cad/part22_sheetmetal_iso.png
```

## Rebuild

```bash
freecadcmd cad/lathe.py       # writes lathe.FCStd + lathe.step, prints the dimension table
freecadcmd cad/_isosvg.py     # writes lathe_iso.svg from the .FCStd
convert -background white cad/lathe_iso.svg cad/lathe_iso.png   # optional PNG for quick viewing
```

Uses the AppImage FreeCAD install described in this account's `freecad`
skill (`freecadcmd`/`freecad` on `PATH`). To look at the model instead of
just its flat preview, use that skill's `launch-local.sh cad/lathe.FCStd`
(GUI, local sessions only) — the real GUI resolves the cylindrical/tapered
parts correctly, unlike the painter's-algorithm SVG preview.

## Coordinate system

Not a building — there's no floor plane, and the machine currently has no
permanent bench mount (it's sitting loose in the workshop, see the
reference photos). Datums instead follow the two surfaces a CNC addition
actually needs to reference:

- `x` = along the bed. `0` = spindle nose face (front of the headstock,
  where a faceplate/drive center mounts). `+x` runs toward the tailstock.
  This is the CNC Z-carriage's travel axis — note the letter mismatch with
  CNC "Z" naming, it's intentional (FreeCAD's x is not the machine's Z),
  don't let it cause confusion in the carriage design later.
- `y` = across the bed, horizontal. `0` = spindle centerline / lathe
  centerline.
- `z` = vertical. `0` = bed-rail top surface (what a Z-carriage would ride
  on). The spindle centerline sits at `z = 7.0"` — derived exactly from the
  manual's "14" swing over bed" spec (swing / 2), not a guess.
- Authored in inches, converted to FreeCAD's native mm (`× 25.4`).

## What's real vs. estimated

Every dimension in `lathe.py` carries a `source` tag (see the module
docstring for the full legend: `manual-spec`, `nameplate`, `bearing-std-*`,
`taper-std-mt2`, `thread-std-unc`, `web-forum`, `DERIVED`, `photo-est`).
About a dozen values are exact (manual specs, the two bearing/taper/thread
standards); everything else is a proportion guessed from the 14 reference
photos in `../` with **no scale reference in any of them** — those parts'
FreeCAD `Label` ends in `_EST` so it's obvious in the model tree, and the
isometric preview tints them orange for the same reason.

The build script asserts, every run, that the `photo-est` sub-lengths sum
back to the manual's overall-envelope numbers (63-3/4" length, 15" height,
40" between centers) within a few inches of tolerance — this is the main
defense against an estimate that's not just imprecise but actually wrong.
If you change an estimate and the build starts raising `AssertionError`,
that's the check doing its job; adjust a neighboring estimate to close the
envelope again rather than loosening the tolerance.

## Measurement list (what to bring calipers/tape to in the workshop for)

Generated fresh by every `freecadcmd cad/lathe.py` run (see its
"MEASUREMENT REQUEST LIST" output for the complete, current set — this is
the prioritized summary):

1. **Bed rails** — cross-section profile (it's a lipped/C-channel, not a
   plain bar as currently modeled: width, height, wall thickness) and
   center-to-center spacing between the two rails. This is the Z-carriage's
   travel surface, so it's the single highest-value measurement here.
2. **Banjo / tool-rest holder** — footprint, the clamp-block dimensions
   underneath the rails, and tool-rest post diameter. Likely mounting point
   for an X cross-slide.
3. **Headstock housing** — overall envelope, and rear-face clearance behind
   the pulley cover (spindle-encoder mounting space).
4. **Tailstock casting** — overall envelope and base/clamp footprint.
5. **Spindle bore** — through-bored or not, and diameter if so (relevant
   for wiring or a through-spindle encoder trigger). Not visible in any
   current photo.
6. **Mounting** — bolt pattern (if any) on the headstock/bed-base
   underside, and current bench height, for planning the CNC electronics
   enclosure and cable routing.

Update the corresponding constants in `lathe.py` (with the measurement as
the new `source` tag, e.g. `"measured-2026-08-10"`) once these are in hand,
then re-run the build — the envelope-closure assertions will immediately
flag if a new measurement contradicts the manual's overall-envelope specs.

## Notes for whoever works on this next

- **Offscreen GUI rendering does not work on this machine** — same
  constraint as `basement-remodel`, see that repo's `cad/README.md` and
  this account's `freecad` skill for why. `_isosvg.py`'s painter's-algorithm
  approach (tessellate every face, cull, paint far-to-near) is the
  headless-friendly substitute; unlike `basement-remodel`'s version it
  tessellates curved faces too, since roughly half this model's parts are
  cylindrical (spindle, quill, tailstock handwheel, banjo post) rather than
  Arch's all-planar wall/floor faces.
- The sanding-disc subsystem (manual parts 34–46: disc, worktable, angle
  gauge, miter gauge) is deliberately modeled as one low-fidelity block —
  it's not on the Z-carriage/C-axis/X-cross-slide motion path the CNC
  addition needs, so fidelity was spent elsewhere.
- See the "FreeCAD model of the Central Machinery 36066 lathe" entry in
  `../../design-notes.md` for the decision to build this and why.
