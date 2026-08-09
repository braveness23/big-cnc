"""Headless shaded-isometric SVG straight from the FreeCAD model geometry.
Reads lathe.FCStd, projects solid faces axonometrically, back-face culls,
paints far-to-near with simple Lambert shading. Run: freecadcmd cad/_isosvg.py

Adapted from basement-remodel/cad/_isosvg.py (same approach, same reason:
this machine has no working offscreen GL context, so freecadcmd can't
saveImage() -- this painter's-algorithm SVG is the headless substitute).

Color is keyed off the object Label: a base color per component family,
tinted toward orange for any label ending "_EST" -- lathe.py appends that
suffix to every part built from a photo-est/GUESS dimension, so the
preview visually matches the model tree without a second color map to
keep in sync.
"""
import os
import math
import FreeCAD

HERE = os.path.dirname(os.path.abspath(__file__))
doc = FreeCAD.openDocument(os.path.join(HERE, "lathe.FCStd"))

# ---- camera (axonometric) ----
az, el = math.radians(-38), math.radians(26)
f = (-math.cos(el)*math.cos(az), -math.cos(el)*math.sin(az), -math.sin(el))  # view dir into screen


def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a, b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]


def norm(a):
    m = math.sqrt(dot(a, a)) or 1.0
    return (a[0]/m, a[1]/m, a[2]/m)


right = norm(cross(f, (0, 0, 1)))
camup = cross(right, f)
light = norm((0.4, -0.5, 0.85))


def screen(p):
    return (dot(p, right), -dot(p, camup))


# base color (r,g,b 0..255) per component family, keyed on Label prefix
FAMILY_COLOR = [
    ("BedRail", (90, 130, 90)),
    ("BedBase", (90, 130, 90)),
    ("Headstock", (60, 110, 70)),      # the machine's actual green paint
    ("Spindle", (170, 170, 175)),      # bare steel
    ("Tailstock", (60, 110, 70)),
    ("Banjo", (60, 60, 60)),
    ("ToolRest", (40, 40, 40)),
    ("SandingDiscSubsystem", (150, 150, 150)),
]
PLACEHOLDER_TINT = (255, 140, 30)  # orange -- flags photo-est/GUESS parts


def basecolor(label):
    for prefix, col in FAMILY_COLOR:
        if label.startswith(prefix):
            if label.endswith("_EST"):
                return tuple((c + t) // 2 for c, t in zip(col, PLACEHOLDER_TINT))
            return col
    return (120, 120, 120)


faces = []  # (avg_depth, screen_pts, fill)
for o in doc.Objects:
    if not hasattr(o, "Shape") or o.Shape is None:
        continue
    col = basecolor(o.Label)
    for fc in o.Shape.Faces:
        # Tessellate rather than walk OuterWire.OrderedVertexes: curved faces
        # (cylinders, cones -- half this model's parts) have circular edges
        # with no interior vertices, so the wire-walk approach silently drops
        # them. Triangles work uniformly for flat and curved faces alike.
        try:
            verts, tris = fc.tessellate(1.0)
        except Exception:
            continue
        for i0, i1, i2 in tris:
            a, b, c = verts[i0], verts[i1], verts[i2]
            n = norm(cross((b.x-a.x, b.y-a.y, b.z-a.z), (c.x-a.x, c.y-a.y, c.z-a.z)))
            if n == (0.0, 0.0, 0.0) or dot(n, f) > -0.02:  # degenerate or back-facing
                continue
            pts = [screen((v.x, v.y, v.z)) for v in (a, b, c)]
            depth = (dot((a.x, a.y, a.z), f) + dot((b.x, b.y, b.z), f) + dot((c.x, c.y, c.z), f)) / 3.0
            shade = 0.45 + 0.55 * max(0.0, dot(n, light))
            fill = tuple(min(255, int(ch * shade)) for ch in col)
            faces.append((depth, pts, fill))

faces.sort(key=lambda t: t[0], reverse=True)  # far first

xs = [p[0] for _, pts, _ in faces for p in pts]
ys = [p[1] for _, pts, _ in faces for p in pts]
minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
PAD, WIDTH = 40, 1200
scale = (WIDTH - 2*PAD) / (maxx - minx)
H = int((maxy - miny) * scale + 2*PAD) + 30


def tx(p): return ((p[0]-minx)*scale + PAD, (p[1]-miny)*scale + PAD + 30)


out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {H}" font-family="Arial">']
out.append(f'<rect x="0" y="0" width="{WIDTH}" height="{H}" fill="#ffffff"/>')
out.append('<text x="20" y="24" font-size="18" font-weight="bold">'
            'Central Machinery 36066 lathe -- isometric, ROUGH OUT (freecadcmd headless render)</text>')
out.append(f'<rect x="20" y="{H-26}" width="16" height="16" fill="rgb(255,170,80)" stroke="#333"/>')
out.append(f'<text x="42" y="{H-13}" font-size="13">orange-tinted parts = photo-est/GUESS, unmeasured -- see cad/README.md</text>')
for _, pts, fill in faces:
    d = " ".join(("%.1f,%.1f" % tx(p)) for p in pts)
    # no stroke: with triangulated (not just planar-quad) faces, a stroke
    # would draw a visible seam down the diagonal of every tessellated
    # flat face -- shading contrast between faces is enough for definition
    out.append(f'<polygon points="{d}" fill="rgb{fill}"/>')
out.append('</svg>')
svg = os.path.join(HERE, "lathe_iso.svg")
open(svg, "w").write("\n".join(out))
print("WROTE", svg, "faces:", len(faces))
