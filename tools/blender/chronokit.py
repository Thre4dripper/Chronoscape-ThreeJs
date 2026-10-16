"""
Chronoscape Blender kit: tiny helpers for building clay-style landmark
miniatures with bpy and exporting them as GLB for the web renderer.

Conventions (must match src/engine/landmarks/GlbModel.tsx):
  * units are metres, origin at the ground centre of the landmark
  * Blender +Z is up, +X is east, +Y is north (exporter converts to glTF +Y up,
    so Blender +Y becomes world -Z, which is north on the map)
  * every top-level object is named p<stage>_<label>; the web app reveals
    stage 0 first (it also stays as the "embossed" proxy), then 1, 2, ...
  * flat colours only, Principled BSDF, high roughness (a clay model, not a photo)
"""
import math
import bpy
import bmesh
from mathutils import Vector

PALETTE = {
    "limestone": "#D9CBB0",
    "travertine": "#D9C7A5",
    "marble": "#EDE6D6",
    "white": "#F1EBE0",
    "terracotta": "#A65238",
    "brick": "#C9A98A",
    "timber": "#9C7A58",
    "sandstone": "#A24A3C",
    "gold": "#C9A24A",
    "bronze": "#8A7A58",
    "sand": "#C8A574",
    "plaza": "#D6C39E",
    "water": "#65888A",
    "dark": "#3A2A1E",
    "green": "#8AA07A",
}


# ---------------------------------------------------------------- scene / materials

def reset_scene():
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.curves):
        for b in list(block):
            if b.users == 0:
                block.remove(b)


def _srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_to_rgba(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return (_srgb_to_linear(r), _srgb_to_linear(g), _srgb_to_linear(b), 1.0)


_MATS = {}


def material(color, roughness=0.88):
    """Flat clay material, cached by colour."""
    color = PALETTE.get(color, color)
    name = f"clay_{color.lstrip('#')}_{int(roughness * 100)}"
    existing = bpy.data.materials.get(name)
    if existing is not None:
        return existing
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    rgba = hex_to_rgba(color)
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = roughness
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = 0.2
    m.diffuse_color = rgba
    return m


def shade(hex_color, amount):
    """Lighten (+) or darken (-) a hex colour by a fraction."""
    hex_color = PALETTE.get(hex_color, hex_color)
    h = hex_color.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16)
        c = c + (255 - c) * amount if amount > 0 else c * (1 + amount)
        out.append(max(0, min(255, int(round(c)))))
    return "#%02X%02X%02X" % tuple(out)


def _finish(obj, name, color):
    obj.name = name
    obj.data.materials.clear()
    obj.data.materials.append(material(color))
    return obj


# ---------------------------------------------------------------- primitives
# All take loc=(x, y, z) as the *ground centre*; z is the base height.

def box(name, w, d, h, loc=(0, 0, 0), color="limestone", rot_z=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(loc[0], loc[1], loc[2] + h / 2))
    o = bpy.context.active_object
    o.scale = (w, d, h)
    o.rotation_euler[2] = rot_z
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    return _finish(o, name, color)


def cylinder(name, r, h, loc=(0, 0, 0), color="limestone", verts=16, r_top=None):
    if r_top is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=(loc[0], loc[1], loc[2] + h / 2))
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r_top, depth=h, location=(loc[0], loc[1], loc[2] + h / 2))
    return _finish(bpy.context.active_object, name, color)


def obelisk(name, base, h, loc=(0, 0, 0), color="sand"):
    shaft = cylinder(name, base / math.sqrt(2), h, loc, color, verts=4, r_top=base * 0.7 / math.sqrt(2))
    shaft.rotation_euler[2] = math.pi / 4
    tip = cylinder(name + "_tip", base * 0.7 / math.sqrt(2), base * 1.2, (loc[0], loc[1], loc[2] + h), color, verts=4, r_top=0)
    tip.rotation_euler[2] = math.pi / 4
    return join([shaft, tip], name)


