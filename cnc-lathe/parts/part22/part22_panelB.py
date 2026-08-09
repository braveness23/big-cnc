"""
Central Machinery (Harbor Freight) SKU# S36066 lathe -- FreeCAD SheetMetal
reconstruction of exploded-view part #22, panel B (see worksheet.md).

THIS SUPERSEDES part22_sheetmetal.py's shape, not just its numbers. That
script modeled part #22 as a rectangular open-top box (flat bottom + two
flat vertical side walls + a folded end cap) -- a guess made from a single
angled, unscaled reference photo. The 2026-08-09 paper tracing + photos of
the real part (traces/part22_panelB_trace_*.jpg) showed that guess was
wrong in *shape*, not just dimensions: one of the "side walls" isn't a flat
rectangle at all -- it's a tapered wedge panel bent into a stepped ("Z")
bracket:
  - a flat top flange (2 holes) that bolts to something ~67mm wide
  - a tapered web, narrowing from 67mm down to 54mm over its height
  - a flat bottom flange (2 holes), narrower than the top, bolting to
    something ~54mm wide
  - the two flanges fold to OPPOSITE sides of the web (matching the real
    part's photo: it sits with both flanges roughly parallel, offset from
    each other, not both folded the same way)
part22_sheetmetal.py's box/trough/end-cap topology is kept for history (not
deleted, same as part22_bracket.py before it) but is now ALSO believed
wrong, not just unmeasured -- see README.md, this folder.

STILL NOT A MEASURED PART. Every number here is the *photo-est* reading
logged in worksheet.md (pixel-measured off the mat's printed grid in the
tracing photos, not a 1:1 scan) -- real, but rough: this is a "does the
silhouette now look like the real part" pass, not a build-ready model. In
particular:
  - Fold direction/angle for each flange is a guess (both look folded ~90
    deg in the photo, opposite senses, but the photo doesn't nail down
    which way is "up" in the real assembly).
  - Hole positions are inset from the flange edges by eye off the photo,
    not the traced hole centers -- the tracing has real poked-through hole
    marks in it that haven't been digitized yet.
  - Whether the *other* side wall (panel C) is really a mirror image of
    this one is unconfirmed (see worksheet.md) -- not modeled here, this
    file is panel B alone.
  - How this panel actually connects to the rest of part #22 (a bottom
    panel? directly to the bed rails?) is unconfirmed and not modeled.

PARAMETRIC / TUNABLE: same convention as part22_sheetmetal.py -- every
dimension lives in the "Dimensions" spreadsheet inside part22_panelB.FCStd,
and the sketch + SheetMetal features are expression-bound to those cells.
Bolt holes are a raw shape boolean, not a parametric Part::Cut, for the
same reason documented in README.md ("Known quirk") -- edit hole_x/hole_y/
hole_d and re-run the script; a bare GUI recompute won't move them.

Run headless (from this directory):  freecadcmd part22_panelB.py
Outputs:       part22_panelB.FCStd, part22_panelB.step
Then:          freecadcmd part22_panelB_isosvg.py

Coordinate system (local to this part):
  x = across the panel (width, at any given height)
  y = up the panel's own flattened length, 0 at the bottom edge of the
      tapered web (NOT the bottom flange -- the flanges extend past 0 and
      past taper_height on either end)
  z = out of the web's flat face; the two flanges fold to +z and -z
      respectively
"""
import os
import sys

import FreeCAD
import Part
import Sketcher

HERE = os.path.dirname(os.path.abspath(__file__))

try:
    import SheetMetalBaseCmd
    import SheetMetalCmd
except ImportError:
    sys.path.insert(0, os.path.join(HERE, "SheetMetal"))
    import SheetMetalBaseCmd
    import SheetMetalCmd

doc = FreeCAD.newDocument("part22_panelB")

# =====================================================================
# DIMENSIONS -- see part22_sheetmetal.py for why this is a spreadsheet
# and not just Python constants (GUI-tunable: edit a cell, recompute).
# =====================================================================
sheet = doc.addObject("Spreadsheet::Sheet", "Dimensions")
sheet.set("A1", "name")
sheet.set("B1", "value")
sheet.set("C1", "source")
sheet.set("D1", "note")
_DIM_ROW = [1]


