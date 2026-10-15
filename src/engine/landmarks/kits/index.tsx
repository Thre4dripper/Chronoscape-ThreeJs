import { useMemo } from "react";
import type { KitParams } from "@/content/schema";
import { Annulus, Box, Columns, Cyl, Dome, GableRoof, Stage, StadiumRing, ellipseRing, mat, peristyle, shade } from "./shared";

/** Procedural miniature kits. All dimensions in metres; the parent applies world scale. */
export function Kit({ params }: { params: KitParams }) {
  switch (params.kit) {
    case "temple":
      return <Temple p={params} />;
    case "amphitheater":
      return <Amphitheater p={params} />;
    case "circus":
      return <Circus p={params} />;
    case "hall":
      return <Hall p={params} />;
    case "cluster":
      return <Cluster p={params} />;
    case "arch":
      return <Arch p={params} />;
    case "fort":
      return <Fort p={params} />;
    case "mosque":
      return <Mosque p={params} />;
    case "street":
      return <Street p={params} />;
  }
}

type P<K extends KitParams["kit"]> = Extract<KitParams, { kit: K }>;

function Temple({ p }: { p: P<"temple"> }) {
  const r = Math.min(p.width / (p.columnsFront * 4.5), 1.4);
  const cols = useMemo(() => peristyle(p.width - r * 2, p.depth - r * 2, p.columnsFront, p.columnsSide), [p, r]);
  const cellaW = p.width * (p.columnsSide > 0 ? 0.62 : 0.85);
  const cellaD = p.depth * (p.columnsSide > 0 ? 0.62 : 0.6);
  const ent = 1.6;
  return (
    <>
      <Stage index={0} count={3}>
        <Box w={p.width} h={p.podium} d={p.depth} color={shade(p.color, -0.08)} />
        {[0, 1, 2].map((i) => (
          <Box key={i} w={p.width * (0.6 - i * 0.05)} h={p.podium / 3} d={p.podium / 3} y={(p.podium / 3) * i} z={p.depth / 2 + (p.podium / 3) * (3 - i) * 0.5} color={shade(p.color, -0.06)} />
        ))}
      </Stage>
      <Stage index={1} count={3} position={[0, p.podium, 0]}>
        <Columns positions={cols} r={r} h={p.columnHeight} color={p.color} />
        <Box w={cellaW} h={p.columnHeight} d={cellaD} z={-p.depth * 0.08} color={shade(p.color, -0.04)} />
        <Box w={cellaW * 0.18} h={p.columnHeight * 0.55} d={0.5} z={cellaD / 2 - p.depth * 0.08 + 0.3} color="#3a2a1e" />
      </Stage>
      <Stage index={2} count={3} position={[0, p.podium + p.columnHeight + r * 0.8, 0]}>
        <Box w={p.width} h={ent} d={p.depth} color={shade(p.color, 0.04)} />
        <GableRoof w={p.width} d={p.depth} h={p.width * 0.16} y={ent} color={p.roofColor} />
      </Stage>
    </>
  );
}

