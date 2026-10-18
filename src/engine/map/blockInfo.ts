import type { Period } from "@/content/schema";
import type { FieldKind, Insula, Lot, Style } from "./fabric";

type Text = { title: string; text: string };

/** Generic houses of each non-Mediterranean tradition: [dense block, garden house / outskirts]. */
const TRADITION: Partial<Record<Style, [Text, Text]>> = {
  gothic: [
    { title: "Gabled town houses", text: "Narrow houses of timber frame and plaster, gable end to the street, their upper floors jutting out over a shop or workshop. Steep roofs of slate or tile shed the northern rain; behind them, yards, wells and privies." },
    { title: "Houses with gardens", text: "Larger houses and religious precincts with kitchen gardens, orchards and vines, on the edge of the built-up town." },
  ],
  courtyard: [
    { title: "Courtyard houses", text: "Blank walls to the lane and a bent entrance for privacy; inside, rooms open onto a courtyard with a well or a tree. Flat roofs are terraces where families sleep on hot nights. Shops cluster along the main streets, not here." },
    { title: "Garden houses", text: "A walled garden with a larger house for a wealthy family: water channels, fruit trees and shade, behind a gate kept by a porter." },
  ],
  sinic: [
    { title: "Courtyard compounds", text: "Single-storey halls of timber and rammed earth around one or more courtyards, facing south. Grey tiled roofs, blank walls to the lane, and the ward's gates shut at dusk by the drum." },
    { title: "Mansion and garden", text: "The walled compound of an official or a wealthy family: several courtyards in a row, a garden of rocks, ponds and pavilions behind." },
  ],
  japanese: [
    { title: "Machiya (town houses)", text: "Narrow fronts and deep plots: a shop opening onto the street behind lattices and a short curtain, living rooms behind, a tiny garden and a fireproof storehouse at the back." },
    { title: "Residences in their grounds", text: "Walled estates of nobles, samurai or temples: timber halls on raised floors, wide eaves, gardens of moss, sand and pond." },
  ],
  mesoamerican: [
    { title: "Patio compounds", text: "Rooms of adobe and stone around an open patio, plastered white, with flat roofs of beams and earth. Several related families shared a compound, with a household shrine and a kitchen fire." },
    { title: "Houses among the fields", text: "Smaller houses of adobe or wattle beside their gardens and fields, farther from the ceremonial centre." },
  ],
  andean: [
    { title: "Kancha (walled compounds)", text: "A rectangle of fieldstone walls around a courtyard, with single rooms opening onto it under steep roofs of ichu grass thatch. Trapezoidal doors and niches; one compound housed an extended family." },
    { title: "Farmsteads", text: "Stone houses with thatched roofs among terraced fields and corrals for llamas and alpacas." },
  ],
  sahel: [
    { title: "Banco courtyard houses", text: "Houses of sun-dried mud brick (banco) around a courtyard, with flat roofs of palm beams and earth, replastered after every rainy season. The richest had a second storey and carved wooden doors." },
    { title: "Houses and gardens", text: "Mud-brick compounds with millet granaries and small gardens, on the edges of the town toward the river or the dunes." },
  ],
  kraal: [
    { title: "Homesteads", text: "Round houses of daga (mud plaster on a timber frame) with conical thatched roofs, set in yards with low walls, granaries on stilts and a hearth outside." },
    { title: "Homesteads", text: "Round houses of daga with conical thatch, scattered among gardens and cattle enclosures." },
  ],
};

/** Pleasure gardens, by tradition. */
export function gardenText(style: Style): string {
  if (style === "courtyard") return "A walled garden laid out in four parts by water channels, with fountains, fruit trees and a pavilion: a paradise on earth, in the Persian phrase.";
  if (style === "sinic" || style === "japanese") return "A garden of ponds, rocks, bridges and pavilions, composed as a landscape in miniature to be walked through slowly.";
  if (style === "mesoamerican") return "Gardens of flowers and medicinal plants, and menageries of birds and animals, kept by lords for pleasure and for study.";
  return "Pleasure gardens: shaded walks, clipped hedges, fountains and statues, where the rich entertained and philosophers walked.";
}

