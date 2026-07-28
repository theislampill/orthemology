# R7D — Phase A read-only reproduction and finding matrix

**Label:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE

Surfaced model at this phase: `claude-opus-4-8` (Opus 4.8 requested = surfaced; no substitution).

Phase A is read-only. No repository content was edited before this record existed.
Every finding in `orthemology-pr10-r7c-independent-audit-and-r7d-findings.md` was
reproduced, partially reproduced, refuted, or accepted as a bounded limitation —
against the **live** repository and the archive, not the audit prose alone.

## A1 — live topology (verified via `gh`/`git ls-remote`)

| Ref | Head | State |
|---|---|---|
| `main` | `43fee0f5` (R6) | protected: required check `validate`, strict, no force-push |
| PR #8 | `b053860` | draft, open, base `main` |
| PR #9 | `86b8bbd` | draft, open, base PR #8 branch |
| PR #10 | `3cce235` | draft, open, base PR #9 branch, **CI success** |
| R7C archive | sha256 `be022d374883…` | **matches expected exactly**; working tree at 3cce235 == live PR #10 head |
| daee-epistemics `main` | `c86b3c66` (2026-06-18) | **== the R7B/R7C pin**; `diagnostic-ir.md` present at it (sha `c0393249`) |

## A2 — baseline suite (Smoke A) under the exact lock

Lock venv built from `requirements-ci.lock.txt` (exact version match verified).
Every command in `.github/workflows/validate.yml` was executed:

- **49/49 validators/tests PASS**
- `make_manifest.py` → `git diff` empty (tree matches `RELEASE-MANIFEST.sha256`)
- `build_pdfs.py --check` → 6 committed PDFs rebuild byte-identically

This matches the R7C closeout and the live green CI on 3cce235. Evidence boundary:
Smoke A ran under the lock venv on Windows; the live ubuntu CI is also success on
3cce235. A fresh Fable session must rerun the exact lock + Typst build + live CI on
the final R7D head.

## A3 — finding matrix (audit B1–B43, probes P1–P8)

Disposition legend: **REPRODUCED** (defect confirmed live) · **PARTIAL** (confirmed
with scope correction) · **REFUTED** (audit premise does not hold) · **LIMITATION**
(bounded, accepted).