def dim(key, value, source, note=""):
    _DIM_ROW[0] += 1
    row = _DIM_ROW[0]
    sheet.set(f"A{row}", key)
    sheet.set(f"B{row}", str(value))
    sheet.setAlias(f"B{row}", key)
    sheet.set(f"C{row}", source)
    sheet.set(f"D{row}", note)
    return value


BOTTOM_WIDTH = dim("bottom_width", 54.0, "photo-est",
                    "width at the bottom of the tapered web, from the tracing")
TOP_WIDTH = dim("top_width", 67.0, "photo-est",
                 "width at the top of the tapered web, from the tracing")
TAPER_HEIGHT = dim("taper_height", 32.0, "photo-est", "height of the tapered web")
TOP_FLANGE_H = dim("top_flange_h", 8.0, "photo-est", "top flange fold length")
BOTTOM_FLANGE_H = dim("bottom_flange_h", 13.0, "photo-est", "bottom flange fold length")
THICKNESS = dim("thickness", 3.0, "assumption",
                 "carried over from part22_sheetmetal.py's assumption, not remeasured")
BEND_RADIUS = dim("bend_radius", 3.0, "assumption", "~1x thickness, typical press-brake minimum")
HOLE_D = dim("hole_d", 8.5, "photo-est",
             "M8 clearance, carried over from part22_sheetmetal.py -- but the "
             "2026-08-09 fastener photos actually read closer to M6 (see "
             "worksheet.md); unresolved, needs a caliper check on an actual bolt shank")
HOLE_TOP_X = dim("hole_top_x", 20.0, "assumption", "top-flange hole offset from centerline, eyeballed")
HOLE_BOTTOM_X = dim("hole_bottom_x", 15.0, "assumption", "bottom-flange hole offset from centerline, eyeballed")
doc.recompute()

print("=" * 70)
print("part22_panelB.py -- dimension table (all photo-est/assumption, NOT measured)")
for row in range(2, _DIM_ROW[0] + 1):
    key = sheet.get(f"A{row}")
    print(f"  {key:20s} = {sheet.get(f'B{row}'):>8}  [{sheet.get(f'C{row}')}]  ({sheet.get(f'D{row}')})")
print("=" * 70)

# --- tapered web: flat trapezoid plate, base of the panel ---
core = doc.addObject("Sketcher::SketchObject", "CoreProfile")
bw2, tw2 = BOTTOM_WIDTH / 2.0, TOP_WIDTH / 2.0
gBot = core.addGeometry(Part.LineSegment(FreeCAD.Vector(-bw2, 0, 0), FreeCAD.Vector(bw2, 0, 0)), False)
gRight = core.addGeometry(Part.LineSegment(FreeCAD.Vector(bw2, 0, 0), FreeCAD.Vector(tw2, TAPER_HEIGHT, 0)), False)
gTop = core.addGeometry(Part.LineSegment(FreeCAD.Vector(tw2, TAPER_HEIGHT, 0),
                                          FreeCAD.Vector(-tw2, TAPER_HEIGHT, 0)), False)
gLeft = core.addGeometry(Part.LineSegment(FreeCAD.Vector(-tw2, TAPER_HEIGHT, 0), FreeCAD.Vector(-bw2, 0, 0)), False)
core.addConstraint(Sketcher.Constraint("Coincident", gBot, 2, gRight, 1))
core.addConstraint(Sketcher.Constraint("Coincident", gRight, 2, gTop, 1))
core.addConstraint(Sketcher.Constraint("Coincident", gTop, 2, gLeft, 1))
core.addConstraint(Sketcher.Constraint("Coincident", gLeft, 2, gBot, 1))
# (no separate Horizontal constraints -- Symmetric-about-the-Y-axis on each
# line's own two endpoints already implies horizontal, adding both is
# redundant and FreeCAD's solver rightly complains)
core.addConstraint(Sketcher.Constraint("Symmetric", gBot, 1, gBot, 2, -2))
core.addConstraint(Sketcher.Constraint("Symmetric", gTop, 1, gTop, 2, -2))
core.addConstraint(Sketcher.Constraint("PointOnObject", gBot, 1, -1))
cBotW = core.addConstraint(Sketcher.Constraint("Distance", gBot, BOTTOM_WIDTH))
cTopW = core.addConstraint(Sketcher.Constraint("Distance", gTop, TOP_WIDTH))
cTaperH = core.addConstraint(Sketcher.Constraint("DistanceY", gBot, 1, gTop, 1, TAPER_HEIGHT))
core.setExpression(f"Constraints[{cBotW}]", "Dimensions.bottom_width")
core.setExpression(f"Constraints[{cTopW}]", "Dimensions.top_width")
core.setExpression(f"Constraints[{cTaperH}]", "Dimensions.taper_height")
doc.recompute()
if core.ConflictingConstraints or core.RedundantConstraints:
    raise RuntimeError(f"CoreProfile sketch is not cleanly constrained: "
                        f"conflicting={core.ConflictingConstraints} redundant={core.RedundantConstraints}")