function Amphitheater({ p }: { p: P<"amphitheater"> }) {
  const arc = (p.arc * Math.PI) / 180;
  const start = arc < Math.PI * 2 ? Math.PI - arc / 2 + Math.PI / 2 : 0;
  const total = p.tiers * p.tierHeight;
  const pillars = useMemo(() => ellipseRing(p.radiusX * 0.985, p.radiusY * 0.985, Math.round(p.radiusX / 2.5), arc, start), [p, arc, start]);
  return (
    <>
      <Stage index={0} count={p.tiers + 1}>
        <Annulus rx={p.radiusX} rz={p.radiusY} inner={0.42} h={p.tierHeight * 0.3} color="#c9b48b" arc={arc} start={start} />
        <Annulus rx={p.radiusX * 0.88} rz={p.radiusY * 0.88} inner={0.5} h={p.tierHeight * 0.45} y={p.tierHeight * 0.3} color={shade(p.color, -0.03)} arc={arc} start={start} />
        <Annulus rx={p.radiusX * 0.74} rz={p.radiusY * 0.74} inner={0.6} h={p.tierHeight * 0.4} y={p.tierHeight * 0.75} color={shade(p.color, -0.06)} arc={arc} start={start} />
        {arc < Math.PI * 2 && <Box w={p.radiusX * 1.6} h={p.tierHeight * 1.2} d={p.radiusY * 0.25} z={-p.radiusY * 0.45} color={shade(p.color, -0.05)} />}
      </Stage>
      {Array.from({ length: p.tiers }, (_, i) => (
        <Stage key={i} index={i + 1} count={p.tiers + 1} position={[0, i * p.tierHeight, 0]}>
          <Annulus rx={p.radiusX} rz={p.radiusY} inner={0.9} h={p.tierHeight} color={shade(p.color, i * 0.02)} arc={arc} start={start} />
          {i < p.tiers - 1 && (
            <instancedMesh args={[undefined, undefined, pillars.length]} material={mat(shade(p.color, 0.08))} castShadow ref={(m) => m && placeInstances(m, pillars, p.tierHeight)}>
              <boxGeometry args={[2.2, p.tierHeight, 2.2]} />
            </instancedMesh>
          )}
        </Stage>
      ))}
      <Stage index={p.tiers} count={p.tiers + 1} position={[0, total, 0]}>
        <Annulus rx={p.radiusX} rz={p.radiusY} inner={0.93} h={1.5} color={shade(p.color, 0.1)} arc={arc} start={start} />
      </Stage>
    </>
  );
}

function Circus({ p }: { p: P<"circus"> }) {
  const L = p.length,
    W = p.width;
  const spinaL = L * 0.55;
  return (
    <>
      <Stage index={0} count={3}>
        <Box w={L - 30} h={0.6} d={W - 30} color={p.trackColor} />
        <StadiumRing length={L} width={W} thickness={14} h={4} color={shade(p.color, -0.04)} />
        <StadiumRing length={L - 8} width={W - 8} thickness={10} h={7} color={shade(p.color, -0.02)} />
        <StadiumRing length={L - 16} width={W - 16} thickness={7} h={10} color={p.color} />
      </Stage>
      <Stage index={1} count={3}>
        <Box w={spinaL} h={2.5} d={8} x={L * 0.02} color={shade(p.color, 0.08)} />
        {[-1, 1].map((s) =>
          [0, 1, 2].map((i) => (
            <Cyl key={`${s}${i}`} r={1.5} rTop={0.3} h={7} x={L * 0.02 + s * (spinaL / 2 + 6) + s * i * 2} z={(i - 1) * 2.5} y={0.6} color={shade(p.color, 0.12)} />
          )),
        )}
        {Array.from({ length: p.obelisks }, (_, i) => (
          <group key={i}>
            <Cyl r={1.6} rTop={1.1} h={22} x={L * 0.02 + (i - (p.obelisks - 1) / 2) * spinaL * 0.4} y={2.5} color="#b89a74" seg={4} />
            <Cyl r={1.1} rTop={0} h={3} x={L * 0.02 + (i - (p.obelisks - 1) / 2) * spinaL * 0.4} y={24.5} color="#b89a74" seg={4} />
          </group>
        ))}
      </Stage>
      <Stage index={2} count={3}>
        {Array.from({ length: 12 }, (_, i) => (
          <Box key={i} w={6} h={8} d={(W - 40) / 12 - 1.5} x={-L / 2 + 10} z={-(W - 40) / 2 + ((W - 40) / 12) * (i + 0.5)} color={shade(p.color, 0.05)} />
        ))}
        <Box w={16} h={14} d={6} x={-L / 2 + 10} z={-W / 2 + 2} color={shade(p.color, 0.1)} />
        <Box w={16} h={14} d={6} x={-L / 2 + 10} z={W / 2 - 2} color={shade(p.color, 0.1)} />
        <Box w={30} h={16} d={14} x={L * 0.05} z={-W / 2 + 4} color={shade(p.color, 0.1)} />
        <GableRoof w={30} d={14} h={5} x={L * 0.05} z={-W / 2 + 4} y={16} color="#A65238" />
      </Stage>
    </>
  );
}

