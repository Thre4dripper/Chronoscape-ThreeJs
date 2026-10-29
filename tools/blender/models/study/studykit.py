"""
Study kit: a small mesh builder for the writing table and the things on it (tools/blender/models/study/*.py).

Geometry is written in the web app's frame -- metres, +Y up, +Z toward the viewer, the table top at y = 0 -- and
converted to Blender's (+Z up) when an object is built, so the glTF export (+Y up) gives back exactly these
coordinates. Builders return a StudyProp: named top-level parts with their own pivots (the web app animates the
anim_* ones and puts its own materials on glass/paper/coals/tex_* parts), plus context objects that only shade the
baked occlusion (the table under a prop, the other legs of the table).

Profiles are 2D point lists walked with the material on the LEFT (bottom to top for a turned piece, counter-
clockwise round a closed section); every face is wound from that rule, so normals always point out.
"""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix

from chronokit import material

TAU = math.tau


def _rot(rx=0.0, ry=0.0, rz=0.0):
    """three.js Euler 'XYZ': R = Rx * Ry * Rz."""
    return Matrix.Rotation(rx, 4, "X") @ Matrix.Rotation(ry, 4, "Y") @ Matrix.Rotation(rz, 4, "Z")


class MB:
    """Collects vertices (three frame) and coloured faces; build() makes one Blender object of it."""

    def __init__(self):
        self.v, self.uv, self.f = [], [], []
        self.M = [Matrix.Identity(4)]

    # ---------------------------------------------------------------- transforms
    def push(self, pos=(0, 0, 0), rot=(0, 0, 0), scale=1.0):
        s = scale if isinstance(scale, (tuple, list)) else (scale, scale, scale)
        S = Matrix.Diagonal((s[0], s[1], s[2], 1.0))
        self.M.append(self.M[-1] @ Matrix.Translation(Vector(pos)) @ _rot(*rot) @ S)
        return self

    def pop(self):
        self.M.pop()

    class _At:
        def __init__(self, mb):
            self.mb = mb

        def __enter__(self):
            return self.mb

        def __exit__(self, *a):
            self.mb.pop()

    def at(self, pos=(0, 0, 0), rot=(0, 0, 0), scale=1.0):
        self.push(pos, rot, scale)
        return MB._At(self)

    # ---------------------------------------------------------------- raw
    def vert(self, p, uv=None):
        self.v.append(self.M[-1] @ Vector(p))
        self.uv.append(uv)
        return len(self.v) - 1

    def face(self, idx, color, want=None, smooth=True):
        """A face; with `want` (a local direction) it is wound so its normal points that way."""
        idx = list(dict.fromkeys(idx))   # a fan at a pole repeats its vertex
        if len(idx) < 3:
            return
        if want is not None:
            w = (self.M[-1].to_3x3().inverted_safe().transposed() @ Vector(want))
            n = Vector()
            pts = [self.v[i] for i in idx]
            for k in range(len(pts)):
                a, b = pts[k], pts[(k + 1) % len(pts)]
                n += Vector(((a.y - b.y) * (a.z + b.z), (a.z - b.z) * (a.x + b.x), (a.x - b.x) * (a.y + b.y)))
            if n.dot(w) < 0:
                idx.reverse()
        elif self.M[-1].to_3x3().determinant() < 0:
            idx.reverse()
        self.f.append((tuple(idx), color, smooth))

    def add(self, other):
        """Append another builder's geometry (already in its own final frame) through the current transform."""
        base = len(self.v)
        M = self.M[-1]
        flip = M.to_3x3().determinant() < 0
        for p, uv in zip(other.v, other.uv):
            self.v.append(M @ p)
            self.uv.append(uv)
        for idx, c, sm in other.f:
            ii = [i + base for i in idx]
            self.f.append((tuple(reversed(ii)) if flip else tuple(ii), c, sm))

    # ---------------------------------------------------------------- primitives
    def lathe(self, prof, color, seg=24, smooth=True, arc=None, colors=None):
        """A turned piece about the local Y axis. prof: [(r, y)] bottom to top, material on the left.
        colors: optional per-segment colour list (len(prof)-1) for painted bands."""
        a0, a1 = arc if arc else (0.0, TAU)
        full = arc is None
        n = seg if full else seg + 1
        angs = [a0 + (a1 - a0) * j / seg for j in range(n)]
        rings = []
        for r, y in prof:
            if r < 1e-7:
                rings.append([self.vert((0, y, 0))] * n)
            else:
                rings.append([self.vert((r * math.cos(a), y, r * math.sin(a))) for a in angs])
        for i in range(len(prof) - 1):
            (r0, y0), (r1, y1) = prof[i], prof[i + 1]
            dr, dy = r1 - r0, y1 - y0
            if abs(dr) < 1e-9 and abs(dy) < 1e-9:
                continue
            c = colors[i] if colors else color
            A, Bv = rings[i], rings[i + 1]
            for j in range(seg):
                k = (j + 1) % n
                am = a0 + (a1 - a0) * (j + 0.5) / seg
                want = (dy * math.cos(am), -dr, dy * math.sin(am))
                self.face((A[j], A[k], Bv[k], Bv[j]), c, want, smooth)
        return self

    def sweep(self, prof, path, color, closed_prof=True, caps=True, smooth=True, up=(0, 1, 0), scales=None, cap_color=None):
        """Sweep a 2D section [(u, v)] (counter-clockwise, material inside) along a 3D polyline.
        u runs along the path's side vector N, v along its binormal B. scales: per path point section scale."""
        P = [Vector(p) for p in path]
        m = len(P)
        if closed_prof:
            area = sum(prof[i][0] * prof[(i + 1) % len(prof)][1] - prof[(i + 1) % len(prof)][0] * prof[i][1] for i in range(len(prof)))
            if area < 0:
                prof = list(reversed(prof))
        T = []
        for i in range(m):
            a = P[max(0, i - 1)]
            b = P[min(m - 1, i + 1)]
            T.append((b - a).normalized())
        upv = Vector(up)
        if abs(T[0].dot(upv)) > 0.95:
            upv = Vector((1, 0, 0)) if abs(T[0].x) < 0.9 else Vector((0, 0, 1))
        N = [upv.cross(T[0]).normalized()]
        for i in range(1, m):
            # parallel transport
            n = N[-1] - T[i] * N[-1].dot(T[i])
            N.append(n.normalized())
        Bn = [T[i].cross(N[i]).normalized() for i in range(m)]
        rings = []
        for i in range(m):
            k = scales[i] if scales else 1.0
            ring = [self.vert(tuple(P[i] + N[i] * (u * k) + Bn[i] * (v * k))) for u, v in prof]
            rings.append(ring)
        np_ = len(prof)
        segs = np_ if closed_prof else np_ - 1
        for i in range(m - 1):
            for j in range(segs):
                k = (j + 1) % np_
                (u0, v0), (u1, v1) = prof[j], prof[k]
                du, dv = u1 - u0, v1 - v0
                tm = ((N[i] + N[i + 1]) * dv - (Bn[i] + Bn[i + 1]) * du)
                self.face((rings[i][j], rings[i][k], rings[i + 1][k], rings[i + 1][j]), color, tuple(tm), smooth)
        if caps and closed_prof:
            cc = cap_color or color
            self.face(rings[0], cc, tuple(-T[0]), False)
            self.face(rings[-1], cc, tuple(T[-1]), False)
        return self

    def tube(self, path, r, color, seg=6, caps=True, smooth=True, scales=None):
        prof = [(r * math.cos(TAU * j / seg), r * math.sin(TAU * j / seg)) for j in range(seg)]
        return self.sweep(prof, path, color, True, caps, smooth, scales=scales)

    def run_x(self, prof, x0, x1, color, smooth=True, caps=False):
        """A straight moulding along +X. prof: [(o, y)] with o toward +Z (outward), material on the left."""
        A = [self.vert((x0, y, o)) for o, y in prof]
        Bv = [self.vert((x1, y, o)) for o, y in prof]
        for j in range(len(prof) - 1):
            (o0, y0), (o1, y1) = prof[j], prof[j + 1]
            do, dy = o1 - o0, y1 - y0
            self.face((A[j], A[j + 1], Bv[j + 1], Bv[j]), color, (0, -do, dy), smooth)
        if caps:
            self.face(A, color, (-1, 0, 0), False)
            self.face(Bv, color, (1, 0, 0), False)
        return self

    def corner(self, prof, color, smooth=True):
        """The mitred corner closing two run_x mouldings that meet at the origin: one along X (outward +Z)
        ending at x = 0, one along -Z... (outward +X) ending at z = 0. Fills x, z >= 0."""
        F = [self.vert((0, y, o)) for o, y in prof]
        Mv = [self.vert((o, y, o)) for o, y in prof]
        S = [self.vert((o, y, 0)) for o, y in prof]
        for j in range(len(prof) - 1):
            (o0, y0), (o1, y1) = prof[j], prof[j + 1]
            do, dy = o1 - o0, y1 - y0
            self.face((F[j], F[j + 1], Mv[j + 1], Mv[j]), color, (0, -do, dy), smooth)
            self.face((Mv[j], Mv[j + 1], S[j + 1], S[j]), color, (dy, -do, 0), smooth)
        return self

    def box(self, w, h, d, c=(0, 0, 0), color="#888888", bevel=0.0, seg=2, smooth=True, skip_top=False):
        """An axis box (w along X, h along Y, d along Z) centred at c, optionally with rounded edges.
        skip_top leaves out the flat top face and returns its corners (local, counter-clockwise from above) for a
        textured part to close it."""
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        for v in bm.verts:
            v.co = Vector((v.co.x * w, v.co.y * h, v.co.z * d))
        if bevel > 0:
            bmesh.ops.bevel(bm, geom=list(bm.edges) + list(bm.verts), offset=bevel, segments=seg, affect="EDGES", profile=0.5, clamp_overlap=True)
        top = None
        if skip_top:
            bm.normal_update()
            top = max((f for f in bm.faces if f.normal.y > 0.999), key=lambda f: f.calc_area())
        corners = self._from_bm(bm, color, c, smooth, skip=top)
        bm.free()
        return corners if skip_top else self

    def _from_bm(self, bm, color, c=(0, 0, 0), smooth=True, skip=None):
        bm.normal_update()
        bm.verts.index_update()
        ids = [self.vert((v.co.x + c[0], v.co.y + c[1], v.co.z + c[2])) for v in bm.verts]
        out = None
        for f in bm.faces:
            if f is skip:
                out = [(v.co.x + c[0], v.co.y + c[1], v.co.z + c[2]) for v in f.verts]
                continue
            self.face([ids[v.index] for v in f.verts], color, tuple(f.normal), smooth)
        return out

    def prism(self, outline, y0, y1, color, smooth=False, bevel=0.0, seg=2, holes=None, side_color=None):
        """An outline [(x, z)] in the XZ plane, extruded from y0 up to y1 (optionally with rounded edges)."""
        bm = bmesh.new()
        vs = [bm.verts.new((x, z, 0)) for x, z in outline]
        f = bm.faces.new(vs)
        bm.normal_update()
        if f.normal.z < 0:
            f.normal_flip()
        res = bmesh.ops.extrude_face_region(bm, geom=[f])
        top = [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, verts=top, vec=(0, 0, y1 - y0))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        if bevel > 0:
            bmesh.ops.bevel(bm, geom=list(bm.edges) + list(bm.verts), offset=bevel, segments=seg, affect="EDGES", profile=0.5, clamp_overlap=True)
        bm.normal_update()
        bm.verts.index_update()
        # (x, z, h) -> three (x, y0 + h, z)
        ids = [self.vert((v.co.x, y0 + v.co.z, v.co.y)) for v in bm.verts]
        for fc in bm.faces:
            n = fc.normal
            col = color if (side_color is None or abs(n.z) > 0.7) else side_color
            self.face([ids[v.index] for v in fc.verts], col, (n.x, n.z, n.y), smooth)
        bm.free()
        return self

    def ring_prism(self, outer, inner, y0, y1, color, smooth=False):
        """A band between two outlines of equal point count, extruded from y0 to y1 (a frame, a rim)."""
        n = len(outer)
        ob = [self.vert((x, y0, z)) for x, z in outer]
        ot = [self.vert((x, y1, z)) for x, z in outer]
        ib = [self.vert((x, y0, z)) for x, z in inner]
        it = [self.vert((x, y1, z)) for x, z in inner]
        for j in range(n):
            k = (j + 1) % n
            mo = Vector((outer[j][0] + outer[k][0], 0, outer[j][1] + outer[k][1])) / 2
            mi = Vector((inner[j][0] + inner[k][0], 0, inner[j][1] + inner[k][1])) / 2
            self.face((ob[j], ob[k], ot[k], ot[j]), color, tuple(mo - mi), smooth)
            self.face((ib[j], ib[k], it[k], it[j]), color, tuple(mi - mo), smooth)
            self.face((ot[j], ot[k], it[k], it[j]), color, (0, 1, 0), False)
            self.face((ob[j], ob[k], ib[k], ib[j]), color, (0, -1, 0), False)
        return self

    def ellipsoid(self, c, rx, ry, rz, color, seg=12, rings=8):
        prof = [(math.sin(math.pi * i / rings), -math.cos(math.pi * i / rings)) for i in range(rings + 1)]
        with self.at(c, scale=(rx, ry, rz)):
            self.lathe(prof, color, seg)
        return self

    def grid(self, x0, x1, z0, z1, nx, nz, height, color_of, uv=False):
        """A height field over a rectangle: height(x, z) -> y; color_of(x, z, y) -> colour per cell."""
        ids = []
        for i in range(nx + 1):
            row = []
            for j in range(nz + 1):
                x = x0 + (x1 - x0) * i / nx
                z = z0 + (z1 - z0) * j / nz
                row.append(self.vert((x, height(x, z), z), ((x - x0) / (x1 - x0), 1 - (z - z0) / (z1 - z0)) if uv else None))
            ids.append(row)
        for i in range(nx):
            for j in range(nz):
                xm = x0 + (x1 - x0) * (i + 0.5) / nx
                zm = z0 + (z1 - z0) * (j + 0.5) / nz
                self.face((ids[i][j], ids[i][j + 1], ids[i + 1][j + 1], ids[i + 1][j]), color_of(xm, zm, height(xm, zm)), (0, 1, 0), True)
        return self

    def quad_uv(self, pts, uvs, color, want=(0, 1, 0)):
        """One flat textured face (a tex_* part)."""
        ids = [self.vert(p, uv) for p, uv in zip(pts, uvs)]
        self.face(ids, color, want, False)
        return self

    # ---------------------------------------------------------------- build
    def build(self, name, pivot=(0, 0, 0), angle=48.0):
        """One Blender object (vertices relative to the pivot, object placed at it); one material slot per colour."""
        px, py, pz = pivot
        bm = bmesh.new()
        bverts = [bm.verts.new((p.x - px, -(p.z - pz), p.y - py)) for p in self.v]
        cols = []
        for _, c, _ in self.f:
            if c not in cols:
                cols.append(c)
        has_uv = any(u is not None for u in self.uv)
        uvl = bm.loops.layers.uv.new("UVMap") if has_uv else None
        for idx, c, sm in self.f:
            try:
                f = bm.faces.new([bverts[i] for i in idx])
            except ValueError:
                continue  # a duplicate face
            f.material_index = cols.index(c)
            f.smooth = sm
            if uvl:
                for loop, i in zip(f.loops, idx):
                    loop[uvl].uv = self.uv[i] or (0.0, 0.0)
        # drop unused verts (pole duplicates etc.)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
        big = [f for f in bm.faces if len(f.verts) > 4]
        if big:
            bmesh.ops.triangulate(bm, faces=big)
        bm.normal_update()
        lim = math.radians(angle)
        for e in bm.edges:
            lf = e.link_faces
            if len(lf) == 2 and (not lf[0].smooth or not lf[1].smooth or lf[0].normal.angle(lf[1].normal, 0.0) > lim or lf[0].material_index != lf[1].material_index):
                e.smooth = False
        me = bpy.data.meshes.new(name)
        bm.to_mesh(me)
        bm.free()
        for c in cols:
            me.materials.append(material(c))
        o = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(o)
        o.location = (px, -pz, py)
        return o