web = doc.addObject("Part::FeaturePython", "Web")
SheetMetalBaseCmd.SMBaseBend(web, core)
web.Thickness = THICKNESS
web.BendSide = "Inside"
web.setExpression("Thickness", "Dimensions.thickness")
core.Visibility = False
doc.recompute()
if not web.Shape.isValid():
    raise RuntimeError("Web (tapered core plate) shape is invalid")

# top edge of the trapezoid (length top_width, at y=taper_height) -> fold up (+z)
top_edge = None
for i, e in enumerate(web.Shape.Edges):
    if isinstance(e.Curve, Part.Line) and abs(e.CenterOfMass.y - TAPER_HEIGHT) < 1e-3 \
            and abs(e.Length - TOP_WIDTH) < 1e-3:
        top_edge = f"Edge{i + 1}"
        break
if top_edge is None:
    raise RuntimeError("couldn't find the web's top edge to fold the top flange from")

topflange = doc.addObject("Part::FeaturePython", "TopFlange")
SheetMetalCmd.SMBendWall(topflange, web, [top_edge])
topflange.length = TOP_FLANGE_H
topflange.angle = 90.0
topflange.radius = BEND_RADIUS
topflange.invert = True
topflange.setExpression("length", "Dimensions.top_flange_h")
topflange.setExpression("radius", "Dimensions.bend_radius")
doc.recompute()
if not topflange.Shape.isValid():
    raise RuntimeError("TopFlange shape is invalid")

# bottom edge of the trapezoid (length bottom_width, at y=0) -> fold down (-z),
# opposite sense from the top flange, matching the "Z-bracket" shape in the photo
bot_edge = None
for i, e in enumerate(topflange.Shape.Edges):
    if isinstance(e.Curve, Part.Line) and abs(e.CenterOfMass.y) < 1e-3 \
            and abs(e.CenterOfMass.z) < 1e-3 and abs(e.Length - BOTTOM_WIDTH) < 1e-3:
        bot_edge = f"Edge{i + 1}"
        break
if bot_edge is None:
    raise RuntimeError("couldn't find the web's bottom edge to fold the bottom flange from")

botflange = doc.addObject("Part::FeaturePython", "BottomFlange")
SheetMetalCmd.SMBendWall(botflange, topflange, [bot_edge])
botflange.length = BOTTOM_FLANGE_H
botflange.angle = 90.0
botflange.radius = BEND_RADIUS
botflange.invert = False
botflange.setExpression("length", "Dimensions.bottom_flange_h")
botflange.setExpression("radius", "Dimensions.bend_radius")
doc.recompute()
if not botflange.Shape.isValid():
    raise RuntimeError("BottomFlange shape is invalid")
if len(botflange.Shape.Solids) != 1:
    raise RuntimeError(f"expected one solid, got {len(botflange.Shape.Solids)}")