function Hall({ p }: { p: P<"hall"> }) {
  const cols = useMemo(() => (p.porticoColumns > 0 ? peristyle(p.width * 0.8, 0.1, p.porticoColumns, 0) : []), [p]);
  return (
    <>
      <Stage index={0} count={2}>
        <Box w={p.width + 2} h={1.5} d={p.depth + 2} color={shade(p.color, -0.1)} />
        <Box w={p.width} h={p.height} d={p.depth} y={1.5} color={p.color} />
        <Box w={p.width * 0.2} h={p.height * 0.45} d={0.5} y={1.5} z={p.depth / 2 + 0.2} color="#3a2a1e" />
        {[-1, 0, 1].map((i) => (
          <Box key={i} w={p.width * 0.1} h={p.height * 0.18} d={0.5} x={i * p.width * 0.25} y={1.5 + p.height * 0.62} z={p.depth / 2 + 0.2} color="#3a2a1e" />
        ))}
        {cols.length > 0 && <Columns positions={cols.map(([x]) => [x, p.depth / 2 + 5])} r={1} h={p.height * 0.7} color={shade(p.color, 0.1)} />}
        {cols.length > 0 && <Box w={p.width * 0.9} h={1.5} d={6} y={1.5 + p.height * 0.7} z={p.depth / 2 + 3} color={shade(p.color, 0.1)} />}
      </Stage>
      <Stage index={1} count={2} position={[0, 1.5 + p.height, 0]}>
        {p.roof === "pitched" && <GableRoof w={p.width} d={p.depth} h={p.width * 0.22} color={p.roofColor} />}
        {p.roof === "flat" && <Box w={p.width + 1} h={1} d={p.depth + 1} color={p.roofColor} />}
        {p.roof === "dome" && <Dome r={Math.min(p.width, p.depth) / 2} color={p.roofColor} />}
      </Stage>
    </>
  );
}

function Cluster({ p }: { p: P<"cluster"> }) {
  return (
    <>
      <Stage index={0} count={2}>
        {p.plaza && <Box w={p.plaza.width} h={0.8} d={p.plaza.depth} color={p.plaza.color} />}
        {p.buildings.map((b, i) => (
          <Box key={i} w={b.width} h={b.height} d={b.depth} x={b.offset[0]} z={b.offset[1]} y={p.plaza ? 0.8 : 0} color={b.color ?? p.color} />
        ))}
      </Stage>
      <Stage index={1} count={2}>
        {p.buildings.map((b, i) => {
          const y = b.height + (p.plaza ? 0.8 : 0);
          if (b.roof === "pitched") return <GableRoof key={i} w={b.width} d={b.depth} h={b.width * 0.2} x={b.offset[0]} z={b.offset[1]} y={y} color={p.roofColor} overhang={0.4} />;
          if (b.roof === "dome") return <Dome key={i} r={Math.min(b.width, b.depth) / 2} x={b.offset[0]} z={b.offset[1]} y={y} color={p.roofColor} />;
          return <Box key={i} w={b.width + 0.6} h={0.6} d={b.depth + 0.6} x={b.offset[0]} z={b.offset[1]} y={y} color={shade(p.roofColor, 0.1)} />;
        })}
      </Stage>
    </>
  );
}

function Arch({ p }: { p: P<"arch"> }) {
  const pierW = p.width / (p.bays * 3 + 1);
  const piers = Array.from({ length: p.bays + 1 }, (_, i) => -p.width / 2 + pierW / 2 + i * (p.width - pierW) / p.bays);
  return (
    <>
      <Stage index={0} count={2}>
        {piers.map((x, i) => (
          <Box key={i} w={pierW} h={p.height * 0.62} d={p.depth} x={x} color={p.color} />
        ))}
        {piers.map((x, i) => (
          <Cyl key={`c${i}`} r={pierW * 0.18} h={p.height * 0.58} x={x} z={p.depth / 2} color={shade(p.color, 0.05)} />
        ))}
      </Stage>
      <Stage index={1} count={2} position={[0, p.height * 0.62, 0]}>
        <Box w={p.width} h={p.height * 0.14} d={p.depth} color={shade(p.color, 0.03)} />
        <Box w={p.width * 0.96} h={p.height * 0.24} d={p.depth * 0.9} y={p.height * 0.14} color={shade(p.color, -0.02)} />
        <Box w={p.width * 0.4} h={p.height * 0.12} d={p.depth * 0.3} y={p.height * 0.38} color="#8a7a58" />
      </Stage>
    </>
  );
}

