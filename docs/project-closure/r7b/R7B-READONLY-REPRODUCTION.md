# R7B — Phase A3: dynamic-depth read-only reproduction

**Label:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE
**Pass:** R7B (Opus 4.8 requested = surfaced; no substitution)
**Baseline suite:** 40/40 green from clean checkout at PR #8 head `b053860`.
**DAEE read-only at pinned commit** `c86b3c6673147b8802fe222373a165a37d4d24a8`
(verified present in the local daee working tree; `c86b3c6 docs: clarify
post-release v0.4.5.0 provenance check`).
**OSM source:** `opendataloader-output/s41586-024-08548-w.md` (Sun et al.,
*Learning produces an orthogonalized state machine in the hippocampus*, Nature 2025).

Every finding is treated as a hypothesis to reproduce / partially reproduce /
refute / accept as a limitation. No repair was performed before this report.

## Finding matrix

| # | Audit finding | Verdict | Evidence at the pin / in the tree |
|---|---|---|---|
| §2 | R7 improved the DAEE ontology but not its **dynamics**; meta-noetic memetics is one short section + one crosswalk row | **reproduced** | `applications/daee-epistemics/NOETIC-ORTHING-APPLICATION.md` §5 is a single paragraph mapping memetics to "metaortheme versioning + cross-episode transport + recurrence-triggered revision + impact-scoped reopening … no new primitive." `DAEE-ORTHEMOLOGY-CROSSWALK.yaml` has exactly one memetics row (`mapping_type: application-extension`). |
| §2.1 | a **represented-standard bearer `μ̃_{α,t}`** is missing | **reproduced** | grep of `applications/daee-epistemics/` for `mu-tilde` / `μ̃` / "represented standard" returns nothing. The package has `μ` (metaortheme type) and `μ̄` (case-bound metaorthemma) only. "A standard propagates / is inherited / mutates" is currently forced onto episode-local `μ̄`, which cannot persist across episodes/actors. |
| §2.2 | carrier / content / governing-rule / application are not separated (a phrase can be orthemma + orthemes + `μ̃` + candidate `μ` + `μ̄` + episode-trace at once) | **reproduced** | No multi-role carrier analysis exists in the R7 package; §3 discusses deformation-placement typing but not a single carrier occupying several object classes under different analyses. |
| §2.3 | memetics is an **ecology `Γ^μ_t`** (typed graph of actors/institutions/artifacts/standards with transmission/mutation/… edges), not a version history | **reproduced** | No graph/ecology structure is present. The three histories the audit names — of the metaortheme *type*, of its *represented versions*, of its case-bound *tokens* — are not distinguished. |
| §3 | DAEE uses gradient/field vocabulary but its own notes bound it; needs G0/G1/G2 adjudication; R7 does not analyze it | **reproduced** | At the pin, `docs/algebraic-notation-and-noetic-formalism.md:61` types `∇` as a "Route-ranking functional … **Not literal physical gradient**, truth metric, warrant proof, or gate bypass"; lines 62–63 bound `∇·`/`∇×` as diagnostics "**not literal divergence/curl unless a rigorous target space is later defined**." The field-gradient audit `docs/audits/v0.4.1.0-field-gradient-loop-closure-coupling-implementation-audit.md:11` calls `∇` "route-gradient **pressure** over eligible live … fields" and line 77 disclaims "literal mathematical performance." DAEE already sits at **G1**; R7 contains no such adjudication. |
| §3.1 | four states must stay separate (actual noetic condition / inferred profile / runtime state / released action) | **reproduced (already partly held)** | R7 `NOETIC-ORTHING-APPLICATION.md` §2 already separates concrete engagement ≠ observed discourse ≠ candidate profiles ≠ `Ψᴵ` ≠ actual interior ≠ released response ≠ uptake. What is missing is the explicit **social/metaorthemic propagation field** as a fifth state and the descent semantics over them. |
| §3.2 | raw burden-count is not a sound potential (discovery can *raise* the ledger while improving position) | **reproduced (gap)** | No burden functional exists in the R7 package; there is nothing yet to make anti-gaming. This is a to-build, not a defect in existing code. |
| §3.3 | fiṭrah is not one coordinate / metaortheme / algorithm / measured scalar; "minimum-entropy attractor" stays provisional/creed-internal | **reproduced (accepted limitation)** | Consistent with the pinned DAEE stance; R7 does not over-claim it, but also does not yet state the boundary. To be stated in Phase F. |
| §4 | Decision 0015 is a static boundary, not a theory of **dynamic orthing / learning** | **reproduced** | `docs/decisions/0015-…` + `docs/related-work/LATENT-STATE-INFERENCE-AND-ORTHEMOLOGY.md` + `examples/latent-state-sensory-aliasing.md` distinguish occurrence ≠ latent state ≠ observation ≠ posterior ≠ representation ≠ inferred profile, and refuse to define orthemes by orthogonality — but contain **no update architecture** (episode inference vs model learning vs metaortheme revision vs analysis-version change). |
| §4 | OSM reported structure (decorrelation → orthogonalized state machine; CSCG reproduces endpoint *and* trajectory; altered-cue adaptation) | **reproduced from source** | Abstract + Results: "progressive decorrelations … ultimately resulting in orthogonalized representations resembling a state machine"; "the clone-structured causal graph … uniquely reproduced both the final orthogonalized states and the learning trajectory"; LSTM/transformers/vanilla RNNs "did not naturally" produce them; "flexible adaptations of the OSM in altered task conditions." |
| §4.5 | current "OSM provides *no support*, purely one-way" is **too categorical** | **partially reproduced → repair as "external exemplification and constraint"** | The R7 latent-state notes correctly refuse validation, but the audit is right that "no support at all" understates it: OSM legitimately supplies an independent example that observation/state separation and endpoint-underdetermines-mechanism *must be representable*. Reclassify (Phase D5), still **not validation**. |
| §5 | epistemology needs a deeper dynamic layer (faculty/represented-standard/metaorthemma/execution/result/truth-linkage; tawātur vs memetic propagation; mental/external anti-reification) | **reproduced (gap)** | The companion treats static evaluability; the false-tawātur / source-independence machinery the audit wants is exactly what `Γ^μ_t` would supply. To build in Phases E/G. Scholarship (`Ibn Taymiyyah's Epistemology.md`, El-Tobgui dissertation) is **secondary reconstruction**, not primary evidence. |
| §6 | **dynamic orthability** is a candidate extension, not a new proof; must not entail guaranteed learnability/convergence/one-gradient/created-truth/the metaphysical bridge | **reproduced (accepted scope)** | The static-orthability companion exists; the dynamic question ("what must reality be like for error to be discoverable and standards revisable without the learner creating truth?") is not yet posed. To build in Phase G, explicitly bounded. |

