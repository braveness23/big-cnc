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
| B | left side wall | | |
| C | right side wall | | |
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

## Overall envelope (cross-check)

| Dimension | Value (mm) | How measured |
|---|---|---|
| Length | | tape measure |
| Width | | tape measure |
| Height | | tape measure |

## Other notes

(Anything that doesn't fit the tables above — asymmetry, damage, a fastener
that couldn't be measured, etc.)