function Fort({ p }: { p: P<"fort"> }) {
  const t = 8;
  const towers: [number, number][] = [];
  const perSide = Math.max(2, Math.round(p.bastions / 4));
  for (let i = 0; i < perSide; i++) {
    const fx = -p.width / 2 + (p.width * i) / (perSide - 1);
    const fz = -p.depth / 2 + (p.depth * i) / (perSide - 1);
    towers.push([fx, -p.depth / 2], [fx, p.depth / 2], [-p.width / 2, fz], [p.width / 2, fz]);
  }
  return (
    <>
      <Stage index={0} count={3}>
        <Box w={p.width} h={1} d={p.depth} color={shade(p.color, 0.25)} />
        <Box w={p.width} h={p.wallHeight} d={t} z={-p.depth / 2} color={p.color} />
        <Box w={p.width} h={p.wallHeight} d={t} z={p.depth / 2} color={p.color} />
        <Box w={t} h={p.wallHeight} d={p.depth} x={-p.width / 2} color={p.color} />
        <Box w={t} h={p.wallHeight} d={p.depth} x={p.width / 2} color={p.color} />
        {towers.map(([x, z], i) => (
          <Cyl key={i} r={t * 1.1} h={p.wallHeight * 1.15} x={x} z={z} color={shade(p.color, -0.05)} seg={10} />
        ))}
      </Stage>
      <Stage index={1} count={3}>
        <Box w={30} h={p.wallHeight * 1.4} d={t * 2.5} x={-p.width / 2} z={0} color={shade(p.color, 0.02)} />
        {[-1, 1].map((s) => (
          <Cyl key={s} r={t} h={p.wallHeight * 1.7} x={-p.width / 2} z={s * 22} color={shade(p.color, -0.04)} seg={8} />
        ))}
        {[-1, 1].map((s) => (
          <Dome key={`d${s}`} r={t * 0.9} x={-p.width / 2} z={s * 22} y={p.wallHeight * 1.7} color="#efe6d2" />
        ))}
      </Stage>
      <Stage index={2} count={3}>
        <Box w={p.width * 0.28} h={9} d={p.depth * 0.18} x={-p.width * 0.1} z={-p.depth * 0.05} color="#d9b8a2" />
        <Box w={p.width * 0.18} h={10} d={p.depth * 0.12} x={p.width * 0.25} z={-p.depth * 0.25} color="#efe6d2" />
        <Box w={p.width * 0.14} h={9} d={p.depth * 0.12} x={p.width * 0.25} z={p.depth * 0.1} color="#efe6d2" />
        <Box w={p.width * 0.14} h={9} d={p.depth * 0.12} x={p.width * 0.25} z={p.depth * 0.3} color="#efe6d2" />
        <Box w={p.width * 0.55} h={3} d={14} x={-p.width * 0.1} z={p.depth * 0.3} color="#8aa07a" />
      </Stage>
    </>
  );
}

