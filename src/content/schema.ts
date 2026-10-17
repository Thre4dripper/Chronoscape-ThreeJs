import { z } from "zod";

/**
 * Chronoscape content schema.
 *
 * Every city is a content pack: one city.json that the renderer loads without
 * knowing which city it is. Positions are in *map units* (metres on an
 * illustrated local grid, origin top-left, y grows downward like an image).
 * `world.scale` converts map units to 3D world units.
 */

export const Vec2 = z.tuple([z.number(), z.number()]);
export type Vec2 = z.infer<typeof Vec2>;

const Hex = z.string().regex(/^#[0-9a-fA-F]{6}$/, "hex colour like #A65238");

export const Confidence = z.enum(["documented", "reconstruction", "interpretation"]);
export type Confidence = z.infer<typeof Confidence>;

export const SourceSchema = z.object({
  id: z.string().min(1),
  title: z.string().min(1),
  author: z.string().optional(),
  year: z.union([z.number(), z.string()]).optional(),
  url: z.url().optional(),
  note: z.string().optional(),
});
export type Source = z.infer<typeof SourceSchema>;

export const PeriodSchema = z.object({
  id: z.string().min(1),
  label: z.string().min(1),
  /** Representative year. Negative = BCE. */
  year: z.number().int(),
  startYear: z.number().int(),
  endYear: z.number().int(),
  summary: z.string().min(1),
  population: z.string().optional(),
  feel: z.string().optional(),
});
export type Period = z.infer<typeof PeriodSchema>;

/* ---------- Map (illustrated, drawn from vector data at load time) ---------- */

export const MapPaletteSchema = z.object({
  parchment: Hex.default("#E6D3AA"),
  ink: Hex.default("#6F4D34"),
  water: Hex.default("#65888A"),
  hill: Hex.default("#777D5A"),
  road: Hex.default("#8A6A4A"),
});

const Periods = z.array(z.string()).optional();
const Polygon = z.array(Vec2).min(3);

export const MapSchema = z.object({
  /** [width, height] in map units. */
  size: Vec2,
  /** Longest edge of the rendered map texture in pixels. */
  resolution: z.number().int().min(1024).max(8192).default(2048),
  palette: MapPaletteSchema.prefault({}),
  water: z
    .array(z.object({ id: z.string().optional(), name: z.string(), path: z.array(Vec2).min(2), width: z.number().positive(), blurb: z.string().optional(), periods: Periods }))
    .default([]),
  islands: z.array(z.object({ name: z.string(), polygon: Polygon, periods: Periods })).default([]),
  hills: z
    .array(z.object({ id: z.string().optional(), name: z.string(), center: Vec2, radius: z.number().positive(), label: z.boolean().default(true), blurb: z.string().optional(), periods: Periods }))
    .default([]),
  roads: z
    .array(
      z.object({
        id: z.string().optional(),
        name: z.string(),
        path: z.array(Vec2).min(2),
        width: z.number().positive().default(8),
        style: z.enum(["major", "minor"]).default("major"),
        blurb: z.string().optional(),
        /** Draw the name along the path. */
        labelled: z.boolean().default(false),
        periods: Periods,
      }),
    )
    .default([]),
  walls: z.array(z.object({ id: z.string().optional(), name: z.string(), path: z.array(Vec2).min(2), closed: z.boolean().default(false), blurb: z.string().optional(), periods: Periods })).default([]),
  gates: z.array(z.object({ id: z.string().optional(), name: z.string(), position: Vec2, periods: Periods })).default([]),
  bridges: z
    .array(
      z.object({
        id: z.string().optional(),
        name: z.string(),
        path: z.array(Vec2).min(2),
        blurb: z.string().optional(),
        /** Built of stone arches or timber trestles on piles. */
        build: z.enum(["stone", "timber"]).default("stone"),
        /** Number of spans across the river. */
        arches: z.number().int().min(1).max(12).default(4),
        /** A landmark that models this bridge in detail: hovering the bridge raises it. */
        landmarkId: z.string().optional(),
        periods: Periods,
      }),
    )
    .default([]),
  aqueducts: z.array(z.object({ name: z.string(), path: z.array(Vec2).min(2), periods: Periods })).default([]),
  /** Built-up areas, drawn as hatched blocks of houses. */
  blocks: z.array(z.object({ name: z.string().optional(), polygon: Polygon, density: z.enum(["dense", "loose"]).default("dense"), periods: Periods })).default([]),
  gardens: z.array(z.object({ name: z.string().optional(), polygon: Polygon, kind: z.enum(["park", "vineyard", "orchard"]).default("park"), periods: Periods })).default([]),
  marsh: z.array(z.object({ name: z.string().optional(), polygon: Polygon, periods: Periods })).default([]),
  districts: z.array(z.object({ id: z.string(), name: z.string(), polygon: Polygon, description: z.string().optional(), periods: Periods })).default([]),
  labels: z
    .array(
      z.object({
        text: z.string(),
        position: Vec2,
        size: z.enum(["sm", "md", "lg"]).default("md"),
        rotation: z.number().default(0),
        periods: Periods,
      }),
    )
    .default([]),
  compass: Vec2.optional(),
  /** Title cartouche position (bottom-left corner of the box) in map units. */
  cartouche: Vec2.optional(),
});
export type CityMap = z.infer<typeof MapSchema>;

/* ---------- Models: a glTF asset or a procedural kit ---------- */

const Kit = {
  temple: z.object({
    kit: z.literal("temple"),
    width: z.number().positive(),
    depth: z.number().positive(),
    columnsFront: z.number().int().min(2).default(6),
    columnsSide: z.number().int().min(0).default(0),
    podium: z.number().positive().default(4),
    columnHeight: z.number().positive().default(12),
    color: Hex.default("#D9CBB0"),
    roofColor: Hex.default("#A65238"),
  }),
  amphitheater: z.object({
    kit: z.literal("amphitheater"),
    radiusX: z.number().positive(),
    radiusY: z.number().positive(),
    tiers: z.number().int().min(1).max(6).default(3),
    tierHeight: z.number().positive().default(12),
    arc: z.number().min(90).max(360).default(360),
    color: Hex.default("#D9C7A5"),
  }),
  circus: z.object({
    kit: z.literal("circus"),
    length: z.number().positive(),
    width: z.number().positive(),
    obelisks: z.number().int().min(0).max(3).default(1),
    color: Hex.default("#D9C7A5"),
    trackColor: Hex.default("#C8A574"),
  }),
  hall: z.object({
    kit: z.literal("hall"),
    width: z.number().positive(),
    depth: z.number().positive(),
    height: z.number().positive(),
    roof: z.enum(["pitched", "flat", "dome"]).default("pitched"),
    porticoColumns: z.number().int().min(0).default(0),
    color: Hex.default("#C9A98A"),
    roofColor: Hex.default("#A65238"),
  }),
  cluster: z.object({
    kit: z.literal("cluster"),
    buildings: z
      .array(
        z.object({
          offset: Vec2,
          width: z.number().positive(),
          depth: z.number().positive(),
          height: z.number().positive(),
          roof: z.enum(["pitched", "flat", "dome"]).default("pitched"),
          color: Hex.optional(),
        }),
      )
      .min(1),
    plaza: z.object({ width: z.number().positive(), depth: z.number().positive(), color: Hex.default("#D6C39E") }).optional(),
    color: Hex.default("#C9A98A"),
    roofColor: Hex.default("#A65238"),
  }),
  arch: z.object({
    kit: z.literal("arch"),
    width: z.number().positive(),
    height: z.number().positive(),
    depth: z.number().positive(),
    bays: z.number().int().min(1).max(3).default(1),
    color: Hex.default("#E2D7C3"),
  }),
  fort: z.object({
    kit: z.literal("fort"),
    width: z.number().positive(),
    depth: z.number().positive(),
    wallHeight: z.number().positive().default(18),
    bastions: z.number().int().min(4).default(8),
    color: Hex.default("#A24A3C"),
  }),
  mosque: z.object({
    kit: z.literal("mosque"),
    width: z.number().positive(),
    depth: z.number().positive(),
    domes: z.number().int().min(1).max(5).default(3),
    minaretHeight: z.number().positive().default(40),
    color: Hex.default("#A24A3C"),
    domeColor: Hex.default("#F1EBE0"),
  }),
  street: z.object({
    kit: z.literal("street"),
    length: z.number().positive(),
    width: z.number().positive(),
    shops: z.number().int().min(2).default(20),
    canal: z.boolean().default(false),
    color: Hex.default("#C9A98A"),
    roofColor: Hex.default("#8E5A3C"),
  }),
};

export const KitSchema = z.discriminatedUnion("kit", [
  Kit.temple,
  Kit.amphitheater,
  Kit.circus,
  Kit.hall,
  Kit.cluster,
  Kit.arch,
  Kit.fort,
  Kit.mosque,
  Kit.street,
]);
export type KitParams = z.infer<typeof KitSchema>;

export const GlbModelSchema = z.object({
  /** Public URL path under assets/, e.g. "models/rome/temple-of-saturn.glb". Model units are metres, origin at ground centre. */
  glb: z.string().regex(/^models\/.+\.glb$/, "glb path like models/<city>/<name>.glb"),
  /** Optional procedural stand-in while the asset streams in or if it fails. */
  fallback: KitSchema.optional(),
});

export const ModelSchema = z.union([GlbModelSchema, KitSchema]);
export type ModelRef = z.infer<typeof ModelSchema>;

/* ---------- Landmarks ---------- */

export const CameraPoseOverride = z.object({
  distance: z.number().positive().optional(),
  tilt: z.number().min(10).max(89).optional(),
  heading: z.number().optional(),
});

export const LandmarkVariantSchema = z.object({
  name: z.string().optional(),
  model: ModelSchema.optional(),
  /** Explains what is different in this period. Surfaced when the period changes. */
  note: z.string().optional(),
  confidence: Confidence.optional(),
});

export const LandmarkSchema = z.object({
  id: z.string().min(1),
  /** Stable geographical identity. A place outlives its buildings. */
  placeId: z.string().min(1),
  name: z.string().min(1),
  category: z.enum(["temple", "civic", "entertainment", "religious", "military", "commercial", "district", "monument"]),
  position: Vec2,
  /** Degrees, clockwise when viewed from above. */
  rotation: z.number().default(0),
  /** Footprint [width, depth] in map units, used for hit-testing and the map's ink outline. */
  footprint: Vec2,
  /** Visual exaggeration for miniature readability. 1 = true scale. */
  scale: z.number().positive().default(1),
  model: ModelSchema,
  reveal: z.enum(["rise", "assemble"]).default("assemble"),
  activePeriods: z.array(z.string()).min(1),
  variants: z.record(z.string(), LandmarkVariantSchema).default({}),
  summary: z.string().min(1),
  details: z.array(z.string()).default([]),
  built: z.string().optional(),
  function: z.string().optional(),
  confidence: Confidence,
  sourceIds: z.array(z.string()).min(1),
  focus: CameraPoseOverride.optional(),
  activity: z.object({ figures: z.number().int().min(0).max(200).default(30), radius: z.number().positive().default(60) }).optional(),
});
export type Landmark = z.infer<typeof LandmarkSchema>;

/* ---------- Spots: the small things (shops, workshops, markets, fountains...) ---------- */

export const SpotKind = z.enum([
  "tavern", "bakery", "market", "shop", "workshop", "house", "inn", "school", "bath", "shrine", "fountain", "works", "dock", "prison", "civic", "monument", "garden", "bank", "church",
]);
export type SpotKind = z.infer<typeof SpotKind>;

export const SpotSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  kind: SpotKind,
  position: Vec2,
  activePeriods: z.array(z.string()).min(1),
  summary: z.string().min(1),
  details: z.array(z.string()).default([]),
  confidence: Confidence,
  sourceIds: z.array(z.string()).min(1),
  /** What is happening here at a given hour of an ordinary day. */
  vignettes: z.array(z.object({ hour: z.number().int().min(0).max(23), text: z.string().min(1) })).default([]),
  variants: z.record(z.string(), z.object({ name: z.string().optional(), note: z.string().optional() })).default({}),
});
export type Spot = z.infer<typeof SpotSchema>;

