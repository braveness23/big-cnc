"""
Central Machinery (Harbor Freight) SKU# S36066 lathe -- FreeCAD SheetMetal
reconstruction of exploded-view part #22 (manual/central-machinery-36066-
manual.pdf p.10 mislabels this "Headstock"; the diagram's own leader line for
#22 points at the bracket beside the tailstock upright, not the headstock
casting -- see manual/exploded-view.png). This model follows the diagram's
leader line, not its label.

THIS IS NOT A MEASURED PART -- same caveat as part22_bracket.py (the earlier
Blender attempt), and it should be read as that attempt's sequel, not a
replacement: PXL_20260808_133251586.jpg makes it obvious this bracket is
folded sheet steel, not solid box tube -- you can see the bend radius on the
outer corners, the constant wall thickness, and the miter/weld seam where the
end panel meets the side walls. The Blender version's docstring flagged this
ambiguity ("a hint of a second fold line ... suggesting it may actually be an
open C-channel") and punted on it. This pass resolves it by rebuilding the
part in FreeCAD using the community SheetMetal workbench (not bundled with
FreeCAD -- see README.md, in this folder, for how it was installed), so the
model is an actual bent-sheet solid (parametric thickness + bend radius), not
a solid block standing in for one.

Geometry read off the photo + the exploded-view crop around item 22:
  - A U-channel trough (open top) that the two bed rails' near ends land in,
    matching the rails' own open-top folded-channel profile.
  - The trough's far end is closed by a taller lip, folded up on 3 sides
    (bottom + both side walls, mitered at the corners) -- this is the raised
    boss the tailstock upright (item 24) bolts to from above.
  - Two hex bolts (items 47/53 in the exploded view) pass down through that
    raised end face -- clearly visible in the photo. A third fastener is
    visible low in the trough (probably item 48) but its exact geometry
    wasn't legible enough to model with any confidence; left out rather than
    guessed.
Panel B (one of the two side walls) turned out NOT to be this simple flat
U-channel wall -- 2026-08-09 tracing + photos showed it's actually a tapered
wedge (flat top flange, tapered wall, flat narrower bottom flange). Not yet
rebuilt to match -- see worksheet.md and traces/ in this folder -- this
script still models the old flat-rectangle-wall guess pending real numbers.

Scale calibration: pixel-measured off the M8 hex bolt heads visible in the
photo (13mm across flats), same method as part22_bracket.py. Quantized to
clean stock/sheet sizes after that. Treat every number below as photo-est,
not measured.

PARAMETRIC / TUNABLE: every dimension lives in the "Dimensions" spreadsheet
inside part22_sheetmetal.FCStd (name, value, source tag, note -- one row
each), not just as Python constants. The sketch and the SheetMetal wall/bend
features are expression-bound to those cells, so opening the .FCStd in the
FreeCAD GUI, editing a cell, and recomputing updates the trough + end-lip
shape live, no script involved. The one exception: the two bolt holes are
cut with a raw Part.Shape boolean, not a parametric Part::Cut (see the
"Known quirk" note in README.md, this folder -- Part::Cut silently no-ops
against this shape in this FreeCAD/OCCT build). Editing HOLE_X/HOLE_Y/HOLE_D
below (or the spreadsheet cells of the same name) and re-running the whole
script picks up new hole placement; a bare GUI recompute won't.

Run headless (from this directory):  freecadcmd part22_sheetmetal.py
Outputs:       part22_sheetmetal.FCStd, part22_sheetmetal.step
Then:          freecadcmd part22_sheetmetal_isosvg.py
               (writes part22_sheetmetal_iso.svg from the .FCStd; convert to
               PNG the same way as cad/README.md documents for lathe_iso,
               one level up, for the whole-machine model)

Coordinate system (local to this part, not tied to lathe.py's bed datum --
this file was built standalone, see README.md in this folder):
  x = across the bed (box width, spans both rails' bolt centers)
  y = vertical, up from the trough floor
  z = along the bed / the rails' length axis. 0 = open end (rails enter);
      +z = toward the closed/raised end (item 24's mounting face)
"""
import os
import sys

