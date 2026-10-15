import * as THREE from "three";
import { registerForWarmup } from "./warmup";

/**
 * The whole scene renders unlit: lighting is either baked into textures in
 * Blender, or (for procedural pieces) a fixed north-west light evaluated in a
 * tiny shader. No light uniforms, no shadow maps, a handful of small shader
 * programs shared by everything. The day clock is a single tint uniform.
 */
export const dayTint = { value: new THREE.Color(1, 1, 1) };

type Opts = {
  color?: THREE.ColorRepresentation;
  map?: THREE.Texture | null;
  /** Evaluate the fixed light from the normal (procedural geometry). Off for baked textures. */
  shade?: boolean;
  transparent?: boolean;
  opacity?: number;
  depthWrite?: boolean;
  side?: THREE.Side;
  polygonOffset?: number;
  vertexColors?: boolean;
  /** Face normals from screen-space derivatives: for meshes exported without normals (flat miniatures). */
  flat?: boolean;
  /** Extra GLSL run at the end of the fragment shader (has vBN, vWP, vUv when USE_UV). */
  extraFrag?: string;
  extraUniforms?: Record<string, { value: unknown }>;
  key?: string;
};

export function bakedMaterial(o: Opts = {}): THREE.MeshBasicMaterial {
  const m = new THREE.MeshBasicMaterial({
    color: o.color ?? 0xffffff,
    map: o.map ?? null,
    transparent: !!o.transparent,
    opacity: o.opacity ?? 1,
    depthWrite: o.depthWrite ?? true,
    side: o.side ?? THREE.FrontSide,
    vertexColors: !!o.vertexColors,
    toneMapped: false,
  });
  if (o.polygonOffset) {
    m.polygonOffset = true;
    m.polygonOffsetFactor = o.polygonOffset;
    m.polygonOffsetUnits = o.polygonOffset;
  }
  const shade = o.shade !== false && !o.map;
  const extra = o.extraFrag ?? "";
  if (extra.includes("vUv")) m.defines = { ...(m.defines ?? {}), USE_UV: "" };
  m.onBeforeCompile = (shader) => {
    shader.uniforms.uDayTint = dayTint;
    Object.assign(shader.uniforms, o.extraUniforms ?? {});
    shader.vertexShader = shader.vertexShader
      .replace("#include <common>", "#include <common>\nvarying vec3 vBN;\nvarying vec3 vWP;")
      .replace(
        "#include <project_vertex>",
        `#include <project_vertex>
        vec3 bn = normal;
        vec4 wp = vec4(transformed, 1.0);
        #ifdef USE_INSTANCING
          bn = mat3(instanceMatrix) * bn;
          wp = instanceMatrix * wp;
        #endif
        vBN = normalize(mat3(modelMatrix) * bn);
        vWP = (modelMatrix * wp).xyz;`,
      );
    const uniformDecl = Object.keys(o.extraUniforms ?? {})
      .map((k) => `uniform ${glslType(o.extraUniforms![k].value)} ${k};`)
      .join("\n");
    shader.fragmentShader = shader.fragmentShader
      .replace("#include <common>", `#include <common>\nvarying vec3 vBN;\nvarying vec3 vWP;\nuniform vec3 uDayTint;\n${uniformDecl}`)
      .replace(
        "#include <opaque_fragment>",
        `${shade ? `vec3 sN = ${o.flat ? "normalize(cross(dFdx(vWP), dFdy(vWP)))" : "normalize(vBN)"};\n float bake = 0.6 + 0.4 * max(dot(sN, normalize(vec3(-0.45, 0.8, -0.4))), 0.0) + 0.06 * sN.y;\n outgoingLight *= bake;` : ""}
        outgoingLight *= uDayTint;
        #include <opaque_fragment>
        ${extra}`,
      );
  };
  // programs are shared by every material with the same recipe
  const recipe = `baked:${shade ? "s" : "t"}${o.flat ? "f" : ""}${o.vertexColors ? "v" : ""}:${o.key ?? ""}:${hashStr(extra)}`;
  m.customProgramCacheKey = () => recipe;
  return m;
}

