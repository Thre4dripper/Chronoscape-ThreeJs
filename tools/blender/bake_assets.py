"""
Bake pipeline for landmark miniatures.

For each model: build it at full detail, merge coplanar faces (lossless), cap the
triangle count (detail that is removed is baked from the full mesh), unwrap all
stage objects into one atlas, and bake Cycles lighting + ambient occlusion +
edge wear into that atlas. The exported GLB carries one texture and is drawn
unlit in the app, so it costs a few draw calls and a tiny shader.

Also renders a top-down shadow decal (assets/models/shadows/<key>.webp) that the
app lays on the paper under the risen model.

In Blender (MCP):  exec(open(".../bake_assets.py").read()); bake("rome/colosseum")
Headless:          blender -b -P tools/blender/bake_assets.py -- rome/colosseum
"""
import json, math, os, sys, importlib, time
import bpy, bmesh
import numpy as np
from mathutils import Vector

ROOT = "/Users/ijlalahmad/Desktop/test/Chronoscape"
for p in (os.path.join(ROOT, "tools", "blender"), os.path.join(ROOT, "tools", "blender", "models")):
    if p not in sys.path:
        sys.path.insert(0, p)

import chronokit
importlib.reload(chronokit)

SUN_DIR = Vector((-0.45, 0.40, 0.80)).normalized()   # toward the light: north-west, high (Blender: +Y north, +Z up)


def builders():
    import archkit
    importlib.reload(archkit)
    import rome, rome_more, rome_fora, delhi
    for m in (rome, rome_more, rome_fora, delhi):
        importlib.reload(m)
    import rome_hero, rome_hero2, props
    importlib.reload(rome_hero)
    importlib.reload(rome_hero2)
    importlib.reload(props)
    hero = {**rome_hero.BUILDERS, **rome_hero2.BUILDERS, **props.BUILDERS}
    return {**rome.BUILDERS, **rome_more.BUILDERS, **rome_fora.BUILDERS, **delhi.BUILDERS, **hero, **city_builders()}



def city_builders():
    import citymods
    importlib.reload(citymods)
    return citymods.city_builders()


def set_cycles(samples):
    scene = bpy.context.scene
    try:
        scene.render.engine = "CYCLES"
    except TypeError as e:
        raise RuntimeError(f"Cycles not available: {e}")
    c = scene.cycles
    if os.environ.get("BAKE_CPU"):
        # headless runs from a terminal can hang initialising Metal; the occlusion bake is light enough for the CPU
        c.device = "CPU"
        c.samples = samples
        c.use_denoising = False
        scene.render.bake.margin = 6
        scene.render.bake.use_clear = False
        return
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "METAL"
        prefs.refresh_devices()
        for d in prefs.devices:
            d.use = d.type != "CPU"
    except Exception:
        pass
    c.device = "GPU"
    c.samples = samples
    c.use_denoising = True
    try:
        c.denoiser = "OPENIMAGEDENOISE"
    except Exception:
        pass
    scene.render.bake.margin = 6
    scene.render.bake.use_clear = False


def lighting():
    scene = bpy.context.scene
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    bg = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs[0].default_value = (0.78, 0.74, 0.66, 1)   # warm paper-coloured sky
    bg.inputs[1].default_value = 0.85
    for o in [o for o in scene.objects if o.type == "LIGHT"]:
        bpy.data.objects.remove(o, do_unlink=True)
    sun_data = bpy.data.lights.new("bake_sun", "SUN")
    sun_data.energy = 3.2
    sun_data.angle = math.radians(4)
    sun_data.color = (1.0, 0.95, 0.86)
    sun = bpy.data.objects.new("bake_sun", sun_data)
    scene.collection.objects.link(sun)
    sun.rotation_euler = (-SUN_DIR).to_track_quat("-Z", "Y").to_euler()