## Refuted / not-accepted

- **None of the audit's substantive findings were refuted.** One is *narrowed*:
  §4.5's implicit request to grant OSM more evidential weight is bounded to
  "external exemplification and constraint" — it must **not** become validation of
  the theory, its terminology, human noetics, or the metaphysical bridge.
- The audit does **not** ask to reopen the settled core (Decisions 0001–0022) or to
  change FCSP-2/ER-2 scientific status; this pass preserves both. FCSP-2/ER-2 and the
  historical packets re-ran green in the baseline suite.

## Consequent Phase plan (bounded, application-level, no new school-neutral primitive unless anti-vacuity forces one)

- **B/C** — math-source & typesetting pipeline (Decision 0023) + migration + PDF repair + `validate_math_source.py` / `validate_pdf_math.py` + notation gallery.
- **D** — dynamic-orthing / latent-state learning extension (Decision 0024): four update levels, world-vs-learner edges, ortheme-admission-by-ablation, OSM claim-status, diagrams.
- **E** — meta-noetic memetics (Decision 0025): `μ̃_{α,t}` bearer, carrier analysis, `Γ^μ_t` ecology, memetic modes, fixtures N11–N20.
- **F** — sound-descent / noetic-field adjudication: G0/G1/G2, anti-gaming burden functional, fiṭrah boundary; recommend **G1**.
- **G** — epistemological/metaphysical placement: dynamic orthability + metaphysical ladder + anti-reification.
- **H** — project layer map. **I** — experiment-packet regression (no run). **J** — ≥10 adversarial passes.

All of the above is delivered as an **Opus candidate** on the child draft PR; a fresh
Fable session reviews and performs the protected merges.
