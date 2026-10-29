"""
Bake the study: the writing table the map lies on and the things on it (tools/blender/models/study/study_*.py,
BUILDERS keyed "study/<name>"). Each model is built, its ambient occlusion baked into the vertex colours (material
colour x occlusion, the table top under it shading the contact), and exported as a small Draco GLB with normals to
assets/models/study/<name>.glb. Parts named tex_* keep their UVs (the app paints them with its canvas textures).

Headless:  BAKE_CPU=1 Blender -b -P tools/blender/bake_study.py -- [filter]
Incremental like bake_all.py: a model is baked again only when its builder file, studykit.py, chronokit.py or this
script changes (digests in assets/models/bake-manifest.json under "study/<name>"). FORCE=1 bakes them all.
"""
import glob
import hashlib
import importlib.util
import json
import math
import os
import sys
import time

import bpy
import bmesh
import numpy as np

ROOT = "/Users/ijlalahmad/Desktop/test/Chronoscape"
TB = os.path.join(ROOT, "tools", "blender")
STUDY = os.path.join(TB, "models", "study")
for p in (TB, os.path.join(TB, "models"), STUDY):
    if p not in sys.path:
        sys.path.insert(0, p)

import chronokit  # noqa: E402

_ns = {"__name__": "bake_assets"}
exec(open(os.path.join(TB, "bake_assets.py")).read(), _ns)
set_cycles, split_seams, base_colors, select_only = _ns["set_cycles"], _ns["_split_seams"], _ns["_base_colors"], _ns["select_only"]

MANIFEST = os.path.join(ROOT, "assets", "models", "bake-manifest.json")
OUT = os.path.join(ROOT, "assets", "models", "study")


