# Measurement worksheet — part #___

Copy this file to `parts/<N>/worksheet.md` and fill in (see `README.md` in
this directory for the full per-part folder layout: `traces/`, build
scripts, FreeCAD documents, etc. all live alongside it). See `README.md`
also for the tracing/measuring technique. Leave a cell blank rather than
guessing — blank means "not captured yet," a guess here defeats the point
of measuring.

- **Part / exploded-view item #**:
- **Date measured**:
- **Measured by**:

## Panels

One row per lettered panel (A, B, C…). `Trace file` is the scanned/photo
filename in this folder. **Trace the true outline** — if a corner is rounded
or chamfered, follow that curve/bevel in the tracing rather than squaring it
off; it gets fit directly from the scan, see Panel corner features below.

| Letter | Description (e.g. "bottom", "left side wall") | Trace file | Notes |
|---|---|---|---|
| A | | | |
| B | | | |

## Panel corner features

Rounded or chamfered corners *within* a panel's own outline (not a bend
between two panels — that's the Bends table below). These should already be
visible in the panel's tracing if it was traced accurately; this table is
just to flag which corners have them and record a cross-check value.

| Panel | Corner (e.g. "top-left") | Type (rounded / chamfered) | Radius or chamfer size (mm) | How measured |
|---|---|---|---|---|
| A | | | | traced / radius gauge / calipers |

## Material

| Property | Value | How measured |
|---|---|---|
| Thickness (mm) | | calipers, at [where] |

## Bends

One row per seam between two panels. Inside radius is the curved transition
at the fold — use a radius gauge, or the sagitta trick (measure a chord
length `c` and its midpoint height `h` off the curve with calipers/ruler,
radius = `h/2 + c^2/(8h)`) if you don't have a gauge set.

| Bend ID | Panels joined | Angle (deg) | Inside radius (mm) | Notes |
|---|---|---|---|---|
| 1 | A-B | | | |

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