def dome(name, r, loc=(0, 0, 0), color="white", squash=1.0, segments=20, rings=12):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=r, location=(loc[0], loc[1], loc[2]))
    o = bpy.context.active_object
    bm = bmesh.new()
    bm.from_mesh(o.data)
    geom = [v for v in bm.verts if v.co.z < -1e-4]
    bmesh.ops.delete(bm, geom=geom, context="VERTS")
    bm.to_mesh(o.data)
    bm.free()
    o.scale = (1, 1, squash)
    bpy.ops.object.transform_apply(scale=True)
    return _finish(o, name, color)


def gable_roof(name, w, d, h, loc=(0, 0, 0), color="terracotta", overhang=0.6):
    """Triangular prism; ridge runs along Y (north-south) through depth d."""
    W, D = w + 2 * overhang, d + 2 * overhang
    verts = [(-W / 2, -D / 2, 0), (W / 2, -D / 2, 0), (0, -D / 2, h), (-W / 2, D / 2, 0), (W / 2, D / 2, 0), (0, D / 2, h)]
    faces = [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]
    return mesh_from(name, verts, faces, loc, color)


def hip_roof(name, w, d, h, loc=(0, 0, 0), color="terracotta", ridge=0.4, overhang=0.6):
    W, D = w + 2 * overhang, d + 2 * overhang
    rl = D * ridge / 2
    verts = [(-W / 2, -D / 2, 0), (W / 2, -D / 2, 0), (W / 2, D / 2, 0), (-W / 2, D / 2, 0), (0, -rl, h), (0, rl, h)]
    faces = [(0, 1, 4), (1, 2, 5, 4), (2, 3, 5), (3, 0, 4, 5), (3, 2, 1, 0)]
    return mesh_from(name, verts, faces, loc, color)


def mesh_from(name, verts, faces, loc=(0, 0, 0), color="limestone"):
    me = bpy.data.meshes.new(name)
    me.from_pydata([Vector(v) + Vector(loc) for v in verts], [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    # make normals consistent
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    return _finish(o, name, color)


def ring_extrude(name, outer_pts, inner_pts, h, loc=(0, 0, 0), color="limestone", closed=True):
    """Solid band between two point loops (same length), extruded up by h."""
    n = len(outer_pts)
    verts = [(x, y, 0) for x, y in outer_pts] + [(x, y, 0) for x, y in inner_pts]
    faces = []
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    o = mesh_from(name, verts, faces, loc, color)
    bm = bmesh.new()
    bm.from_mesh(o.data)
    res = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])
    top = [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=top, vec=(0, 0, h))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(o.data)
    bm.free()
    return o


def ellipse_pts(rx, ry, n, arc=math.tau, start=0.0):
    closed = abs(arc - math.tau) < 1e-6
    return [(rx * math.cos(start + arc * i / (n if closed else n - 1)), ry * math.sin(start + arc * i / (n if closed else n - 1))) for i in range(n)], closed


def ellipse_ring(name, rx, ry, inner, h, loc=(0, 0, 0), color="travertine", n=64, arc=math.tau, start=0.0):
    outer, closed = ellipse_pts(rx, ry, n, arc, start)
    inn, _ = ellipse_pts(rx * inner, ry * inner, n, arc, start)
    return ring_extrude(name, outer, inn, h, loc, color, closed)


def stadium_pts(length, width, n_arc=24):
    """Outline with a flat end at -x and a semicircle at +x."""
    r = width / 2
    pts = [(-length / 2, -r), (length / 2 - r, -r)]
    for i in range(1, n_arc):
        a = -math.pi / 2 + math.pi * i / n_arc
        pts.append((length / 2 - r + r * math.cos(a), r * math.sin(a)))
    pts += [(length / 2 - r, r), (-length / 2, r)]
    return pts


def stadium_ring(name, length, width, thickness, h, loc=(0, 0, 0), color="travertine"):
    outer = stadium_pts(length, width)
    inner = stadium_pts(length - 2 * thickness, width - 2 * thickness)
    return ring_extrude(name, outer, inner, h, loc, color, closed=True)


