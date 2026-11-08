# Candidates Under Review & Nomination for Tier A

This tracker lists jailbreak techniques currently under community observation or undergoing replication for potential inclusion or tier promotion.

To propose a candidate or challenge a grade without opening a PR, open a discussion in GitHub Discussions or file an issue using the [Technique Proposal Template](https://github.com/Teycir/AIJailbreaksRanking/issues/new?template=new_technique.yml).

---

## Promotion Criteria for Tier A

To reach **Tier A (Reliable now)**, a technique must meet all five gates:

1. **Substance-aware evaluation:** Scored with StrongREJECT, HarmBench rubrics, or manual expert harm evaluation. Keyword-match ("I cannot" absence) is disqualifying.
2. **Defense robustness:** Must retain measurable bypass ability when tested against active guardrails (e.g., LlamaGuard, NeMo Guardrails, representation-level circuit breakers).
3. **Black-box access:** Operates over standard user-facing inference APIs (no white-box logits, activation steering, or teacher-forcing required).
4. **Multi-family transfer:** Empirically verified on at least two independent frontier model families (e.g., OpenAI GPT-4o / o1, Anthropic Claude 3.5 / 3.7, Google Gemini 1.5 / 2.5).
5. **Independent replication:** Confirmed by parties outside the original paper's author group.

---

## Active Watchlist & Candidates

| Candidate / Variant | Class | Initial Claim | Current Assessment | Missing Gate |
|---|---|---|---|---|
| **CodeChameleon** | formatting / AST | 86.6% on GPT-4 (author-reported) | Heuristic transformation; degrades significantly behind intent classifiers. | Needs substance-aware independent replication across frontier targets. |
| **ArtPrompt** | ASCII art obfuscation | High on GPT-4 / Claude | Vision / multi-modal models parse the text cleanly; high heuristic signature. | Fails against multi-modal judges; heuristic pattern easily classified. |
| **AutoDAN / PAIR variants** | automated search | High query efficiency in older benchmarks | Evaluated primarily against older alignment baselines (Llama-2, GPT-3.5). | Current frontier alignment raises queries-to-success; sits in Tier B. |
| **Context-Aware Multi-turn (Crescendomation variants)** | multi-turn | >95% automated | Variants of Crescendo with automated turn budgeting. | Under observation for whether automated versions hold up without human-in-the-loop adaptation. |

---

## How to Submit Evidence

When submitting replication evidence for any candidate above:
- State exact target model and date tested (e.g., `gpt-4o-2024-08-06`).
- Provide sample size ($N \ge 50$ preferred).
- Disclose evaluator implementation (HarmBench rubric prompt, StrongREJECT evaluator script, or judge model).
- Note temperature and top-p settings used.
