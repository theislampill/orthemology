# Pilot 0 — frozen packet protocol (DESIGN-V1)

**Status: READY TO RUN, NOT RUN. No human data collected; no model-utility result exists; nothing here adopts any term.** This packet supersedes the wording of DESIGN-FREEZE-V0 (`../orthemic-terminology-evaluation-spec.md`, frozen hash `ff68084f…67b5`) as a *versioned* superseding design — v0 is immutable history; every v0 rule not amended below carries over. Amendments in v1: (i) a fourth arm **C′** (sham labels); (ii) a fifth construct family, **metaorthemma/binding**; (iii) packet-level freeze hashing over the whole `pilot0/` directory (`FREEZE-HASH.txt`).

## 1. Purpose of Pilot 0

Pilot 0 is a *feasibility and instrumentation* pilot, not an efficacy study. It answers only: are the items unambiguous? do the rubrics score deterministically? are the four arms' renderings semantically matched? are the sham labels matched and interpretable? what are the variance components needed for Pilot 1's simulation-based power? **No adoption/retirement conclusion of any kind may be drawn from Pilot 0.**

## 2. Arms

- **A — ordinary baseline:** no framework language (matched filler reading equalizes exposure time).
- **B — distinctions without neologisms:** the operational distinctions in ordinary words; for the metaorthemma family the ordinary alternatives are rotated across variants: *configuration token*, *instantiated governing configuration*, *bound governing record*.
- **C — coordinated coined vocabulary:** orthemma / ortheme / metaortheme / metaorthemma / orthing, one primer.
- **C′ — sham-label control (MANDATORY in Pilot 0):** the Arm-C primer with every coinage 1:1 substituted by a matched sham label. Role: distinguish (a) benefit of *these specific terms*, (b) benefit of *any concise learnable labels*, (c) benefit of *the distinctions themselves* (Arm B). C′ is mandatory in Pilot 1 if Pilot 0 shows the shams are matched and interpretable; a preregistered secondary control in confirmatory v1 if power permits; never a replacement for the primary A/B/C comparisons.

**Sham-label generation and matching criteria** (all checkable): same count of labels; 1:1 mapping preserving morphological structure (shared stem transformed identically: orth→tarv); syllable count within ±1 of the original; same affix pattern (-emma token / -eme type / meta- prefix / -ing process); no entry in a standard English dictionary and no established technical meaning (documented check per label); pronounceable by the raters' report. Mapping: orthemma→**tarvemma**, ortheme→**tarveme**, metaortheme→**metatarveme**, metaorthemma→**metatarvemma**, orthing→**tarving**. Interpretability gate for Pilot 1: rater comprehension-check accuracy for C′ primer within 10 pp of C's.

- **`orthable` is excluded** from the operational core in every arm (R2 disposition: exploratory in the companion lane only; a separate philosophical-comprehension module would be required to test it and none is justified now).

## 3. Items

`items/ITEMS.json` — for each item: id, construct family, arm-specific renderings (semantically identical scenario; only vocabulary varies), the probe question(s), and the deterministic expected-answer key. Families and counts (≥1 tested item per family in Pilot 0; ≥3 variants per family deferred to Pilot 1):

| Family | Items | Core probe |
|---|---|---|
| occurrence/version identity | P0-ID-1 | does the response detect that the evidence describes a different version/copy? |
| plural profile / candidates | P0-PL-1 | are both independent defects preserved (not collapsed)? is the discriminating test named? |
| pathway vs result (correct-by-luck) | P0-PW-1 | is the right-answer/weak-rule defect detected and the neighboring failure predicted? |
| false closure | P0-FC-1 | is the completion claim rejected against the undisposed residual? |
| governing-rule revision | P0-RR-1 | is the recurring class attributed to the rule, not the instances? |
| **metaorthemma / binding (new in v1)** | P0-MB-1 | correct general standard + defective case-specific binding + faithful execution + luckily correct result: does the response localize the defect to the *binding* (wrong reference plane/stale calibration), not the standard, the procedure, or the executor? |
| multi-actor separation | P0-MA-1 | are shared occurrence / actor-relative target / current profile / objective / policy kept apart? |
| negative controls | P0-NC-1, P0-NC-2 | single-fault trivial cases: near-zero added overhead in every arm (guard endpoint) |

## 4. Scoring, adjudication, contamination, pinning

- **Rubrics:** `rubrics/SCORING-RUBRICS.md` — deterministic keys per probe; every endpoint scored 0/1 against explicit criteria; compression measured as token counts among accuracy-matched responses with primer cost amortized (v0 B.8 rule).
- **Adjudication:** `rubrics/ADJUDICATION-MANUAL.md` — tie-break and edge-case procedure; disagreements resolved by the written rule, never by discussion-to-consensus without a recorded rule change (which is a deviation).
- **Contamination/carryover plan:** fresh context per item for model executors; between-subject rater assignment across arms (a rater who has seen the C or C′ primer never scores A/B comprehension endpoints); Latin-square item order; early-vs-late drift reported.
- **Model-version pinning template** and **run manifest schema:** `RUN-MANIFEST.schema.json` — model IDs, decoding parameters, dates, packet freeze hash, per-run seeds where the API exposes them.
- **Deviation ledger:** `DEVIATION-LEDGER.md` — any departure from this packet is logged against `FREEZE-HASH.txt` before analysis.
- **Analysis skeleton:** `analysis/analyze_pilot0.py` — parsing, rubric application, variance-component summaries; deterministic; runnable today against synthetic transcripts (smoke-tested); produces NO efficacy verdicts by construction.

## 5. What Pilot 0 may conclude

Feasibility findings only: item ambiguity fixes; rubric determinism failures; sham matching; variance components. Model self-scoring is never treated as evidence of term utility. Any wording change to items/rubrics after freeze is a new packet version with a new hash.
