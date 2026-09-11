"""
Central Machinery (Harbor Freight) SKU# S36066, 14" x 40" wood lathe --
exploded-view part #22, the tailstock-end bed riser bracket.

Rebuilt 2026-08-12 from the photographic evidence. This is the FOURTH attempt
at this part; the first three (part22_bracket.py, part22_sheetmetal.py,
part22_panelB.py) were deleted 2026-08-10 for being confident-looking models
built on numbers that turned out to be ~2x off with the taper backwards. This
one is built from a fresh read of the same photos and is STILL NOT MEASURED --
see "Accuracy" below before trusting any number in it.

WHAT THE PART IS
----------------
One piece of sheet steel, one flat blank, two parallel bends of the SAME hand
-- a channel / C-section. It stands at the tailstock end of the lathe bed: the
narrow flange bolts up under the bed, the tapered web carries the load
straight down, the wide flange bolts to the stand. Wide at the bottom, narrow
at the top, which is what you would draw if you wanted a stable footprint and
a compact joint at the bed.

      narrow flange (2 holes)  .--------
                               |            <- 90 deg bend
                               |
         tapered web           |            (the web is the channel's back)
                               |
                               |            <- 90 deg bend, SAME hand
      wide flange (2 holes)    '-----------

BEND HAND -- corrected 2026-08-12
---------------------------------
Both flanges fold the SAME way. This file originally modelled them folding to
opposite sides (a Z / offset section); Dave has the part in hand and corrected
it. Worth recording *why* the wrong read survived three attempts, because the
evidence was never actually ambiguous:

  traces/part22_panelB_trace_comparison.jpg is near-overhead. In it the web is
  only mildly foreshortened while BOTH flange bands are heavily foreshortened.
  That is a channel opening toward the camera. A Z would show one flange
  foreshortened and the other roughly edge-on. The measurement was there; it
  got argued away in favour of the lower-angle photo, which is genuinely hard
  to read.

This matters more than "it's a mirror image" makes it sound: the flanges are
different depths (33 vs 25) AND different widths (142 vs 207), so the opposite
-hand version is a DIFFERENT PART, not this one flipped over.

Evidence, in order of how much weight it carries:
  traces/part22_panelB_trace_paper.jpg  -- the flat blank, traced onto kraft
      paper and photographed on a printed cm grid. Every linear dimension
      below is pixel-measured off that grid. This is the primary source.
  traces/part22_panelB_trace_realpart.jpg
  traces/part22_panelB_trace_comparison.jpg -- part and tracing side by side,
      near-overhead; this is the one that shows the bend hand.
  ../../PXL_20260808_133255545.jpg -- the part installed on the machine. The
      upper bolt pair and lower bolt pair are ~1.5:1 in spacing, matching the
      105mm / 160mm hole pitches below, with a large vertical drop between
      them and almost no horizontal shift. That is what settles the bend
      angle at ~90 deg (a shallow web would trade drop for reach) and which
      flange is up.
  ../../manual/exploded-view.png -- item #22 at the tailstock end, with #47
      bolts entering it from above. The manual's parts list mislabels #22
      "Headstock"; the diagram's own leader line points at this bracket.

PRIORS USED (inference, not measurement -- see design-notes.md 2026-08-12)
-------------------------------------------------------------------------
  * Top-flange hole diameter: part #47 is the bolt that enters #22 from above
    in the exploded view, and cad/hardware_specs.py has it measured at 8.0mm
    shank on 2026-08-10 -> M8 -> 9.0mm close-fit clearance. This is the one
    hole dimension with a real measurement behind it, one step removed.
  * Inside bend radius: 2.0mm. Air-bent mild steel of thickness t takes an
    inside radius of roughly 1t at minimum on a standard 88-deg die; t=2 was
    given, so r=2. Not measured off the part.
  * K-factor 0.44 for the bend allowance -- the usual mild-steel default.
  * Bottom-flange hole diameter: NO prior. The exploded view calls out #48 and
    #53 in that area and neither has been measured. 9.0mm is a placeholder
    that happens to match the top; do not read it as a finding.

ACCURACY -- READ THIS
---------------------
Thickness (2.0mm) is measured -- 2026-08-10, corroborated from two directions
(Dave gave it, and the superseded part22_bracket.py recorded it independently).
Bend hand was confirmed against the real part. Everything else is photo-est:
the tracing was photographed, not
scanned at 1:1, so there is perspective and lens distortion in the source and
no way to bound it from here. Treat every linear dimension as +/- 3mm and
every hole position as +/- 2mm. The bend allowance math below is carried to
0.01mm because the arithmetic should round-trip, NOT because the part is known
that well.

This is good enough to check fit against the machine, order stock, and argue
about. It is not good enough to cut from. worksheet.md in this folder is still
the thing to fill in.

Deliberately NOT modelled: corner breaks / deburr radii on the sheared edges,
paint thickness (the part is hammertone green, factory powder coat), and the
slight rounding visible at the blank's corners in the tracing.

PARAMETRIC -- IN THIS SCRIPT, NOT IN THE .FCStd
-----------------------------------------------
Every dimension is a dim() call below with its own source tag, per the
convention in cad/hardware_specs.py, and all geometry derives from those.
Derived values (bend allowance, straight leg lengths) are tagged DERIVED and
recomputed here, never typed in. Change a value and re-run and the solid, STEP,
STL, flat pattern, cut list and bend allowances all follow.

The .FCStd is NOT parametric. The spreadsheet inside it is labelled
"Dimensions_REFERENCE_ONLY" because it records provenance and drives nothing:
the model is stored as a plain Part::Feature holding a baked shape, with an
empty ExpressionEngine and no dependencies. Verified 2026-08-13 by setting
width_bottom 207 -> 250 in the sheet and recomputing -- the bounding box did
not move. Making it GUI-parametric would need a constrained Sketcher profile
expression-bound to the sheet plus PartDesign/SheetMetal features; the
SheetMetal add-on is not installed on this machine, which is what killed the
earlier part22_panelB.py.

So: EDIT THIS FILE, then `freecadcmd part22_channel.py`.

Run headless from this directory:   freecadcmd part22_channel.py
Outputs:  part22_channel.FCStd
          part22_channel.step
          part22_channel_flat.svg   <- 1:1 printable blank, for overlaying
                                       on traces/part22_panelB_trace_paper.jpg
Then:     freecadcmd part22_channel_isosvg.py

COORDINATE SYSTEM (final, "as installed" orientation)
  x = across the machine, 0 on the bracket centreline
  y = along the bed; both flanges reach toward -y
  z = up; z=0 is the underside of the wide bottom flange
"""
import math
import os