import FreeCAD
import Part
import Sketcher

HERE = os.path.dirname(os.path.abspath(__file__))

# Prefer the addon manager's install location; fall back to a path next to
# this file for environments (like the one this was first built in) that
# don't have the FreeCAD Addon Manager available to install it the normal
# way. See README.md in this folder, "Sheet metal workbench".
try:
    import SheetMetalBaseCmd
    import SheetMetalCmd
except ImportError:
    sys.path.insert(0, os.path.join(HERE, "SheetMetal"))
    import SheetMetalBaseCmd
    import SheetMetalCmd

doc = FreeCAD.newDocument("part22_sheetmetal")

# =====================================================================
# DIMENSIONS -- a Spreadsheet inside the document, not just Python
# constants, so every value is directly editable from the FreeCAD GUI
# (Dimensions sheet -> edit a cell -> recompute) as well as from this
# script. dim() writes each value to both: the returned float drives this
# script's own build (sketch/feature starting values, hole placement), and
# the "Value" column cell (aliased to `key`) is what the sketch constraints
# and SheetMetal properties are expression-bound to below, plus a Source/
# Note column pair so the photo-est-vs-measured provenance travels with the
# .FCStd itself, not just this script's docstring. Source-tag legend: same
# as part22_bracket.py / lathe.py -- "photo-est" = pixel-proportioned from a
# reference photo with no independent scale check; "assumption" = a
# modeling choice with no photo evidence either way, chosen for
# plausibility, not measured; "measured" = calipers/tape/tracing (none yet).
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


BOX_WIDTH = dim("box_width", 150.0, "photo-est",
                "outer width across both side walls, box front face")
TROUGH_HEIGHT = dim("trough_height", 50.0, "photo-est",
                     "open U-channel side-wall height, matches rail channel depth")
TROUGH_LENGTH = dim("trough_length", 110.0, "photo-est",
                     "depth of the open trough before the raised end lip")
CAP_FOLD_LENGTH = dim("cap_fold_length", 90.0, "photo-est",
                       "SheetMetal 'Wall' bend length for the raised end lip; "
                       "auto-miter clips this down to ~75mm actual rise")
THICKNESS = dim("thickness", 3.0, "assumption",
                 "~11ga steel plate, plausible for a welded structural bracket "
                 "this size; not legible in the photo")
BEND_RADIUS = dim("bend_radius", 3.0, "assumption", "~1x thickness, typical press-brake minimum")
HOLE_D = dim("hole_d", 8.5, "photo-est", "M8 clearance, matches part22_bracket.py's bolts 47/53")
HOLE_X = dim("hole_x", 25.0, "assumption",
             "bolt spacing off-center on the end face; kept close to centerline so both "
             "holes land clear of the mitered corner seams (see README.md, this folder)")
HOLE_Y = dim("hole_y", 25.0, "assumption", "bolt height on the raised end face, same reason")
doc.recompute()

print("=" * 70)
print("part22_sheetmetal.py -- dimension table (all photo-est/assumption, NOT measured)")
print("also written to the 'Dimensions' spreadsheet inside the .FCStd -- edit there to tune")
for row in range(2, _DIM_ROW[0] + 1):
    key = sheet.get(f"A{row}")
    print(f"  {key:20s} = {sheet.get(f'B{row}'):>8}  [{sheet.get(f'C{row}')}]  ({sheet.get(f'D{row}')})")
print("=" * 70)

# --- base wall: open U-channel trough (open top), swept along +z ---
# Sketch geometry is fully constrained (not just placed at these starting
# coordinates) and dimensioned by two expressions bound to the spreadsheet,
# so tuning box_width/trough_height in the GUI and recomputing reshapes
# this profile -- and everything built from it -- without touching Python.
profile = doc.addObject("Sketcher::SketchObject", "TroughProfile")
w2 = BOX_WIDTH / 2.0
gLeft = profile.addGeometry(Part.LineSegment(FreeCAD.Vector(-w2, TROUGH_HEIGHT, 0),
                                              FreeCAD.Vector(-w2, 0, 0)), False)
