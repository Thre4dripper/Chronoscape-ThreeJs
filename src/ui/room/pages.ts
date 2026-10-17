import * as THREE from "three";
import type { Atlas } from "@/content/schema";
import { compassRose, spaced } from "@/world/world";
import { ROMAN } from "./toon";

/**
 * The first page inside an atlas, under its cover: an index of its maps, set
 * like an old title page. Each row's place on the page (in texture v) is kept
 * in userData.rows so the held atlas can tell which map the pointer is on.
 */
export function indexTexture(a: Atlas, w = 512, h = 712) {
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  const g = c.getContext("2d")!;
  const grad = g.createLinearGradient(0, 0, w, h);
  grad.addColorStop(0, "#f6ebcf");
  grad.addColorStop(1, "#e8d6ab");
  g.fillStyle = grad;
  g.fillRect(0, 0, w, h);
  g.strokeStyle = "#4a3322";
  g.lineWidth = 2;
  g.strokeRect(20, 20, w - 40, h - 40);
  g.lineWidth = 1;
  g.strokeRect(27, 27, w - 54, h - 54);
  g.fillStyle = "#3d2a1c";
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.font = '600 30px "Cinzel", Georgia, serif';
  spaced(g, "INDEX MAPPARVM", w / 2, 74, 5);
  g.font = 'italic 22px "IM Fell English", Georgia, serif';
  g.fillStyle = "#8a3f26";
  g.fillText(a.title, w / 2, 110);
  // a rule with a star
  g.strokeStyle = "#4a3322";
  g.beginPath();
  g.moveTo(90, 136);
  g.lineTo(w / 2 - 14, 136);
  g.moveTo(w / 2 + 14, 136);
  g.lineTo(w - 90, 136);
  g.stroke();
  g.fillStyle = "#4a3322";
  g.beginPath();
  for (let i = 0; i < 8; i++) {
    const r = i % 2 ? 3 : 8, an = (i / 8) * Math.PI * 2 - Math.PI / 2;
    g.lineTo(w / 2 + Math.cos(an) * r, 136 + Math.sin(an) * r);
  }
  g.fill();
  const rows: { v0: number; v1: number; title: string }[] = [];
  const top = 166, rowH = Math.min(110, (h - top - 70) / a.maps.length);
  a.maps.forEach((m, i) => {
    const y = top + i * rowH;
    const ready = !!m.city;
    g.textAlign = "left";
    g.fillStyle = "#8a5a3a";
    g.font = '600 20px "Cinzel", Georgia, serif';
    g.fillText(ROMAN[i] ?? String(i + 1), 48, y + 24);
    g.fillStyle = "#3d2a1c";
    g.font = '700 26px "Cinzel", Georgia, serif';
    g.fillText(m.title, 100, y + 22);
    g.font = 'italic 19px "IM Fell English", Georgia, serif';
    g.fillStyle = "#4a3322";
    g.fillText(m.subtitle, 100, y + 52);
    g.textAlign = "right";
    g.font = '600 13px "Cinzel", Georgia, serif';
    g.fillStyle = ready ? "#a65238" : "rgba(74,51,34,0.55)";
    g.fillText(ready ? "✦ READY" : "IN PREPARATION", w - 46, y + 24);
    g.strokeStyle = "rgba(74,51,34,0.25)";
    g.setLineDash([2, 4]);
    g.beginPath();
    g.moveTo(48, y + rowH - 10);
    g.lineTo(w - 46, y + rowH - 10);
    g.stroke();
    g.setLineDash([]);
    rows.push({ v0: 1 - (y - 8) / h, v1: 1 - (y + rowH - 4) / h, title: m.title });
  });
  g.textAlign = "center";
  g.font = 'italic 17px "IM Fell English", Georgia, serif';
  g.fillStyle = "rgba(61,42,28,0.7)";
  g.fillText("Point at a map to read about it; click to open it.", w / 2, h - 48);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  t.userData.rows = rows;
  return t;
}

/** The inside of an atlas's front board: marbled endpaper with a printed bookplate. */
export function bookplateTexture(a: Atlas, w = 512, h = 712) {
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  const g = c.getContext("2d")!;
  // marbled endpaper: swirls of the atlas's colour on cream
  g.fillStyle = "#e9dcbc";
  g.fillRect(0, 0, w, h);
  let seed = a.id.length * 131 + 7;
  const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  for (let i = 0; i < 140; i++) {
    const x = rnd() * w, y = rnd() * h, r = 8 + rnd() * 34;
    g.strokeStyle = i % 3 ? a.color + "55" : "#3d2a1c33";
    g.lineWidth = 1 + rnd() * 3;
    g.beginPath();
    g.ellipse(x, y, r, r * (0.4 + rnd() * 0.6), rnd() * Math.PI, 0, Math.PI * 2);
    g.stroke();
  }
  // the bookplate
  const pw = 300, ph = 380, px = (w - pw) / 2, py = (h - ph) / 2;
  g.fillStyle = "#f6ecd2";
  g.fillRect(px, py, pw, ph);
  g.strokeStyle = "#3d2a1c";
  g.lineWidth = 3;
  g.strokeRect(px + 10, py + 10, pw - 20, ph - 20);
  g.lineWidth = 1;
  g.strokeRect(px + 18, py + 18, pw - 36, ph - 36);
  g.fillStyle = "#3d2a1c";
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.font = '600 26px "Cinzel", Georgia, serif';
  spaced(g, "EX LIBRIS", w / 2, py + 58, 6);
  compassRose(g, w / 2, py + 165, 64);
  g.font = '700 24px "Cinzel", Georgia, serif';
  const words = a.title.toUpperCase().split(" ");
  const lines: string[] = [];
  let cur = "";
  for (const wd of words) {
    const t = cur ? cur + " " + wd : wd;
    if (g.measureText(t).width > pw - 60 && cur) {
      lines.push(cur);
      cur = wd;
    } else cur = t;
  }
  lines.push(cur);
  lines.forEach((l, i) => g.fillText(l, w / 2, py + 268 + i * 30));
  g.font = 'italic 19px "IM Fell English", Georgia, serif';
  g.fillStyle = "#8a3f26";
  g.fillText("The Map Room, Chronoscape", w / 2, py + ph - 42);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}