import FreeCAD as App
import Part

HERE = os.path.dirname(os.path.abspath(__file__))
V = App.Vector

doc = App.newDocument("part22_channel")

# =====================================================================
# DIMENSIONS
# =====================================================================
sheet = doc.addObject("Spreadsheet::Sheet", "Dimensions")
# The label says REFERENCE_ONLY because it is: this sheet records provenance,
# it does NOT drive the model. The solid is baked here in Python and stored as
# a plain Part::Feature with no ExpressionEngine, so editing a cell in the GUI
# and recomputing moves nothing (verified 2026-08-13). Edit this file instead.
sheet.Label = "Dimensions_REFERENCE_ONLY"
for col, head in zip("ABCD", ("name", "value", "source", "note")):
    sheet.set(f"{col}1", head)
sheet.set("F1", "REFERENCE ONLY -- editing these cells does NOT change the geometry.")
sheet.set("F2", "The solid is baked by part22_channel.py. Change a value there and re-run:")
sheet.set("F3", "    freecadcmd part22_channel.py")
_ROW = [1]


def dim(key, value, source, note=""):
    _ROW[0] += 1
    r = _ROW[0]
    sheet.set(f"A{r}", key)
    sheet.set(f"B{r}", str(value))
    sheet.setAlias(f"B{r}", key)
    sheet.set(f"C{r}", source)
    sheet.set(f"D{r}", note)
    return value


# --- material and forming -------------------------------------------
T = dim("thickness", 2.0, "measured-2026-08-10",
        "2mm sheet steel. Given by Dave 2026-08-12, and independently "
        "corroborated: the superseded part22_bracket.py carried "
        "'measured-2026-08-10: stock is 2mm sheet steel, not solid bar'. "
        "That file is deleted -- see git history")
R_IN = dim("bend_radius", 2.0, "assumed-standard",
           "inside radius ~= 1t, typical air bend in mild steel")
K = dim("k_factor", 0.44, "assumption",
        "standard mild-steel default; only affects the flat pattern")
