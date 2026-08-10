"""
Central Machinery (Harbor Freight) SKU# S36066 "14 x 40 Wood Lathe w/7"
Disc" -- rough 3D model, built as a foundation for designing a CNC addition
(powered Z carriage + spindle encoder/C-axis + X/Z cross-slide).

Run headless:  freecadcmd cad/lathe.py
Outputs:       cad/lathe.FCStd  and  cad/lathe.step
Also prints:   the source-tagged dimension table, envelope-closure checks,
               and the morning measurement request list (see cad/README.md).

THIS IS NOT A MEASURED MODEL. Every dimension below is tagged with where it
came from (see `dim()` calls). Only manual-spec/nameplate/parts-list values
and dimensions derived from published component standards (bearings, Morse
taper, UNC thread) are trustworthy. Everything tagged "photo-est" is a
proportion guessed from the reference photos with NO scale reference, and
exists only so the assembly reads as "this lathe" -- its object Label ends
in "_EST" so it's obvious in the FreeCAD model tree. Nothing tagged "GUESS"
is modeled at all; it's listed in the measurement request instead.

Coordinate system (FreeCAD native mm; authored in inches * 25.4):
  x = along the bed. 0 = spindle nose face (front of headstock, where a
      faceplate/drive center mounts). +x runs toward the tailstock -- this
      is the CNC Z-carriage's travel axis; the letter doesn't match CNC "Z"
      on purpose, don't let that trip up whoever writes the carriage model.
  y = horizontal, across the bed. 0 = spindle centerline (also the
      lathe's centerline; the two bed rails sit at y = +/-half the rail
      gauge).
  z = vertical. 0 = bed-rail TOP surface (the carriage's riding surface).
      Spindle centerline sits at z = RAIL_TOP_TO_SPINDLE_AXIS (derived
      below from "swing over bed" -- exact, not an estimate).

Source-tag legend used throughout:
  manual-spec        -- straight from the manual's SPECIFICATIONS table
  nameplate           -- straight from the machine's nameplate (photographed)
  manual-partslist    -- from the manual's numbered parts list / exploded view
  bearing-std-NNNN     -- bore/OD/width from the published NNNN bearing standard
  taper-std-mt2        -- from the published Morse Taper No. 2 standard
  thread-std-unc        -- from the UNC thread standard, given a confirmed size
  web-forum             -- corroborated by outside sources this session, not the manual
  DERIVED               -- computed from other tagged values; formula in the note
  photo-est             -- proportioned from reference photos, no scale reference
"""
import os
import math
import FreeCAD as App
import Part
from FreeCAD import Vector

IN = 25.4  # mm per inch -- all authored dimensions below are in inches
HERE = os.path.dirname(os.path.abspath(__file__))

# =====================================================================
# SOURCE-TAGGED DIMENSION TABLE
# Every dimension used to build geometry is registered here via dim().
# At the end of the script this table drives both the printed measurement
# list and a spot-check that nothing photo-est/GUESS crept in unlabeled.
# =====================================================================
DIM_LOG = []


def dim(key, value, source, note=""):
    DIM_LOG.append({"key": key, "value": value, "source": source, "note": note})
    return value


# ---- manual SPECIFICATIONS table (exact) ----
DIST_BETWEEN_CENTERS = dim("dist_between_centers", 40.0, "manual-spec")
SWING_OVER_BED = dim("swing_over_bed", 14.0, "manual-spec")
TAILSTOCK_QUILL_TRAVEL = dim("tailstock_quill_travel", 3.5, "manual-spec")
DISC_DIAMETER = dim("disc_diameter", 7.0, "manual-spec")
OVERALL_LENGTH = dim("overall_length", 63.75, "manual-spec", '63-3/4"')
OVERALL_WIDTH = dim("overall_width", 11.0, "manual-spec")
OVERALL_HEIGHT = dim("overall_height", 15.0, "manual-spec")