gBottom = profile.addGeometry(Part.LineSegment(FreeCAD.Vector(-w2, 0, 0),
                                                FreeCAD.Vector(w2, 0, 0)), False)
gRight = profile.addGeometry(Part.LineSegment(FreeCAD.Vector(w2, 0, 0),
                                               FreeCAD.Vector(w2, TROUGH_HEIGHT, 0)), False)
profile.addConstraint(Sketcher.Constraint("Coincident", gLeft, 2, gBottom, 1))
profile.addConstraint(Sketcher.Constraint("Coincident", gBottom, 2, gRight, 1))
profile.addConstraint(Sketcher.Constraint("Vertical", gLeft))
profile.addConstraint(Sketcher.Constraint("Horizontal", gBottom))
profile.addConstraint(Sketcher.Constraint("Vertical", gRight))
# centered on the sketch's Y axis, bottom edge pinned to the X axis (y=0)
profile.addConstraint(Sketcher.Constraint("Symmetric", gLeft, 1, gRight, 2, -2))
profile.addConstraint(Sketcher.Constraint("PointOnObject", gBottom, 1, -1))
cWidth = profile.addConstraint(Sketcher.Constraint("Distance", gBottom, BOX_WIDTH))
cHeight = profile.addConstraint(Sketcher.Constraint("Distance", gLeft, TROUGH_HEIGHT))
profile.setExpression(f"Constraints[{cWidth}]", "Dimensions.box_width")
profile.setExpression(f"Constraints[{cHeight}]", "Dimensions.trough_height")
doc.recompute()
if profile.ConflictingConstraints or profile.RedundantConstraints:
    raise RuntimeError(f"TroughProfile sketch is not cleanly constrained: "
                        f"conflicting={profile.ConflictingConstraints} "
                        f"redundant={profile.RedundantConstraints}")

trough = doc.addObject("Part::FeaturePython", "Trough")
SheetMetalBaseCmd.SMBaseBend(trough, profile)
trough.Thickness = THICKNESS
trough.Radius = BEND_RADIUS
trough.Length = TROUGH_LENGTH
trough.BendSide = "Inside"
trough.setExpression("Thickness", "Dimensions.thickness")
trough.setExpression("Radius", "Dimensions.bend_radius")
trough.setExpression("Length", "Dimensions.trough_length")
profile.Visibility = False
doc.recompute()
if not trough.Shape.isValid():
    raise RuntimeError("Trough (base SheetMetal wall) shape is invalid")

# --- raised end lip: fold a wall up from the trough's far (open) end on all
# three sides (bottom + both side walls) in one multi-edge bend, so
# SheetMetal's auto-miter forms the corner seams instead of a hand-built
# boolean union -- this is the same operation a person would do in the GUI
# by selecting all three far-end edges together before clicking "Make Wall".
far_z = TROUGH_LENGTH
candidates = []  # (name, midpoint, length)
for i, e in enumerate(trough.Shape.Edges):
    if abs(e.CenterOfMass.z - far_z) > 1e-3:
        continue
    if not isinstance(e.Curve, Part.Line):
        continue
    if e.Length < THICKNESS * 2:  # skip the short thickness-direction edges
        continue
    candidates.append((f"Edge{i + 1}", e.CenterOfMass, e.Length))

# Each of the 3 walls contributes an inner/outer pair of long edges here;
# SheetMetal's "Wall" bend needs the OUTER one (farthest from the trough's
# own interior) as the fold line, same as clicking the outer visible edge in
# the GUI. Bottom wall: outer = smaller y. Side walls: outer = larger |x|.
bottom = [c for c in candidates if abs(c[1].x) < BOX_WIDTH * 0.4]
left = [c for c in candidates if c[1].x <= -BOX_WIDTH * 0.4]
right = [c for c in candidates if c[1].x >= BOX_WIDTH * 0.4]
if not (len(bottom) == 2 and len(left) == 2 and len(right) == 2):
    raise RuntimeError(f"expected 2+2+2 candidate edges, got bottom={bottom} left={left} right={right}")
far_edges = [
    min(bottom, key=lambda c: c[1].y)[0],
    min(left, key=lambda c: c[1].x)[0],
    max(right, key=lambda c: c[1].x)[0],
]