function Mosque({ p }: { p: P<"mosque"> }) {
  const plat = 8;
  const hallD = p.depth * 0.28;
  const hallZ = -p.depth / 2 + hallD / 2;
  const domeR = Math.min(p.width / (p.domes * 2.6), hallD * 0.45);
  return (
    <>
      <Stage index={0} count={3}>
        <Box w={p.width + 20} h={plat} d={p.depth + 20} color={shade(p.color, -0.08)} />
        {[0, 1, 2, 3].map((i) => (
          <Box key={i} w={p.width * 0.35} h={plat / 4} d={6 + i * 4} y={(plat / 4) * (3 - i)} z={p.depth / 2 + 10 + 4 + i * 2} color={shade(p.color, -0.08)} />
        ))}
      </Stage>
      <Stage index={1} count={3} position={[0, plat, 0]}>
        <Box w={p.width} h={6} d={4} z={p.depth / 2} color={p.color} />
        <Box w={4} h={6} d={p.depth} x={-p.width / 2} color={p.color} />
        <Box w={4} h={6} d={p.depth} x={p.width / 2} color={p.color} />
        <Box w={p.width * 0.22} h={14} d={10} z={p.depth / 2} color={shade(p.color, 0.04)} />
        <Box w={10} h={12} d={p.depth * 0.2} x={-p.width / 2} color={shade(p.color, 0.04)} />
        <Box w={10} h={12} d={p.depth * 0.2} x={p.width / 2} color={shade(p.color, 0.04)} />
        <Cyl r={p.width * 0.06} h={1.2} color="#9fb7bd" seg={8} />
      </Stage>
      <Stage index={2} count={3} position={[0, plat, 0]}>
        <Box w={p.width} h={16} d={hallD} z={hallZ} color={p.color} />
        <Box w={p.width * 0.26} h={22} d={hallD * 0.5} z={hallZ + hallD * 0.3} color={shade(p.color, 0.04)} />
        {Array.from({ length: p.domes }, (_, i) => {
          const x = (i - (p.domes - 1) / 2) * domeR * 2.5;
          const big = i === Math.floor(p.domes / 2);
          return <Dome key={i} r={big ? domeR * 1.15 : domeR} x={x} z={hallZ} y={16} color={p.domeColor} squash={1.15} />;
        })}
        {[-1, 1].map((s) => (
          <group key={s}>
            <Cyl r={3.2} rTop={2.4} h={p.minaretHeight} x={s * (p.width / 2 + 2)} z={hallZ - hallD / 2 + 4} color={p.color} seg={8} />
            <Dome r={3} x={s * (p.width / 2 + 2)} z={hallZ - hallD / 2 + 4} y={p.minaretHeight} color={p.domeColor} />
          </group>
        ))}
      </Stage>
    </>
  );
}

function Street({ p }: { p: P<"street"> }) {
  const L = p.length,
    W = p.width;
  const n = p.shops;
  const shopL = L / n;
  const shops = Array.from({ length: n }, (_, i) => ({
    x: -L / 2 + shopL * (i + 0.5),
    h: 7 + ((i * 7) % 5),
    d: 14 + ((i * 3) % 6),
  }));
  return (
    <>
      <Stage index={0} count={2}>
        <Box w={L} h={0.8} d={W + 40} color="#d6c39e" />
        {p.canal && <Box w={L * 0.95} h={1} d={W * 0.18} color="#65888A" />}
        {p.canal && <Cyl r={W * 0.35} h={1.2} color="#65888A" seg={8} />}
        {p.canal && <Cyl r={W * 0.2} h={1.6} color="#7fa0a2" seg={8} />}
      </Stage>
      <Stage index={1} count={2}>
        {shops.map((s, i) => (
          <group key={i}>
            <Box w={shopL - 1.5} h={s.h} d={s.d} x={s.x} z={W / 2 + s.d / 2} color={i % 3 === 0 ? shade(p.color, 0.08) : p.color} />
            <Box w={shopL - 1.5} h={s.h + ((i * 5) % 4)} d={s.d} x={s.x} z={-W / 2 - s.d / 2} color={i % 4 === 1 ? shade(p.color, -0.06) : p.color} />
            <Box w={shopL - 0.9} h={0.8} d={s.d + 0.6} x={s.x} y={s.h} z={W / 2 + s.d / 2} color={p.roofColor} />
            <Box w={shopL - 0.9} h={0.8} d={s.d + 0.6} x={s.x} y={s.h + ((i * 5) % 4)} z={-W / 2 - s.d / 2} color={p.roofColor} />
          </group>
        ))}
      </Stage>
    </>
  );
}

import * as THREE from "three";
const dummy = new THREE.Object3D();
function placeInstances(m: THREE.InstancedMesh, pts: [number, number][], h: number) {
  pts.forEach(([x, z], i) => {
    dummy.position.set(x, h / 2, z);
    dummy.rotation.set(0, -Math.atan2(z, x), 0);
    dummy.updateMatrix();
    m.setMatrixAt(i, dummy.matrix);
  });
  m.instanceMatrix.needsUpdate = true;
}
