"""Headless shaded-isometric SVG for part22_panelB.FCStd. Same painter's-
algorithm approach as cad/_isosvg.py / part22_sheetmetal_isosvg.py. Run:
  freecadcmd part22_panelB_isosvg.py (from this directory)
"""
import os
import math
import FreeCAD

HERE = os.path.dirname(os.path.abspath(__file__))
doc = FreeCAD.openDocument(os.path.join(HERE, "part22_panelB.FCStd"))

az, el = math.radians(-38), math.radians(26)
f = (-math.cos(el) * math.cos(az), -math.cos(el) * math.sin(az), -math.sin(el))


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


COLOR = (60, 110, 70)

faces = []
for o in doc.Objects:
    if not (hasattr(o, "Shape") and o.Shape and o.Visibility):
        continue
    for fc in o.Shape.Faces:
        try:
            verts, tris = fc.tessellate(0.3)
        except Exception:
            continue
        for i0, i1, i2 in tris:
            a, b, c = verts[i0], verts[i1], verts[i2]
            n = norm(cross((b.x-a.x, b.y-a.y, b.z-a.z), (c.x-a.x, c.y-a.y, c.z-a.z)))
            if n == (0.0, 0.0, 0.0) or dot(n, f) > -0.02:
                continue
            pts = [screen((v.x, v.y, v.z)) for v in (a, b, c)]
            depth = (dot((a.x, a.y, a.z), f) + dot((b.x, b.y, b.z), f) + dot((c.x, c.y, c.z), f)) / 3.0
            shade = 0.45 + 0.55 * max(0.0, dot(n, light))
            fill = tuple(min(255, int(ch * shade)) for ch in COLOR)
            faces.append((depth, pts, fill))

faces.sort(key=lambda t: t[0], reverse=True)

xs = [p[0] for _, pts, _ in faces for p in pts]
ys = [p[1] for _, pts, _ in faces for p in pts]
minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
PAD, WIDTH = 40, 900
scale = (WIDTH - 2*PAD) / (maxx - minx)
H = int((maxy - miny) * scale + 2*PAD) + 30


def tx(p): return ((p[0]-minx)*scale + PAD, (p[1]-miny)*scale + PAD + 30)


out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {H}" font-family="Arial">']
out.append(f'<rect x="0" y="0" width="{WIDTH}" height="{H}" fill="#ffffff"/>')
out.append('<text x="20" y="24" font-size="16" font-weight="bold">'
            'Part #22 panel B -- tapered wedge, PHOTO-EST (not measured)</text>')
for _, pts, fill in faces:
    d = " ".join(("%.1f,%.1f" % tx(p)) for p in pts)
    out.append(f'<polygon points="{d}" fill="rgb{fill}"/>')
out.append('</svg>')
svg = os.path.join(HERE, "part22_panelB_iso.svg")
open(svg, "w").write("\n".join(out))
print("WROTE", svg, "faces:", len(faces))