def columns(name, positions, r, h, loc=(0, 0, 0), color="limestone", capital=True, verts=10):
    """A row of tapered columns with square capitals, joined into one mesh."""
    objs = []
    for i, (x, y) in enumerate(positions):
        objs.append(cylinder(f"{name}_c{i}", r, h, (loc[0] + x, loc[1] + y, loc[2]), color, verts=verts, r_top=r * 0.86))
        if capital:
            objs.append(box(f"{name}_k{i}", r * 2.6, r * 2.6, r * 0.8, (loc[0] + x, loc[1] + y, loc[2] + h), shade(color, 0.06)))
    return join(objs, name)


def peristyle(w, d, front, side, inset=0.0):
    """Column positions around a rectangle: front/back rows along x, sides along y."""
    x0, x1, y0, y1 = -w / 2 + inset, w / 2 - inset, -d / 2 + inset, d / 2 - inset
    pts = []
    for i in range(front):
        x = 0 if front == 1 else x0 + (x1 - x0) * i / (front - 1)
        pts.append((x, y0))  # front row, south (-y)
        if side > 0:
            pts.append((x, y1))
    if side > 2:
        for j in range(1, side - 1):
            y = y0 + (y1 - y0) * j / (side - 1)
            pts += [(x0, y), (x1, y)]
    return pts


def steps(name, w, total_h, n, loc=(0, 0, 0), color="limestone", tread=1.2, direction=-1):
    """Flight of steps descending from the platform edge toward ±y."""
    objs = []
    rise = total_h / n
    for i in range(n):
        depth = tread * (i + 1)
        y = loc[1] + direction * (depth / 2)
        objs.append(box(f"{name}_{i}", w, depth, rise, (loc[0], y, loc[2] + total_h - rise * (i + 1)), color))
    return join(objs, name)


# ---------------------------------------------------------------- assembly / export

def join(objs, name):
    objs = [o for o in objs if o is not None]
    if not objs:
        return None
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1:
        bpy.ops.object.join()
    o = bpy.context.active_object
    o.name = name
    return o


class Model:
    """Collects objects per reveal stage, joins each stage, exports GLB."""

    def __init__(self, name):
        self.name = name
        self.stages = {}
        self.labels = {}

    def add(self, stage, obj, label=None):
        if obj is None:
            return
        self.stages.setdefault(stage, []).append(obj)
        if label:
            self.labels[stage] = label
        return obj

    def finish(self):
        out = []
        for idx in sorted(self.stages):
            label = self.labels.get(idx, f"stage{idx}")
            o = join(self.stages[idx], f"p{idx}_{label}")
            # origin at world origin so the stage scales from the ground plane
            bpy.context.scene.cursor.location = (0, 0, 0)
            bpy.ops.object.select_all(action="DESELECT")
            o.select_set(True)
            bpy.context.view_layer.objects.active = o
            bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
            bpy.ops.object.shade_flat()
            out.append(o)
        self.objects = out
        return out

    def export(self, path):
        bpy.ops.object.select_all(action="DESELECT")
        for o in self.objects:
            o.select_set(True)
        kwargs = dict(filepath=path, export_format="GLB", use_selection=True, export_apply=True)
        props = bpy.ops.export_scene.gltf.get_rna_type().properties.keys()
        for k, v in dict(export_yup=True, export_animations=False, export_skins=False, export_morph=False,
                         export_texcoords=False, export_normals=True, export_cameras=False, export_lights=False,
                         export_extras=False, export_image_format="NONE").items():
            if k in props:
                kwargs[k] = v
        bpy.ops.export_scene.gltf(**kwargs)
        tris = sum(len(o.data.polygons) for o in self.objects)
        return {"file": path, "stages": [o.name for o in self.objects], "faces": tris}


def frame_all():
    """Point the default camera at the model for screenshots."""
    bpy.ops.object.select_all(action="SELECT")
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            with bpy.context.temp_override(area=area, region=next(r for r in area.regions if r.type == "WINDOW")):
                bpy.ops.view3d.view_all()
    bpy.ops.object.select_all(action="DESELECT")


