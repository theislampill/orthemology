# R2 independent read-only audit (R3 Phase 1)

**Date:** 2026-07-20 · **Executor:** Claude Fable 5 under the R3 owner authorization (consolidated prompt v2; the concrete/sound-reason amendment controls where it conflicts with the original R3 program) · **Audited state:** fresh clone of remote `main` = `27f66dd8e25131140054691caf91c67cb0407b73` (verified via the GitHub API; branch protected; latest main CI run 29729529973 success) · **Mode:** read-only — no repository file was modified before this report was complete.

This audit independently *tests* the R2 state; it does not repeat R2's own reports. It corroborates the owner's independent audit where the evidence supports it and records exact reproductions.

## 1.1 Repository baseline — PASS

- 114 files in the fresh clone; remote/main identity exactly as expected.
- All six validators re-run from the fresh clone: `validate_repo` 0 failures; `validate_verdict_semantics` 57 checks / 0 failures; `validate_notation` 0 failures (UTF-8 console; the cp1252 console error is an environment artifact, not a validator failure); `validate_schemas` 0 failures; `validate_claim_sources` 0 failures; `validate_cross_document_consistency` 0 failures. `freeze_pilot0.py --check` PASS; `build_pdfs.py --check` 0 failures.
- **Coverage caveat (the audit's central finding):** these passes prove exactly what the validators test — positive-fixture consistency, link/manifest integrity, notation hygiene — and nothing more. Every blocking finding below lives outside their coverage.

## 1.2 Semantic cross-document review

**SEM-1 (BLOCKING) — type/token collapse in the school-neutral companion.** `companion/orthability-and-the-ground-of-intelligibility.md` line 17 calls diagnoses/parses "concrete orthemes"; line 19 introduces "concrete metaortheme" for a locally operative standard; line 27 says the higher-order faculty's "outputs are concrete metaorthemes." Under the settled ontology (D1/M1, core, README) an ortheme is a repeatable state-type and a diagnosis is a placement `p̂`; a case-bound governing token is a metaorthemma. The companion's usage collapses the distinction the core makes non-redundant. Confirmed by grep: the collapse is **confined to this one file** — the theory, manuscript, glossary, and overview layers contain no occurrence of "concrete ortheme"/"concrete metaortheme"/"sound ortheme".

Per the controlling amendment, the repair is **relocation and disambiguation, not deletion**: the concrete/sound two-axis insight is philosophically sound (and Taymiyyan-supported); its bearers are mislabeled. §2's product "mode of instantiation × normative status" must become a three-axis model (object level × instantiation × normative status × result status) with soundness assigned to placements, adequacy to types/tokens, fidelity to executions.

**SEM-2 (BLOCKING) — orthability equivocation.** Line 13 defines orthability "always relative to the resolving practice's standards," while §§4–5 argue orthability is antecedent to every created practice. The bridge (local `Orthable(m; A)` vs objective conditions of evaluability vs created representation/application) is absent. The transcendental chain's step 2 trades on the unbridged senses.

**SEM-3 (MAJOR) — design-argument reification risk.** §3.3's "know the objective orthemes, know the fitting metaorthemes" phrasing invites Platonic reification the Atharī paper explicitly forbids (§4.2 there). Needs the amendment's §14.4 rewording.

No result/pathway leakage, vacuous applicability, undefined aggregation, or hidden empirical claim was found in the theory/manuscript layer beyond the items already risk-accepted in FORMAL-AUDIT-R2 (`RequiredBy` informality; factorized-Π_A presentation — see FORM-1/FORM-2 below).

## 1.3 Source audit baseline

**SRC-1 (BLOCKING, CONFIRMED) — Qurʾānic locus error.** Independently verified against the Uthmānī text (Qurʾān MCP source): 20:11 = «فلما أتاها نودي يا موسى» (the call only); 20:12 = «إني أنا ربك فاخلع نعليك...». The Atharī paper §3.1 attributes "O Mūsā, verily I am your Lord" to **20:11**; the correct citation is **20:11–12**. The same wrong locus appears in `docs/sourcing/SOURCING-LEDGER.md` row 31, `companion/sourcing/COMPANION-SOURCING-LEDGER.md`, and the generated Atharī PDF.

**Full āyah-locus audit:** all 29 āyāt cited across the Atharī paper were fetched and checked: 4:87, 4:122, 5:116, 19:52, 42:11, 7:54, 36:82, 55:1–3, 2:120, 3:61, 18:109, 31:27, 87:1, 7:180, 76:25, 32:2, 6:114, 16:102, 9:6, 28:30, 79:24, 29:49, 80:13–14, 98:2–3, 4:164. **Result: 28 correct; exactly one error (20:11).** Note for the registry: 2:120 and 3:61 support their claim only as school-internal inference ("من العلم" read as the revealed knowledge), not by direct statement; the registry must mark direct-statement vs school-internal-inference per locus.

**SRC-2 (BLOCKING) — sourcing lane not closed.** Status counts (raw string counts incl. legend mentions): main ledger ≈26 RECORD-CONFIRMED / 5 VIA-COMPILATION / 4 WEB-VERIFIED rows; companion ledger ≈11 RECORD-CONFIRMED / 5 VIA-COMPILATION / 3 WEB-VERIFIED / 1 UNVERIFIED rows. The Atharī paper's own front-matter admits printed editions were not opened and §7 admits no Ashʿarī/Māturīdī tradition-internal source was verified. R2's classification of edition-level verification as *owner-assigned* was too broad: **ordinary source verification is not owner-only**; it becomes owner-blocked only after a documented failed search for accessible scans/editions. The R2 CLOSURE-BURDEN-LEDGER rows 14/23 therefore overstate closure.

## 1.4 Schema adversarial baseline — 7/7 malformed classes ACCEPTED

Run against the actual schemas (`scratchpad/r3_adversarial_baseline.py`, jsonschema 2020-12 with the repo's registry): **all seven malformed record classes validate successfully** under the current schemas:

| # | Malformed record | Accepted? |
|---|---|---|
| N1 | metaorthemma with empty `binding`, no governed component/scope/instrument/executor | ACCEPTED |
| N2 | episode with only id/occurrence/actor/analysis/time/empty placement — no evidence, policy, claims, verdicts | ACCEPTED |
| N3 | verdict record: required `EVIDENCE_SUPPORT = fail` **and** `pathway_state = adequate` | ACCEPTED |
| N4 | claim verdict: `TOKEN_TRUTH_LINKED = pass` on a `result_correct = fail` claim | ACCEPTED |
| N5 | meta-token anchored to a different occurrence *and* analysis than its episode | ACCEPTED |
| N6 | duplicate `evidence_id`s in one episode | ACCEPTED |
| N7 | undeclared extra top-level fields | ACCEPTED |

N3/N4 are caught by `validate_schemas.py`'s custom checks **only for checked-in examples** — the schema layer itself enforces nothing. Cross-record checks (N5) and uniqueness (N6) have no automated home at all. Finding **SCH-1 (BLOCKING)**.

## 1.5 Terminology-instrument baseline — matching claim not satisfied

Deterministic word counts over `terminology/pilot0/items/ITEMS.json` (per-arm rendering, whitespace tokens):

| Item | A | B | C | C′ | B−A | Notes |
|---|---|---|---|---|---|---|
| P0-ID-1 | 11 | 32 | 25 | 25 | +21 | B states the target distinction (answer leakage) |
| P0-PL-1 | 4 | 28 | 22 | 22 | +24 | same |
| P0-PW-1 | 14 | 32 | 30 | 30 | +18 | same |
| P0-FC-1 | 7 | 31 | 20 | 20 | +24 | **C ≡ C′** (no sham contrast possible) |
| P0-RR-1 | 16 | 30 | 21 | 21 | +14 | same |
| P0-MB-1 | 28 | 54 | 35 | 35 | +26 | B supplies three ordinary-language aliases at once |
| P0-MA-1 | 5 | 40 | 29 | 29 | +35 | same |
| P0-NC-1 | 5 | 13 | 13 | 13 | +8 | negative controls **not** arm-identical |
| P0-NC-2 | 5 | 13 | 13 | 13 | +8 | same |

The protocol's "scenario semantics identical across arms; only vocabulary varies" claim is not satisfied: B teaches the distinction and often supplies the answer while A asks a bare question; B−A ranges +14…+35 on substantive items (matching the owner audit's estimate); P0-FC-1 cannot contribute to any C-vs-C′ estimate; negative controls differ across arms. The v1 packet is a smoke-test prototype, not a matched inferential instrument. Finding **TERM-1 (BLOCKING for the "ready-to-run matched instrument" label; not for the packet's existence)**. v1 + `FREEZE-HASH.txt` (ece0412f…) must be preserved as immutable superseded history.

## 1.6 PDF read-only baseline — not reproducible, not publication-clean

- **Double-build test:** the full tree was copied clean, `build_pdfs.py` run twice ~2 s apart. **All four PDF SHA-256 hashes changed between builds** (e.g. manuscript A2C3C645… → 689915DF…). `pypdf` metadata of the committed manuscript PDF shows a live `/CreationDate: D:20260720085314Z`. Non-reproducibility is direct, not inferred.
- **Text extraction of the committed manuscript PDF (31 pages):** literal `> ` blockquote markers PRESENT; raw Markdown links `[..](..)` PRESENT; raw pipe-table rows `|---|` PRESENT; standalone `---` rules PRESENT.
- **Code findings** (`scripts/build_pdfs.py`): `emit()` silently skips an unrenderable line after two attempts; `--check` verifies only file existence + source-hash sidecar drift (it does not rebuild or compare output); rendering is line-inspection, not a Markdown parser; known missing-glyph warnings (⃗, ⊨) accepted in R2.
- Sidecars record source commit `68ce774e…` while the archive is at `27f66dd8…` — legitimate (artifacts committed before the merge commit) but the source-revision vs artifact-revision distinction is nowhere documented. Finding **PDF-1 (BLOCKING for the "reproducible" claim)**.

## 1.7 Bounded daee-epistemics review

Public repo `theislampill/daee-epistemics` reviewed (read-only). Five generic control disciplines confirmed present and importable in ordinary-language form, with source locations: (1) evaluator/practitioner symmetry (`atomics/skill/SKILL.md` — the practitioner runs the same deformation check on itself before applying it outward); (2) whole-state reread after each burden lands (`references/diagnostics/recursive-state-transitions.md` — `Land(Bn)` → reread of the entire live field before continue/stop); (3) inference-boundary/source-status legend (`references/diagnostics/diagnostic-ir.md`); (4) canonical atomized source (`atomics/skill/`) generating an uncommitted runtime (`skill/`) via a freshness-checked build pipeline; (5) bounded release/closure contract (`references/rubrics/diagnostic-render-contract.md` — closure as a formal residual-pressure condition). **Boundary:** its theology is not evidence for orthemology; no repo merge; no term import merely by conceptual neighborhood.

## Severity-ranked issue ledger

| ID | Severity | Finding | R3 phase |
|---|---|---|---|
| SEM-1 | BLOCKING | type/token collapse in school-neutral companion (3 loci); repair = relocation per amendment, preserving concrete/sound distinction | P3 |
| SEM-2 | BLOCKING | orthability equivocation (practice-relative def vs practice-antecedent argument) | P4 |
| SRC-1 | BLOCKING | 20:11 → 20:11–12 in paper, both ledgers, PDF | P6 |
| SRC-2 | BLOCKING | sourcing lane misclassified as closed; verification is not owner-only | P6 |
| SCH-1 | BLOCKING | schemas accept 7/7 malformed classes; no negative tests; no cross-record semantics | P7 |
| TERM-1 | BLOCKING | pilot0 v1 arms not matched as protocol claims (B teaches/leaks; C≡C′ on FC-1; NC not identical) | P8 |
| PDF-1 | BLOCKING | PDFs not byte-reproducible (live timestamps); raw Markdown leakage; silent line-skip; weak `--check` | P9 |
| ACC-1 | BLOCKING | R2 closure ledgers overstate ("CLOSED", "publication-clean", "reproducible", verification owner-only) | P2 (first commit) |
| SEM-3 | MAJOR | design-argument "know the objective orthemes" reification risk | P3/P11 |
| FORM-1 | MAJOR | Π_A presented as universally factorized; applicability/absence/openness not separated | P5 |
| FORM-2 | MAJOR | `RequiredBy` informal; no typed contract/derivation trace; "closed" label too strong | P5 |
| SRC-3 | MAJOR | 2:120/3:61 (and similar) need direct-statement vs school-internal-inference marking | P6 |
| INT-1 | MINOR | evaluator symmetry / whole-state reread / inference legend not yet instantiated as fixtures | P10 |

## R3 mutation plan (exact order)

1. **P2** — first commit: supersession addenda on STATUS, OPEN-DECISIONS, R2 closure docs; open `R3-CORRECTION-LEDGER.md` (ACC-1).
2. **P3** — Decision 0009 + companion three-axis repair + `CONCRETE-AND-SOUND-REASON.md` + semantic-role validator + CR-1…CR-8 fixtures (SEM-1, SEM-3).
3. **P4** — Decision 0010 + `ARGUMENT-MAP-ORTHABILITY.md` + layered orthability senses (SEM-2).
4. **P5** — Π_A generalization + `ReqPath` typed interface + 8 counterexamples; `R3-FORMAL-AUDIT.md`, `R3-COUNTEREXAMPLE-LEDGER.md` (FORM-1/2).
5. **P6** — `references/quran-loci.yaml` + validator; 20:11–12 fix; hadith/classical verification; kalām nafsī split; bibliography re-verification with graded statuses; R3 sourcing artifacts (SRC-1/2/3).
6. **P7** — strict schemas + cross-record semantic validator + negative/mutation tests + registry-generated enums (SCH-1).
7. **P8** — pilot0-v2 matched packet + deterministic matching audit + execution-readiness spec (TERM-1); v1 preserved.
8. **P9** — reproducible structural PDF pipeline (SOURCE_DATE_EPOCH from source commit; double-build byte identity; hard-fail on loss; text-structure + visual QA) (PDF-1).
9. **P10** — daee-epistemics mapping doc + evaluator-symmetry and whole-state-reread fixtures + inference-boundary legend (INT-1).
10. **P11** — manuscript/companion editorial pass; CI expansion (offline-deterministic only).
11. **P12** — adversarial reviews A–F + the amendment's 15 adversarial questions.
12. **P13** — final read-only sign-off from a fresh clone; PR; merge; closeout.

**Not reopened (verified untouched):** D1, M1, O2, D3, D4, O3; `archive/`; R1 decision records 0001–0003; frozen terminology v0 spec; pilot0 v1 freeze hash. No contradiction requiring any of them to be reopened was found.
