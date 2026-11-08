import React from "react";
import {
  AbsoluteFill,
  Sequence,
  interpolate,
  Easing,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { loadFont as loadSerif } from "@remotion/google-fonts/InstrumentSerif";
import { loadFont as loadMono } from "@remotion/google-fonts/IBMPlexMono";

const serif = loadSerif("normal", { weights: ["400"], subsets: ["latin"] }).fontFamily;
const mono = loadMono("normal", { weights: ["400", "500"], subsets: ["latin"] }).fontFamily;

const C = {
  bg: "#08090A",
  fg: "#F2F0EA",
  muted: "#8B8B84",
  accent: "#D8FF3E",
  line: "rgba(242,240,234,0.14)",
  faint: "rgba(242,240,234,0.085)",
};

const M = 110; // page margin

const fade = (f: number, start: number, dur = 16) =>
  interpolate(f, [start, start + dur], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
  });

const rise = (f: number, fps: number, delay: number) =>
  spring({ frame: f - delay, fps, config: { damping: 200, mass: 0.7, stiffness: 90 } });

const Label: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({
  children,
  style,
}) => (
  <div
    style={{
      fontFamily: mono,
      fontSize: 20,
      letterSpacing: "0.22em",
      textTransform: "uppercase",
      color: C.muted,
      ...style,
    }}
  >
    {children}
  </div>
);

/** Clipped line reveal: text slides up from behind a mask. */
const Reveal: React.FC<{
  children: React.ReactNode;
  progress: number;
  style?: React.CSSProperties;
}> = ({ children, progress, style }) => (
  <div style={{ overflow: "hidden", ...style }}>
    <div
      style={{
        transform: `translateY(${(1 - progress) * 105}%)`,
      }}
    >
      {children}
    </div>
  </div>
);

const Grain: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none", opacity: 0.055, mixBlendMode: "overlay" }}>
    <svg width="100%" height="100%">
      <filter id="grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch" />
      </filter>
      <rect width="100%" height="100%" filter="url(#grain)" />
    </svg>
  </AbsoluteFill>
);

const Grid: React.FC<{ opacity: number }> = ({ opacity }) => (
  <AbsoluteFill style={{ opacity }}>
    {[0.2, 0.4, 0.6, 0.8].map((x) => (
      <div
        key={x}
        style={{ position: "absolute", left: `${x * 100}%`, top: 0, bottom: 0, width: 1, background: C.faint }}
      />
    ))}
  </AbsoluteFill>
);

const SceneTitle: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p1 = rise(f, fps, 10);
  const p2 = rise(f, fps, 22);
  const rule = interpolate(f, [52, 84], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });

  return (
    <AbsoluteFill style={{ padding: M }}>
      <div style={{ display: "flex", justifyContent: "space-between", opacity: fade(f, 4) }}>
        <Label>Evidence-graded catalog</Label>
        <Label style={{ color: C.fg }}>17 techniques — 09 recommended</Label>
      </div>

      <div style={{ position: "absolute", left: M, right: M, top: 330 }}>
        <Reveal progress={p1}>
          <div
            style={{
              fontFamily: serif,
              fontSize: 176,
              lineHeight: 0.92,
              letterSpacing: "-0.02em",
              color: C.fg,
            }}
          >
            AI Jailbreaks
          </div>
        </Reveal>
        <Reveal progress={p2} style={{ marginTop: 8 }}>
          <div
            style={{
              fontFamily: serif,
              fontSize: 176,
              lineHeight: 0.92,
              letterSpacing: "-0.02em",
              color: C.fg,
            }}
          >
            Ranking<span style={{ color: C.accent }}>.</span>
          </div>
        </Reveal>
      </div>

      <div
        style={{
          position: "absolute",
          left: M,
          right: M,
          top: 660,
          height: 1,
          background: C.line,
          transform: `scaleX(${rule})`,
          transformOrigin: "left center",
        }}
      />
      <div style={{ position: "absolute", left: M, bottom: M, opacity: fade(f, 66) }}>
        <Label style={{ color: C.fg, letterSpacing: "0.18em" }}>
          Substance-scored · never keyword-matched
        </Label>
      </div>
    </AbsoluteFill>
  );
};

const TIERS = [
  { tier: "A", count: 3, label: "Reliable now", accent: true },
  { tier: "B", count: 6, label: "Under precondition" },
  { tier: "C", count: 5, label: "Historical / heuristic" },
  { tier: "D", count: 3, label: "Discarded, on record" },
];