ANGLE = dim("bend_angle", 90.0, "photo-est",
            "both bends; from PXL_20260808_133255545.jpg -- large vertical "
            "drop, negligible horizontal shift between the two bolt pairs")
SAME_HAND = dim("bend_same_hand", 1, "observed-2026-08-12",
                "1 = both flanges fold the same way (channel). Dave checked "
                "the real part 2026-08-12 and corrected an earlier Z-section "
                "read. Set 0 for the opposite-hand (Z) variant")

# --- flat pattern, measured off the kraft-paper tracing --------------
# All four of these are read bend-line-to-bend-line / bend-line-to-edge on
# the flat blank, which is what the tracing actually shows.
FLAT_WEB = dim("flat_web_len", 100.0, "photo-est",
               "bend line to bend line, along the blank")
FLAT_TOP_TAB = dim("flat_top_tab", 33.0, "photo-est",
                   "narrow-end tab: bend line to free edge")
FLAT_BOT_TAB = dim("flat_bot_tab", 25.0, "photo-est",
                   "wide-end tab: bend line to free edge")
W_TOP = dim("width_top", 142.0, "photo-est",
            "blank width at the narrow end; the tab is parallel-sided, the "
            "taper starts at the bend line")
W_BOT = dim("width_bottom", 207.0, "photo-est",
            "blank width at the wide end; tab also parallel-sided")

# --- holes ------------------------------------------------------------
HOLE_D_TOP = dim("hole_d_top", 9.0, "inferred-standard",
                 "M8 close clearance. Part #47 (the bolt entering #22 from "
                 "above in the exploded view) measured 8.0mm shank -- see "
                 "cad/hardware_specs.py, measured-2026-08-10")
HOLE_D_BOT = dim("hole_d_bot", 9.0, "assumption",
                 "PLACEHOLDER. Fastener here is #48/#53, never measured. "
                 "Matching the top is a guess, not a finding")
PITCH_TOP = dim("hole_pitch_top", 105.0, "photo-est", "centre to centre")
PITCH_BOT = dim("hole_pitch_bot", 160.0, "photo-est", "centre to centre")
INSET_TOP = dim("hole_inset_top", 16.0, "photo-est",
                "hole centre back from the flange's free edge")
INSET_BOT = dim("hole_inset_bot", 12.5, "photo-est",
                "hole centre back from the flange's free edge")

# =====================================================================
# DERIVED -- bend allowance and straight leg lengths
# =====================================================================
# The tracing's drawn bend line sits at the middle of the bend, so each tab
# reading contains half a bend allowance that is not straight material.
a = math.radians(ANGLE)
BA = dim("bend_allowance", round(a * (R_IN + K * T), 4), "DERIVED",
         "rad(angle) * (r + k*t), per bend")
LEG_TOP = dim("leg_top", round(FLAT_TOP_TAB - BA / 2.0, 4), "DERIVED",
              "straight narrow flange, bend tangent to free edge")
LEG_BOT = dim("leg_bot", round(FLAT_BOT_TAB - BA / 2.0, 4), "DERIVED",
              "straight wide flange, bend tangent to free edge")
LEG_WEB = dim("leg_web", round(FLAT_WEB - BA, 4), "DERIVED",
              "straight web, tangent to tangent")
BLANK_LEN = dim("blank_length", round(FLAT_TOP_TAB + FLAT_WEB + FLAT_BOT_TAB, 4),
                "DERIVED", "developed length of the flat blank")
doc.recompute()

R_OUT = R_IN + T


# =====================================================================
# GEOMETRY
# =====================================================================
# Built with the web flat in the XY plane (z = 0..T) and the flanges folding
# up out of it, because that is the frame the bend maths is natural in. The
# whole thing gets rotated into the installed orientation at the end.
#
#   y = up the blank; y=0 is the wide-end bend tangent, y=LEG_WEB the narrow
#   z = out of the web's face