def wear_materials(objs):
    """Give every material a subtle edge-wear / cavity response (Cycles pointiness), so bakes read like a painted miniature."""
    seen = set()
    for o in objs:
        for slot in o.material_slots:
            m = slot.material
            if not m or m.name in seen:
                continue
            seen.add(m.name)
            nt = m.node_tree
            bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
            if not bsdf or any(n.type == "NEW_GEOMETRY" for n in nt.nodes):
                continue
            base = tuple(bsdf.inputs["Base Color"].default_value)
            geo = nt.nodes.new("ShaderNodeNewGeometry")
            ramp = nt.nodes.new("ShaderNodeValToRGB")
            ramp.color_ramp.elements[0].position = 0.44
            ramp.color_ramp.elements[0].color = (base[0] * 0.78, base[1] * 0.76, base[2] * 0.74, 1)
            ramp.color_ramp.elements[1].position = 0.58
            ramp.color_ramp.elements[1].color = (min(1, base[0] * 1.06), min(1, base[1] * 1.05), min(1, base[2] * 1.04), 1)
            mid = ramp.color_ramp.elements.new(0.5)
            mid.color = base
            nt.links.new(geo.outputs["Pointiness"], ramp.inputs["Fac"])
            nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])


def tri_count(o):
    return sum(len(p.vertices) - 2 for p in o.data.polygons)


def planar(o, angle=2.0):
    bm = bmesh.new()
    bm.from_mesh(o.data)
    # faces lying on the ground and facing down are never seen: drop them (saves texels and triangles)
    mw = o.matrix_world
    ground = [f for f in bm.faces if (mw.to_3x3() @ f.normal).z < -0.95 and (mw @ f.calc_center_median()).z < 0.05]
    bmesh.ops.delete(bm, geom=ground, context="FACES")
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(angle), verts=bm.verts, edges=bm.edges, delimit={"MATERIAL"})
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.to_mesh(o.data)
    bm.free()


def duplicate(o, name):
    d = o.copy()
    d.data = o.data.copy()
    d.name = name
    bpy.context.collection.objects.link(d)
    return d


def select_only(objs, active=None):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = active or objs[0]


