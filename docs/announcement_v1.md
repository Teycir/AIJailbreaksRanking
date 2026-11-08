# v1.0 Launch & Community Announcement Kit

Ready-to-use announcements highlighting the core differentiator of AIJailbreaksRanking: **substance scoring vs. the 96% → 2.7% evaluator illusion**.

---

## 1. X (Twitter) Thread

**Tweet 1 (Hook):**
Most published LLM jailbreak papers report 90%+ Attack Success Rates (ASR).
Almost all of them collapse to near zero under rigorous evaluation.

Here is why: translating a malicious prompt into a low-resource language scored 96.0% ASR on GPT-4 under keyword-matching.
Under substance scoring (checking if actionable harm was actually produced)?

**2.7%.**

That’s why we built **AIJailbreaksRanking**: https://github.com/Teycir/AIJailbreaksRanking 🧵👇

**Tweet 2 (The Problem):**
Standard benchmarks often use refusal-detection judges that check if "I cannot" or "As an AI" is absent.
If a model outputs: *"Sure! The history of lockpicking is fascinating..."* and produces nothing actionable, keyword judges score it as a 100% successful jailbreak.
StrongREJECT and HarmBench proved how pervasive this illusion is.

**Tweet 3 (The Ranking Standard):**
AIJailbreaksRanking is an evidence-graded, living catalog of LLM jailbreak techniques:
- **Tier A (Reliable now):** Survives substance-aware evaluation, reproducible across frontier targets (Crescendo, BoN, LRM Agent Persuasion).
- **Tier B (Conditional):** High ASR only under strict preconditions (prefill, multi-turn, grammar control).
- **Tier C (Historical/Heuristic):** Heuristic or patched on modern models.
- **Tier D (Discarded):** Benchmark artifacts and non-transferable techniques with recorded failure proof.

**Tweet 4 (Built for Agents and Researchers):**
No fluff. Every entry has:
- A stable slug and JSON record (`data/techniques.json`)
- Clean machine-readable `llms.txt` and flat summary CSV
- Primary literature citations with sample sizes ($N$) and evaluator types
- 3 harmless worked examples per entry
- Actionable defense mappings (`docs/defenses.md`)

**Tweet 5 (Call to action):**
If you red-team LLMs, build safety guardrails, or research alignment:
⭐ Star the repo: https://github.com/Teycir/AIJailbreaksRanking
Propose candidates or challenge grades via our structured issue templates!

---

## 2. LinkedIn Post

**Headline:** Why a "96% success rate" LLM jailbreak actually achieved only 2.7% — and why we need substance scoring in AI Red Teaming.

In AI security research, we frequently see pre-prints claiming >90% Attack Success Rates (ASR) against frontier models like GPT-4, Claude 3.5, and Gemini.

Yet red teams trying to operationalize these attacks often find they don't work. Why the discrepancy?

The culprit is **evaluator methodology**.

When a paper evaluates jailbreaks by simply checking whether the model omitted canned refusal phrases (e.g., "I'm sorry, but I cannot..."), any polite or evasive deflection is scored as a successful compromise.

A stark example:
Low-resource language translation was reported at **96.0% ASR** against GPT-4 under refusal-detection metrics. When re-evaluated using substance-aware rubrics (evaluating whether actionable, harmful substance was emitted), the actual success rate dropped to **2.7%**.

To bring rigor and transparency to this space, I've open-sourced **AIJailbreaksRanking**:
👉 https://github.com/Teycir/AIJailbreaksRanking

Key highlights:
1. **Evidence-based Tiers (A through D):** Techniques are graded by whether they hold up under substance scoring (StrongREJECT / HarmBench class) and transfer across model families.
2. **Discard Discipline:** Failed or non-transferring techniques (like GCG suffixes or translation ciphers) are kept in Tier D with transparent autopsy notes, so teams stop wasting time testing dead ends.
3. **Defense-Oriented:** Every entry documents the specific countermeasure that works (whole-transcript judges, immutable system suffixes, sampling budget limits).
4. **Machine-Readable:** Structured schema, `llms.txt`, and flat CSV export for security agents and automated pipelines.

If you are an AI red teamer, ML engineer, or AI safety evaluator, explore the repository and let me know your thoughts!

---

## 3. Reddit Post (for r/netsec, r/LocalLLaMA, r/MachineLearning)

**Title:** AIJailbreaksRanking: An evidence-graded catalog of LLM jailbreak techniques (filtering out keyword-match artifacts)

**Body:**
Hey everyone,

If you track LLM security papers, you've likely noticed that every week a new paper claims 90%+ jailbreak success on frontier models. But when you test them, they often produce benign filler or fail behind basic guardrails.

The core reason is **evaluator choice**:
- Keyword / binary refusal judges check if "I cannot" is absent.
- Substance-aware judges (e.g., StrongREJECT, HarmBench rubrics) check whether actionable, harmful information was actually generated.

A classic paper claimed **96.0% ASR** for low-resource language translation. Under substance scoring, it collapsed to **2.7%**.

We built **AIJailbreaksRanking** to solve this:
Repository: https://github.com/Teycir/AIJailbreaksRanking

### How it's structured:
- **Tier A (Reliable now):** Only techniques that survive substance scoring and transfer across model families (e.g., Crescendo, LRM agent persuasion, Best-of-N sampling).
- **Tier B (Reliable under precondition):** Requires specific primitives like assistant-turn prefill (Sockpuppetting) or constrained decoding / JSON schema control (EnumAttack/DictAttack).
- **Tier C (Historical / Heuristic):** Degraded on current frontier models (Many-Shot, DAN, puzzle games).
- **Tier D (Discarded):** Documented failures kept as negative controls (GCG token suffixes, base64/cipher, translation).

### Features:
- Fully typed JSON Schema (`data/schema.json`) + flat summary CSV (`data/techniques-summary.csv`)
- Flat `llms.txt` and `AGENTS.md` for AI agent consumption
- Mapped defenses (`docs/defenses.md`): what actually works vs. what fails
- CLI query tool: `python3 scripts/query.py --tier A --csv`
- CI validation enforcing strict metadata and evidence consistency

Looking for feedback and community contributions!
