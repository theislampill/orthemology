# Validator results known at interruption — PR #3 containment

**Containment model:** `claude-opus-4.8`. **No test was rerun during the containment pass**, per the owner's instruction not to rerun a broad suite merely to produce a green claim. Every result below is reported with the exact state it ran against and whether later edits may have invalidated it.

## The one authoritative machine result

| Commit | Required check `validate` | CI runs |
|---|---|---|
| `00cf05d6` (Phase D, pre-substitution) | **success** | 29757727655, 29757730897 |
| `de19ccf4` (Phase F, current pushed head) | **FAILURE** | 29758519395, 29758527272 |

Failing step at `de19ccf4` — *PDF clean rebuild, byte-equality with committed artifacts, text-structure QA*:

```
[FAIL] orthemma-ortheme-systems-draft source unchanged: manuscript/orthemma-ortheme-systems-revised-draft.md — source drifted; rebuild required
[FAIL] orthemma-ortheme-systems-draft clean rebuild byte-identical to committed artifact
[FAIL] orthemic-core-reference-draft source unchanged: theory/orthemic-core-formalization.md — source drifted; rebuild required
[FAIL] orthemic-core-reference-draft clean rebuild byte-identical to committed artifact
```

Cause: the Phase E commit edited `manuscript/orthemma-ortheme-systems-revised-draft.md` (new §12.1) and `theory/orthemic-core-formalization.md` (latent cross-reference) without rebuilding the committed PDFs. The rebuild was performed locally afterwards but exists **only in the uncommitted working tree**, now preserved on the quarantine branch. **The pushed PR head is red.**

## Local validator results claimed earlier in the session

All of the following were run locally against a working tree that has since been modified. None was rerun during containment. Treat every row as *superseded pending re-execution by a fresh Fable session*.

| Command | Last observed result | State it ran against | May later edits have invalidated it? |
|---|---|---|---|
| `python scripts/validate_repo.py` | 0 failures | working tree at Phase F commit time | **Yes** — manifest covers tracked files; PDFs and two new files changed after |
| `python scripts/generate_current_state.py --check` | 0 failures | Phase F commit time | **Yes** — state regenerated again afterwards |
| `python scripts/validate_current_state.py` | 0 failures | Phase F commit time | **Yes** |
| `python scripts/validate_state_convergence.py` | 0 failures (6/6 incl. commit-boundary convergence, tamper and exclusion controls) | Phase D–F range | Possibly — not rerun after PDF rebuild |
| `python scripts/validate_source_status.py` | 0 failures | Phase F commit | Unlikely, but unverified |
| `python scripts/validate_claim_sources.py` | 0 failures | Phase F commit | Unlikely, but unverified |
| `python scripts/validate_verdict_semantics.py --fixtures tests/verdict-fixtures.json` | 57 checks, 0 failures | Phase D range | Unlikely, but unverified |
| `python scripts/validate_notation.py` | 0 failures | Phase D range | Unlikely, but unverified |
| `python scripts/validate_type_token_semantics.py` | 0 failures | Phase F commit | Unlikely, but unverified |
| `python scripts/validate_reason_fixtures.py` | 0 failures | Phase D range | Unlikely, but unverified |
| `python scripts/validate_claim_reasoning_paths.py` | 0 failures (81 checks) | Phase D range | Unlikely, but unverified |
| `python scripts/validate_decision_dependencies.py` | 0 failures | Phase G scan | Unlikely, but unverified |
| `python scripts/validate_latent_state_fixtures.py` | 0 failures | Phase E | Unlikely, but unverified |
| `python scripts/validate_schemas.py` | 0 failures | Phase D range | Unlikely, but unverified |
| `python scripts/validate_cross_record_semantics.py` | 0 failures | Phase D range | Unlikely, but unverified |
| `python scripts/validate_negative_fixtures.py` | 0 failures | Phase D range | Unlikely, but unverified |
| `python scripts/validate_recursive_mutations.py` | 1,813 mutants; 1,546 schema-killed; 248 semantic-killed; 19 survivors all declared equivalent; 0 unjustified | Phase D range | Unlikely, but unverified |
| `python scripts/derive_reqpath.py` | 0 failures | Phase D range | Unlikely, but unverified |
| `python scripts/generate_from_registry.py --check` | 0 failures | Phase D range | Unlikely, but unverified |
| `python scripts/validate_quran_loci.py` | 0 failures | Phase F | Unlikely, but unverified |
| `python scripts/validate_cross_document_consistency.py` | 0 failures | Phase F | Unlikely, but unverified |
| `python scripts/freeze_pilot0.py --check` (v1 and v2) | 0 failures | Phase A baseline only | Not rerun since Phase A |
| `python scripts/audit_terminology_matching.py` | 0 failures | Phase A baseline only | Not rerun since Phase A |
| `python scripts/validate_internal_references.py` (new, uncommitted before quarantine) | 0 failures | Phase G working tree | **Never run in CI**; never run at any commit |
| `python scripts/build_pdfs.py` then `--check` | 0 failures; all four PDFs byte-identical on double build; sidecar source and PDF hashes consistent | Phase H working tree | This is the fix for the red CI, but it was **never committed to the PR branch** |

## Explicit non-claim

**No "all green" claim is made for any commit.** The only rerun-free, machine-attested facts are the two CI rows at the top: green at `00cf05d6`, red at `de19ccf4`.
