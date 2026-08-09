"""
Central Machinery (Harbor Freight) SKU# S36066 lathe -- simplified solid for
exploded-view part #22 (the parts list on manual/central-machinery-36066-manual.pdf
p.10 mislabels this "Headstock"; the diagram's own leader line for #22 actually
points at a bracket beside the tailstock upright, not the headstock casting --
see manual/exploded-view.png. This model follows the diagram, not the label.)

THIS IS NOT A MEASURED PART. It's a proof-of-concept for reconstructing clean
CAD geometry from a 2D exploded-view line drawing alone (no physical part in
hand): scale was calibrated off the M8 bolt hardware (items 47/48) visible in
the same drawing, proportions were read off the isometric sketch, and the
result was quantized to clean stock sizes (30mm square section, etc). Treat
every dimension below as diagram-est, not measured -- it has not been checked
against the real part.

Simplification: modeled as a solid box-section bar. The drawing shows a hint
of a second fold line near the top (suggesting it may actually be an open
C-channel, not solid tube) that this pass did not attempt to resolve.

Run headless:  blender --background --python part22_bracket.py (from this directory)
Outputs:       part22_bracket.blend, part22_bracket.stl,
               part22_bracket_iso.png (render, for comparison against the
               exploded-view crop it was built from)
"""
import os
import bpy
import mathutils

HERE = os.path.dirname(os.path.abspath(__file__))

# --- clean scene ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Units: 1 Blender unit = 1 mm
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 0.001


def cube(name, sx, sy, sz, loc=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return ob


def cyl(name, radius, depth, loc, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    return ob


def boolean(target, tool, op):
    mod = target.modifiers.new(name=op, type='BOOLEAN')
    mod.operation = op
    mod.object = tool
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(tool, do_unlink=True)


# --- quantized dimensions (mm), derived from pixel measurement vs M8 hardware scale ---
BODY_L = 180   # long axis, along bed rail direction
BODY_W = 30    # cross-section width (box-tube stock)
BODY_H = 30    # cross-section height
FOOT_L = 20    # foot tab length, sticking out at near end
FOOT_W = 30
FOOT_H = 15
HOLE_D = 8.5   # M8 clearance

# main body: box tube running along X
body = cube("Body", BODY_L, BODY_W, BODY_H, loc=(0, 0, 0))

# foot flange at the near end, offset down (matches drawing: tab bends
# outward near the bottom where bolt 48 passes through)
foot = cube("Foot", FOOT_L, FOOT_W, FOOT_H,
            loc=(-(BODY_L / 2 - FOOT_L / 2), 0, -(BODY_H / 2 + FOOT_H / 2)))
boolean(body, foot, 'UNION')

# hole for bolt 47 (far end, through the top face)
h1 = cyl("Hole47", HOLE_D / 2, BODY_H * 2, loc=(BODY_L / 2 - 20, 0, 0))
boolean(body, h1, 'DIFFERENCE')

# hole for bolt 48 (near end, through the foot tab)
h2 = cyl("Hole48", HOLE_D / 2, FOOT_H * 2, loc=(-(BODY_L / 2 - FOOT_L / 2), 0, -(BODY_H / 2 + FOOT_H / 2)))
boolean(body, h2, 'DIFFERENCE')

body.name = "Part22_Bracket_diagram_est"

for f in body.data.polygons:
    f.use_smooth = False

mat = bpy.data.materials.new("SteelBracket")
mat.diffuse_color = (0.55, 0.57, 0.6, 1.0)
body.data.materials.append(mat)

# --- camera: isometric-ish view similar to the source exploded-view angle ---
bpy.ops.object.camera_add(location=(320, -280, 220))
cam = bpy.context.active_object
direction = (0 - cam.location.x, 0 - cam.location.y, 0 - cam.location.z)
cam.rotation_euler = mathutils.Vector(direction).to_track_quat('-Z', 'Y').to_euler()
scene.camera = cam
cam.data.type = 'ORTHO'
cam.data.ortho_scale = 260

bpy.ops.object.light_add(type='SUN', location=(200, -200, 300))
bpy.context.active_object.data.energy = 3.0
bpy.ops.object.light_add(type='SUN', location=(-200, 200, 150))
bpy.context.active_object.data.energy = 1.2

scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 32
scene.cycles.use_denoising = False
scene.view_layers[0].cycles.use_denoising = False
scene.render.resolution_x = 1000
scene.render.resolution_y = 1000
scene.render.filepath = os.path.join(HERE, "part22_bracket_iso.png")
scene.render.image_settings.file_format = 'PNG'
scene.world = bpy.data.worlds.new("World")
scene.world.color = (1, 1, 1)

bpy.ops.render.render(write_still=True)

bpy.ops.object.select_all(action='DESELECT')
body.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.export_mesh.stl(filepath=os.path.join(HERE, "part22_bracket.stl"), use_selection=True)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "part22_bracket.blend"))

print("DONE", BODY_L, BODY_W, BODY_H)