const SceneTiers: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const maxBar = 560;

  return (
    <AbsoluteFill style={{ padding: M }}>
      <div style={{ display: "flex", justifyContent: "space-between", opacity: fade(f, 2) }}>
        <Label>01 — Tier distribution</Label>
        <Label>n = 17</Label>
      </div>

      <div style={{ position: "absolute", left: M, right: M, top: 250 }}>
        {TIERS.map((t, i) => {
          const p = spring({
            frame: f - 14 - i * 7,
            fps,
            config: { damping: 200, mass: 0.8, stiffness: 70 },
          });
          const shown = Math.round(interpolate(p, [0, 1], [0, t.count]));
          const w = (t.count / 6) * maxBar * p;
          return (
            <div
              key={t.tier}
              style={{
                display: "flex",
                alignItems: "center",
                height: 132,
                borderTop: i === 0 ? `1px solid ${C.line}` : "none",
                borderBottom: `1px solid ${C.line}`,
              }}
            >
              <div
                style={{
                  fontFamily: serif,
                  fontSize: 76,
                  width: 110,
                  color: t.accent ? C.accent : C.fg,
                  opacity: 0.45 + 0.55 * p,
                  lineHeight: 1,
                }}
              >
                {t.tier}
              </div>
              <div style={{ flex: 1 }}>
                <div
                  style={{
                    fontFamily: mono,
                    fontSize: 21,
                    letterSpacing: "0.18em",
                    textTransform: "uppercase",
                    color: t.accent ? C.fg : C.muted,
                    marginBottom: 18,
                    opacity: p,
                  }}
                >
                  {t.label}
                </div>
                <div style={{ height: 8, background: C.faint, width: maxBar }}>
                  <div
                    style={{
                      height: "100%",
                      width: w,
                      background: t.accent ? C.accent : "rgba(242,240,234,0.55)",
                    }}
                  />
                </div>
              </div>
              <div
                style={{
                  fontFamily: mono,
                  fontSize: 56,
                  width: 120,
                  textAlign: "right",
                  color: t.accent ? C.accent : C.fg,
                  fontVariantNumeric: "tabular-nums",
                }}
              >
                {shown}
              </div>
            </div>
          );
        })}
      </div>

      <div style={{ position: "absolute", left: M, bottom: M, opacity: fade(f, 78) }}>
        <Label>Default when uncertain: C — inflation costs more than omission</Label>
      </div>
    </AbsoluteFill>
  );
};

const SceneThesis: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const strike = interpolate(f, [28, 56], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  const dropP = rise(f, fps, 58);

  return (
    <AbsoluteFill style={{ padding: M }}>
      <div style={{ display: "flex", justifyContent: "space-between", opacity: fade(f, 2) }}>
        <Label>02 — Why the filter exists</Label>
        <Label style={{ color: C.muted }}>low-resource-language attack</Label>
      </div>

      <div
        style={{
          position: "absolute",
          left: M,
          right: M,
          top: 300,
          display: "flex",
          alignItems: "baseline",
          gap: 48,
        }}
      >
        <div style={{ position: "relative" }}>
          <div
            style={{
              fontFamily: serif,
              fontSize: 210,
              lineHeight: 1,
              color: C.muted,
              fontVariantNumeric: "tabular-nums",
            }}
          >
            96.0%
          </div>
          <div
            style={{
              position: "absolute",
              left: -8,
              right: 8,
              top: "52%",
              height: 6,
              background: C.fg,
              transform: `scaleX(${strike})`,
              transformOrigin: "left center",
            }}
          />
        </div>

        <div style={{ fontFamily: mono, fontSize: 48, color: C.muted, opacity: strike }}>
          →
        </div>

        <div
          style={{
            fontFamily: serif,
            fontSize: 210,
            lineHeight: 1,
            color: C.accent,
            opacity: dropP,
            transform: `translateY(${(1 - dropP) * 40}px)`,
          }}
        >
          2.7%
        </div>
      </div>

      <div style={{ position: "absolute", left: M, top: 610, opacity: fade(f, 52) }}>
        <Label style={{ color: C.fg, fontSize: 22, letterSpacing: "0.16em" }}>
          Keyword-match ASR → substance-scored ASR · same model, same responses
        </Label>
      </div>

      <div style={{ position: "absolute", left: M, bottom: M, maxWidth: 980, opacity: fade(f, 80) }}>
        <div style={{ fontFamily: mono, fontSize: 24, lineHeight: 1.6, color: C.muted }}>
          An evaluator change alone moves a technique between state of the art and
          discarded. Tier D exists to keep that on the record.
        </div>
      </div>
    </AbsoluteFill>
  );
};

const SceneEnd: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p1 = rise(f, fps, 4);
  const p2 = rise(f, fps, 14);
  const caret = Math.floor(f / 16) % 2 === 0 ? 1 : 0;

  return (
    <AbsoluteFill style={{ padding: M }}>
      <div style={{ position: "absolute", left: M, right: M, top: 330 }}>
        <Reveal progress={p1}>
          <div
            style={{
              fontFamily: serif,
              fontSize: 118,
              lineHeight: 1.02,
              letterSpacing: "-0.015em",
              color: C.fg,
            }}
          >
            Read the filter,
            <br />
            not the list<span style={{ color: C.accent }}>.</span>
          </div>
        </Reveal>
      </div>

      <div style={{ position: "absolute", left: M, bottom: 210, opacity: fade(f, 30) }}>
        <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <div style={{ fontFamily: mono, fontSize: 40, color: C.fg }}>
            github.com/Teycir/AIJailbreaksRanking
          </div>
          <div style={{ width: 12, height: 40, background: C.accent, opacity: caret }} />
        </div>
      </div>

      <div style={{ position: "absolute", left: M, right: M, bottom: M, display: "flex", justifyContent: "space-between", opacity: fade(f, 46) }}>
        <Label>MIT · schema-validated · corrections in CHANGELOG</Label>
        <Label style={{ color: C.fg }}>v1.2.0</Label>
      </div>
    </AbsoluteFill>
  );
};

export const Video: React.FC = () => {
  const f = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: C.bg }}>
      <Grid opacity={0.9} />

      <Sequence from={0} durationInFrames={150}>
        <SceneTitle />
      </Sequence>
      <Sequence from={150} durationInFrames={210}>
        <SceneTiers />
      </Sequence>
      <Sequence from={360} durationInFrames={140}>
        <SceneThesis />
      </Sequence>
      <Sequence from={500} durationInFrames={100}>
        <SceneEnd />
      </Sequence>

      <Grain />

      <div
        style={{
          position: "absolute",
          left: 0,
          bottom: 0,
          height: 2,
          width: `${(f / durationInFrames) * 100}%`,
          background: C.accent,
        }}
      />
    </AbsoluteFill>
  );
};