def bend_profile(y0, leg, alpha):
    """Closed face for one bend + its flange, in the plane x=0.

    Web lies at y < y0, z in [0, T]. The material rounds through `alpha` and
    the flange runs on for `leg`. Folds toward +z. Returns a Part.Face.
    """
    ang = math.radians(alpha)
    cy, cz = y0, T + R_IN               # bend centre

    def arc_pt(rad, th):
        return V(0.0, cy + rad * math.sin(th), cz - rad * math.cos(th))

    o0, om, o1 = arc_pt(R_OUT, 0.0), arc_pt(R_OUT, ang / 2), arc_pt(R_OUT, ang)
    i0, im, i1 = arc_pt(R_IN, 0.0), arc_pt(R_IN, ang / 2), arc_pt(R_IN, ang)
    d = V(0.0, math.cos(ang), math.sin(ang))      # flange run direction
    o2, i2 = o1 + d * leg, i1 + d * leg
    edges = [Part.Arc(o0, om, o1).toShape(),
             Part.LineSegment(o1, o2).toShape(),
             Part.LineSegment(o2, i2).toShape(),   # free edge, length T
             Part.LineSegment(i2, i1).toShape(),
             Part.Arc(i1, im, i0).toShape(),
             Part.LineSegment(i0, o0).toShape()]   # interface back to the web
    return Part.Face(Part.Wire(Part.__sortEdges__(edges)))


def flange_holes(y0, leg, alpha, inset, pitch, dia):
    """Two cutting cylinders through the flange built by bend_profile()."""
    ang = math.radians(alpha)
    cy, cz = y0, T + R_IN
    rmid = (R_IN + R_OUT) / 2.0
    mid = V(0.0, cy + rmid * math.sin(ang), cz - rmid * math.cos(ang))
    d = V(0.0, math.cos(ang), math.sin(ang))
    n = V(0.0, -math.sin(ang), math.cos(ang))     # normal to the flange face
    centre = mid + d * (leg - inset)
    cuts = []
    for sx in (-1.0, 1.0):
        base = centre + V(sx * pitch / 2.0, 0.0, 0.0) - n * (2.0 * T)
        cuts.append(Part.makeCylinder(dia / 2.0, 4.0 * T, base, n))
    return cuts


# --- web: the tapered trapezoid, flat -------------------------------
web_pts = [V(-W_BOT / 2, 0.0, 0.0), V(W_BOT / 2, 0.0, 0.0),
           V(W_TOP / 2, LEG_WEB, 0.0), V(-W_TOP / 2, LEG_WEB, 0.0)]
web = Part.Face(Part.makePolygon(web_pts + [web_pts[0]])).extrude(V(0, 0, T))

# --- narrow flange: bend at y=LEG_WEB, folds to +z ------------------
top = bend_profile(LEG_WEB, LEG_TOP, ANGLE).extrude(V(W_TOP, 0, 0))
top.translate(V(-W_TOP / 2, 0, 0))
top_holes = flange_holes(LEG_WEB, LEG_TOP, ANGLE,
                         INSET_TOP, PITCH_TOP, HOLE_D_TOP)

# --- wide flange: bend at y=0 ---------------------------------------
# bend_profile() always puts the web on the -y side and folds to +z, so the
# wide flange is built at y0=0 and then spun to sit on the other end of the
# web. WHICH spin sets the bend hand, and it is the one thing on this part
# that was wrong until 2026-08-12:
#
#   same hand (channel, correct): 180 deg about Z. Maps (x,y,z)->(-x,-y,z),
#       so the flange still folds to +z. The prism is symmetric about x=0,
#       so the x flip is a no-op.
#   opposite hand (Z-section):    180 deg about X through z=T/2. Maps
#       (y,z)->(-y,T-z), flipping the fold to -z.
#
# Both are proper rotations, so neither inverts the solid.
if SAME_HAND:
    SPIN_PT, SPIN_AX = V(0, 0, 0), V(0, 0, 1)
else:
    SPIN_PT, SPIN_AX = V(0, 0, T / 2.0), V(1, 0, 0)

bot = bend_profile(0.0, LEG_BOT, ANGLE).extrude(V(W_BOT, 0, 0))
bot.translate(V(-W_BOT / 2, 0, 0))
bot.rotate(SPIN_PT, SPIN_AX, 180)
bot_holes = flange_holes(0.0, LEG_BOT, ANGLE,
                         INSET_BOT, PITCH_BOT, HOLE_D_BOT)
for h in bot_holes:
    h.rotate(SPIN_PT, SPIN_AX, 180)

# --- assemble -------------------------------------------------------
# The three lumps share exact planar faces at y=0 and y=LEG_WEB (the web's
# ends are W_BOT and W_TOP wide, matching the two flange prisms), so the fuse
# is coincident-face clean and removeSplitter() leaves no internal seams.
solid = web.fuse(top).fuse(bot).removeSplitter()
for h in top_holes + bot_holes:
    solid = solid.cut(h)