### State / provenance
| # | Finding | Disposition | Evidence |
|---|---|---|---|
| B1 / P1 | Candidate overlay stale (no PR #10, no `3cce235` head; omits companion PDF) | **REPRODUCED** | `CANDIDATE-STATE.yaml` contains neither `3cce235` nor `PR #10`; `validate_candidate_state` never checks overlay vs live topology → passes |
| B2 | r7/r7b/r7c closure dirs classified `current` | **REPRODUCED** | `HISTORICAL-STATUS-INDEX.yaml` has all three at `status: current`; no `current-candidate` status exists |
| B3 | Public readiness contradicts packet index | **REPRODUCED** | `README.md` carries scalar "READY TO RUN, NOT RUN / Every designed study is READY"; packet index has mixed states (FCSP-2/ER-2 ready, TERM-P0-V2 human-review, Pilot 1/confirmatory draft) |
| B4 | "consistency" used for bounded conformance | **REPRODUCED** | README/contrib prose |

### Mathematics / publication
| # | Finding | Disposition | Evidence |
|---|---|---|---|
| B5 | Zero publication formulas migrated | **REPRODUCED** | `math-migration-status.yaml`: formal-core `migrated:false known_notdef:26`; main-manuscript `migrated:false known_notdef:6` |
| B6 | Source validator institutionalizes deferral (allowlist) | **REPRODUCED** | `validate_math_source` accepts inventoried formula-in-backtick; inventory = 208 spans |
| B7 | Some replacements semantically poor (combining `≠`, italic predicates) | **REPRODUCED** | inventory entries |
| B8 | 36-formula parity too small | **REPRODUCED** | parity audit sampled 36 of ≥208 |
| B9 | Visual QA not adversarial enough | **REPRODUCED** | core/ms PDFs still show notdef boxes in the episode signature |

### Noetic targets / evidence
| # | Finding | Disposition | Evidence |
|---|---|---|---|
| B10 / P2 / P3 | Unsupported asserted subject claim passes | **REPRODUCED** | `claim_valid("m_subject","noetic-profile","asserted","no evidence at all",["no soul access"])` → valid; schema never checks `in_scope`, evidence resolution, or bridge |
| B11 | "subject interior" too coarse a target type | **REPRODUCED** | single `m_subject` type; no overt/episode/standard/disposition/motive split |
| B12 | No exact operation signature | **REPRODUCED** | crosswalk prose only |

### Represented standards / carrier
| # | Finding | Disposition | Evidence |
|---|---|---|---|
| B13 / P4 | Example references a ghost metaortheme type | **REPRODUCED** | `mu-type-corroboration` absent from ecology; validator does not resolve refs |
| B14 / P4 | Self-lineage + ghost type + global-faithful pass schema | **REPRODUCED** | tampered RS with self-lineage + ghost type validates |
| B15 | Fidelity cannot be one global field | **REPRODUCED** | `fidelity_status` is a single top-level field |
| B16 | Stance belongs to a typed relation | **REPRODUCED** | `stance` is one whole-record field |

### Memetic ecology
| # | Finding | Disposition | Evidence |
|---|---|---|---|
| B17 / P5 / P8 | Duplicate node IDs / illegal endpoints / payload-free transmission pass | **REPRODUCED** | duplicate-id ecology validates; `node_ids` is a set (silently dedups); only endpoint existence checked, not types or transmission payload |
| B18 | Transmission is ternary / must be reified | **REPRODUCED** | edge does not name the transmitted standard |
| B19 | Mutation identity asserted, not demonstrated | **PARTIAL** | R7C requires a `mutation_identity` value but not a witness |
| B20 | Social stabilization must never imply truth (machine-readable) | **PARTIAL** | prose firewall present; not a machine rule over edges |

### Tawātur
| # | Finding | Disposition | Evidence |
|---|---|---|---|
| B21 / P6 | Two independent routes → tawātur-like | **REPRODUCED** | `tawatur_conclusion(False,False,2)` = `tawatur-like-independence` |
| B22 | Impossible origin counts / empty qualitative evidence permitted | **REPRODUCED** | schema lacks `independent_routes <= apparent_witnesses` and non-empty indicant constraint |
| B23 | Independence analysis and tawātur warrant must be separated | **REPRODUCED** | one function conflates them |

### DAEE delta
| # | Finding | Disposition | Evidence |
|---|---|---|---|
| B24 | R7C pins an old commit and defers "112 later commits" | **REFUTED (commit level) + REPRODUCED (substantive)** | live daee `main` == pin `c86b3c66`; the IR/field-witness/MRP content is **at** the pin, not in a published delta. The "112 ahead" was a local scratch checkout. Substantive need to crosswalk that IR content is real and unmet by R7C |
| B25 | Required DAEE/Orthemology correspondence table | **REPRODUCED (need)** | R7C crosswalk did not adjudicate IR/burden/owner-activation/route-pressure/Δ/field-witness/MRP/Ψ-N/Ψ-I/T_lang |

### Corrective dynamics
| # | Finding | Disposition | Evidence |
|---|---|---|---|
| B26 | Candidate YAML says G1 `adopted` | **REPRODUCED** | `NOETIC-FIELD-DYNAMICS.yaml` (to reclassify proposed-candidate) |
| B27 | "locally sound" too strong | **REPRODUCED** | prose in SOUND-DESCENT |
| B28 / B29 | Stages compressed under "descent"; need a transition record | **REPRODUCED** | no `CorrectiveTransition` schema |
| B30 | Fast/slow coupling named, not connected | **REPRODUCED** | two-timescales prose only |

### OSM / dynamic
| # | Finding | Disposition | Evidence |
|---|---|---|---|
| B31 | `Geom_A` only a name | **REPRODUCED** | no extraction/metric/invariance/uncertainty |
| B32 | `ProfileOf_A` underspecified | **REPRODUCED** | relation typed but no evidence basis/transport |
| B33 | Merger/ablation contrast needs full operational def | **REPRODUCED** | `Δ^merge_A` scalar only |
| B34 / P7 | Dynamic update transport free-text; silent transport passes | **REPRODUCED** | `validate_dynamic_orthing` checks only field presence; a "everything transports silently" rule stays green |
| B35 | OSM object separation needs one more layer | **PARTIAL** | R7C split to 4 rows; audit wants ~11-way |
| B36 | Source claim must stay bounded | **REPRODUCED (guard needed)** | keep the CSCG comparison bounded |

### Epistemology / metaphysics
| # | Finding | Disposition | Evidence |
|---|---|---|---|
| B37 | Companion still a sketch (~1,392 words, 4 refs) | **REPRODUCED** | word/ref count |
| B38 | Wrong Decision 0005 references | **REPRODUCED** | companion L75 attributes `Inst_A`/`O*(m;A)` to 0005 (belongs to 0001; 0005 = symbol normalization) |
| B39 | Dynamic orthability overcompressed | **REPRODUCED** | modalities not separated |
| B40 | OSM rung too broad | **REPRODUCED** | over-generalizes one paradigm |
| B41 | Ladder is navigation, not an argument map | **PARTIAL** | R7C has a 10-rung table; audit wants per-rung objection/rival-exit/school-status machine-readable |
| B42 | Arabic/divine-Speech needs an explicit bounded place | **REPRODUCED (need)** | absent from the dynamic companion |
| B43 | Source hierarchy must remain strict | **REPRODUCED (need)** | secondary vs primary labels |

## Refutations recorded (not accepted as-is)

1. **B24 at the commit level** — there is no published post-pin DAEE delta; `main == pin`.
   The correct action is a fuller crosswalk of the pinned content (= current main),
   not "adopting 112 commits." Recorded so a fresh Fable session does not chase a
   nonexistent delta.
2. **B8 parity premise** stands, but the R7C refutation of R7B's "pandoc not
   provisionable" (audit acknowledges it) also stands — P1 vs P2 must be decided on
   the full corpus, not re-litigated on provisionability.

## Environment limitation (carried from the audit)

The R7D pass ran validators + PDF byte-checks under the lock venv on Windows and
confirmed live ubuntu CI success on 3cce235. It does **not** substitute for the
required fresh-Fable rerun of the exact lock, Typst build, and live GitHub CI on the
final R7D head, nor for independent review of every hunk, source, and rendered page.
