# R4 PR #3 — read-only reproduction pass (independent review session)

**Date:** 2026-07-20
**Reviewing session harness identity (self-attested):** `claude-fable-5` (Fable 5); no substitution observed during this pass.
**Historical provenance disagreement (recorded, not adjudicated):**
- `implementing_run_internal_harness_claim`: the R4 implementing run's internal report says its harness surfaced `claude-fable-5`.
- `owner_observed_ui_substitution`: the owner's UI reported a safeguard substitution to `claude-opus-4.8`.
Neither observation is overwritten or resolved here.

## 1. Live remote and PR verification (A1)

| Fact | Verified value |
|---|---|
| Repository | `theislampill/orthemology` (public), default branch `main` |
| Authentication | `gh` authenticated as `theislampill`; scopes `repo`, `workflow` |
| Live `main` | `63d15ecf4aa50672265100b7d5620af764421862` (matches expected R3 base) |
| PR | #3, OPEN, **draft** |
| PR base | `main` @ `63d15ecf4aa50672265100b7d5620af764421862` |
| PR head branch | `closure/r4-semantic-contract-source-integrity` |
| PR head commit | `25d035a31311dc328b95e15c942238a796cb37c6` (7 commits over base) |
| Mergeability | `MERGEABLE`, merge state `BLOCKED` (required check failing) |
| Branch protection on `main` | required status check `validate` (strict), force-pushes and deletions disallowed, no enforce-admins |
| Archive vs live head | the downloaded audit archive's stated source revision (`25d035a…`) equals the live PR head; the live head is the authoritative basis of this review |

## 2. Historical immutability (A2)

`git diff --name-status 63d15ec..25d035a`: **58 added, 42 modified, 0 deleted.**
No modified or deleted path touches `archive/`, decisions 0001–0010, the frozen pilot0 v1 packet, prior manifests, or provenance history. Decisions 0011–0015 are additions. R1/R2/R3 bodies are preserved.

## 3. Check reproduction (A3)

All 21 workflow steps were re-run locally from a fresh clone at `25d035a` (Python 3.11.9, pinned deps incl. `typst==0.15.0`). Results:

| Step | Local result |
|---|---|
| `validate_repo.py` | 0 failures |
| `generate_current_state.py --check` | **FAIL — 1 failure** (`derived block is current`) |
| `validate_current_state.py` | **FAIL — 1 failure** (same drift, dependent check) |
| `validate_source_status.py` | 0 failures |
| `validate_verdict_semantics.py` | 57 checks, 0 failures |
| `validate_notation.py` | 0 failures |
| `validate_type_token_semantics.py` | 0 failures |
| `validate_reason_fixtures.py` | 0 failures |
| `validate_latent_state_fixtures.py` | 0 failures |
| `validate_schemas.py` | 0 failures |
| `validate_cross_record_semantics.py` | 0 failures |
| `validate_negative_fixtures.py` | 0 failures |
| `validate_recursive_mutations.py` | 1,247 mutants; 1,113 schema-killed; 125 semantic-killed; 9 declared-equivalent; 0 unjustified survivors |
| `derive_reqpath.py` | 0 failures |
| `generate_from_registry.py --check` | 0 failures |
| `validate_quran_loci.py` | 0 failures |
| `validate_claim_sources.py` | 0 failures |
| `validate_cross_document_consistency.py` | 0 failures |
| `freeze_pilot0.py --check` (v1 and v2) | 0 failures |
| `audit_terminology_matching.py` | 0 failures |
| manifest (`make_manifest.py` + diff) | no drift |
| `build_pdfs.py --check` | all four PDFs rebuild **byte-identical**; 0 failures |

CI confirmation: run 29751470223 on head `25d035a` fails at exactly the drift-check step with
`[FAIL] docs/current-state.yaml derived block is current` / exit 1. The Node-runtime message about
`actions/checkout@v4` / `actions/setup-python@v5` is a **deprecation warning, not a failing check**;
no other step reached execution in CI after the failure, but all were reproduced green locally.

Immediate drift cause: `docs/current-state.yaml` line 56 records
`source_commit_at_generation: e027067e6a1a1a558fd8e73ea64352f821043b02` while HEAD is `25d035a…`.

## 4. Independent-audit finding matrix (A4)

Classification of every finding in `orthemology-pr3-independent-audit.md`:

