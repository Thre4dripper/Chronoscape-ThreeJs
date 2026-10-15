import type { FieldKind, Insula, Lot, Style } from "./fabric";

/** What an ordinary city block was, by era style and type. City-agnostic. */
export function describeBlock(style: Style, b: Insula, lots: Lot[]): { title: string; text: string; facts: string } {
  const own = lots.slice(b.lot0, b.lot1).filter((l) => l.kind !== "court");
  const towers = own.filter((l) => l.kind === "tower").length;
  const hAvg = own.reduce((a, l) => a + l.h, 0) / Math.max(1, own.length);
  const storeys = Math.max(1, Math.round(hAvg / 3.3));
  const facts = `${own.length} building${own.length === 1 ? "" : "s"} · about ${storeys} storey${storeys === 1 ? "" : "s"}${towers ? ` · ${towers} tower${towers > 1 ? "s" : ""}` : ""} · ${Math.round(b.w)} × ${Math.round(b.d)} m`;
  if (style === "archaic") return { title: "Huts of the early village", text: "Oval huts of wattle and daub on a timber frame, with thatched roofs and a hearth in the middle, as the post-holes on the Palatine show. Families kept pigs and sheep in fenced yards.", facts: `${own.length} hut${own.length === 1 ? "" : "s"}` };
  if (style === "antique") {
    if (b.type === "villa") return { title: "Domus with garden", text: "A private house for one family and its slaves: an atrium open to the sky, a peristyle garden, dining rooms. Blank walls to the street, sometimes a shop let out at the corner.", facts };
    const tall = own.filter((l) => l.h >= 13).length;
    if (b.type === "court") return { title: "Insula around a courtyard", text: "Shops and flats of brick-faced concrete around a light well. Tabernae (shops) open onto the street, the best flats are on the first floor, cheap rooms under the roof.", facts };
    if (tall >= Math.max(2, own.length * 0.25)) return { title: "Insulae (apartment blocks)", text: "Rented flats over shops, some of them four or five storeys high: Augustus capped the height at about 20 m. Fires and collapses were common, and water came from the street fountain, not the tap.", facts };
    return { title: "Shops and houses", text: "Mostly two- and three-storey buildings: a row of tabernae with wide arched openings at street level, the shopkeeper's family living on the mezzanine or the floor above, a timber balcony over the street.", facts };
  }
  if (style === "medieval") {
    if (towers) return { title: "Houses and a baronial tower", text: "Two- and three-storey houses of reused brick and tufa, with a fortified tower of one of the baronial families rising among them. Towers were the strongholds of the street wars.", facts };
    if (b.density === "loose") return { title: "Scattered houses and vineyards", text: "A few houses with orchards and vineyards among the ruins, inside the old walls but far from the crowded river bend.", facts };
    return { title: "Houses of the abitato", text: "Narrow houses of two or three storeys with an outside stair, a shop or workshop at street level, and a loggia or wooden balcony above. Stone from ancient buildings is in every wall.", facts };
  }
  if (b.type === "palazzo") return { title: "Palazzo with a cortile", text: "The town house of a cardinal or banking family, built around an arcaded courtyard. Shops were often let out along the street front to help pay for it.", facts };
  if (b.density === "loose") return { title: "Vigna with a casino", text: "A suburban vineyard estate with a small pleasure house, where Roman families went to escape the summer heat of the abitato.", facts };
  return { title: "Case and botteghe", text: "Stuccoed houses of three or four storeys with shops and workshops below, many rebuilt along the new straight streets laid out by the popes.", facts };
}

/** What a piece of countryside was used for, by era style. */
export function describeField(style: Style, kind: FieldKind): { title: string; text: string } {
  const ancient = style === "antique" || style === "archaic";
  switch (kind) {
    case "furrow":
      return ancient
        ? { title: "Grain field", text: "Emmer, wheat and barley, ploughed with a yoke of oxen and an iron-shod ard. Market gardens near the city paid better: most of Rome's bread grain came by ship from Egypt, Sicily and Africa." }
        : { title: "Grain field", text: "Wheat and barley ploughed with oxen, sown by hand from a basket. Fields like this ran right up to the walls; the city's own grain never fed it for a full year." };
    case "pasture":
      return { title: "Pasture", text: ancient ? "Grazing for sheep and goats. Flocks moved between summer hills and winter lowlands along the drove roads, and many were sold in the Forum Boarium." : "Rough grazing for sheep and goats. Shepherds from the Campagna brought flocks right inside the walls, and cattle grazed among the ruins of the Forum." };
    case "vineyard":
      return { title: "Vineyard", text: ancient ? "Vines trained on stakes or trees in neat rows. Wine was the everyday drink, watered down at every meal." : "A vigna: vines in rows among the ruins, with a small hut for the owner. Roman families of every class kept one, and the harvest in September was a holiday." };
    default:
      return { title: "Orchard and garden", text: "Fruit trees, olives and vegetable beds: figs, apples, cabbages, leeks and beans, carried into the city markets before dawn." };
  }
}
