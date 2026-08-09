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
FreeCAD -- see README.md, in this folder, for how it was installed), so the model is an
actual bent-sheet solid (parametric thickness + bend radius), not a solid
block standing in for one.

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

Scale calibration: pixel-measured off the M8 hex bolt heads visible in the
photo (13mm across flats), same method as part22_bracket.py. Quantized to
clean stock/sheet sizes after that. Treat every number below as photo-est,
not measured.

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

DIM_LOG = []


def dim(key, value, source, note=""):
    DIM_LOG.append({"key": key, "value": value, "source": source, "note": note})
    return value


# =====================================================================
# SOURCE-TAGGED DIMENSION TABLE (see part22_bracket.py / README.md (this folder) for
# the legend this reuses: photo-est = pixel-proportioned off the M8 bolt
# heads with no other scale reference; assumption = a modeling choice with
# no photo evidence either way, chosen for plausibility, not measured).
# =====================================================================
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

print("=" * 70)
print("part22_sheetmetal.py -- dimension table (all photo-est/assumption, NOT measured)")
for d in DIM_LOG:
    note = f"  ({d['note']})" if d["note"] else ""
    print(f"  {d['key']:20s} = {d['value']!r:>8}  [{d['source']}]{note}")
print("=" * 70)

doc = FreeCAD.newDocument("part22_sheetmetal")

# --- base wall: open U-channel trough (open top), swept along +z ---
profile = doc.addObject("Sketcher::SketchObject", "TroughProfile")
w2 = BOX_WIDTH / 2.0
profile.addGeometry(Part.LineSegment(FreeCAD.Vector(-w2, TROUGH_HEIGHT, 0),
                                      FreeCAD.Vector(-w2, 0, 0)), False)
profile.addGeometry(Part.LineSegment(FreeCAD.Vector(-w2, 0, 0),
                                      FreeCAD.Vector(w2, 0, 0)), False)
profile.addGeometry(Part.LineSegment(FreeCAD.Vector(w2, 0, 0),
                                      FreeCAD.Vector(w2, TROUGH_HEIGHT, 0)), False)
doc.recompute()

trough = doc.addObject("Part::FeaturePython", "Trough")
SheetMetalBaseCmd.SMBaseBend(trough, profile)
trough.Thickness = THICKNESS
trough.Radius = BEND_RADIUS
trough.Length = TROUGH_LENGTH
trough.BendSide = "Inside"
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
doc.recompute()
if not endcap.Shape.isValid():
    raise RuntimeError("EndCap (folded end lip) shape is invalid")
if len(endcap.Shape.Solids) != 1:
    raise RuntimeError(f"expected one fused solid, got {len(endcap.Shape.Solids)}")

# --- bolt holes through the raised end face (items 47/53) ---
# NOTE: built as a raw Part.Shape boolean (not a parametric Part::Cut
# document object) -- in this build (FreeCAD 1.1.3 / OCCT 7.9.3 from
# conda-forge, the only install path available in the sandbox this was
# first built in, see README.md in this folder), Part::Cut against a SheetMetal
# Part::FeaturePython Base silently no-ops (recomputes without error, but
# removes no material) even though the identical boolean succeeds when
# called directly on the shape geometry. Filed as a local environment quirk,
# not chased further; this sidesteps it at the cost of the holes not being
# parametric (move HOLE_X/HOLE_Y above and re-run the whole script instead).
cap_face_z = TROUGH_LENGTH + THICKNESS + BEND_RADIUS  # just past the trough's far face
hole_len = THICKNESS * 4  # cut clean through, generous margin either side
final_shape = endcap.Shape.copy()
for hx in (-HOLE_X, HOLE_X):
    cyl = Part.makeCylinder(HOLE_D / 2.0, hole_len,
                             FreeCAD.Vector(hx, HOLE_Y, cap_face_z - hole_len / 2.0),
                             FreeCAD.Vector(0, 0, 1))
    final_shape = final_shape.cut(cyl)
if not final_shape.isValid():
    raise RuntimeError("Final cut shape is invalid")

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