# ---------------------------------------------------------------- extra primitives

def ellipse_disc(name, rx, ry, h, loc=(0, 0, 0), color="sand", verts=64):
    o = cylinder(name, 1.0, h, loc, color, verts=verts)
    o.scale = (rx, ry, 1)
    bpy.ops.object.transform_apply(scale=True)
    return o


def slab_from_pts(name, pts, h, loc=(0, 0, 0), color="sand"):
    """Flat n-gon outline extruded up by h."""
    verts = [(x, y, 0) for x, y in pts]
    o = mesh_from(name, verts, [tuple(range(len(pts)))], loc, color)
    bm = bmesh.new()
    bm.from_mesh(o.data)
    res = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])
    top = [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=top, vec=(0, 0, h))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(o.data)
    bm.free()
    return o


def boolean_cut(obj, cutter):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new("cut", "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = cutter
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)
    return obj


def mini_temple(name, w, d, podium, col_h, front, side, loc=(0, 0, 0), color="limestone", roof_color="terracotta", col_r=None):
    """Returns (base, body, roof) objects for a small temple facing -y."""
    col_r = col_r or min(w / (front * 4.5), 1.4)
    base = join([
        box(f"{name}_podium", w, d, podium, loc, shade(color, -0.08)),
        steps(f"{name}_steps", w * 0.6, podium, max(2, int(podium // 1.2)), (loc[0], loc[1] - d / 2, loc[2]), shade(color, -0.06)),
    ], f"{name}_base")
    cols = columns(f"{name}_cols", peristyle(w - col_r * 2, d - col_r * 2, front, side), col_r, col_h, (loc[0], loc[1], loc[2] + podium), color)
    cw = w * (0.62 if side > 0 else 0.85)
    cd = d * (0.62 if side > 0 else 0.6)
    cella = box(f"{name}_cella", cw, cd, col_h, (loc[0], loc[1] + d * 0.08, loc[2] + podium), shade(color, -0.04))
    door = box(f"{name}_door", cw * 0.18, 0.6, col_h * 0.55, (loc[0], loc[1] + d * 0.08 - cd / 2 - 0.2, loc[2] + podium), "dark")
    body = join([cols, cella, door], f"{name}_body")
    ent_z = loc[2] + podium + col_h + col_r * 0.8
    roof = join([
        box(f"{name}_ent", w, d, 1.6, (loc[0], loc[1], ent_z), shade(color, 0.04)),
        gable_roof(f"{name}_roof", w, d, w * 0.16, (loc[0], loc[1], ent_z + 1.6), roof_color),
    ], f"{name}_roof")
    return base, body, roof


def render_preview(path, size=900, angle_deg=35, azimuth_deg=-35):
    """Workbench render of everything in the scene from a three-quarter view."""
    import mathutils
    scene = bpy.context.scene
    meshes = [o for o in scene.objects if o.type == "MESH"]
    pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    center = (lo + hi) / 2
    extent = max(hi - lo)
    cam_data = bpy.data.cameras.new("preview_cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = extent * 1.25
    cam_data.clip_end = extent * 20
    cam = bpy.data.objects.new("preview_cam", cam_data)
    scene.collection.objects.link(cam)
    el, az = math.radians(angle_deg), math.radians(azimuth_deg)
    direction = Vector((math.cos(el) * math.sin(az), -math.cos(el) * math.cos(az), math.sin(el)))
    cam.location = center + direction * extent * 4
    cam.rotation_euler = (-direction).to_track_quat("-Z", "Y").to_euler()
    scene.camera = cam
    try:
        scene.render.engine = "BLENDER_WORKBENCH"
    except TypeError:
        pass
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "MATERIAL"
    scene.display.shading.show_shadows = True
    scene.display.shading.show_cavity = True
    scene.render.resolution_x = size
    scene.render.resolution_y = int(size * 0.6)
    scene.render.resolution_percentage = 100
    scene.render.filepath = path
    scene.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)
    bpy.data.cameras.remove(cam_data)
    return path