def bake(key, tex_px=None, budget=None, samples=48, out_dir=None, density=6.0):
    t0 = time.time()
    B = builders()
    chronokit.reset_scene()
    m = B[key]()
    if hasattr(m, "stages"):
        m.finish()
    highs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    names = [o.name for o in highs]
    size = max(max(o.dimensions) for o in highs)
    tex_given = tex_px
    # triangle cap: models under it keep every (planar-merged) triangle
    budget = budget or (70000 if size > 150 else 40000 if size > 60 else 20000)
    set_cycles(samples)
    lighting()
    wear_materials(highs)

    # ---- lossless planar merge; collapse further only when over the triangle cap
    for h in highs:
        planar(h)
    tri_total = sum(tri_count(h) for h in highs)
    ratio = min(1.0, budget / max(1, tri_total))
    decimate = ratio < 0.98
    lows = []
    for h, nm in zip(highs, names):
        if decimate:
            h.name = nm + "__hi"
            lo = duplicate(h, nm)
            mod = lo.modifiers.new("dec", "DECIMATE")
            mod.decimate_type = "COLLAPSE"
            mod.ratio = max(0.25, ratio)
            mod.use_collapse_triangulate = True
            select_only([lo])
            bpy.ops.object.modifier_apply(modifier=mod.name)
        else:
            lo = h      # bake straight onto the model: no ray-casting between near-identical copies
        lows.append(lo)

    # ---- atlas size from visible surface area: about 6 texels per metre, power of two, 512..4096
    if not tex_given:
        # ground-level floors (plazas, gardens, arena sand) need few texels: leave them out of the sizing
        area = 0.0
        for lo in lows:
            mw = lo.matrix_world
            for p in lo.data.polygons:
                c = mw @ p.center
                if c.z < 1.2 and (mw.to_3x3() @ p.normal).z > 0.9:
                    area += p.area * 0.08
                else:
                    area += p.area
        want = math.sqrt(area) * density
        tex_px = 512
        while tex_px < want and tex_px < 4096:
            tex_px *= 2
    else:
        tex_px = tex_given

    # ---- one atlas for the whole model
    select_only(lows)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.003, area_weight=0.0, correct_aspect=True, scale_to_bounds=False)
    try:
        bpy.ops.uv.pack_islands(margin=0.002, rotate=True)
    except Exception:
        pass
    bpy.ops.object.mode_set(mode="OBJECT")
    img = bpy.data.images.new(f"bake_{key.replace('/', '_')}", tex_px, tex_px, alpha=False)
    img.generated_color = (0.5, 0.45, 0.4, 1)
    bake_mat = bpy.data.materials.new("baked")
    bake_mat.use_nodes = True
    nt = bake_mat.node_tree
    tex_node = nt.nodes.new("ShaderNodeTexImage")
    tex_node.image = img
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    nt.links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
    nt.nodes.active = tex_node

    t_bake = time.time()
    if decimate:
        for lo in lows:
            lo.data.materials.clear()
            lo.data.materials.append(bake_mat)
        for h, lo in zip(highs, lows):
            select_only([h, lo], active=lo)
            ext = max(0.05, size * 0.004)
            bpy.ops.object.bake(type="COMBINED", use_selected_to_active=True, cage_extrusion=ext, max_ray_distance=ext * 4, margin=6, use_clear=False, target="IMAGE_TEXTURES")
    else:
        # every original material gets the atlas as its active (unconnected) image node: that is the bake target
        mats = {slot.material for lo in lows for slot in lo.material_slots if slot.material}
        for mm in mats:
            n = mm.node_tree.nodes.new("ShaderNodeTexImage")
            n.image = img
            mm.node_tree.nodes.active = n
        select_only(lows)
        bpy.ops.object.bake(type="COMBINED", margin=6, use_clear=True, target="IMAGE_TEXTURES")
        highs = [duplicate(lo, lo.name + "__shadowsrc") for lo in lows]   # shadow render needs the coloured model
        for lo in lows:
            lo.data.materials.clear()
            lo.data.materials.append(bake_mat)
    t_bake = time.time() - t_bake
    out_dir = out_dir or os.path.join(ROOT, "assets", "models")
    denoise(img)
    tex_path = os.path.join(ROOT, "tools", "blender", "baked", key + ".png")
    os.makedirs(os.path.dirname(tex_path), exist_ok=True)
    img.filepath_raw = tex_path
    img.file_format = "PNG"
    img.save()
    # the exporter embeds the texture; use JPEG-like WEBP? glTF core only allows PNG/JPEG
    img.file_format = "JPEG"

    # ---- shadow decal (rendered before the highs are removed)
    t_sh = time.time()
    shadow = render_shadow(key, highs, size)
    t_sh = time.time() - t_sh

    for h in highs:
        bpy.data.objects.remove(h, do_unlink=True)
    for lo in lows:
        select_only([lo])
        bpy.ops.object.shade_flat()

    path = os.path.join(out_dir, key + ".glb")
    select_only(lows)
    for e in bpy.context.scene.objects:      # keep named markers (smoke origins and the like)
        if e.type == "EMPTY":
            e.select_set(True)
    kw = dict(filepath=path, export_format="GLB", use_selection=True, export_apply=True)
    props = bpy.ops.export_scene.gltf.get_rna_type().properties.keys()
    for k, v in dict(export_yup=True, export_animations=False, export_texcoords=True, export_normals=False, export_cameras=False, export_lights=False,
                     export_extras=False, export_image_format="JPEG", export_jpeg_quality=86,
                     export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6,
                     export_draco_position_quantization=14, export_draco_texcoord_quantization=12).items():
        if k in props:
            kw[k] = v
    bpy.ops.export_scene.gltf(**kw)
    tris = sum(tri_count(o) for o in lows)
    return {"key": key, "tris": tris, "from_tris": tri_total, "tex": tex_px, "kb": os.path.getsize(path) // 1024, "s": round(time.time() - t0, 1), "bake_s": round(t_bake, 1), "shadow_s": round(t_sh, 1)}


def denoise(img):
    """Run Open Image Denoise over the baked atlas through the compositor (bakes are never denoised by Cycles)."""
    scene = bpy.context.scene
    prev_engine, prev_cam = scene.render.engine, scene.camera
    scene.use_nodes = True
    tree = scene.node_tree if hasattr(scene, "node_tree") and scene.node_tree else None
    if tree is None:
        try:
            tree = bpy.data.node_groups.new("bake_denoise", "CompositorNodeTree")
            scene.compositing_node_group = tree
        except Exception:
            tree = scene.node_tree
    for n in list(tree.nodes):
        tree.nodes.remove(n)
    src = tree.nodes.new("CompositorNodeImage")
    src.image = img
    dn = tree.nodes.new("CompositorNodeDenoise")
    try:
        dn.prefilter = "ACCURATE"
    except Exception:
        pass
    out_node = None
    for t in ("CompositorNodeComposite", "NodeGroupOutput"):
        try:
            out_node = tree.nodes.new(t)
            break
        except Exception:
            continue
    tree.links.new(src.outputs[0], dn.inputs[0])
    if out_node.bl_idname == "NodeGroupOutput":
        try:
            tree.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
        except Exception:
            pass
    tree.links.new(dn.outputs[0], out_node.inputs[0])
    # a camera is required to render; the compositor output replaces the (cheap) workbench render
    cd = bpy.data.cameras.new("dn_cam")
    cam = bpy.data.objects.new("dn_cam", cd)
    scene.collection.objects.link(cam)
    scene.camera = cam
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x, scene.render.resolution_y = img.size
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    tmp = os.path.join(ROOT, "tools", "blender", "baked", "_denoise.png")
    scene.render.filepath = tmp
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    bpy.ops.render.render(write_still=True)
    den = bpy.data.images.load(tmp, check_existing=False)
    img.pixels = den.pixels[:]
    bpy.data.images.remove(den)
    os.remove(tmp)
    bpy.data.objects.remove(cam, do_unlink=True)
    bpy.data.cameras.remove(cd)
    scene.use_nodes = False
    try:
        scene.compositing_node_group = None
    except Exception:
        pass
    bpy.data.node_groups.remove(tree) if tree.name.startswith("bake_denoise") else None
    scene.render.engine = prev_engine
    scene.camera = prev_cam


def render_shadow(key, objs, size):
    """Top-down render of the model's cast shadow alone, on a transparent background."""
    scene = bpy.context.scene
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    x0, x1 = min(p.x for p in pts), max(p.x for p in pts)
    y0, y1 = min(p.y for p in pts), max(p.y for p in pts)
    z1 = max(p.z for p in pts)
    pad = z1 * 0.9 + 4
    cx, cy = (x0 + x1) / 2 - SUN_DIR.x * pad * 0.0, (y0 + y1) / 2
    span = max(x1 - x0, y1 - y0) + 2 * pad
    bpy.ops.mesh.primitive_plane_add(size=span * 1.2, location=(cx, cy, 0.01))
    catcher = bpy.context.active_object
    catcher.is_shadow_catcher = True
    hidden = [o for o in scene.objects if o.type == "MESH" and o is not catcher]
    for o in hidden:
        o.visible_camera = False
    cam_data = bpy.data.cameras.new("shadow_cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = span
    cam = bpy.data.objects.new("shadow_cam", cam_data)
    scene.collection.objects.link(cam)
    cam.location = (cx, cy, z1 + 100)
    cam.rotation_euler = (0, 0, 0)
    scene.camera = cam
    px = int(max(128, min(1024, span * 2)))
    scene.render.resolution_x = scene.render.resolution_y = px
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = True
    scene.cycles.samples = 48
    out = os.path.join(ROOT, "assets", "models", "shadows", key + ".webp")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    scene.render.image_settings.file_format = "WEBP"
    scene.render.image_settings.color_mode = "RGBA"
    tmp_sh = os.path.join(bpy.app.tempdir or "/tmp", "cs_shadow.png")
    tmp_cov = os.path.join(bpy.app.tempdir or "/tmp", "cs_cover.png")
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = tmp_sh
    bpy.ops.render.render(write_still=True)
    # second pass: the model's own top-down coverage. The decal lies under the model, so
    # wherever the model itself covers the ground (plazas, arena sand, precinct slabs) the
    # decal must be clear, or it shows through those low floors as a black stain.
    catcher.hide_render = True
    for o in hidden:
        o.visible_camera = True
    scene.cycles.samples = 1
    scene.render.filepath = tmp_cov
    bpy.ops.render.render(write_still=True)
    scene.cycles.samples = 48
    a = bpy.data.images.load(tmp_sh, check_existing=False)
    b = bpy.data.images.load(tmp_cov, check_existing=False)
    pa = np.array(a.pixels[:], dtype=np.float32).reshape(-1, 4)
    pb = np.array(b.pixels[:], dtype=np.float32).reshape(-1, 4)
    pa[:, 3] *= np.clip(1.0 - pb[:, 3] * 1.15, 0.0, 1.0)
    a.pixels[:] = pa.ravel().tolist()
    a.update()
    scene.render.image_settings.file_format = "WEBP"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.quality = 80
    a.save_render(out, scene=scene)
    bpy.data.images.remove(a)
    bpy.data.images.remove(b)
    bpy.data.objects.remove(cam, do_unlink=True)
    bpy.data.cameras.remove(cam_data)
    bpy.data.objects.remove(catcher, do_unlink=True)
    meta_path = os.path.join(ROOT, "assets", "models", "shadows", "manifest.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    # map axes: x east, y south (Blender y is north)
    meta[key] = {"size": round(span, 2), "cx": round(cx, 2), "cy": round(-cy, 2)}
    json.dump(meta, open(meta_path, "w"), indent=1, sort_keys=True)
    return meta[key]


if __name__ == "__main__" and "-b" in sys.argv:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    B = builders()
    keys = [k for k in B if not argv or any(a in k for a in argv)]
    for k in keys:
        print(bake(k))


# ====================================================================== clean miniature bake
# Flat material colours with ambient occlusion baked into the vertices: no texture at
# all, so the model stays crisp at any zoom and the files stay small. The browser adds
# the fixed sun from face normals and inks the creases.

def _densify(o, max_edge):
    """Split long edges so the baked occlusion has vertices to live on (wall bases, under cornices)."""
    bm = bmesh.new()
    bm.from_mesh(o.data)
    long_edges = [e for e in bm.edges if e.calc_length() > max_edge]
    if long_edges:
        # one cut per max_edge of length, capped so huge floors don't explode
        by_cuts = {}
        for e in long_edges:
            n = min(12, int(e.calc_length() / max_edge))
            by_cuts.setdefault(n, []).append(e)
        for n, es in by_cuts.items():
            bmesh.ops.subdivide_edges(bm, edges=es, cuts=n, use_grid_fill=False)
        bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.to_mesh(o.data)
    bm.free()


def _split_seams(o):
    """Duplicate vertices along material borders, so per-vertex colours never bleed between materials."""
    bm = bmesh.new()
    bm.from_mesh(o.data)
    seams = [e for e in bm.edges if len(e.link_faces) == 2 and e.link_faces[0].material_index != e.link_faces[1].material_index]
    if seams:
        bmesh.ops.split_edges(bm, edges=seams)
    bm.to_mesh(o.data)
    bm.free()


def _ink(o, angle=32.0):
    """Edges-only copy of the model's creases and silhouettes, exported as glTF lines (the browser draws them as is)."""
    bm = bmesh.new()
    bm.from_mesh(o.data)
    lim = math.radians(angle)
    keep = []
    for e in bm.edges:
        lf = e.link_faces
        if len(lf) < 2 or (len(lf) == 2 and lf[0].normal.angle(lf[1].normal, 0.0) > lim):
            keep.append(e)
    verts, idx, edges = [], {}, []
    for e in keep:
        pair = []
        for v in e.verts:
            if v.index not in idx:
                idx[v.index] = len(verts)
                verts.append(tuple(v.co))
            pair.append(idx[v.index])
        edges.append(tuple(pair))
    bm.free()
    if not edges:
        return None
    me = bpy.data.meshes.new(o.name + "_ink")
    me.from_pydata(verts, edges, [])
    ink = bpy.data.objects.new(o.name + "_ink", me)
    ink.matrix_world = o.matrix_world.copy()
    bpy.context.scene.collection.objects.link(ink)
    return ink


def _base_colors(o):
    """Linear base colour per material slot."""
    out = []
    for slot in o.material_slots:
        m = slot.material
        c = (0.8, 0.8, 0.8)
        if m and m.use_nodes:
            b = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
            if b:
                c = tuple(b.inputs["Base Color"].default_value)[:3]
        elif m:
            c = tuple(m.diffuse_color)[:3]
        out.append(c)
    return out or [(0.8, 0.8, 0.8)]


def bake_vc(key, budget=None, samples=96, out_dir=None, shadow=None, ao_res=None):
    t0 = time.time()
    B = builders()
    chronokit.reset_scene()
    m = B[key]()
    if hasattr(m, "stages"):
        m.finish()
    objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    size = max(max(o.dimensions) for o in objs)
    budget = budget or (220000 if size > 150 else 120000 if size > 60 else 60000)
    set_cycles(samples)
    lighting()
    for o in objs:
        planar(o)
    tri0 = sum(tri_count(o) for o in objs)
    inks = []
    # occlusion resolution: about 1/45 of the model, never finer than 0.6 m
    # props are instanced many times: coarser occlusion keeps them light
    ao_res = ao_res or (10.0 if key.startswith("props/") else 45.0)
    max_edge = max(0.6 if not key.startswith("props/") else 0.3, size / ao_res)
    for o in objs:
        _densify(o, max_edge)
    tri1 = sum(tri_count(o) for o in objs)
    if tri1 > budget:
        # densifying is the optional part: undo it rather than collapse real geometry
        chronokit.reset_scene()
        m = B[key]()
        if hasattr(m, "stages"):
            m.finish()
        objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
        for o in objs:
            planar(o)
        scale_edge = max_edge * math.sqrt(tri1 / budget) * 1.4
        for o in objs:
            _densify(o, scale_edge)
        tri1 = sum(tri_count(o) for o in objs)

    for o in objs:
        _split_seams(o)
    # ---- ambient occlusion into a per-vertex colour attribute
    scene = bpy.context.scene
    scene.world.light_settings.distance = max(1.2, min(10.0, size * 0.05))
    for o in objs:
        me = o.data
        for a in list(me.color_attributes):
            me.color_attributes.remove(a)
        ca = me.color_attributes.new("AO", "BYTE_COLOR", "POINT")
        me.color_attributes.active_color = ca
        me.color_attributes.render_color_index = me.color_attributes.active_color_index
    select_only(objs)
    t_b = time.time()
    bpy.ops.object.bake(type="AO", target="VERTEX_COLORS", margin=0, use_clear=True)
    t_b = time.time() - t_b

    # ---- colour = material base colour x shaped occlusion
    flat = bpy.data.materials.get("vc_flat") or bpy.data.materials.new("vc_flat")
    flat.use_nodes = True
    bsdf = next(n for n in flat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    vcn = next((n for n in flat.node_tree.nodes if n.type == "VERTEX_COLOR"), None) or flat.node_tree.nodes.new("ShaderNodeVertexColor")
    vcn.layer_name = "Col"
    flat.node_tree.links.new(vcn.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 1.0
    for o in objs:
        me = o.data
        cols = np.array(_base_colors(o), dtype=np.float32)
        ao_attr = me.color_attributes["AO"]
        nv = len(me.vertices)
        ao = np.empty(nv * 4, dtype=np.float32)
        ao_attr.data.foreach_get("color", ao)
        a = np.clip(ao.reshape(-1, 4)[:, 0], 0, 1)
        # per-vertex material and "faces up" flag, from the faces using each vertex (seams are split)
        vmat = np.zeros(nv, dtype=np.int32)
        vup = np.zeros(nv, dtype=bool)
        for poly in me.polygons:
            up = poly.normal.z > 0.7
            for vi in poly.vertices:
                vmat[vi] = poly.material_index
                if up:
                    vup[vi] = True
        base = cols[np.clip(vmat, 0, len(cols) - 1)]
        # floors and terraces: softer occlusion, so sparse vertices never show as blotches
        k = np.where(vup, 0.7 + 0.3 * np.sqrt(a), 0.38 + 0.62 * np.power(a, 0.8))
        rgb = base * k[:, None]
        out = me.color_attributes.new("Col", "BYTE_COLOR", "POINT")
        out.data.foreach_set("color", np.concatenate([rgb, np.ones((nv, 1), np.float32)], 1).ravel())
        me.color_attributes.remove(me.color_attributes["AO"])
        me.color_attributes.active_color = me.color_attributes["Col"]
        me.materials.clear()
        me.materials.append(flat)

    # ---- cast shadow decal on the paper (masked to the model's own footprint)
    t_sh = time.time()
    if shadow is None:
        shadow = not key.startswith("props/")
    sh = render_shadow(key, objs, size) if shadow else None
    t_sh = time.time() - t_sh

    out_dir = out_dir or os.path.join(ROOT, "assets", "models")
    path = os.path.join(out_dir, key + ".glb")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    select_only(objs + inks)
    for e in bpy.context.scene.objects:
        if e.type == "EMPTY":
            e.select_set(True)
    kw = dict(filepath=path, export_format="GLB", use_selection=True, export_apply=True)
    props = bpy.ops.export_scene.gltf.get_rna_type().properties.keys()
    for k_, v in dict(export_yup=True, export_animations=False, export_texcoords=False, export_normals=False, export_cameras=False, export_lights=False,
                      export_extras=False, export_vertex_color="MATERIAL", export_materials="EXPORT",
                      export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=7,
                      export_draco_position_quantization=14, export_draco_color_quantization=8).items():
        if k_ in props:
            kw[k_] = v
    bpy.ops.export_scene.gltf(**kw)
    return {"key": key, "tris": tri1, "from_tris": tri0, "kb": os.path.getsize(path) // 1024, "s": round(time.time() - t0, 1), "bake_s": round(t_b, 1), "shadow_s": round(t_sh, 1), "edge": round(max_edge, 2), "ink": sum(len(i.data.edges) for i in inks)}
