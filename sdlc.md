# Chronoscape: Product Direction & Technical Blueprint

Working title · Interactive historical atlas · Product-first architecture · Version 1.0 concept

We're building a reusable historical exploration platform where an illustrated map transforms into a living 3D reconstruction of the past.

The decisions are now settled: illustrated parchment, hover previews and click-to-explore interactions, exploration plus timelines and historical stories, a multi-city platform architecture, and ancient Rome as the first city.

The product priority is scalability. That means we need to design a system where adding Paris, Delhi, or Constantinople is primarily a content-production task, not an excuse to rewrite the rendering engine. Humanity has produced enough avoidable architectural disasters already.

## 1. Product vision

[DESCUBRE ROMA: El origen de la ciudad.](https://images.openai.com/static-rsc-4/RsMX_1eK0Ma0h4ph1xL--t9-_AbfSk6cEbeL9qhE478MLZdPnbt5zjS7fTi-9N83pW1fnlz7z71pUYh3dM3wmnvAq2vS-rhVjqfdYiRdbxWxpbMGAUBGlfdinlSbkR1s3D-HtNtD-MTn2904aMiW8EYPuoH8hEBFb2jBSiN4s8g?purpose=inline)

[Clay World Cities Gemini Image Prompt | PromptBase](https://images.openai.com/static-rsc-4/jzszAtu0NTW_pa8AkeyVsVyoh4gA5K7Kji7Py5albfvJGRbHzB6JFoqY-1pD96IXO2tBq7WDoaScQYNaSl2RkcExVizRAyuyZcB5fmj23vLEKSY49WO0VNOm1YLgTR_pD3XdZ0c8X--Cy1taqUdYRQ_5mN_avV_hAaNudN_2MeU?purpose=inline)

[Historical city travel guide: Rome, 1st century AD | British Museum](https://images.openai.com/static-rsc-4/hKcP8RgDtncbKwhPRaWHmcyBFZjMXDF3OPK-ZC3S5veGdbwmbllpvEarc-8POHvu1_p0bUFoG3wHckkr34qgAmPvglLXOricuFCS8w3MDAhVHSSWUmobBmcXISRSZhGoSbkKC83vnprgmn_u_4lNL7Olt8XTNF0oNykPwPEKAcI?purpose=inline)

12

Product promise: Explore a historical city as if it were a living illustration in an ancient atlas. Discover a location, watch its architecture rise from the map, and enter a scene that reveals how the place once looked and functioned.

The product combines three experiences into one interface:

- Explore: freely navigate the city's geography, districts, landmarks, and daily life.
- Travel through time: switch historical periods and see the city's landscape and architecture change.
- Experience history: follow events and stories connected to real locations, with animated reconstructions that make the context tangible.

### What we are building, and what we are not

| We are building                                               | We are not building                         |
| ------------------------------------------------------------- | ------------------------------------------- |
| An illustrated historical world with interactive 3D landmarks | A conventional pin-based map                |
| A reusable multi-city platform                                | A collection of unrelated city microsites   |
| Historically sourced reconstructions                          | A fantasy city presented as historical fact |
| Cinematic, user-controlled exploration                        | A forced sequence of slides and pop-ups     |
| A scalable content and asset pipeline                         | A hardcoded demo that cannot grow           |

The key differentiator is the transition between the illustrated map and the reconstructed world. The map is not just navigation. It is the interface through which history becomes visible.

## 2. The product experience

[File:Rome antique (larousse modf).jpg - Wikimedia Commons](https://images.openai.com/static-rsc-4/kulh-fkPZty07IycX-O0IFRABTyG8JQzerwvlKPEA5709u7q2-TrowSPs9X9k3slAPs0Z_PakwJ9k2k7Vl3592eO5L6c0fZFt9nk1tyBUNhnt_Tg5K5TSQ2K8c8v4xDAdYe6M9-u3ODNYuK3zdaXPFKa3p_h5owRICuWFG3noaE?purpose=inline)

## 1. Discover the city

Free exploration

Users land on a full-screen illustrated map. They pan, zoom, and glide over streets, monuments, river crossings, and districts. Labels appear contextually instead of covering the map with clutter.

[Bionic Ux - Design process never ends - Hyper-realistic Isometric Diorama](https://images.openai.com/static-rsc-4/lKRBPAP923Yw7O9VZU19BWowBt1Zt5m-Tvt0l-xo7lDUb3WNEB7xt6XGjnYCmdJfA-e3tmJcuKbqFlZqjypCiONcePOx3Ua2up-jLkx_RpQFrS6IN_mc97XFY8DdJjko80yuQe6zBe9QRJWHs_r0eRARzTdCijmR9bqwRwIp3WI?purpose=inline)

## 2. Reveal the landmark

Hover preview

Hovering highlights the location and lifts a selected structure out of the paper. A short animation introduces its architecture and a compact label identifies it.

[Miniature Ancient Roman Marketplace Digital by Bee Yen Lee | Saatchi Art Canada](https://images.openai.com/static-rsc-4/556GsLSGZ0u7kWP-ruT5QJl6rFtc_A-KZJEujNOflSXiLo85Rr4GVg-wM3DJ9wKay_mtCO-HeDw5fv95oS-__7hqEHMQYVsBnzpPBfW4T2o7sNGS8JJ0OzOtZgvffKNiH1wrZwOPCeQUURpYfm23HMC4H8FZ6WKMK2avyB25AYw?purpose=inline)

## 3. Enter the scene

Click to explore

Clicking a landmark moves the camera closer, expands the reconstruction, introduces animated activity, and opens a historical information panel with sources and a timeline.

[Take a romp through Ancient Rome’s great buildings with this handy (almost) pocket-sized book - The Art Newspaper - International art news and events](https://images.openai.com/static-rsc-4/WWliDDV5AjgJc7wWrLTfigYtUvXxPwAoOZrkdtqYVwUaVWQOA7xJLqbib3yfcPkZ0equyKP09RohgS0h37hU34KXCcVutOFPDxpCfI-Gb0SUtvtbD_zmgfbyQ9QCoSM17eFX4ChOZP82tFUhyxOVl6binXgS69AufU9itokEg6Y?purpose=inline)

## 4. Change the past

Time travel

A timeline lets users switch between supported dates. Buildings, roads, boundaries, and activities update according to the selected period, with changes explained rather than silently substituted.

[Before the 2nd century BC, the politics of ancient Rome developed rapidly. What were the principles of establishing and selecting officials? - iNEWS](https://images.openai.com/static-rsc-4/q0iTLBUt3dTOnB5ta6kOFxkpkPJW6i8Etir6d5_tXQxqabEFtc0NVS8Nky75WPpdh8JQzDkYjbHqlQS3iWL_PTiBdkr4RilFdGLgXiHVr7O7ehcuXydD5arJtUS-351034iOTxI84-jmccz9C-bP4Ha5RbKyf1-v7tHQrjzuBSc?purpose=inline)

## 5. Follow a story

Event-driven exploration

A story can guide users through multiple places, such as a triumphal procession or the transformation of the Forum. The map remains navigable, and every stop has a historical source trail.

The five experiences share one world, one camera system, one interaction model, and one historical data model.

## 3. Product interface and interaction specification

The experience should be full-screen by default. The map gets most of the screen; the interface appears only when it helps the user.

## CHRONOSCAPE

ROMA · ANCIENT WORLD

[Ancient Rome Map | Ninska Designs](https://images.openai.com/static-rsc-4/bv-eWrYI1bODQt_pCnvjRwmdt52-dvokHRmWDmVnr-WP-9p-_xetjv62kqdfyEOSKx0-Qg7C1W1wgqmCmxgA7_gWhPxvWDvS0qk7gJykZ6u9yz_Y_V74yvvGAkc9EH52Q6uSO6LyhUHA3yjjUM1mroiS0vskOBNkUUas_Zjetv8?purpose=inline)

[ninskadesigns.com](https://www.ninskadesigns.com/products/ancient-rome-map-antique-reproduction-roman-history-classics-italy-available-framed-326948453?utm_source=chatgpt.com)

ROMAN FORUM

76 CE · EXPLORING

DRAG TO EXPLORE

Interface direction mockup. The map image is illustrative, not a geographically verified reconstruction.

### The interaction state machine

We should explicitly model interactions rather than scatter hover flags and camera animations throughout the component tree.

Exploring

Flat illustrated map, free camera movement

Previewing

Hover highlight, landmark emergence, short animation

Focused

Camera transition, detailed model, contextual information

Immersed

Scene animations, historical events, period selection

Conceptual progression. Closing or pressing Escape returns to the previous exploration context.

These states need a few rules to prevent the interface from turning into an animation traffic jam.

| Trigger                    | Expected behavior                                                    |
| -------------------------- | -------------------------------------------------------------------- |
| Pointer enters landmark    | Highlight immediately; begin a short, interruptible reveal           |
| Pointer leaves landmark    | Fade the preview after a brief delay, unless focus is active         |
| Click landmark             | Cancel competing previews and smoothly enter focused mode            |
| Select a historical period | Update all period-dependent content as one coordinated transition    |
| Start a story              | Guide the camera to its first location and show story progress       |
| Press Escape               | Exit the topmost interaction layer and restore the previous view     |
| Switch cities              | Reset city-specific camera and selection state; load the new content |
| Touch a landmark           | Tap to preview; explicit second tap or action to enter               |

Important engineering rule: animations must be interruptible. If someone moves the camera while a landmark is emerging, the renderer should adapt instead of forcing them to watch an animation they no longer care about.

### Camera behavior

- Start with an orthographic camera or a perspective camera with a long focal length.
- Use an adjustable tilt, approximately 35 to 50 degrees for the default aerial view.
- Use damped pan and zoom, with boundaries defined per city.
- Animate camera transitions with easing and explicit cancellation.
- Preserve camera position when opening and closing a landmark.
- Keep hover effects subtle at city scale and richer at district scale.
- Support reduced-motion preferences and touch controls.

An orthographic camera will give us a stronger illustrated-atlas look. Perspective can be introduced for closer scenes if we want greater depth. We should test both before locking the rendering implementation.

## 4. Visual design system

The visual language needs to remain consistent across Rome, Paris, Delhi, and every future city, even though their architecture should look distinct.

[Natural background - old paper texture - plenty of space for your design](https://images.openai.com/static-rsc-4/WoVBfLBJzBtE_SnWnvcnPhLvaUJaraMuebZaFGRNfIpmcUxOAch11crL_ngLHNmg0_RsgBdlZ-QtPqZPAlaD-RziiwkqkE64beC547vN9-jC3jIAKhcRYyk8HTG0SjyUrhljzBQqCcoOikFPZ9y8Ngee--AHjBTC6yCUTr0286Fv2wGou2o-46y4MS78lIWw?purpose=inline)

The map surface

Fine paper grain, subtle edge wear, faded pigment, and carefully drawn contours. Texture should be restrained enough that streets and landmarks remain readable.

[Luigi Rossini  (Ravenna, 1790 - Roma, 1875) : Veduta generale del foro romano...  - Asta Stampe e Disegni XVI-XX secolo, Dipinti dell'800 e del '900. - Libreria Antiquaria Gonnelli - Casa d'Aste - Gonnelli Casa d'Aste](https://images.openai.com/static-rsc-4/PrHKFwnyn11yoZXxGXHXoa_gGARgDo3zKgbgnV2LjHWiI6QikCOLnNLzwdvqH8XK9uSXJqecnQLsGDLoUCHM9IBZhpc3tifwqoy6LEAXH3ZzBQiu1pB4phlTpW489m1WWJPqHgyJSu0hNY_HjRvVi5kntvpAJ6-E3o31z4E3eU4?purpose=inline)

Ink and cartography

Fine linework, hand-lettered-style labels, district boundaries, compass marks, and engraved symbols. Labels should be real UI text where practical, not baked into image textures.

[Ancient roman temple architecture building | Free Photo Illustration - rawpixel](https://images.openai.com/static-rsc-4/ywBdDTQc15misjUQih_MukFWPXyvaNJ32sEsFp9UcUZ_JLfMkFwIeD2lZ6WDCsdW_Uz0DP-WMC4T8VITXXNrUBGrWtQx2zihJOUw4awYYst3vlsfMWXVr5lDoLRaqtwME1MfyFAmSCCrkDZ1frN3IUom0sZUIxjZH34U39W8SBw?purpose=inline)

Raised geometry

Terracotta, limestone, muted marble, weathered timber, and matte surfaces. The 3D models should feel like crafted architectural miniatures connected to the flat illustration.

[Clay World Cities Gemini Image Prompt | PromptBase](https://images.openai.com/static-rsc-4/jzszAtu0NTW_pa8AkeyVsVyoh4gA5K7Kji7Py5albfvJGRbHzB6JFoqY-1pD96IXO2tBq7WDoaScQYNaSl2RkcExVizRAyuyZcB5fmj23vLEKSY49WO0VNOm1YLgTR_pD3XdZ0c8X--Cy1taqUdYRQ_5mN_avV_hAaNudN_2MeU?purpose=inline)

Motion and atmosphere

Soft shadows, gentle ambient occlusion, restrained haze, and smooth transitions. Avoid excessive glow, explosive particles, and the visual vocabulary of a mobile game.

### Starter palette

### Parchment

\#E6D3AA

### Sepia ink

\#6F4D34

### Terracotta

\#A65238

### Olive

\#777D5A

### River

\#65888A

### Panel surface

\#493626

These are starting tokens, not sacred artifacts. We'll adjust them against real maps, model materials, and accessibility tests.

## 5. Historical Rome as the first content pack

Rome is our launch environment, but we should not attempt to reconstruct the entire city at once. Start with a defined historical period and a compact, connected region.

My suggested starting point is imperial Rome around 100 CE, with the Roman Forum as the first exploration district. This is a practical artistic baseline, not a claim that every building or reconstruction detail can be known with certainty.

[Julius Caesar](https://images.openai.com/static-rsc-4/JJpFyYBf8JTw42BIl2KzmUqRqlycjeb9ScyNYayXuUhsPQnyUNbLKdtG1aSEi0evaGEaV6CrZXRSgJLHMes_g0ADE1CVf72ddroDwU2FxYlmvN1mPhKRa-8DWp4qQlAnGjAzIEqGHj7Eo-ty06W2Z3Be5_GpYkynArOxr1lI_AA?purpose=inline)

[Historia desde Neuquén: El Coliseo de Roma: Una maravilla de la antiguedad](https://images.openai.com/static-rsc-4/sKPQezg1M7DiRaXekF4eLvcbr2DB_zBP-sAFeWVQBa8Af1JRNmhxl4LCXFoS7Sc8IZwR5yBd-XPLWZWYX5ZRdJYdpLQQEv9AfLu0C-dUkKGxltu4n-6iIM12LEQ2-S61udUQgdEpqNQhnG1u79AtgyE4p8wZlVBnXy9xOavwFj4?purpose=inline)

[Circo Máximo | Roma antigua, Paisaje urbano, Roma](https://images.openai.com/static-rsc-4/msQvmC0Flg-VmUQjWwYQgHi0nZI9mo14EAW-V4qjgl6KdFi_RX6GQzNMoIbIt0iYWG8zHDj__o_lZeA3bl4h8Q1vDpuvmNH330TWjfq4tIQhjyVkF-XyZZQErNyfF0Ic7jJew4CkMyeajvbnwstiph--dUfnuupeZZ58U3BBFyU?purpose=inline)

13

| Landmark         | Why it belongs in the prototype                               | Interaction                             |
| ---------------- | ------------------------------------------------------------- | --------------------------------------- |
| Roman Forum      | Dense architectural core and civic life                       | Temples and civic buildings emerge      |
| Temple of Saturn | Recognizable architecture and a compact model                 | Columns and podium assemble             |
| Curia Julia      | Clear historical function and interior storytelling potential | Exterior reveal, then interior scene    |
| Colosseum        | Distinctive landmark with strong visual payoff                | Monumental structure rises from map     |
| Circus Maximus   | Large-scale geography and public entertainment                | Track and surrounding structures emerge |

The five sites provide different model scales, architectural forms, and interaction patterns. We can reuse the same rendering system while varying the content.

A key constraint: each site must have period-specific geometry and historically reviewed notes. A single generic Roman building wearing five different labels is not a content strategy.

### What the first scenes demonstrate

- Architecture: materials, construction forms, height, and spatial layout.
- Daily life: plausible activities, crowds, trade, movement, and environmental sound.
- Civic function: how buildings were used and why their locations mattered.
- Historical events: curated, sourced stories attached to the relevant geography.
- Chronology: what changed between supported dates, including construction, rebuilding, and decay.

We should include confidence metadata internally and distinguish documented facts, evidence-based reconstructions, and artistic interpretation in the UI where it matters.

## 6. Technical architecture

The architecture should separate four concerns: rendering the world, defining historical content, coordinating interactions, and delivering assets.

### Experience Layer

City browser · Timeline · Landmark panel · Story navigation

### World Interaction Engine

Camera controller · Selection · Reveal animations · Period transitions · Scene state

3D Renderer

Geometry, materials, lighting, hit testing

Historical Content

Cities, periods, places, sources, stories

### Asset Delivery

Map tiles or textures · glTF models · animation data · audio · content manifests

### Recommended technology stack

| Layer                | Recommendation                                             | Responsibility                                             |
| -------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| Frontend             | React + TypeScript                                         | Application UI, routing, accessibility                     |
| 3D                   | Three.js + React Three Fiber                               | World rendering, camera, geometry, lighting                |
| Interaction          | Custom state machine; lightweight state store              | Hover, selection, camera transitions, period changes       |
| Animation            | Three.js animation system plus custom procedural animation | Landmark emergence and scene activity                      |
| 3D asset creation    | Blender, exported as glTF/GLB                              | Architecture, props, character animation                   |
| Content              | Versioned JSON or typed content manifests                  | City definitions, landmarks, timelines, source metadata    |
| Static delivery      | Object storage and CDN                                     | Textures, models, audio, map assets                        |
| Backend, when needed | API plus PostgreSQL                                        | Publishing, editorial tools, user progress, saved journeys |
| Testing              | Unit tests, browser integration tests, visual regression   | Correctness and performance                                |

I would not introduce a backend database, message queue, or microservice fleet just to render a few Roman temples. Static content is enough to validate the core product. We can add persistence and editorial services when the workflow requires them.

### Repository structure

A monorepo will keep the renderer, content schema, and asset tooling versioned together.

```
chronoscape/
├── apps/
│   └── web/
│       ├── routes/
│       ├── components/
│       └── experience/
├── packages/
│   ├── renderer/
│   │   ├── camera/
│   │   ├── materials/
│   │   ├── interaction/
│   │   └── animation/
│   ├── content-schema/
│   ├── city-runtime/
│   ├── historical-ui/
│   └── asset-pipeline/
├── content/
│   ├── cities/
│   │   └── rome/
│   │       ├── city.json
│   │       ├── periods/
│   │       ├── landmarks/
│   │       ├── stories/
│   │       └── sources/
│   └── shared/
├── assets/
│   ├── maps/
│   ├── models/
│   ├── textures/
│   └── audio/
├── tests/
└── docs/
```

This is a logical structure, not a mandate to create 40 packages before the first landmark renders. Start with a few cohesive packages and extract boundaries as they become real.

### Data model: the foundation for every future city

The content model needs to distinguish a city, a historical period, a geographical place, a particular historical structure, and a story. These are related entities, but they are not interchangeable.

For example, a location can persist while its buildings change. The Forum remains a geographical place even as its architecture and function evolve.

```
type City = {
  id: string;
  name: string;
  defaultPeriodId: string;
  bounds: [number, number, number, number];
  mapAsset: string;
  periods: HistoricalPeriod[];
  districts: District[];
  landmarks: Landmark[];
  stories: HistoricalStory[];
};

type HistoricalPeriod = {
  id: string;
  label: string;
  startYear: number;
  endYear: number;
  calendar: "CE_BCE";
};

type Landmark = {
  id: string;
  placeId: string;
  name: string;
  position: [number, number];
  activePeriods: string[];
  assetByPeriod: Record<string, string>;
  revealAnimation: string;
  sceneId: string;
  sourceIds: string[];
};

type HistoricalStory = {
  id: string;
  title: string;
  periodId: string;
  steps: {
    landmarkId: string;
    narrationId: string;
    eventDate?: string;
  }[];
  sourceIds: string[];
};
```

This is an illustrative starting schema. Before implementation, we'd refine coordinate systems, date ranges, multilingual content, model variants, asset versions, and source records.

A few important decisions:

- Use stable geographical identities. A place can outlive a building.
- Represent time explicitly. Structures may be built, modified, destroyed, or restored at different dates.
- Keep content independent of presentation. Historical text should not live inside React components.
- Store sources with the claims they support. A source attached to a whole city is not enough for every individual assertion.
- Validate manifests at build time. Missing assets and invalid landmark references should fail validation before reaching the browser.

### Map coordinates and 3D coordinates

This deserves special care.

A 2D illustrated map may use image pixels or normalized coordinates, while 3D objects use world-space positions and elevations. Those coordinate systems need an explicit conversion layer.

For the first city, we can use a custom local coordinate system anchored to the illustrated map. We don't need full GIS precision for every artistic element, but we do need consistent transformations between map position, model placement, and camera targets.

If we later support geographically accurate maps, we can introduce georeferencing and projection metadata without forcing the rendering engine to understand every map's source format.

### How a new city gets added

1\. Define the city

Metadata, map bounds, supported periods, districts.

2\. Add historical places and assets

Landmarks, models, material variants, animations, source records.

3\. Author stories and timelines

Events linked to places and periods.

4\. Validate and publish

Check references, asset sizes, date consistency, and historical review status.

The renderer should never need an `if (city === "rome")` branch just to decide how a landmark rises out of the map. City-specific differences belong in content, assets, and declared capabilities.

## 7. Performance and asset strategy

This project can easily become a browser performance disaster if every building, texture, animation, and historical era is loaded at startup.

We need a deliberate level-of-detail strategy.

| View                     | Rendering strategy                                                      |
| ------------------------ | ----------------------------------------------------------------------- |
| City overview            | Flat map, labels, minimal landmark proxies                              |
| District view            | Selected raised geometry, nearby landmarks, simplified props            |
| Landmark preview         | Detailed model for the hovered landmark, short reveal animation         |
| Focused scene            | High-detail landmark, selected props, limited animated characters       |
| Historical period change | Load required asset variants, transition, then release unused resources |

### Practical targets

These are proposed engineering targets for the first release, not measured performance claims.

- Aim for 60 FPS on supported desktop hardware under the typical exploration workload.
- Avoid loading every detailed 3D model at startup.
- Keep the initial experience useful while secondary assets load.
- Use texture compression, geometry optimization, and instancing for repeated objects.
- Limit shadow-casting lights and animated objects in large scenes.
- Reuse geometry and materials where possible, while disposing of resources when no longer needed.
- Establish a mobile performance tier with lower detail and reduced effects.
- Monitor actual frame times, memory usage, load latency, and errors on representative devices.

We should measure both average frame rate and frame-time spikes. A scene that averages 60 FPS but stutters whenever a user hovers over a landmark is still broken.

The asset pipeline should also generate thumbnails and lightweight previews so the city browser doesn't need to load the full 3D world for every city card.

## 8. Phased implementation roadmap

The project should progress through validated milestones. We can build a platform from the beginning without trying to deliver every feature in the first release. Those are different things, despite how often software teams confuse them.

### P0

Foundation

Product specification and technical spike

1 week

- Finalize coordinate conventions, content schema, and interaction states.
- Prototype camera controls, hover detection, and a parchment material.
- Compare orthographic and perspective camera behavior.
- Establish the asset pipeline and initial performance baseline.

Exit criterion: one simple scene demonstrates the intended map-to-3D transition, and the key technical choices are validated.

### P1

Vertical slice

Build one excellent landmark

2–3 weeks

- Create the initial illustrated map and one detailed landmark.
- Implement hover emergence, click-to-focus, and camera return.
- Add the historical information panel.
- Test keyboard, pointer, touch, and reduced-motion behavior.

Exit criterion: one landmark is satisfying to explore, transitions reliably, and works across the supported desktop browsers.

### P2

Rome alpha

Complete the first playable district

3–5 weeks

- Add the remaining prototype landmarks.
- Introduce multiple detail levels and lazy asset loading.
- Add a working historical period selector.
- Create one short historical story with multiple stops.
- Validate the content schema against multiple different landmark types.

Exit criterion: a connected Roman district supports exploration, historical context, period switching, and story navigation.

### P3

Platform alpha

Prove the multi-city architecture

2–4 weeks

- Implement a city registry and generic city loader.
- Add a second, deliberately different test city with a small content pack.
- Build automated content validation and asset checks.
- Separate shared rendering behavior from city-specific configuration.
- Test switching cities and periods without stale state or asset leaks.

Exit criterion: a second city can be published through content and asset configuration without changing the core renderer.

### P4

Beta

Harden and prepare for release

3–5 weeks

- Optimize rendering and initial load time.
- Add error handling, accessibility checks, and mobile adaptations.
- Complete historical review and source attribution.
- Introduce persistent progress or saved journeys if user testing validates the need.
- Establish deployment, monitoring, and regression testing.

Exit criterion: the experience meets agreed performance and reliability targets on a defined device matrix.

Planning estimate: approximately 11–18 weeks for an experienced small team, assuming a constrained first district, available 3D production capacity, and no major research or asset-creation delays. A solo developer producing custom historical models and animations should expect a longer schedule.

## 9. Definition of done for the first release

The first release should be considered complete only when the following are true.

## Release checklist

0 / 15

### Experience

The illustrated map supports smooth pan and zoom.

Hover previews and click-to-focus transitions work reliably.

Users can exit scenes and restore their previous camera position.

At least one historical story links multiple locations.

### History

Every published landmark has a supported period and source references.

Period changes update relevant models, labels, and historical content consistently.

Interpretations and uncertain reconstructions are identified appropriately.

### Platform

A city can be loaded from validated content definitions.

A second test city works without renderer-specific city conditionals.

Missing assets and invalid references are caught before publication.

Assets load progressively and are released when no longer needed.

### Quality

Supported desktop browsers pass interaction tests.

Performance targets are measured on representative hardware.

Keyboard navigation and reduced-motion behavior are tested.

A production build and deployment pipeline are repeatable.

Copy checklist

This checklist is interactive planning state, not a claim that any of the features have already been implemented.

## 10. Major risks and how we manage them

| Risk                                   | Why it matters                                                  | Mitigation                                                            |
| -------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------- |
| Asset production becomes too expensive | Every city and era needs credible visual content                | Modular architecture kits, reusable props, constrained initial scope  |
| Historical inaccuracies                | Attractive visuals can make invented details seem authoritative | Source records, editorial review, uncertainty labels                  |
| Performance degrades with scale        | Detailed geometry and animation are expensive                   | Level of detail, instancing, progressive loading, profiling           |
| Hover interactions become annoying     | Accidental previews disrupt navigation                          | Delayed exit, interruptible animation, explicit click-to-focus        |
| New cities require code changes        | The platform fails its central product promise                  | Schema-driven content, city-agnostic renderer, second-city validation |
| Time periods become inconsistent       | Buildings and events can appear in the wrong era                | Explicit date ranges, period-aware assets, content validation         |
| Parchment styling hurts readability    | Texture and decorative labels obscure navigation                | Contrast testing, restrained texture, real text overlays              |

One additional risk deserves attention: historical geography is not always certain, and maps are often reconstructed from incomplete archaeological evidence. Our content pipeline should support approximate placements, source citations, and confidence annotations rather than pretending every street corner has a definitive coordinate.

## 11. Product boundaries: what we deliberately postpone

The following are not required for the first playable release:

- AI-generated historical characters that converse with visitors.
- Multiplayer exploration.
- A complete reconstruction of every Roman neighborhood.
- User-generated city publishing.
- A sophisticated CMS and collaborative editorial workflow.
- Procedurally generated entire cities.
- VR support.
- Live integrations with GIS or archaeological databases.

Some may eventually be valuable. None should distract us from proving that the core map-to-world interaction works.

## 12. The immediate next step

The next deliverable should be a technical design specification and vertical-slice prototype plan, not a large backlog of vaguely defined features.

I'd start with this concrete prototype:

1. A parchment map covering a small part of the Roman Forum.
2. One historically reviewed temple or civic building.
3. A 3D model that emerges from its exact position on the map.
4. A hover preview with an interruptible animation.
5. A click-to-focus camera transition.
6. A small historical panel with a supported date and references.
7. A clean return to the original map state.
8. A content definition that allows the same landmark interaction to work with a different model.

Once this works, we validate the architecture by adding a second landmark through data alone. Then we build the timeline, multi-stop stories, and second-city support.

The strategic principle: build the engine once, prove it with Rome, and scale through content. The first city establishes the quality bar; the second city proves whether the architecture is actually reusable. Everything else is a hypothesis until those two tests pass.