# --- bolt holes, 2 per flange ---
# Same raw-shape-boolean workaround as part22_sheetmetal.py (Part::Cut
# silently no-ops against this shape in this FreeCAD/OCCT build -- see
# README.md, "Known quirk"). Positions found by outer-face inspection +
# isInside sampling (same technique as part22_sheetmetal.py's end-cap
# holes) -- top flange's outer face sits at z = thickness + bend_radius +
# top_flange_h-ish, bottom flange's outer face at z = -(same, bottom side).
hole_len = THICKNESS * 4
# Outer-face Z isn't a clean function of length/radius/thickness (bend
# geometry curves through the radius, same non-additive behavior noted in
# part22_sheetmetal.py's end-cap comments) -- found by inspecting the built
# shape's faces instead of computing it, same approach as finding the fold
# edges above. Look for the flange's outer flat face: large, roughly square,
# y-range matching "past the taper on the top/bottom side".
def outer_face_z(shape, y_min, y_max):
    # Want a face that's FLAT in Z (lies in a Z=const plane -- the flange's
    # broad outer or inner surface), not one of the narrow transition faces
    # at the bend radius (those have large Z-extent, small Y-extent, and are
    # otherwise easy to mistake for the target if only filtering on Y range
    # and picking "largest area").
    best = None
    for f in shape.Faces:
        bb = f.BoundBox
        if bb.ZMax - bb.ZMin > 0.5:  # not flat in Z, skip
            continue
        if bb.YMin >= y_min - 0.5 and bb.YMax <= y_max + 0.5 and (bb.XMax - bb.XMin) > TOP_WIDTH * 0.5:
            if best is None or f.Area > best.Area:
                best = f
    if best is None:
        return None
    return best.BoundBox, (best.BoundBox.ZMin + best.BoundBox.ZMax) / 2.0


top_face_bbox, _ = outer_face_z(botflange.Shape, TAPER_HEIGHT + BEND_RADIUS, TAPER_HEIGHT + TOP_FLANGE_H + BEND_RADIUS)
bot_face_bbox, _ = outer_face_z(botflange.Shape, -(BOTTOM_FLANGE_H + BEND_RADIUS), -BEND_RADIUS)
if top_face_bbox is None or bot_face_bbox is None:
    raise RuntimeError("couldn't locate the flanges' outer faces to place bolt holes")
top_face_z = max(top_face_bbox.ZMin, top_face_bbox.ZMax, key=abs)
bot_face_z = max(bot_face_bbox.ZMin, bot_face_bbox.ZMax, key=abs)
top_hole_y = (top_face_bbox.YMin + top_face_bbox.YMax) / 2.0
bot_hole_y = (bot_face_bbox.YMin + bot_face_bbox.YMax) / 2.0

final_shape = botflange.Shape.copy()
holes = (
    (-HOLE_TOP_X, top_hole_y, top_face_z, "top-left"),
    (HOLE_TOP_X, top_hole_y, top_face_z, "top-right"),
    (-HOLE_BOTTOM_X, bot_hole_y, bot_face_z, "bottom-left"),
    (HOLE_BOTTOM_X, bot_hole_y, bot_face_z, "bottom-right"),
)
for hx, hy, hz, label in holes:
    cyl = Part.makeCylinder(HOLE_D / 2.0, hole_len,
                             FreeCAD.Vector(hx, hy, hz - hole_len / 2.0),
                             FreeCAD.Vector(0, 0, 1))
    before = final_shape.Volume
    final_shape = final_shape.cut(cyl)
    removed = before - final_shape.Volume
    expected = 3.14159265 * (HOLE_D / 2.0) ** 2 * THICKNESS
    if removed < expected * 0.5:
        raise RuntimeError(f"{label} hole removed only {removed:.1f}mm^3 of the expected "
                            f"~{expected:.1f}mm^3 -- it likely misses the flange; re-check "
                            f"hole_top_x/hole_bottom_x/hole_d against the current flange dimensions")
if not final_shape.isValid():
    raise RuntimeError("Final cut shape is invalid")

final = doc.addObject("Part::Feature", "Part22_PanelB")
final.Shape = final_shape
final.Label = "Part22_PanelB_EST"
for o in (core, web, topflange, botflange):
    o.Visibility = False

doc.recompute()
print("Final bounding box:", final.Shape.BoundBox)
print("Final volume (mm^3):", round(final.Shape.Volume, 1))

doc.saveAs(os.path.join(HERE, "part22_panelB.FCStd"))
final.Shape.exportStep(os.path.join(HERE, "part22_panelB.step"))
print("DONE -- wrote part22_panelB.FCStd, part22_panelB.step")
