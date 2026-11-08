# Ranking promo (Remotion)

20 s, 1920x1080, 30 fps. Four hard cuts: wordmark, tier distribution, the
evaluator thesis (96.0% struck through, 2.7%), end card.

```bash
npm install
npm run studio    # live preview at http://localhost:3000
npm run render    # -> out/ranking.mp4
```

Composition `RankingPromo` in `src/Video.tsx`. All numbers and labels are
inlined constants — if the catalog changes, update `TIERS` and the counts in
`src/Video.tsx` (three places) to match `data/techniques.json`.

Fonts: Instrument Serif (display) and IBM Plex Mono (meta), fetched at bundle
time by `@remotion/google-fonts`; both OFL.

Rendered output is committed at `out/ranking.mp4` so the README link works
without a build step.
