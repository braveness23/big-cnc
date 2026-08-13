# part22/ — exploded-view part #22

The bracket beside the tailstock upright. The manual's own parts list
mislabels this item "Headstock" on p.10 — the diagram's own leader line for
#22 actually points at this bracket, not the headstock casting (see
`manual/exploded-view.png`). Both CAD attempts made so far (now removed,
see below) followed the diagram's leader line, not its label.

## Files

| File | What |
|---|---|
| `worksheet.md` | Measurement worksheet — fill in as real measurements (calipers/tape) come in. See `../README.md` for the capture protocol. |
| `traces/` | Scanned/photographed panel tracings and reference photos. Raw evidence, kept regardless of CAD status. |
| `part22_channel.py` | Fourth CAD attempt, 2026-08-12. Still photo-est, ±3mm — see its docstring. Builds `.FCStd` + `.step` + a 1:1 printable flat pattern. |
| `part22_channel_isosvg.py` | Headless isometric render of the above (no GL on this box). |

## Status: one model, still unmeasured

**2026-08-12** — `part22_channel.py` is a fresh reconstruction from the same
photos, on Dave's given assumption of 2mm steel. It reads the part as a
**channel / C-section**, not a trough and not a Z: a single blank,
158 x 207mm, two 90° bends of the *same* hand, narrow flange (142mm, 2 holes
@ 105) up to the bed, wide flange (207mm, 2 holes @ 160) down to the stand.
Formed envelope 207 x 35 x 103mm, ~430g.

That is roughly **2x larger than the deleted attempts, with the taper the
other way round** — the earlier numbers were misread off the same tracing.
Print `part22_channel_flat.svg` at 1:1 and lay it on
`traces/part22_panelB_trace_paper.jpg` before believing anything here; that
overlay is the check the previous three attempts never got.

**Bend hand was wrong on the first pass and Dave corrected it** against the
real part on 2026-08-12 — the model had both flanges folding to opposite
sides. Worth recording that the evidence was never actually ambiguous:
`traces/part22_panelB_trace_comparison.jpg` is near-overhead, and in it the
web is only mildly foreshortened while *both* flange bands are heavily
foreshortened. That is a channel opening toward the camera. This folder's
own earlier notes (and the deleted `part22_panelB.py` docstring) also assert
"folded to opposite sides" — that claim came from the lower-angle photo and
should be treated as retracted.

Still unresolved: **the bottom-flange hole diameter.** The exploded view
calls out #48/#53 there and neither has been measured. Ø9 in the model is a
placeholder. The *top* flange holes do trace to a measurement (part #47,
8.0mm shank, `cad/hardware_specs.py`) → M8 → Ø9 clearance.

Everything below is the 2026-08-10 write-up of why those three were deleted.
It still applies: **none of this is measured.**

## Why the first three attempts were deleted

Three CAD reconstruction attempts were made (Blender solid bar → FreeCAD
box/trough → FreeCAD tapered-wedge panel) and all three were deleted
2026-08-10 — every one of them was a photo-est guess, none were ever
measured, and the third one's own numbers turned out to be contradicted by
a more careful re-trace of the same source photo (roughly 2x off, taper
direction backwards). Confident-looking `.FCStd`/`.step` files built from
guessed numbers were doing more harm than good sitting in this folder next
to real photos. All three are still in git history if a starting point is
ever wanted again — they are not gone, just not live files.

**What's actually solid**: the topology guess that this is a tapered wedge
panel with two flanges folded ~~to opposite sides~~ (not a rectangular box) —
that came from the photo tracing and looks right. What's not solid: every
single dimension. None of this is ready to model until real measurements
land in `worksheet.md`.

> **Retracted 2026-08-12** — "folded to opposite sides" is wrong; both
> flanges fold the same way. See the status section above.

## Re-numbering, once real measurements exist

`part22_channel.py` is set up so this is an edit, not a rebuild: every
dimension is a `dim(name, value, source, note)` call at the top of the file
with its own source tag, and the geometry is derived from those. Update the
values from `worksheet.md`, re-run, and the flat pattern, cut list, bend
allowances and STEP all follow.

> **The `.FCStd` itself is NOT parametric — edit the `.py`, not the GUI.**
> The model is a plain `Part::Feature` holding a baked shape: empty
> `ExpressionEngine`, no dependencies. The spreadsheet inside is labelled
> `Dimensions_REFERENCE_ONLY` because it records provenance and drives
> nothing. Verified 2026-08-13 — setting `width_bottom` 207 → 250 in the
> sheet and recomputing left the bounding box at 207.0. Making it
> GUI-parametric needs a constrained Sketcher profile expression-bound to
> the sheet plus PartDesign/SheetMetal features, and the SheetMetal add-on
> isn't installed here (that's what killed `part22_panelB.py`).

What to measure first, in order of how much it would change:
`bend_angle` (assumed 90°) · `thickness` (given as 2mm, never calipered) ·
`hole_d_bot` · then the linear dimensions. (`bend_same_hand` is settled —
Dave checked the real part.)

Note it deliberately does **not** use
[shaise/FreeCAD_SheetMetal](https://github.com/shaise/FreeCAD_SheetMetal),
which the deleted `part22_panelB.py` depended on. That add-on isn't
installed on this box and isn't bundled with FreeCAD, so the model is built
from plain `Part` primitives instead — three prisms sharing exact coincident
faces, fused, then `removeSplitter()`. The bend allowance is computed
explicitly (k-factor, tagged `DERIVED`) rather than delegated, and the
script round-trips the flat pattern back out as a self-check.