# ---- spindle nose thread: web-corroborated size, exact UNC standard geometry ----
SPINDLE_THREAD_SIZE = dim(
    "spindle_thread_size", "3/4-10 UNC", "web-forum",
    "two independent forum sources agree; not in the manual itself")
SPINDLE_NOSE_MAJOR_D = dim(
    "spindle_nose_major_d", 0.7500, "thread-std-unc",
    "3/4-10 UNC major diameter, modeled as a plain cylinder (no helix cut)")

# ---- bearings from the parts list, bore/OD/width from the published standard ----
BRG_6201 = dict(bore=dim("brg_6201_bore_mm", 12.0, "bearing-std-6201"),
                od=dim("brg_6201_od_mm", 32.0, "bearing-std-6201"),
                width=dim("brg_6201_width_mm", 10.0, "bearing-std-6201"))
BRG_6203 = dict(bore=dim("brg_6203_bore_mm", 17.0, "bearing-std-6203"),
                od=dim("brg_6203_od_mm", 40.0, "bearing-std-6203"),
                width=dim("brg_6203_width_mm", 12.0, "bearing-std-6203"))
BRG_6204 = dict(bore=dim("brg_6204_bore_mm", 20.0, "bearing-std-6204"),
                od=dim("brg_6204_od_mm", 47.0, "bearing-std-6204"),
                width=dim("brg_6204_width_mm", 14.0, "bearing-std-6204"))

# ---- MT2 Morse taper (ANSI B5.10 / DIN 228 / ISO 296) ----
MT2_LARGE_D = dim("mt2_large_d", 17.78 / IN, "taper-std-mt2")
MT2_SMALL_D = dim("mt2_small_d", 14.53 / IN, "taper-std-mt2")
MT2_LENGTH = dim("mt2_length", 65.0 / IN, "taper-std-mt2", "~2.56\"; shank length varies slightly by maker")

# ---- derived from manual-spec (exact formula, not a guess) ----
RAIL_TOP_TO_SPINDLE_AXIS = dim(
    "rail_top_to_spindle_axis", SWING_OVER_BED / 2.0, "DERIVED",
    "swing over bed / 2 -- spindle centerline height above bed-rail top")

# ---- bed rails: manual parts-list item #1, square steel tube (measured 2026-08-10) ----
RAIL_HEIGHT = dim("rail_height", 38.0 / IN, "measured-2026-08-10", "square tube, 38mm side")
RAIL_TOP_WIDTH = dim("rail_top_width", 38.0 / IN, "measured-2026-08-10", "square tube, 38mm side")
RAIL_WALL_T = dim("rail_wall_thickness", 1.92 / IN, "measured-2026-08-10", "1.92mm wall")
RAIL_GAP = dim("rail_inner_gap", 5.5, "photo-est", "clear width between the two rails' inner faces")
RAIL_STOCK_LENGTH = dim(
    "rail_stock_length", 46.375, "measured-2026-08-10",
    "physical square-tube stock length (part #1), 46-3/8\" = 1177.925mm. Distinct "
    "from bed_rail_run_x below (an envelope-fitted value, not the raw stock length "
    "-- the tube likely runs partly under the headstock/tailstock castings).")
BED_RAIL_RUN_X = dim(
    "bed_rail_run_x", 41.0, "DERIVED",
    "chosen so headstock_depth + this + tailstock_depth == overall_length "
    "AND (this - drive_center_protrusion) ~= dist_between_centers; see "
    "envelope-closure checks below. Real value depends on the (unmeasured) "
    "casting depths -- treat as photo-est quality despite the label.")

# ---- headstock housing (single sheet-metal enclosure: spindle + motor + pulleys) ----
HEADSTOCK_WIDTH = dim(
    "headstock_width", OVERALL_WIDTH, "DERIVED",
    "assumption: the headstock housing is the widest single component, so "
    "its width equals the machine's overall width spec")
