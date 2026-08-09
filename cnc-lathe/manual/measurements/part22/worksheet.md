# Measurement worksheet — part #22

See `../README.md` for the tracing/measuring technique. Leave a cell blank
rather than guessing — blank means "not captured yet," a guess here defeats
the point of measuring.

- **Part / exploded-view item #**: 22 (bracket beside the tailstock upright;
  see `cnc-lathe/cad/part22_sheetmetal.py`'s docstring for why it's *not*
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

## Material

| Property | Value | How measured |
|---|---|---|
| Thickness (mm) | | calipers, at [where] |

## Bends

One row per seam between two panels. Rows below match the guessed A/B/C/D
panels above — add, remove, or relabel to match reality.

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