/** What an ordinary city block was, by era style and type; a period may describe its own houses. */
export function describeBlock(style: Style, b: Insula, lots: Lot[], period?: Period): { title: string; text: string; facts: string } {
  const own = lots.slice(b.lot0, b.lot1).filter((l) => l.kind !== "court");
  const towers = own.filter((l) => l.kind === "tower").length;
  const hAvg = own.reduce((a, l) => a + l.h, 0) / Math.max(1, own.length);
  const storeys = Math.max(1, Math.round(hAvg / 3.3));
  const facts = `${own.length} building${own.length === 1 ? "" : "s"} · about ${storeys} storey${storeys === 1 ? "" : "s"}${towers ? ` · ${towers} tower${towers > 1 ? "s" : ""}` : ""} · ${Math.round(b.w)} × ${Math.round(b.d)} m`;
  const custom = period && (b.density === "loose" || b.type === "villa" ? period.outskirts : period.houses);
  if (custom) return { ...custom, facts };
  const t = TRADITION[style];
  if (t) return { ...(b.density === "loose" || b.type === "villa" ? t[1] : t[0]), facts };
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
  const other = FIELDS[style]?.[kind === "vineyard" ? "orchard" : kind];
  if (other) return other;
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

/** Countryside outside the Mediterranean: rice, maize, millet and dates instead of wheat and vines. */
const FIELDS: Partial<Record<Style, Partial<Record<FieldKind, Text>>>> = {
  courtyard: {
    furrow: { title: "Irrigated fields", text: "Wheat, barley, cotton and sugar cane, watered by canals and wells worked by oxen. Fields were measured carefully: the land tax was the state's main income." },
    pasture: { title: "Grazing", text: "Rough grazing for sheep, goats and camels, and the herds of the caravans camped outside the gates." },
    orchard: { title: "Orchards and palm groves", text: "Date palms, pomegranates, figs, apricots and melons in walled gardens watered by channels." },
  },
  sinic: {
    furrow: { title: "Fields of millet and wheat", text: "Millet, wheat and vegetables on the loess plain, and rice wherever water could be led. Farmers paid their taxes in grain and cloth and did their labour service on the walls and canals." },
    pasture: { title: "Commons", text: "Rough ground for oxen and the post horses, and mulberry trees for the silkworms." },
    orchard: { title: "Orchards and market gardens", text: "Peaches, jujubes, pears and vegetables grown for the city markets." },
  },
  japanese: {
    furrow: { title: "Rice paddies", text: "Flooded fields of rice, levelled and banked, planted by hand in early summer and harvested in autumn; rice was also the unit in which incomes and taxes were reckoned." },
    pasture: { title: "Dry fields", text: "Barley, millet, beans and radishes on ground the water could not reach." },
    orchard: { title: "Orchards and groves", text: "Persimmons, plums and tea bushes, and bamboo groves for building and baskets." },
  },
  mesoamerican: {
    furrow: { title: "Milpa and chinampas", text: "Maize, beans and squash grown together; in the lake, chinampas, long raised beds of mud and reeds between canals, gave several harvests a year." },
    pasture: { title: "Scrub and maguey", text: "Maguey plants for fibre and pulque, nopal cactus, and scrub for firewood. There were no grazing animals: turkeys and dogs were kept in the yards." },
    orchard: { title: "House gardens", text: "Chillies, tomatoes, avocados, amaranth and flowers grown beside the houses." },
  },
  andean: {
    furrow: { title: "Terraced fields", text: "Stone-walled terraces stepping down the slopes, growing maize low down and potatoes and quinoa higher up, watered by channels from the mountain streams." },
    pasture: { title: "Grazing on the puna", text: "Herds of llamas and alpacas for wool and carrying, tended by herders on the high grasslands." },
    orchard: { title: "Gardens", text: "Maize, beans, chillies and coca grown on the warmer valley terraces." },
  },
  sahel: {
    furrow: { title: "Millet and rice fields", text: "Millet and sorghum on the dry ground, rice in the floodplain of the Niger as the waters fell after the rains." },
    pasture: { title: "Grazing", text: "Cattle, goats and camels of the herders who traded milk and meat at the markets." },
    orchard: { title: "Gardens", text: "Small irrigated gardens of onions, tobacco and vegetables near the wells and the river." },
  },
  kraal: {
    furrow: { title: "Fields of sorghum and millet", text: "Sorghum, finger millet and beans, cleared from the bush and worked with iron hoes." },
    pasture: { title: "Cattle grazing", text: "Cattle were wealth: herds grazed the grasslands in the care of young men and were moved with the seasons." },
    orchard: { title: "Gardens", text: "Gourds, beans and groundnuts grown close to the homesteads." },
  },
};