| Audit § | Finding | Classification | Evidence |
|---|---|---|---|
| §1 | Candidate accomplishes substantial work; validators pass | **Reproduced** | full local suite above |
| §2 | One actual CI failure; Node message is a warning | **Reproduced** | CI log run 29751470223 + local rerun |
| §2.1 | Drift: recorded `e027067` vs head `25d035a` | **Reproduced** | `docs/current-state.yaml:56` |
| §2.2 | Self-referential contract: generator embeds `git rev-parse HEAD` in a tracked file; equality cannot converge | **Reproduced** | `scripts/generate_current_state.py:109`; committing the regenerated file necessarily creates a new HEAD |
| §3 | Decisions 0009 and 0011 both adopted with incompatible strict-soundness formulas; no supersession notice in 0009 | **Reproduced** | 0009 line 39 (whole-episode `PathwayAdequate(e)`) vs 0011 §2 (claim-relative); grep for "supersed" in 0009 → none |
| §4 | 0011 claims CR-9, `examples/shared-upstream-corroboration-failure.json`, `scripts/validate_claim_reasoning_paths.py`, six claim-relative cases — none exist; correction ledger marks it DONE | **Reproduced** | `tests/reason-fixtures.json` has only CR-1…CR-8; the named script and example are absent; `R4-CORRECTION-LEDGER.md` row C6 = DONE; `companion/CONCRETE-AND-SOUND-REASON.md` cites the ghost artifacts |
| §4 | `validate_reason_fixtures.py` still computes strict soundness from whole-episode `PathwayAdequate` | **Reproduced** | script line 7 and expected-value check |
| §5 | `ReqReason_q(e)` is a supplied projection with no governance derivation; omission attack possible | **Reproduced** | cross-record validator recomputes adequacy over the record's own `req_reason` only; no derivation rule exists |
| §6.1 | Analysis inheritance: no cycle/self-inheritance/effective-completeness check | **Reproduced** (code inspection) | cross-record §2 checks only that `inherits_from` resolves |
| §6.2 | `domain_ref`/`policy_class` not required by the full-analysis contract | **Partially reproduced** — properties exist; exact required-set check deferred to the repair phase probe |
| §6.3 | Token identity: embedded uniqueness episode-local, standalone separate, flat global resolution set → ambiguous duplicates | **Reproduced** (code inspection) | `all_token_ids` is a flat union; duplicate embedded IDs across episodes undiagnosed |
| §6.4 | Cross-ledger token-scope false positive: every token looped against every ledger | **Reproduced** | cross-record §7: `for led in ledgers: for tok in all_token_recs: …` |
| §6.5 | `of_type`/`mu_ref` unresolved references and precedence edges unchecked | **Reproduced** (code inspection) | only shape of `of_type` checked; no resolution or precedence-cycle logic present |
| §6.6 | Silent external analysis/occurrence references accepted | **To be probed in repair phase** (accepted as plausible; version checks are conditional on a matching declaration) |
| §6.7 | Lexicographic ISO timestamp comparison; no tz-aware parsing; no effective_from<=expiry | **Reproduced** | cross-record RelSpec block compares raw strings (`dat >= rt`) |
| §6.8 | Correctness claims are bundle-local only | **Reproduced in substance** — wording review in repair phase |
| §7 | Mutation suite genuine; coverage claim must match operator set; new families needed | **Reproduced** | local run: 1,247/1,113/125/9/0; operator families lack the §6 gap classes |
| §8 | 0015 integration incomplete: orphan `latent-state-additions.bib`; no source-status/ledger/matrix rows; no manuscript subsection; no formal-core cross-ref; "six-way" vs seven rows; over-absolute nonidentifiability/transport/statability wording | **Reproduced** | fragment exists and is ignored by `validate_claim_sources.py` (reads only `orthemology.bib`); no "latent" text in `manuscript/` or `theory/`; no LAT rows in `source-status.yaml`; 0015 §1 says "six-way" |
| §9 | Decision 0013 registry scope overstated (selective rows vs "every load-bearing claim") | **Reproduced** | registry has CIR-1..4, ELT-1..3, ATH-1..7, EXT-1 only |
| §9.1 | CIR-1 compound status (bibliographic verified vs wording compilation-mediated) under one `SECONDARY_VERIFIED` | **Reproduced** | CIR-1 notes admit publisher text not opened; wording compilation-mediated |
| §9.2 | Atharī evidence-status precision recheck | **Accepted as audit scope** — executed in the source-integrity phase |
| §10 | `validate_current_state.py` claims exact OPEN-DECISIONS equality but does fuzzy first-3-words substring matching | **Reproduced** | script lines 80–87 |
| §11 | Actions `checkout@v4`/`setup-python@v5` deprecated; upgrade | **Reproduced** | workflow file |
| §12 | Provenance disposition: record two attributed observations | **Adopted** (recorded above) |

**No audit finding was refuted.** One finding (§6.2) is downgraded to partial pending an exact probe; §6.6 is accepted-plausible pending probe; both are scheduled for the repair phase regardless because the repair covers them either way.

## 5. Disposition

Repair proceeds per the controlling instruction: Phase B (convergent state contract), C (strict-soundness reconciliation), D (schema completion), E (0015 integration), F (source status), G/H (whole-corpus + PDFs), I (adversarial passes), J (sign-off and merge).