# Part.cut() hands back a Compound wrapping the result. Unwrap the single solid
# so downstream gets a plain Part::Solid -- STEP/STL/renders don't care, but CAM
# and some meshers are fussy about being handed a compound.
if solid.ShapeType == "Compound" and len(solid.Solids) == 1:
    solid = solid.Solids[0]

# --- into the installed orientation: web up, flanges horizontal -----
solid.rotate(V(0, 0, 0), V(1, 0, 0), 90)          # +y (up the web) -> +z
solid.translate(V(0, 0, -solid.BoundBox.ZMin))    # z=0 at the bracket's foot

obj = doc.addObject("Part::Feature", "Part22Channel_EST")
obj.Label = "Part22Channel_EST"
obj.Shape = solid
doc.recompute()


# =====================================================================
# VERIFY -- a clean fuse is not evidence the shape is right
# =====================================================================
print("=" * 72)
print("part #22 -- tailstock-end bed riser, channel section, 2mm steel")
print("=" * 72)

ok = True


def check(label, got, want, tol):
    global ok
    good = abs(got - want) <= tol
    ok = ok and good
    print(f"  [{'ok' if good else 'FAIL'}] {label:<38} {got:9.3f}  (want {want:.3f})")


# Round-trip the flat pattern out of the formed legs. If the bend-allowance
# bookkeeping has a sign error anywhere, this is what catches it -- a valid
# STEP export would not.
print("\nflat pattern round-trip")
check("developed length", LEG_TOP + BA + LEG_WEB + BA + LEG_BOT, BLANK_LEN, 1e-3)
check("blank width (wide end)", W_BOT, 207.0, 1e-3)
check("blank width (narrow end)", W_TOP, 142.0, 1e-3)

bb = solid.BoundBox
print("\nsolid")
print(f"  valid={solid.isValid()}  closed={solid.isClosed()}  "
      f"type={solid.ShapeType}  solids={len(solid.Solids)}")
if solid.ShapeType != "Solid":
    ok = False
    print("  [FAIL] expected a bare Solid, got", solid.ShapeType)
vol = solid.Volume
sheet_vol = 0.5 * (W_TOP + W_BOT) * FLAT_WEB * T + W_TOP * FLAT_TOP_TAB * T \
    + W_BOT * FLAT_BOT_TAB * T
holes_vol = 2 * math.pi * (HOLE_D_TOP / 2) ** 2 * T \
    + 2 * math.pi * (HOLE_D_BOT / 2) ** 2 * T
# Not a volumetric proof -- the bend corners and the flange holes both make
# this approximate. It is a "did the fuse duplicate or drop a lump" check.
check("no lump lost/duplicated (mm3)", vol, sheet_vol - holes_vol, 0.02 * sheet_vol)

# Bend hand, checked off the geometry rather than trusted. A channel is only
# as deep as its deepest flange; a Z-section is as deep as both put together.
# This is the check that would have caught the 2026-08-12 error.
want_depth = (max(LEG_TOP, LEG_BOT) if SAME_HAND else LEG_TOP + LEG_BOT) + R_OUT
check("depth implies " + ("channel" if SAME_HAND else "Z-section"),
      bb.YLength, want_depth, 0.5)

print("\ninstalled envelope (x across, y along bed, z up)")
print(f"  {bb.XLength:.1f} wide  x  {bb.YLength:.1f} deep  x  {bb.ZLength:.1f} tall  mm")
print(f"  mass @ 7.85 g/cm3: {vol * 7.85e-3:.0f} g")

print("\ncut list")
print(f"  blank: {BLANK_LEN:.0f} x {W_BOT:.0f} mm, {T:.1f}mm steel")
print(f"  bend 1 @ {FLAT_BOT_TAB:.0f}mm from the wide edge, {ANGLE:.0f} deg, r{R_IN:.0f} inside")
print(f"  bend 2 @ {FLAT_TOP_TAB:.0f}mm from the narrow edge, {ANGLE:.0f} deg, r{R_IN:.0f} inside, "
      f"{'SAME hand -- both flanges the same way' if SAME_HAND else 'OPPOSITE hand'}")
print(f"  bend allowance {BA:.2f}mm each (k={K})")
print(f"  4 holes: 2 x d{HOLE_D_TOP:.1f} @ {PITCH_TOP:.0f} pitch, 2 x d{HOLE_D_BOT:.1f} @ {PITCH_BOT:.0f} pitch")


