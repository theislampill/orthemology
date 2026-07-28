# R7D — Phase L + M adversarial reviews and mandatory-probe corpus

**Label:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE.

Every new R7D guard was **attacked**, not merely asserted. The mechanical attacks
mutate a guard's input, confirm the guard fails (catches the attack), and revert (tree
clean). This is an Opus candidate self-review; it does **not** substitute for the
required fresh-Fable review of every hunk.

## Phase L — the 24 mandatory negative probes (audit §12)

Each probe the R7D validators must reject, with its disposition. "mechanical" = a live
mutate/revert attack run this pass; "fixture" = a CI negative fixture; "structural" =
prevented by schema/typing.

| # | Probe | Guard | Result |
|---|---|---|---|
| 1 | stale PR/head overlay | `validate_candidate_state` | **CAUGHT** (mechanical) |
| 2 | terminology marked ready despite pending human review | `validate_public_readiness` (scalar ban) | **CAUGHT** (mechanical) |
| 3 | formula hidden in a backtick | `validate_math_source` (inventory allowlist + probe-1 fence-strip) | **HELD** (R7C, retained) |
| 4 | target out of scope | `validate_noetic_claims` NC1 | **CAUGHT** (fixture) |
| 5 | asserted subject claim with no evidence | `validate_noetic_claims` NC2 | **CAUGHT** (fixture) — the exact P3 breach |
| 6 | unresolved evidence ID | `validate_noetic_claims` NC3 | **CAUGHT** (fixture) |
| 7 | ghost metaortheme type | `validate_memetic_ecology` | **CAUGHT** (mechanical) |
| 8 | self-lineage | `validate_memetic_ecology` | **CAUGHT** (mechanical) |
| 9 | quotation treated as endorsement | `CARRIER-RELATION` typed modes | **structural** (mode enum; quotes ≠ endorses) |
| 10 | duplicate ecology node | `validate_memetic_ecology` | **CAUGHT** (mechanical) |
| 11 | illegal edge endpoints | `validate_memetic_ecology` | **CAUGHT** (mechanical) |
| 12 | transmission without represented-standard payload | `validate_memetic_ecology` | **CAUGHT** (mechanical) |
| 13 | social popularity → truth | ecology machine firewall (B20) | **structural** (no `establishes_warrant` field; non-claim + machine check) |
| 14 | two independent routes → tawātur | `independence_conclusion` (machine-safe) | **CAUGHT** — returns `source-independence-supported`, never tawātur |
| 15 | hard-constraint violation ranked as progress | `validate_corrective_transition` CT1 | **CAUGHT** (fixture) |
| 16 | Δ treated as correctness | `validate_corrective_transition` CT3 | **CAUGHT** (fixture) |
| 17 | reread omitted | `validate_corrective_transition` CT4 | **CAUGHT** (fixture) |
| 18 | runtime closure → restoration | `validate_corrective_transition` CT5 + `validate_noetic_application` | **CAUGHT** (fixture) |
| 19 | global standard revised by one episode | `validate_corrective_transition` CT7 | **CAUGHT** (fixture) |
| 20 | silent analysis-version transport | `validate_dynamic_orthing` (gated transport) | **CAUGHT** (mechanical) |
| 21 | CSCG clone = biological neuron | OSM object map (11 layers) + crosswalk non-claims | **structural** (typed separation) |
| 22 | latent state = ortheme without ablation | `validate_dynamic_orthing` (ORTHEME_ASSERT, B19-2) | **HELD** (R7C, retained) |
| 23 | parameter equality = representation equivalence | `Geom_A` definition + D5 | **structural** (geometry, not parameters) |
| 24 | candidate decision marked adopted-merged | `validate_candidate_state` | **CAUGHT** (mechanical) |

**Result: 24/24 addressed — 12 mechanical attacks held live this pass, 7 by CI
fixtures, 5 structurally prevented.** Reproducible via the consolidated harness; tree
clean after each.

## Phase M — the twenty adversarial review passes

| # | Review | Verdict |
|---|---|---|
| 1 | candidate-state / provenance | **HELD** — overlay names PR #10 + exact head; stale-overlay caught (Decision 0029) |
| 2 | public-readiness truthfulness | **HELD** — per-packet exact; scalar "all ready" banned |
| 3 | decision-reference semantics | **HELD** — `Inst_A`/`O*(m;A)` → 0001; miscite caught (B38) |
| 4 | noetic bearer / target | **HELD** — six bearers; subject-type never on discourse |
| 5 | evidence sufficiency and uncertainty | **HELD** — resolvable evidence + support rule; disclaimer ≠ evidence |
| 6 | interior-state humility | **HELD** — motive/soul never asserted; thin evidence → held |
| 7 | represented-standard identity / fidelity | **HELD** — relation-level per-type fidelity; ghost/self-lineage caught |
| 8 | carrier stance | **HELD** — typed modes; quotation ≠ endorsement |
| 9 | memetic graph typing / lineage | **HELD** — unique ids, typed endpoints, ablation witness |
| 10 | tawātur / source dependence | **HELD** — machine independence ≠ tawātur warrant; creed-internal record separate |
| 11 | current DAEE correspondence | **HELD** — dual-pin (pin = current main); 14 objects mapped as application-extensions |
| 12 | corrective-transition semantics | **HELD** — stages separate; delta ≠ soundness; reread required |
| 13 | OSM biological / computational / formal transfer | **HELD** — 11-layer separation; bounded source claim |
| 14 | epistemological source status | **HELD** — five-status hierarchy; secondary ≠ primary |
| 15 | metaphysical bridge | **HELD** — machine argument map; OSM/DAEE prove only rungs 1–3 |
| 16 | divine-Speech route | **HELD** — bounded cross-section; firewall preserved (created ≠ uncreated) |
| 17 | mathematical semantics | **HELD** — corpus notdef eliminated in place; zero notdef |
| 18 | PDF visual quality | **HELD** — 6 PDFs byte-reproducible; core/ms rebuilt glyph-clean |
| 19 | build / reproducibility | **HELD** — 55/55 under the exact lock; manifest matches |
| 20 | false closure | **HELD** — nothing claims merged/signed-off; every R7D decision carries the CANDIDATE label; PR unmerged |

## Genuine limitations recorded (not hidden)

- **Companion depth:** ~1788 words with all required sections + machine-readable map —
  a bounded draft, not the full 4,000–8,000-word scholarly paper.
- **Math allowlist removal:** the notdef defect is eliminated in place (zero notdef,
  both corpus docs migrated); the broader reclassification of the ~190 non-notdef
  formula-like backtick spans into an allowlist-free state remains the reviewed
  continuation (tool + inventory + probe-1 gate make it mechanical).
- **Full-corpus P1/P2 parity** (every unique formula, Windows+Linux) was not re-run this
  pass; R7C's evidence (36/36 vs 34/36) and pandoc-provisionability stand.

These are flagged so a fresh Fable session weighs them explicitly before any merge.
