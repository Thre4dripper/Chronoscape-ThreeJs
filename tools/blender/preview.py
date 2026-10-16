"""Render the current scene the way the app shows baked models: unlit, textured, orthographic three-quarter view."""
import math
import bpy
from mathutils import Vector


def shoot(path, el=28, az=-35, zoom=1.0, w=1000, h=650, textured=True):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.use_nodes = False
    try:
        sc.compositing_node_group = None
    except Exception:
        pass
    sh = sc.display.shading
    sh.light = "FLAT" if textured else "STUDIO"
    sh.color_type = "TEXTURE" if textured else "MATERIAL"
    sh.show_shadows = not textured
    sh.show_cavity = not textured
    meshes = [o for o in sc.objects if o.type == "MESH" and not o.hide_render]
    pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    center, ext = (lo + hi) / 2, max(hi - lo)
    cd = bpy.data.cameras.new("preview_cam")
    cd.type = "ORTHO"
    cd.ortho_scale = ext * 1.25 / zoom
    cd.clip_end = ext * 20
    cam = bpy.data.objects.new("preview_cam", cd)
    sc.collection.objects.link(cam)
    e, a = math.radians(el), math.radians(az)
    d = Vector((math.cos(e) * math.sin(a), -math.cos(e) * math.cos(a), math.sin(e)))
    cam.location = center + d * ext * 4
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = False
    sc.render.filepath = path
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)
    bpy.data.cameras.remove(cd)