function glslType(v: unknown) {
  if (typeof v === "number") return "float";
  if (v instanceof THREE.Color || v instanceof THREE.Vector3) return "vec3";
  if (v instanceof THREE.Vector2) return "vec2";
  return "float";
}

function hashStr(s: string) {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
  return h.toString(36);
}

const shadedCache = new Map<string, THREE.MeshBasicMaterial>();
/** A shared shaded material for a flat colour (props, plants, figures). */
export function shaded(color: THREE.ColorRepresentation): THREE.MeshBasicMaterial {
  const key = new THREE.Color(color).getHexString();
  let m = shadedCache.get(key);
  if (!m) {
    m = bakedMaterial({ color });
    shadedCache.set(key, m);
  }
  return m;
}

/**
 * Clean-miniature models: colour and occlusion live in the vertices, the fixed sun
 * comes from the face normal. Pushed back a hair so ink lines drawn on the creases win.
 */
const miniCache = new Map<boolean, THREE.MeshBasicMaterial>();
export function miniatureMaterial(flat = true) {
  let m = miniCache.get(flat);
  if (!m) {
    m = bakedMaterial({ vertexColors: true, flat, polygonOffset: 1, key: "mini" });
    miniCache.set(flat, m);
  }
  return m;
}

/**
 * Convert everything under `root` (a loaded glTF) to the unlit pipeline:
 * textured materials keep their baked texture, plain ones get the fixed light.
 */
export function bakeify(root: THREE.Object3D) {
  const done = new Map<THREE.Material, THREE.Material>();
  root.traverse((o) => {
    const mesh = o as THREE.Mesh;
    if (!mesh.isMesh) return;
    mesh.castShadow = false;
    mesh.receiveShadow = false;
    const conv = (mat: THREE.Material) => {
      let out = done.get(mat);
      if (!out) {
        const std = mat as THREE.MeshStandardMaterial;
        out = std.map
          ? bakedMaterial({ map: std.map, transparent: std.transparent, key: "tex" })
          : mesh.geometry.getAttribute("color")
            ? miniatureMaterial(!mesh.geometry.getAttribute("normal"))
            : mesh.geometry.getAttribute("normal")
              ? shaded(std.color ?? 0xcccccc)
              : bakedMaterial({ color: std.color ?? 0xcccccc, flat: true, key: "flat" });
        done.set(mat, out);
      }
      return out;
    };
    mesh.material = Array.isArray(mesh.material) ? mesh.material.map(conv) : conv(mesh.material);
  });
  return root;
}

/** Day clock to tint: warm low sun at dawn and dusk, blue-grey at night. */
export function tintForHour(hour: number, out: THREE.Color) {
  const day = new THREE.Color(1, 0.985, 0.95);
  const golden = new THREE.Color(1.0, 0.86, 0.7);
  const night = new THREE.Color(0.42, 0.47, 0.64);
  const h = ((hour % 24) + 24) % 24;
  if (h >= 8 && h <= 17) return out.copy(day);
  if (h >= 6 && h < 8) return out.copy(golden).lerp(day, (h - 6) / 2);
  if (h > 17 && h <= 19.5) return out.copy(day).lerp(golden, (h - 17) / 2.5);
  if (h > 19.5 && h <= 21) return out.copy(golden).lerp(night, (h - 19.5) / 1.5);
  if (h >= 4.5 && h < 6) return out.copy(night).lerp(golden, (h - 4.5) / 1.5);
  return out.copy(night);
}

// the shared shaded program is used by almost everything: warm it up front
registerForWarmup(shaded(0xcccccc), bakedMaterial({ color: 0xcccccc, vertexColors: true }), miniatureMaterial(true));