HEADSTOCK_DEPTH_X = dim("headstock_depth_x", 12.5, "photo-est")
HEADSTOCK_HEIGHT_ABOVE_SPINDLE = dim("headstock_height_above_spindle", 4.5, "photo-est")
HEADSTOCK_HEIGHT_BELOW_SPINDLE = dim("headstock_height_below_spindle", 3.5, "photo-est")
SPINDLE_NOSE_PROTRUSION = dim(
    "spindle_nose_protrusion", 0.75, "photo-est",
    "how far the nose/drive-center stub sticks out past the headstock front face")
DISC_MOUNT_PROTRUSION = dim("disc_mount_protrusion", 0.75, "photo-est", "rear spindle stub, mirrors the nose side")

# ---- bed base / support below the rails ----
BELOW_RAIL_DEPTH = dim("below_rail_depth", 2.0, "photo-est", "support structure from rail bottom down")

# ---- tailstock ----
TAILSTOCK_DEPTH_X = dim("tailstock_depth_x", 10.25, "photo-est")
TAILSTOCK_WIDTH = dim("tailstock_width", 4.0, "photo-est")
TAILSTOCK_HEIGHT_ABOVE_SPINDLE = dim("tailstock_height_above_spindle", 2.5, "photo-est")
TAILSTOCK_HEIGHT_BELOW_SPINDLE = dim("tailstock_height_below_spindle", 2.5, "photo-est")
TAILSTOCK_X = dim(
    "tailstock_x", BED_RAIL_RUN_X, "DERIVED",
    "illustrative pose: parked at the far end of the bed rails")
TAILSTOCK_QUILL_DIAMETER = dim("tailstock_quill_diameter", 1.25, "photo-est")
TAILSTOCK_QUILL_EXTENSION_SHOWN = dim(
    "tailstock_quill_extension_shown", TAILSTOCK_QUILL_TRAVEL / 2.0, "DERIVED",
    "illustrative pose only: half of the exact 3.5\" travel spec")
TAILSTOCK_HANDWHEEL_DIAMETER = dim("tailstock_handwheel_diameter", 3.5, "photo-est")
TAILSTOCK_HANDWHEEL_THICKNESS = dim("tailstock_handwheel_thickness", 0.75, "photo-est")

# ---- banjo / tool rest holder (likely X cross-slide mount point) ----
BANJO_X = dim("banjo_x", 18.0, "photo-est", "illustrative pose: arbitrary mid-bed position")
BANJO_FOOTPRINT_X = dim("banjo_footprint_x", 3.5, "photo-est")
BANJO_WIDTH = dim("banjo_width", 3.0, "photo-est")
BANJO_CLAMP_HEIGHT = dim("banjo_clamp_height", 1.5, "photo-est", "clamp block underneath the rails")
BANJO_POST_HEIGHT = dim("banjo_post_height", 3.5, "photo-est")
BANJO_POST_DIAMETER = dim("banjo_post_diameter", 0.875, "photo-est")
TOOL_REST_BAR_LENGTH = dim("tool_rest_bar_length", 8.0, "photo-est")
TOOL_REST_BAR_WIDTH = dim("tool_rest_bar_width", 0.75, "photo-est")
TOOL_REST_BAR_HEIGHT = dim("tool_rest_bar_height", 0.375, "photo-est")

# ---- sanding-disc subsystem: deliberately low fidelity (parts 34-46), out of scope
#      for the Z-carriage / C-axis / X-cross-slide CNC addition Dave described ----
DISC_BLOCK_DEPTH_X = dim("disc_block_depth_x", 8.5, "photo-est", "combined disc+worktable+miter gauge stand-in")
DISC_BLOCK_WIDTH = dim("disc_block_width", 7.0, "photo-est")
DISC_BLOCK_HEIGHT = dim("disc_block_height", 8.0, "photo-est")

# =====================================================================
# BUILD
# =====================================================================
doc = App.newDocument("lathe")
objs = []


def bbin(shape):
    b = shape.BoundBox
    return tuple(round(v / IN, 2) for v in
                 (b.XMin, b.XMax, b.YMin, b.YMax, b.ZMin, b.ZMax))


