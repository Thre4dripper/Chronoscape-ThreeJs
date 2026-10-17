# Chronoscape: where this goes next

Brainstorm after the Rome expansion. The engine now supports eight eras, period-aware
maps, small places with hourly vignettes, dated events with effects, hoverable map
features and a day clock. Everything below builds on that, roughly in order of
payoff per effort.

## 1. Make the small things the heart of it

- **Lives, not just places.** Give each spot a few named people (a baker, a fuller,
  a bookseller's slave, a rosary seller) with a one-line biography drawn from
  epigraphy, Martial, Juvenal, the 1526 census. Hover the figure, meet the person.
- **Follow a coin / a loaf / an amphora.** Chains of spots: grain ship at the
  Emporium, porters, Horrea, the pistrinum, the breadline at the Porticus Minucia.
  A story type that walks an object through the city.
- **Sounds of the hour.** A tiny ambient layer per spot kind and hour (hammering,
  water, crowd, bells). Cheap, huge atmosphere.
- **Props on the map.** Instanced stalls, carts, amphorae, boats and laundry lines
  at spots when you zoom in, so the districts read as lived-in before you hover.

## 2. Time as a dimension, not a dropdown

- **Scrub the years.** A continuous slider between eras; buildings appear in their
  construction year (we already have `built` text; add `builtYear`/`goneYear`).
- **Construction scenes.** Scaffolding, cranes and stone deliveries during a
  building's construction window (the engine has the staged reveal; add a
  "half-built" stage).
- **Before/after wipe.** Split the plate: 100 CE on the left, 1300 on the right,
  drag the seam. The period-aware map makes this almost free.
- **Catastrophe layers.** Fires of 64 and 80, the flood of 1557, Alaric 410 as
  replayable overlays with spreading effects along the street network.

## 3. The map as an illustration you can read

- **Hand-drawn symbol set.** Replace the generic block hatching with period
  symbols: insulae, domus, horrea, churches with campanili, tower-houses,
  vineyards, kilns.
- **Named streets everywhere.** The road network should be dense enough that
  every spot sits on a named street with its own blurb; label along the curve.
- **Legend and marginalia.** A proper key in the cartouche, decorative sea
  monsters in the Tiber for the 1560 plate, surveyors' notes for uncertain areas.
- **Confidence shading.** A toggle that fades anything "interpretation" so you can
  see what is actually known.

## 4. Learning loops

- **Field notebook.** Everything you visit goes into a journal; vignettes you
  have seen, people you met, sources you opened. Shareable as a page.
- **Questions on the map.** "Where did bread come from?" "Why is the Forum full of
  cows in 1300?" Each answered by a short guided walk (the story system).
- **Then-and-now.** Overlay the modern street grid; most spots still have a
  street name that remembers them (Via dei Chiavari, Pescheria, Calcarario).
- **Classroom mode.** Teacher sets era, hour and a list of spots; students get a
  deep link and a worksheet generated from the vignettes and sources.

## 5. Depth where it pays

- **Interiors for five buildings**: a thermopolium counter, an insula stair, the
  Curia floor, a bath hall, a medieval tower-house. Street level already exists;
  interiors are the next layer.
- **Character crowds with purpose.** Figures already walk the streets; give them
  schedules (bakers at 4, senators at 8, bathers at 14) so the day clock changes
  who is where.
- **Processions as paths.** Triumphs and papal processions animate along the
  route with the camera following.

## 6. Pipeline and quality

- **Review flags per claim.** The writers' "unsure" lists are in the hand-off;
  move them into the content as `review: "..."` fields and show a discreet mark.
- **Source links that resolve.** Link-check script for the 200 sources; prefer
  stable URLs (Perseus, LacusCurtius, Wikipedia).
- **LOD and streaming.** Load only the current era's models; proxies for far
  zoom; dispose on era switch (partly done: inactive landmarks unmount).
- **Content linting.** Word limits, hour coverage, every district has spots,
  every era has events and a story.

## Order I would do it in

1. Props on the map and ambient sound (cheap, immediate).
2. Named people at spots and the field notebook.
3. Construction scenes and the year scrubber.
4. Interiors for five buildings.
5. Before/after wipe and catastrophe layers.
6. Classroom mode and then-and-now.