def study_builders():
    out, src = {}, {}
    for f in sorted(glob.glob(os.path.join(STUDY, "study_*.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        for k, fn in mod.BUILDERS.items():
            out[k] = fn
            src[k] = f
    return out, src


def digest(files):
    h = hashlib.sha1()
    for f in files:
        h.update(f.encode() + hashlib.sha1(open(f, "rb").read()).hexdigest().encode())
    return h.hexdigest()


def densify(o, max_edge, cap=6):
    """Split long edges so the occlusion has vertices to live on (a book's cover, the apron under the top)."""
    bm = bmesh.new()
    bm.from_mesh(o.data)
    by = {}
    for e in bm.edges:
        n = min(cap, int(e.calc_length() / max_edge))
        if n:
            by.setdefault(n, []).append(e)
    for n, es in by.items():
        bmesh.ops.subdivide_edges(bm, edges=es, cuts=n, use_grid_fill=False)
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 3])
    bm.to_mesh(o.data)
    bm.free()


def tris(o):
    return sum(len(p.vertices) - 2 for p in o.data.polygons)


def bake_one(key, fn, samples=64):
    t0 = time.time()
    chronokit.reset_scene()
    for block in (bpy.data.meshes, bpy.data.materials):
        for b in list(block):
            if b.users == 0:
                block.remove(b)
    prop = fn()
    objs = prop.objects
    meshes = [o for o in objs if o.type == "MESH"]
    # glass is drawn see-through in the app: it neither takes nor casts occlusion
    clear = [o for o in meshes if o.name.startswith("glass")]
    for o in clear:
        o.hide_render = True
    baked = [o for o in meshes if o not in clear]
    if prop.ground:
        # a table top under the model while baking, so its foot darkens where it stands
        bpy.ops.mesh.primitive_plane_add(size=3.0, location=(0, 0, -0.0002))
        g = bpy.context.active_object
        g.name = "bake_ground"
    set_cycles(samples)
    scene = bpy.context.scene
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    bg = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs[0].default_value = (1, 1, 1, 1)
    world.light_settings.distance = prop.ao
    for o in baked:
        if not o.name.startswith("tex_"):
            densify(o, prop.edge)
        split_seams(o)
        me = o.data
        for a in list(me.color_attributes):
            me.color_attributes.remove(a)
        ca = me.color_attributes.new("AO", "BYTE_COLOR", "POINT")
        me.color_attributes.active_color = ca
        me.color_attributes.render_color_index = me.color_attributes.active_color_index
    select_only(baked)
    bpy.ops.object.bake(type="AO", target="VERTEX_COLORS", margin=0, use_clear=True)

    flat = bpy.data.materials.get("study_vc") or bpy.data.materials.new("study_vc")
    flat.use_nodes = True
    bsdf = next(n for n in flat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    vcn = next((n for n in flat.node_tree.nodes if n.type == "VERTEX_COLOR"), None) or flat.node_tree.nodes.new("ShaderNodeVertexColor")
    vcn.layer_name = "Col"
    flat.node_tree.links.new(vcn.outputs["Color"], bsdf.inputs["Base Color"])
    for o in baked:
        me = o.data
        cols = np.array(base_colors(o), dtype=np.float32)
        nv = len(me.vertices)
        ao = np.empty(nv * 4, dtype=np.float32)
        me.color_attributes["AO"].data.foreach_get("color", ao)
        a = np.clip(ao.reshape(-1, 4)[:, 0], 0, 1)
        vmat = np.zeros(nv, dtype=np.int32)
        for poly in me.polygons:
            for vi in poly.vertices:
                vmat[vi] = poly.material_index
        base = cols[np.clip(vmat, 0, len(cols) - 1)]
        # occlusion kept gentle: the app's lamp pool and fixed light do the rest
        k = 0.42 + 0.58 * np.power(a, 0.85)
        rgb = base * k[:, None]
        out = me.color_attributes.new("Col", "BYTE_COLOR", "POINT")
        out.data.foreach_set("color", np.concatenate([rgb, np.ones((nv, 1), np.float32)], 1).ravel())
        me.color_attributes.remove(me.color_attributes["AO"])
        me.color_attributes.active_color = me.color_attributes["Col"]
        me.materials.clear()
        me.materials.append(flat)

    for o in clear:
        o.hide_render = False
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, key.split("/", 1)[1] + ".glb")
    select_only(meshes)
    kw = dict(filepath=path, export_format="GLB", use_selection=True, export_apply=True)
    props = bpy.ops.export_scene.gltf.get_rna_type().properties.keys()
    for k_, v in dict(export_yup=True, export_animations=False, export_texcoords=True, export_normals=True, export_cameras=False, export_lights=False,
                      export_extras=False, export_vertex_color="MATERIAL", export_materials="EXPORT", export_tangents=False,
                      export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=7,
                      export_draco_position_quantization=14, export_draco_normal_quantization=10,
                      export_draco_texcoord_quantization=12, export_draco_color_quantization=8).items():
        if k_ in props:
            kw[k_] = v
    bpy.ops.export_scene.gltf(**kw)
    return {"key": key, "tris": sum(tris(o) for o in meshes), "parts": {o.name: tris(o) for o in meshes}, "kb": round(os.path.getsize(path) / 1024, 1), "s": round(time.time() - t0, 1)}


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    flt = argv[0] if argv else None
    B, src = study_builders()
    # the study's builders share helpers (the ancient things roll their papyrus with the desk's rolled maps):
    # any change to one of them re-bakes them all, which takes seconds
    shared = sorted(glob.glob(os.path.join(STUDY, "*.py"))) + [os.path.join(TB, "chronokit.py"), os.path.join(TB, "bake_study.py")]
    manifest = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
    todo = []
    for k in sorted(B):
        if flt and flt not in k:
            continue
        d = digest(sorted(set([src[k]] + shared)))
        glb = os.path.join(OUT, k.split("/", 1)[1] + ".glb")
        if not os.environ.get("FORCE") and not flt and manifest.get(k) == d and os.path.exists(glb):
            continue
        todo.append((k, d))
    print(f"study: {len(todo)} to bake", flush=True)
    for k, d in todo:
        r = bake_one(k, B[k])
        print("study:", json.dumps(r), flush=True)
        manifest = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
        manifest[k] = d
        with open(MANIFEST, "w") as fh:
            json.dump(manifest, fh, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