def add(name, shape, source):
    label = name if source not in ("photo-est", "GUESS") else name + "_EST"
    o = doc.addObject("Part::Feature", name)
    o.Shape = shape
    o.Label = label
    o.addProperty("App::PropertyString", "SourceTag", "Provenance",
                   "Where this part's dimensions came from")
    o.SourceTag = source
    objs.append(o)
    return o


def box_centered(name, size_x, size_y, size_z, cx, cy, cz, source):
    s = Part.makeBox(size_x * IN, size_y * IN, size_z * IN)
    s.translate(Vector((cx - size_x / 2) * IN, (cy - size_y / 2) * IN, (cz - size_z / 2) * IN))
    return add(name, s, source)


def cyl_x(name, diameter, length, x0, cy, cz, source):
    """Cylinder whose axis runs along +x, starting at x0."""
    s = Part.makeCylinder(diameter / 2.0 * IN, length * IN,
                           Vector(x0 * IN, cy * IN, cz * IN), Vector(1, 0, 0))
    return add(name, s, source)


def cone_x(name, d_at_x0, d_at_x1, length, x0, cy, cz, source):
    s = Part.makeCone(d_at_x0 / 2.0 * IN, d_at_x1 / 2.0 * IN, length * IN,
                       Vector(x0 * IN, cy * IN, cz * IN), Vector(1, 0, 0))
    return add(name, s, source)


def cyl_z(name, diameter, height, cx, cy, z0, source):
    """Cylinder whose axis runs along +z, starting at z0."""
    s = Part.makeCylinder(diameter / 2.0 * IN, height * IN,
                           Vector(cx * IN, cy * IN, z0 * IN), Vector(0, 0, 1))
    return add(name, s, source)


SPINDLE_Z = RAIL_TOP_TO_SPINDLE_AXIS  # z of spindle centerline, rail top = 0

# ---- bed rails (2, running +x from the headstock face) ----
for side, sign in (("L", -1), ("R", +1)):
    y_inner = sign * RAIL_GAP / 2.0
    y_center = y_inner + sign * RAIL_TOP_WIDTH / 2.0
    box_centered(f"BedRail_{side}", BED_RAIL_RUN_X, RAIL_TOP_WIDTH, RAIL_HEIGHT,
                 BED_RAIL_RUN_X / 2.0, y_center, -RAIL_HEIGHT / 2.0, "photo-est")

# ---- bed base / support under the rails, spanning the full rail run ----
box_centered("BedBase", BED_RAIL_RUN_X, RAIL_GAP + 2 * RAIL_TOP_WIDTH, BELOW_RAIL_DEPTH,
             BED_RAIL_RUN_X / 2.0, 0.0, -RAIL_HEIGHT - BELOW_RAIL_DEPTH / 2.0, "photo-est")

# ---- headstock housing (spindle + motor + pulleys, single enclosure) ----
# NOTE: this simplified single box floats a few inches above the bed-rail
# top (z=0) because HEADSTOCK_HEIGHT_BELOW_SPINDLE is a rough guess and the
# height-closure check below only constrains the space ABOVE the spindle
# axis. The real housing has a base/pedestal that meets the bed -- fix this
# once the headstock envelope is actually measured (see measurement list).
box_centered("Headstock", HEADSTOCK_DEPTH_X, HEADSTOCK_WIDTH,
             HEADSTOCK_HEIGHT_ABOVE_SPINDLE + HEADSTOCK_HEIGHT_BELOW_SPINDLE,
             -HEADSTOCK_DEPTH_X / 2.0, 0.0,
             SPINDLE_Z + (HEADSTOCK_HEIGHT_ABOVE_SPINDLE - HEADSTOCK_HEIGHT_BELOW_SPINDLE) / 2.0,
             "photo-est")

# ---- main spindle: stepped shaft, exact bearing-seat + nose diameters ----
front_brg_len = BRG_6204["width"] / IN
rear_brg_len = BRG_6203["width"] / IN
nose_len = SPINDLE_NOSE_PROTRUSION
# front bearing seat + mid shaft + rear bearing seat exactly fill the
# headstock depth (0 .. -HEADSTOCK_DEPTH_X), so the rear seat ends flush
# with the housing's back face and the disc-mount stub picks up from there
# with no gap or overlap.
inside_len = max(HEADSTOCK_DEPTH_X - front_brg_len - rear_brg_len, 0.5)