/* ---------- Events: things happening in a period, at a place ---------- */

export const EventKind = z.enum(["construction", "festival", "procession", "riot", "disaster", "civic", "ceremony", "daily"]);
export const EventEffect = z.enum(["fire", "crowd", "construction", "procession", "none"]);

export const EventSchema = z.object({
  id: z.string().min(1),
  title: z.string().min(1),
  periodId: z.string().min(1),
  date: z.string().min(1),
  kind: EventKind,
  at: z.union([z.object({ landmarkId: z.string() }), z.object({ spotId: z.string() }), z.object({ position: Vec2 })]),
  effect: EventEffect.default("none"),
  text: z.string().min(1),
  sourceIds: z.array(z.string()).min(1),
});
export type HistoricalEvent = z.infer<typeof EventSchema>;

/* ---------- Stories ---------- */

export const StorySchema = z.object({
  id: z.string().min(1),
  title: z.string().min(1),
  periodId: z.string().min(1),
  summary: z.string().min(1),
  steps: z
    .array(
      z
        .object({
          landmarkId: z.string().optional(),
          spotId: z.string().optional(),
          title: z.string(),
          text: z.string(),
          when: z.string().optional(),
          sourceIds: z.array(z.string()).default([]),
        })
        .refine((st) => !!st.landmarkId !== !!st.spotId, { message: "a step needs exactly one of landmarkId or spotId" }),
    )
    .min(2),
  sourceIds: z.array(z.string()).min(1),
});
export type Story = z.infer<typeof StorySchema>;

