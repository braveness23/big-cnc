"""
Fastener/hardware specifications for items identified in the Central
Machinery 36066 exploded-view parts list (manual/exploded-view.png).

Companion to lathe.py's source-tagged dimension table: same dim()
provenance convention (see lathe.py's module docstring for the base tag
legend), applied here to fasteners instead of machine geometry. This is a
plain data module -- no FreeCAD/Blender dependency -- so other scripts
(e.g. part22_bracket.py, which currently only tracks bolts 47/48 as a
clearance-hole diameter) can import FASTENERS from here for the full spec.

Source tags used here (extends lathe.py's legend):
  manual-partslist      -- item number from the manual's exploded-view parts list
  measured-YYYY-MM-DD    -- measured directly off the physical part with calipers, dated
  assumed-metric-coarse  -- not measured; assumed default ISO coarse pitch for the diameter
  DERIVED                -- computed from other tagged values here; formula in note

Run directly to print the recorded specs:
    python cad/hardware_specs.py
"""

DIM_LOG = []


def dim(key, value, source, note=""):
    DIM_LOG.append({"key": key, "value": value, "source": source, "note": note})
    return value


# ---- Part 47: bolt through bracket #22's far-end hole (see part22_bracket.py Hole47) ----
PART_47_BOLT = dict(
    item_no=dim("part47_item_no", 47, "manual-partslist"),
    type="hex bolt",
    diameter_mm=dim("part47_diameter_mm", 8.0, "measured-2026-08-10"),
    length_mm=dim("part47_length_mm", 55.0, "measured-2026-08-10",
                   "measured under-head to tip (flat-bottomed hex head)"),
    thread_pitch_mm=dim("part47_thread_pitch_mm", 1.25, "assumed-metric-coarse",
                         "M8 coarse pitch assumed by default -- not confirmed with a thread gauge"),
    property_class=dim("part47_property_class", "4.8", "measured-2026-08-10", "stamped on bolt head"),
    tensile_mpa=dim("part47_tensile_mpa", 400, "DERIVED", "property class 4.8 -> 4 x 100 MPa"),
    yield_mpa=dim("part47_yield_mpa", 320, "DERIVED", "property class 4.8 -> 400 MPa x 0.8"),
    head_width_af_mm=dim("part47_head_width_af_mm", 13.0, "measured-2026-08-10",
                          "raw caliper reading was 13.78mm, taken across corners rather than "
                          "across flats on the hex; a 13mm wrench/socket fits"),
    head_type="hex",
)

# ---- Part 48: bolt through bracket #22's foot tab (see part22_bracket.py Hole48) ----
# Same hardware as part 47, shorter -- passes through the thinner foot tab (FOOT_H=15mm)
# rather than the full body section.
PART_48_BOLT = dict(
    item_no=dim("part48_item_no", 48, "manual-partslist"),
    type="hex bolt",
    diameter_mm=dim("part48_diameter_mm", 8.0, "DERIVED", "same hardware as part 47"),
    length_mm=dim("part48_length_mm", 15.75, "measured-2026-08-10",
                   "measured under-head to tip (flat-bottomed hex head)"),
    thread_pitch_mm=dim("part48_thread_pitch_mm", 1.25, "assumed-metric-coarse",
                         "M8 coarse pitch assumed by default -- not confirmed with a thread gauge"),
    property_class=dim("part48_property_class", "4.8", "DERIVED", "same hardware as part 47"),
    tensile_mpa=dim("part48_tensile_mpa", 400, "DERIVED", "property class 4.8 -> 4 x 100 MPa"),
    yield_mpa=dim("part48_yield_mpa", 320, "DERIVED", "property class 4.8 -> 400 MPa x 0.8"),
    head_width_af_mm=dim("part48_head_width_af_mm", 13.0, "DERIVED", "same hardware as part 47"),
    head_type="hex",
)

# ---- Part 53: nut mating to the part-47/part-48 bolts ----
PART_53_NUT = dict(
    item_no=dim("part53_item_no", 53, "manual-partslist"),
    type="hex nut",
    thread_diameter_mm=dim("part53_thread_diameter_mm", 8.0, "DERIVED", "must match parts 47/48"),
    thread_pitch_mm=dim("part53_thread_pitch_mm", 1.25, "DERIVED", "must match parts 47/48"),
    mates_with=["PART_47_BOLT", "PART_48_BOLT"],
)

# ---- Washers under the part-47/part-48 bolt heads (no item number given/visible) ----
WASHER_M8 = dict(
    item_no=None,
    type="flat washer",
    inner_diameter_mm=dim("washer_m8_id_mm", 8.0, "DERIVED", "clearance for M8 shaft"),
    qty_per_bolt=dim("washer_m8_qty_per_bolt", 2, "manual-partslist", "no item number given for this component"),
)
LOCK_WASHER_M8 = dict(
    item_no=None,
    type="split lock washer",
    inner_diameter_mm=dim("lock_washer_m8_id_mm", 8.0, "DERIVED", "clearance for M8 shaft"),
    qty_per_bolt=dim("lock_washer_m8_qty_per_bolt", 1, "manual-partslist", "no item number given for this component"),
)

# fastener stack, head to nut, for both bolt locations on part 22
BOLT_STACK = ["PART_47_BOLT or PART_48_BOLT", "2x WASHER_M8", "1x LOCK_WASHER_M8", "PART_53_NUT"]

FASTENERS = {47: PART_47_BOLT, 48: PART_48_BOLT, 53: PART_53_NUT}
WASHERS = {"flat": WASHER_M8, "lock": LOCK_WASHER_M8}

if __name__ == "__main__":
    for entry in DIM_LOG:
        note = f"  # {entry['note']}" if entry["note"] else ""
        print(f"{entry['key']:28s} {str(entry['value']):<8s} [{entry['source']}]{note}")