def P(*pts):
    """Shorthand for a profile list."""
    return [tuple(p) for p in pts]


def arc_pts(cx, cy, r, a0, a1, n):
    """Points on a circular arc (degrees, counter-clockwise from +x), for building profiles."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def rrect(w, d, r, n=4):
    """A rounded rectangle outline [(x, z)] counter-clockwise seen from above (+Y)."""
    out = []
    for cx, cz, a0 in ((w / 2 - r, d / 2 - r, 0), (-w / 2 + r, d / 2 - r, 90), (-w / 2 + r, -d / 2 + r, 180), (w / 2 - r, -d / 2 + r, 270)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            out.append((cx + r * math.cos(a), cz + r * math.sin(a)))
    return out


class StudyProp:
    """The exported parts of one study model (with pivots), plus context objects that only shade its occlusion."""

    def __init__(self, name, ao=0.04, edge=0.02, ground=True):
        self.name = name
        self.objects = []
        self.context = []
        self.ao = ao          # occlusion distance, metres
        self.edge = edge      # longest edge kept for the occlusion to live on
        self.ground = ground  # a table top under it while baking

    def part(self, name, mb, pivot=(0, 0, 0), angle=48.0):
        o = mb.build(name, pivot, angle)
        self.objects.append(o)
        return o

    def ctx(self, mb, name="ctx"):
        o = mb.build(name)
        self.context.append(o)
        return o
