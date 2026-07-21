# R7C — Phase A read-only reproduction matrix

**Label:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE
**Pass:** R7C (Opus 4.8 requested = surfaced; no substitution)
**Baseline (Smoke A):** 46/46 green from the grandchild branch off PR #9 head `86b8bbd`.
**Method:** deterministic, offline; live topology verified via `gh`; three semantic
tamper probes run against the committed tree and reverted (tree clean after each).

Every finding is a hypothesis to reproduce / partially reproduce / refute / accept.
No repair precedes this matrix.

## Prompt A2 findings (1–19)

| # | Finding | Verdict | Evidence |
|---|---|---|---|
| 1 | zero corpus expressions migrated | **reproduced** | `docs/math-migration-status.yaml`: manuscript/core/companions all `migrated: false` |
| 2 | PDFs retain 26 / 6 notdef glyphs | **reproduced** | core PDF NUL=26, manuscript NUL=6 (pinned in the ledger) |
| 3 | PDF validator *expects* those defects | **reproduced** | `validate_pdf_math.py` asserts `notdef == known_notdef` (26/6) for unmigrated docs |
| 4 | hundreds of formal expressions remain in backticks | **reproduced** | inline-code spans: manuscript **354**, core **390**, multi-actor **14**, neutral companion **35**, Atharī **16** (majority math-like) |
| 5 | gallery target-profile equation ill-typed | **reproduced** | `notation-gallery.md:81` defines `𝒢_{α,A_α} = { x ∈ 𝓜_A ∣ O*(x;A_α) ∈ Π_A }` — a set of **occurrences** `x`, contradicting the registry ("grounded target **profile** set ⊆ Π_{A_α}") |
| 6 | gallery source-syntax prose renders badly | **reproduced** | gallery PDF prose shows leaked ``/`` math-placeholder sentinels (where `$...$` was described) and raw `\vec\mu`/`\vec C` source. Root cause: `_protect_math` protects `$...$` **inside code spans**; R7B visual-QA missed it because it only counted NUL glyphs |
| 7 | math validator ignores a backtick formula | **reproduced** | probe: a new doc with `` `O^*(m; A) = {o in O_A : Inst_A(m,o)}` `` → `validate_math_source.py` PASSES |
| 8 | D5 compares model parameters | **reproduced** | dynamic-orthing doc:75 `θ^CSCG_final ≈ θ^RNN_final` (parameter vectors, not representation geometry) |
| 9 | D6 many-to-many written as a function | **reproduced** | doc:85 `Z_A → Π_A is many-to-many` (function arrow for a relation) |
| 10 | D7 compares a set to a scalar tolerance | **reproduced** | doc:94 `… changes warranted {prediction,…,loss} > ε_A` (set vs scalar) |
| 11 | dynamic validator accepts latent=ortheme | **reproduced** | probe: crosswalk row → "latent model state z_t IS an ortheme by declaration" → `validate_dynamic_orthing.py` PASSES |
| 12 | memetics validator accepts μ̃=metaorthemma | **reproduced** | probe: `μ̃` gloss → "the same object as a case-bound metaorthemma" → `validate_meta_noetic_memetics.py` PASSES |
| 13 | discourse and subject noetic target conflated | **reproduced** | R7 crosswalk types the immediate `m` (this objection/utterance) and treats the interior condition as `O*(m;A)` of that same `m`; no `m_subject`/`m_discourse` split |
| 14 | ecology lacks typed graph semantics | **reproduced** | `DYNAMIC-CROSSWALK.yaml` `Γ^μ` lists node/edge *names* only — no identity/version/timestamp/provenance/status/typed-endpoints/schema |
| 15 | G1 order places hard constraints below ordinary dimensions | **reproduced** | `NOETIC-FIELD-DYNAMICS.yaml` `lexicographic_order` = [disclosure, evidence, dependency, **hard-constraints (4th)**, holds, reduction, closure] |
| 16 | dynamic companion short / no References / not built | **reproduced** | `companion/dynamic-orthing-noetic-learning-and-orthability.md` ≈ 790 words, no References section, absent from `build_pdfs.py` DOCS |
| 17 | Decisions 0023–0025 marked adopted despite candidate | **reproduced** | `decision-status.yaml`: `0023/0024/0025: {status: adopted}` while files say "OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW" |
| 18 | merged state and candidate overlay mixed | **reproduced** | `current-state.yaml` authored as merged R6 (review/signoff pointers R4/R6) yet its derived decision IDs include 0023–0025; historical index calls R7/R7B "current" |
| 19 | OSM citation is a local extraction path | **reproduced** | Decision 0024 / crosswalk cite `opendataloader-output/s41586-024-08548-w.md` — an extraction surface, not a public scholarly citation (DOI 10.1038/s41586-024-08548-w) |

## Refuted / narrowed

- **B4 (Decision 0023 closed on a false provisioning premise): reproduced — the
  audit is correct.** Independently **refuted R7B's premise**: pandoc **3.6.4** was
  downloaded from the official release, `sha256 a9e5feb3d56d2fb0e3e765d1c33b8ee6b72e6963d7de31504edeec8cd1be34b1`,
  extracted, run (`pandoc.exe 3.6.4`), and its **Typst writer** produced valid Typst
  math for the corpus notation. Pandoc **is** deterministically provisionable here;
  Phase H must run a real P1/P2 parity, not decide on PATH availability.
- No audit finding was refuted in the sense of being wrong. One R7B *claim* was
  refuted: "pandoc not provisionable."

## Consequent R7C plan (terminal-status tracked; sequential; no subagents)

B (candidate-state integrity, Decision 0026) → gallery + D5/D6/D7 fixes → semantic
validator hardening (defeat probes 1–3) → C (multi-target noetic, 0027) → D
(represented standards + ecology schema, 0028) → E/F (OSM/dynamic + constrained
descent) → G (companion expansion + PDF) → H (P1/P2 parity + full-corpus migration
+ zero-defect gate) → I (semantic validators + negative corpus) → J (≥12 adversarial)
→ grandchild draft PR. Each item closes terminally (done / changed / deferred /
blocked / unverified); the closeout reports honest statuses, not blanket completion.