endcap = doc.addObject("Part::FeaturePython", "EndCap")
SheetMetalCmd.SMBendWall(endcap, trough, far_edges)
endcap.length = CAP_FOLD_LENGTH
endcap.angle = 90.0
endcap.radius = BEND_RADIUS
endcap.invert = True   # fold toward the trough's open (+y) side, i.e. upward
endcap.AutoMiter = True
endcap.setExpression("length", "Dimensions.cap_fold_length")
endcap.setExpression("radius", "Dimensions.bend_radius")
doc.recompute()
if not endcap.Shape.isValid():
    raise RuntimeError("EndCap (folded end lip) shape is invalid")
if len(endcap.Shape.Solids) != 1:
    raise RuntimeError(f"expected one fused solid, got {len(endcap.Shape.Solids)}")

# --- bolt holes through the raised end face (items 47/53) ---
# NOTE: built as a raw Part.Shape boolean (not a parametric Part::Cut
# document object) -- in this build (FreeCAD 1.1.3 / OCCT 7.9.3 from
# conda-forge, the only install path available in the sandbox this was
# first built in, see README.md in this folder), Part::Cut against this
# shape silently no-ops (recomputes without error, but removes no material)
# even though the identical boolean succeeds when called directly on the
# shape geometry -- confirmed it isn't SheetMetal-specific (a plain
# Part::Feature built from the exact same shape has the same problem;
# a shape built from Part.makeBox() does not), so it's some BRep property
# of SheetMetal's generated geometry the Part::Cut feature's recompute path
# doesn't like in this build. Not chased further. Practical upshot: this is
# the one part of the model NOT driven live by the spreadsheet -- change
# hole_x/hole_y/hole_d and re-run the whole script to move the holes,
# a bare GUI recompute won't pick it up.
cap_face_z = TROUGH_LENGTH + THICKNESS + BEND_RADIUS  # just past the trough's far face
hole_len = THICKNESS * 4  # cut clean through, generous margin either side
hole_area = 3.14159265 * (HOLE_D / 2.0) ** 2
expected_removed = 2 * hole_area * THICKNESS  # approx, ignores any radius/bend overlap
final_shape = endcap.Shape.copy()
for hx in (-HOLE_X, HOLE_X):
    cyl = Part.makeCylinder(HOLE_D / 2.0, hole_len,
                             FreeCAD.Vector(hx, HOLE_Y, cap_face_z - hole_len / 2.0),
                             FreeCAD.Vector(0, 0, 1))
    final_shape = final_shape.cut(cyl)
if not final_shape.isValid():
    raise RuntimeError("Final cut shape is invalid")
actual_removed = endcap.Shape.Volume - final_shape.Volume
if actual_removed < expected_removed * 0.5:
    # If HOLE_X/HOLE_Y were tuned to sit off the raised end face (e.g. after
    # a big box_width/trough_height change without re-checking clearance),
    # the cut silently misses material instead of erroring -- catch that
    # here rather than shipping a bracket with holes that didn't cut.
    raise RuntimeError(
        f"bolt holes removed only {actual_removed:.1f}mm^3 of the expected "
        f"~{expected_removed:.1f}mm^3 -- hole_x/hole_y likely land off the "
        f"raised end face for the current box_width/trough_height/cap_fold_length; "
        f"re-check clearance (see the isInside-sampling approach used to pick "
        f"the original values, in this file's git history) before trusting this cut")

final = doc.addObject("Part::Feature", "Part22_Bracket_SheetMetal")
final.Shape = final_shape
final.Label = "Part22_Bracket_SheetMetal_EST"
for o in (trough, endcap):
    o.Visibility = False

doc.recompute()
print("Final bounding box:", final.Shape.BoundBox)
print("Final volume (mm^3):", round(final.Shape.Volume, 1))

doc.saveAs(os.path.join(HERE, "part22_sheetmetal.FCStd"))
final.Shape.exportStep(os.path.join(HERE, "part22_sheetmetal.step"))
print("DONE -- wrote part22_sheetmetal.FCStd, part22_sheetmetal.step")
