# Measurement worksheet — part #22

See `../README.md` for the tracing/measuring technique. Leave a cell blank
rather than guessing — blank means "not captured yet," a guess here defeats
the point of measuring.

- **Part / exploded-view item #**: 22 (bracket beside the tailstock upright;
  see `part22_sheetmetal.py`'s docstring, in this folder, for why it's *not*
  the "Headstock" the manual's own parts list calls it)
- **Date measured**:
- **Measured by**:

## Panels

One row per lettered panel (A, B, C…). `Trace file` is the scanned/photo
filename in this folder. The `part22_sheetmetal.py` reconstruction guessed
at a bottom + two side walls + a raised end panel — listed below as a
*labeling suggestion only*, to save you inventing letters from scratch. It's
not a confirmed panel breakdown; relabel/add/split rows to match what the
real part actually turns out to be (it may not even be the same number of
panels — e.g. the end could be one panel or two, or welded from a separate
piece entirely).

| Letter | Description (e.g. "bottom", "left side wall") | Trace file | Notes |
|---|---|---|---|
| A | bottom of trough | | |
| B | side wall — **not a plain rectangle**, confirmed 2026-08-09: a tapered/wedge panel — flat top flange (2 holes) → tapered wall, wider at top → flat bottom flange (2 holes), narrower than the top flange. `part22_sheetmetal.py` wrongly modeled this as a flat rectangle; needs a rebuild once this row has real numbers. | `part22_panelB_trace_paper.jpg` (tracing, photo not scan — see note below), `part22_panelB_trace_realpart.jpg`, `part22_panelB_trace_comparison.jpg` | Photo-est reading (pixel-measured off the mat's printed grid, NOT a 1:1 scan): top flange ~67mm wide x ~7-10mm tall; tapered wall ~66mm wide at top narrowing to ~54mm wide at bottom, ~30-35mm tall; bottom flange ~54mm wide x ~12-15mm tall. **Treat as rough scale only** — rescan at 1:1 (no "fit to page") for real geometry, per `../README.md`. |
| C | other side wall — presumed mirror of B (tapered the same way) but not confirmed; could differ | | if C isn't a mirror of B, trace it separately rather than assuming |
| D | raised end panel (tailstock-post mounting face) | | |

**Trace the true outline** — you flagged rounded/chamfered panel corners on
this part, so follow those curves/bevels in the tracing rather than
squaring them off; log which corners in the table below.

## Panel corner features

| Panel | Corner (e.g. "top-left") | Type (rounded / chamfered) | Radius or chamfer size (mm) | How measured |
|---|---|---|---|---|
| | | | | traced / radius gauge / calipers |

## Material

| Property | Value | How measured |
|---|---|---|
| Thickness (mm) | | calipers, at [where] |

## Bends

One row per seam between two panels. Rows below match the guessed A/B/C/D
panels above — add, remove, or relabel to match reality. Inside radius is
the curved transition at the fold (you flagged bend-line fillets on this
part) — radius gauge, or the sagitta trick (chord length `c` and midpoint
height `h` off the curve, radius = `h/2 + c^2/(8h)`) if you don't have one.

| Bend ID | Panels joined | Angle (deg) | Inside radius (mm) | Notes |
|---|---|---|---|---|
| 1 | A-B | | | |
| 2 | A-C | | | |
| 3 | A-D | | | |
| 4 | B-D | | | |
| 5 | C-D | | | |

## Holes

| Hole ID | Panel | Diameter (mm) | Position (ref. to a panel corner/edge) | Notes |
|---|---|---|---|---|
| 1 | A | | | |
| 2 | B, top-left | | | round in photo |
| 3 | B, top-right | | | round in photo |
| 4 | B, bottom-left | | | photo suggests this one may not be round (square/hex?) — worth a close look, could be a carriage-bolt seat |
| 5 | B, bottom-right | | | round in photo |

## Fasteners (photo-est, pixel-measured off the mat's printed grid — real error margin, confirm with calipers)

From `part22_fasteners_tailstock_1.jpg` / `_2.jpg`, described as the fasteners found at the tailstock end (presumably the ones through panel B/C and/or the bolts noted elsewhere in this worksheet — confirm which holes these actually belong to).

| Item | Reading | Likely standard size |
|---|---|---|
| Bolt | shank ⌀ ≈ 5.5–5.8mm, length ≈ 86mm, head across-corners ≈ 15mm | Shank points to **M6**; head-corner reading points closer to M8 — these disagree, a caliper across the shank (not the head, which has more photo parallax error) settles it |
| Washer 1 | OD ≈ 13.1mm, ID ≈ 6.6mm | bore consistent with M6 |
| Washer 2 | OD ≈ 15.3mm, ID ≈ 6.5mm | bore consistent with M6 |
| Ring 3 | OD ≈ 13.1mm, ID ≈ 6.8mm | possibly a split lock washer — couldn't tell from the photo whether it has a split, please confirm |
| Nut | across-flats ≈ 14.5mm | noisy reading, roughly M8-ish AF — worth confirming against the bolt shank size directly (it should thread onto it) |

## Overall envelope (cross-check)

| Dimension | Value (mm) | How measured |
|---|---|---|
| Length | | tape measure |
| Width | | tape measure |
| Height | | tape measure |

## Other notes

(Anything that doesn't fit the tables above — asymmetry, damage, a fastener
that couldn't be measured, etc.)