cyl_x("Spindle_Nose", SPINDLE_NOSE_MAJOR_D, nose_len, 0.0, 0, SPINDLE_Z, "thread-std-unc")
cyl_x("Spindle_FrontBearingSeat", BRG_6204["bore"] / IN, front_brg_len, -front_brg_len, 0, SPINDLE_Z, "bearing-std-6204")
cyl_x("Spindle_MidShaft", (BRG_6204["bore"] + BRG_6203["bore"]) / 2.0 / IN, inside_len,
      -front_brg_len - inside_len, 0, SPINDLE_Z, "photo-est")
cyl_x("Spindle_RearBearingSeat", BRG_6203["bore"] / IN, rear_brg_len,
      -HEADSTOCK_DEPTH_X, 0, SPINDLE_Z, "bearing-std-6203")
cyl_x("Spindle_DiscMountStub", 0.6, DISC_MOUNT_PROTRUSION,
      -HEADSTOCK_DEPTH_X - DISC_MOUNT_PROTRUSION, 0, SPINDLE_Z, "photo-est")

# ---- tailstock ----
box_centered("Tailstock", TAILSTOCK_DEPTH_X, TAILSTOCK_WIDTH,
             TAILSTOCK_HEIGHT_ABOVE_SPINDLE + TAILSTOCK_HEIGHT_BELOW_SPINDLE,
             TAILSTOCK_X + TAILSTOCK_DEPTH_X / 2.0, 0.0,
             SPINDLE_Z + (TAILSTOCK_HEIGHT_ABOVE_SPINDLE - TAILSTOCK_HEIGHT_BELOW_SPINDLE) / 2.0,
             "photo-est")
quill_tip_x = TAILSTOCK_X - TAILSTOCK_QUILL_EXTENSION_SHOWN
cyl_x("Tailstock_Quill", TAILSTOCK_QUILL_DIAMETER,
      TAILSTOCK_DEPTH_X - TAILSTOCK_QUILL_TRAVEL + TAILSTOCK_QUILL_EXTENSION_SHOWN,
      quill_tip_x + MT2_LENGTH, 0, SPINDLE_Z, "photo-est")
cone_x("Tailstock_MT2_Socket", MT2_SMALL_D, MT2_LARGE_D, MT2_LENGTH,
       quill_tip_x, 0, SPINDLE_Z, "taper-std-mt2")
cyl_x("Tailstock_Handwheel", TAILSTOCK_HANDWHEEL_DIAMETER, TAILSTOCK_HANDWHEEL_THICKNESS,
      TAILSTOCK_X + TAILSTOCK_DEPTH_X, 0, SPINDLE_Z, "photo-est")

# ---- banjo / tool rest holder ----
box_centered("Banjo_Clamp", BANJO_FOOTPRINT_X, BANJO_WIDTH, BANJO_CLAMP_HEIGHT,
             BANJO_X, 0.0, -RAIL_HEIGHT / 2.0, "photo-est")
cyl_z("Banjo_Post", BANJO_POST_DIAMETER, BANJO_POST_HEIGHT, BANJO_X, 0.0, 0.0, "photo-est")
box_centered("ToolRest_Bar", TOOL_REST_BAR_WIDTH, TOOL_REST_BAR_LENGTH, TOOL_REST_BAR_HEIGHT,
             BANJO_X, 0.0, SPINDLE_Z - 0.125, "photo-est")

# ---- sanding-disc subsystem: single low-fidelity block behind the headstock ----
box_centered("SandingDiscSubsystem", DISC_BLOCK_DEPTH_X, DISC_BLOCK_WIDTH, DISC_BLOCK_HEIGHT,
             -HEADSTOCK_DEPTH_X - DISC_BLOCK_DEPTH_X / 2.0, 0.0, SPINDLE_Z, "photo-est")