# =====================================================================
# FLAT-PATTERN SVG -- print at 1:1 and lay it on the paper tracing
# =====================================================================
# This is the check that actually discriminates. Three previous attempts at
# this part produced clean STEP files that were the wrong shape; the only
# thing that caught it was putting the geometry next to the real part.
def flat_svg():
    pad = 15.0
    w, h = W_BOT + 2 * pad, BLANK_LEN + 2 * pad

    def p(u, v):                       # blank coords -> svg (v=0 at wide edge)
        return (u + W_BOT / 2 + pad, BLANK_LEN - v + pad)

    outline = [(-W_BOT / 2, 0), (W_BOT / 2, 0),
               (W_BOT / 2, FLAT_BOT_TAB), (W_TOP / 2, FLAT_BOT_TAB + FLAT_WEB),
               (W_TOP / 2, BLANK_LEN), (-W_TOP / 2, BLANK_LEN),
               (-W_TOP / 2, FLAT_BOT_TAB + FLAT_WEB), (-W_BOT / 2, FLAT_BOT_TAB)]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" '
         f'viewBox="0 0 {w:.2f} {h:.2f}" font-family="Arial">',
         f'<rect width="{w:.2f}" height="{h:.2f}" fill="#fff"/>',
         '<polygon points="%s" fill="none" stroke="#000" stroke-width="0.5"/>'
         % " ".join("%.2f,%.2f" % p(u, v) for u, v in outline)]
    hand = "same hand" if SAME_HAND else "opposite hand"
    for v, lbl in ((FLAT_BOT_TAB, f"bend 1 - up ({hand})"),
                   (FLAT_BOT_TAB + FLAT_WEB, f"bend 2 - up ({hand})")):
        half = (W_BOT if v == FLAT_BOT_TAB else W_TOP) / 2
        x0, y0 = p(-half, v)
        x1, _ = p(half, v)
        o.append(f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y0:.2f}" '
                 f'stroke="#c00" stroke-width="0.4" stroke-dasharray="4 2"/>')
        o.append(f'<text x="{x1 + 1:.2f}" y="{y0:.2f}" font-size="3" fill="#c00">{lbl}</text>')
    for u, v, d in ((-PITCH_BOT / 2, INSET_BOT, HOLE_D_BOT),
                    (PITCH_BOT / 2, INSET_BOT, HOLE_D_BOT),
                    (-PITCH_TOP / 2, BLANK_LEN - INSET_TOP, HOLE_D_TOP),
                    (PITCH_TOP / 2, BLANK_LEN - INSET_TOP, HOLE_D_TOP)):
        cx, cy = p(u, v)
        o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{d / 2:.2f}" '
                 f'fill="none" stroke="#000" stroke-width="0.4"/>')
    o.append(f'<text x="{pad:.2f}" y="{pad - 4:.2f}" font-size="4">'
             f'part #22 blank -- {BLANK_LEN:.0f} x {W_BOT:.0f} x {T:.1f}mm -- '
             f'both bends the SAME way -- PHOTO-EST, print at 1:1</text>')
    o.append('</svg>')
    return "\n".join(o)


with open(os.path.join(HERE, "part22_channel_flat.svg"), "w") as fh:
    fh.write(flat_svg())
print("\nWROTE part22_channel_flat.svg")

doc.saveAs(os.path.join(HERE, "part22_channel.FCStd"))
Part.export([obj], os.path.join(HERE, "part22_channel.step"))
print("WROTE part22_channel.FCStd, part22_channel.step")

# Mesh export, so the render pipeline (part22_channel_blender.py) consumes the
# SAME geometry rather than re-modelling it by hand -- a second hand-built copy
# is a second source of truth, and this part has already been wrong twice.
try:
    import MeshPart
    mesh = MeshPart.meshFromShape(Shape=solid, LinearDeflection=0.05,
                                  AngularDeflection=0.12, Relative=False)
    mesh.write(os.path.join(HERE, "part22_channel.stl"))
    print("WROTE part22_channel.stl (%d facets)" % mesh.CountFacets)
except ImportError:
    import Mesh
    Mesh.export([obj], os.path.join(HERE, "part22_channel.stl"))
    print("WROTE part22_channel.stl (default tessellation)")
print("\nRESULT:", "all checks passed" if ok else "CHECKS FAILED -- do not trust this model")