/* ---------- City ---------- */

export const CitySchema = z.object({
  id: z.string().regex(/^[a-z0-9-]+$/),
  name: z.string().min(1),
  subtitle: z.string().min(1),
  description: z.string().min(1),
  defaultPeriodId: z.string().min(1),
  map: MapSchema,
  world: z
    .object({
      /** World units per map unit. */
      scale: z.number().positive().default(0.02),
      /** Multiplies the era's default house heights (a city of towers, or of low courtyard houses). */
      heightScale: z.number().positive().optional(),
    })
    .prefault({}),
  camera: z
    .object({
      projection: z.enum(["perspective", "orthographic"]).default("perspective"),
      start: z.object({
        target: Vec2,
        distance: z.number().positive(),
        tilt: z.number().min(10).max(89).default(50),
        heading: z.number().default(0),
      }),
      minDistance: z.number().positive().default(4),
      maxDistance: z.number().positive().default(80),
    })
    .optional(),
  periods: z.array(PeriodSchema).min(1),
  landmarks: z.array(LandmarkSchema).min(1),
  spots: z.array(SpotSchema).default([]),
  events: z.array(EventSchema).default([]),
  stories: z.array(StorySchema).default([]),
  sources: z.array(SourceSchema).min(1),
});
export type City = z.infer<typeof CitySchema>;

