"""Studio render of part #22 -- Blender/Cycles, geometry straight from FreeCAD.

This does NOT re-model the bracket. It imports part22_channel.stl, which
part22_channel.py writes from the same solid it exports to STEP, so the render
and the CAD can't drift apart. Re-run part22_channel.py first if you've changed
a dimension.

Paint is the machine's hammertone green, faked with a noise bump -- the real
finish is a speckled powder coat (see traces/part22_panelB_trace_realpart.jpg).

Headless only: this box has no GL, so Workbench/EEVEE fail on EGL and Cycles
CPU is the only engine that works. The build also has no OpenImageDenoise, so
denoising must stay off.

Run (from this directory):
    freecadcmd part22_channel.py                       # writes the .stl
    blender -b -noaudio -P part22_channel_blender.py -- <out.png> <width> <samples>
"""
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(bpy.data.filepath or __file__)) \
    if "__file__" in dir() else os.getcwd()
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = ARGS[0] if ARGS else os.path.join(HERE, "part22_channel_render.png")
RES = int(ARGS[1]) if len(ARGS) > 1 else 1000
SAMPLES = int(ARGS[2]) if len(ARGS) > 2 else 128
STL = os.path.join(HERE, "part22_channel.stl")

if not os.path.exists(STL):
    sys.exit("missing %s -- run 'freecadcmd part22_channel.py' first" % STL)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.lights):
    for item in list(coll):
        coll.remove(item)

# ---- import the CAD mesh ------------------------------------------------
try:
    bpy.ops.wm.stl_import(filepath=STL)            # Blender 4.2+
except AttributeError:
    bpy.ops.import_mesh.stl(filepath=STL)          # Blender <= 4.1
part = bpy.context.selected_objects[0]
part.name = "Part22Channel_EST"

# Orientation: lay it web-down with both flanges UP, matching how the real
# part was photographed (traces/part22_panelB_trace_realpart.jpg). Standing it
# on the wide bottom flange -- its in-service pose -- buries that flange
# against the floor and the C-section reads as a plain wedge from every angle.
bpy.ops.object.select_all(action='DESELECT')
part.select_set(True)
bpy.context.view_layer.objects.active = part
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
part.location = (0, 0, 0)
part.rotation_euler = (math.radians(-90), 0, math.radians(-24))
bpy.context.view_layer.update()

# re-centre and ground AFTER rotating, then take dimensions from the world bbox
wv = [part.matrix_world @ v.co for v in part.data.vertices]
xs = [v.x for v in wv]; ys = [v.y for v in wv]; zs = [v.z for v in wv]
part.location.x -= (min(xs) + max(xs)) / 2.0
part.location.y -= (min(ys) + max(ys)) / 2.0
part.location.z -= min(zs)


import mathutils
DIMS = mathutils.Vector((max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)))
bpy.ops.object.shade_smooth()
part.data.use_auto_smooth = True
part.data.auto_smooth_angle = math.radians(28)


# ---- hammertone green powder coat --------------------------------------
def hammertone():
    m = bpy.data.materials.new("HammertoneGreen")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.105, 0.215, 0.115, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.25
    bsdf.inputs["Roughness"].default_value = 0.44

    tex = nt.nodes.new("ShaderNodeTexNoise")     # the speckle
    tex.inputs["Scale"].default_value = 220.0
    tex.inputs["Detail"].default_value = 6.0
    tex.inputs["Roughness"].default_value = 0.75
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.28
    bump.inputs["Distance"].default_value = 0.06
    nt.links.new(tex.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

    # let the speckle break up roughness too, so highlights sparkle
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[0].color = (0.34, 0.34, 0.34, 1)
    ramp.color_ramp.elements[1].position = 0.72
    ramp.color_ramp.elements[1].color = (0.60, 0.60, 0.60, 1)
    nt.links.new(tex.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Roughness"])
    return m


part.data.materials.clear()
part.data.materials.append(hammertone())

# ---- studio -------------------------------------------------------------
floor_m = bpy.data.materials.new("Floor")
floor_m.use_nodes = True
fb = floor_m.node_tree.nodes["Principled BSDF"]
fb.inputs["Base Color"].default_value = (0.25, 0.26, 0.28, 1)
fb.inputs["Roughness"].default_value = 0.38
bpy.ops.mesh.primitive_plane_add(size=4000, location=(0, 0, 0))
bpy.context.object.data.materials.append(floor_m)

world = bpy.data.worlds.new("W")
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.045, 0.052, 0.062, 1)
bg.inputs[1].default_value = 1.0

R = max(DIMS)          # scale the rig off the part, not off magic numbers


def area(name, loc, rot, size, energy):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.size, ld.energy = size, energy
    ob = bpy.data.objects.new(name, ld)
    ob.location, ob.rotation_euler = loc, rot
    bpy.context.collection.objects.link(ob)


area("key",  (-1.1 * R, -1.3 * R, 1.5 * R),
     (math.radians(44), 0, math.radians(-42)), 1.5 * R, 62 * R * R)
area("fill", (1.5 * R, -0.9 * R, 0.6 * R),
     (math.radians(78), 0, math.radians(60)), 1.8 * R, 16 * R * R)
area("rim",  (0.6 * R, 1.5 * R, 1.1 * R),
     (math.radians(126), 0, math.radians(192)), 1.3 * R, 44 * R * R)

cam_d = bpy.data.cameras.new("cam")
cam_d.lens = 72
cam = bpy.data.objects.new("cam", cam_d)
bpy.context.collection.objects.link(cam)
# Frame the part instead of hand-tuning: put the camera far enough back that
# the body diagonal fits the horizontal FOV, at a fixed 3/4 azimuth/elevation.
_diag = math.sqrt(DIMS.x ** 2 + DIMS.y ** 2 + DIMS.z ** 2)
_fov = 2 * math.atan(18.0 / cam_d.lens)          # 36mm sensor, horizontal
_dist = (_diag * 0.54) / math.tan(_fov / 2)
# low-ish elevation on purpose: the flanges are only 23/31mm deep on a
# 207x103 part, so from a high angle they foreshorten into invisibility
_az, _el = math.radians(34), math.radians(34)
cam.location = (_dist * math.sin(_az) * math.cos(_el),
                -_dist * math.cos(_az) * math.cos(_el),
                _dist * math.sin(_el))
bpy.context.scene.camera = cam
bpy.ops.object.empty_add(location=(0, 0, DIMS.z * 0.40))
tt = cam.constraints.new('TRACK_TO')
tt.target = bpy.context.object
tt.track_axis, tt.up_axis = 'TRACK_NEGATIVE_Z', 'UP_Y'

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = False        # this build has no OpenImageDenoise
sc.render.resolution_x = RES
sc.render.resolution_y = int(RES * 0.78)
sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.filepath = OUT

print("PART_DIMS_MM %.1f x %.1f x %.1f" % (DIMS.x, DIMS.y, DIMS.z))
print("TRIS %d" % len(part.data.polygons))
bpy.ops.render.render(write_still=True)
print("RENDER_DONE", OUT)