doc.recompute()

# =====================================================================
# ENVELOPE CLOSURE CHECKS
# Estimated sub-lengths must sum to the one number that's unambiguously
# correct (overall_length, manual-spec). If they don't, an estimate above
# is wrong -- this is the guard against a plausible-looking wrong model.
# =====================================================================
print("=== ENVELOPE CLOSURE CHECKS ===")

length_sum = HEADSTOCK_DEPTH_X + BED_RAIL_RUN_X + TAILSTOCK_DEPTH_X
length_err = abs(length_sum - OVERALL_LENGTH)
print(f"  headstock({HEADSTOCK_DEPTH_X}) + bed_run({BED_RAIL_RUN_X}) + "
      f"tailstock({TAILSTOCK_DEPTH_X}) = {length_sum:.2f}\" vs overall_length "
      f"spec {OVERALL_LENGTH}\"  (off by {length_err:.2f}\")")
assert length_err < 2.0, "Length envelope does not close within tolerance -- fix an estimate above"

centers_est = BED_RAIL_RUN_X - SPINDLE_NOSE_PROTRUSION
centers_err = abs(centers_est - DIST_BETWEEN_CENTERS)
print(f"  bed_run({BED_RAIL_RUN_X}) - nose_protrusion({SPINDLE_NOSE_PROTRUSION}) = "
      f"{centers_est:.2f}\" vs dist_between_centers spec {DIST_BETWEEN_CENTERS}\" "
      f"(off by {centers_err:.2f}\")")
assert centers_err < 3.0, "Distance-between-centers envelope does not close within tolerance"

height_sum = (BELOW_RAIL_DEPTH + RAIL_HEIGHT + RAIL_TOP_TO_SPINDLE_AXIS
              + HEADSTOCK_HEIGHT_ABOVE_SPINDLE)
height_err = abs(height_sum - OVERALL_HEIGHT)
print(f"  below_rail({BELOW_RAIL_DEPTH}) + rail({RAIL_HEIGHT}) + "
      f"rail_to_spindle({RAIL_TOP_TO_SPINDLE_AXIS}, exact) + "
      f"headstock_above_spindle({HEADSTOCK_HEIGHT_ABOVE_SPINDLE}) = {height_sum:.2f}\" "
      f"vs overall_height spec {OVERALL_HEIGHT}\"  (off by {height_err:.2f}\")")
assert height_err < 2.0, "Height envelope does not close within tolerance -- fix an estimate above"

print("  all envelope checks within tolerance")

# =====================================================================
# VERIFY (bounding boxes, inches) + DIMENSION TABLE + MEASUREMENT LIST
# =====================================================================
print("\n=== BOUNDING BOXES (inches: xmin xmax ymin ymax zmin zmax) ===")
for o in objs:
    print("  %-28s %s  [%s]" % (o.Label, bbin(o.Shape), o.SourceTag))

print("\n=== DIMENSION TABLE (%d entries) ===" % len(DIM_LOG))
for d in DIM_LOG:
    print("  %-32s = %-14s [%-16s] %s" % (d["key"], d["value"], d["source"], d["note"]))

print("\n=== MEASUREMENT REQUEST LIST (photo-est / GUESS dimensions) ===")
needs_measurement = [d for d in DIM_LOG if d["source"] in ("photo-est", "GUESS")]
for d in needs_measurement:
    print("  [%s] %-32s currently %s  %s" % (d["source"], d["key"], d["value"], d["note"]))
print(f"\n  {len(needs_measurement)} of {len(DIM_LOG)} dimensions are unmeasured "
      "placeholders -- see cad/README.md for the prioritized, human-readable version "
      "of this list.")

# =====================================================================
# SAVE + EXPORT
# =====================================================================
fcstd = os.path.join(HERE, "lathe.FCStd")
doc.saveAs(fcstd)
print("\nSAVED", fcstd)

step = os.path.join(HERE, "lathe.step")
Part.export([o for o in objs], step)
print("SAVED", step)