export const CityIndexSchema = z.object({
  cities: z
    .array(
      z.object({
        id: z.string().regex(/^[a-z0-9-]+$/),
        name: z.string(),
        subtitle: z.string(),
        status: z.enum(["playable", "test", "draft"]).default("playable"),
      }),
    )
    .min(1),
});
export type CityIndex = z.infer<typeof CityIndexSchema>;

/* ---------------------------------------------------------------- the map room */

const LonLat = z.tuple([z.number().min(-180).max(180), z.number().min(-90).max(90)]);

/** One map inside an atlas: a playable city at a chosen era, or one still in preparation. */
export const AtlasMapSchema = z.object({
  /** A city pack id; without one the map is shown as "in preparation". */
  city: z.string().optional(),
  /** The era the map opens at. */
  period: z.string().optional(),
  title: z.string(),
  subtitle: z.string(),
  blurb: z.string(),
  /** Where it is on the globe, [lon, lat]. */
  at: LonLat,
  /** The little engraved drawing that marks it on the world map. */
  glyph: z.enum(["temple", "arena", "obelisk", "ziggurat", "lighthouse", "stupa", "dome", "pagoda", "cathedral", "tower", "mughal", "adobe", "enclosure", "steps"]).default("temple"),
});

/** An atlas on the map-room shelf: a region of the world in an age. */
export const AtlasSchema = z.object({
  id: z.string().regex(/^[a-z0-9-]+$/),
  title: z.string(),
  region: z.string(),
  era: z.string(),
  from: z.number().int(),
  to: z.number().int(),
  color: z.string().regex(/^#[0-9a-fA-F]{6}$/),
  blurb: z.string(),
  themes: z.array(z.string()).default([]),
  /** Rough outline of the region on the globe, [lon, lat] points. */
  area: z.array(LonLat).min(3),
  maps: z.array(AtlasMapSchema).min(1),
});

export const AtlasCatalogSchema = z.object({ atlases: z.array(AtlasSchema).min(1) });
export type AtlasMap = z.infer<typeof AtlasMapSchema>;
export type Atlas = z.infer<typeof AtlasSchema>;
export type AtlasCatalog = z.infer<typeof AtlasCatalogSchema>;
