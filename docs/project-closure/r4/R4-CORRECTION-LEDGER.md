# R4 correction ledger

**CANDIDATE PASS — REQUIRES INDEPENDENT REVIEW.** Every material correction made in the R4 pass. R1/R2/R3 records keep their bodies; corrections supersede by dated notice, never by rewriting.

| # | Finding | Correction | Status |
|---|---|---|---|
| C1 | B10 public-state drift (VERSION/headers R2; README decisions 0001–0008 and "seven examples"; owner list stale; ledger count mismatch) | `docs/current-state.yaml` (authored+derived) + generator + drift validator; VERSION, README, STATUS, OPEN-DECISIONS and all five primary headers synchronized to R4; decision 0014 | **DONE** |
| C2 | **SELF-1** (found by R4, not in the audit): R2/R3 closeout prose and three R3 documents reported the pilot-0 **v1** freeze hash as `ece0412f…`; the committed packet has always recorded `988a6522…` and passed its own check | Correction recorded in STATUS and here; historical bodies untouched; `validate_current_state.py` now compares recorded state to the packet file so prose can no longer drift from artifact | **DONE** |
| C3 | B1 `p̂` typed both as one partial profile and as a set of complete profiles | Core gloss rewritten: `p̂` is **exactly one** partial profile; alternatives live in `Ĉ ⊆ Π_A`; weights in the separate belief layer; archived patches retain the old gloss as history | **DONE** |
| C4 | B2 strict soundness claim-level in name, episode-level in its conjunct | `ReqReason_q(e) ⊆ ReqPath(e)` projection; `ReasoningPathAdequate_q`; `StrictlySoundReasoning_q := ReasoningPathAdequate_q ∧ TOKEN_TRUTH_LINKED_q`; `PathwayAdequate(e)` retained for the episode; decision 0011 | **DONE** |
| C5 | B3 objectivity overstated ("objective given `A`") | Full-index formulation adopted in current normative prose; index block required in the verdict schema | **DONE** |
| C6 | B4 evaluator symmetry + corroboration asserted to give non-circularity | Withdrawn and replaced with the mitigation formulation; shared-upstream dependence made representable (CR-9 / `shared-upstream-corroboration-failure`) | **DONE** |
| C7 | B5 metaorthemma existence and typing cardinality ambiguous | One existence rule (material binding or **no token**) and one cardinality rule (**exactly one** `of_type`; many-to-many marked unimplemented), stated once and schema-enforced | **DONE** |
| C8 | B6 schemas accept 10/11 malformed classes | Reference-model semantic contract across all schemas + typed RelSpec/PerturbSpec + expanded cross-record semantics; decision 0012 | **DONE (schema phase)** |
| C9 | B7 mutation coverage narrower than the headline | 18 path-aware operator families + 28 invalid fixtures: 1,247 mutants, 1,113 schema-killed, 125 semantic-killed, 9 declared-equivalent, 0 unjustified survivors; per-family reporting with explicit coverage limits; the "208 mutants" figure retained only as history | **DONE** |
| C10 | B8 concrete/ideal-reason attribution mislocated | Doko & Turner 2023 credited for the application; Evans 1998 as the reported source with the page **not** independently verified (RR-2); Turner 2022 rescoped; Turner 2023 chapter corrected; El-Tobgui's three records separated; decision 0013 | **DONE** |
| C11 | B9 Atharī blanket source status vs the R3 closeout | Per-claim rows ATH-1…ATH-7 in the registry; the blanket front-matter disclaimer withdrawn; **no creed position altered** | **DONE** |
| C12 | Part II latent-state amendment | Decision 0015, related-work note, worked example, LS-1…LS-7 fixtures with ten anti-conflation assertions, three verified bib records | **DONE** |
| C13 | **Amendment's own citation error** (found by R4): the controlling amendment cites "Rajeev V. Raju" for the *Science Advances* paper | Corrected to **Rajkumar Vasudeva Raju** (conflation with Rajeev V. Rikhye of the 2021 *Nature Communications* paper); recorded in decision 0015, the related-work note, and the bib | **DONE** |
| C14 | Audit's B6 phrasing overstated one sub-case | Recorded as a **partial refutation**: "verdict record missing required statuses" is accepted at the schema layer but **is** caught by cross-record semantics; the other ten classes were accepted by both | **RECORDED** |

| C15 | **SELF-2** (found immediately after the first closeout): the first revision of `R4-SCHEMA-AND-MUTATION-REPORT.md`, decision 0012's scope note, ledger row C9, the draft PR body, and the session closeout all stated that the recursive mutation engine and `tests/invalid/` were **not built**. They **were** built; the work landed during the final commit window and the claim was written from a stale check | All five surfaces corrected; a dated correction notice added at the top of the report; the true figures recorded (18 families, 1,247 mutants, 1,113 schema-killed, 125 semantic-killed, 9 declared-equivalent, 0 unjustified survivors) | **DONE** |

| C16 | **SELF-3** (found immediately after SELF-2): my corrected report attributed probe classes **P7** (verdict record missing required statuses) and **P8** (`not-applicable` without reason outside `required_path`) to the **schema** layer | **Both are caught at the semantic layer.** My probe instances predated the R4 contract and lacked newly-required fields (`index`; non-empty `required_path`), so the schema rejected them for *incidental* reasons that masked which layer catches the defect under test. Re-derived empirically with completed instances: P7 → semantic ("required verdict carries no status at all" + pathway recomputation); P8 → semantic ("not-applicable without a recorded reason"). Both range over **dynamic verdict-id keys**, which JSON Schema cannot quantify over — the layer split is principled, not accidental. The headline result is unaffected: **0 of 11 classes accepted by both layers.** | **DONE** |

## Findings raised by R4 against its own inputs and its own reporting

Five corrections in this pass were to the *controlling instructions and to this run's own claims*, not to the repository:

- **C2 / SELF-1** — my R2 and R3 closeouts mis-reported the pilot-0 v1 freeze hash.
- **C13** — the controlling amendment's conflated author name.
- **C14** — one audit sub-case overstated (partial refutation).
- **C15 / SELF-2** — **this run reported completed work as not completed.** The error direction is the unusual one — understating rather than overstating — but it is the same defect: a completion claim written from a stale observation instead of checked against the artifact at the moment of claiming. It was caught only because the owner surfaced the agent-completion record.

- **C16 / SELF-3** — my *correction to* SELF-2 mis-attributed two rejection layers, because I re-derived them from stale probe instances instead of instances valid under the new contract.

A correction ledger that only ever corrects other people's work is not doing its job; a project whose subject is false closure has to apply the standard to its own reporting in both directions.

**Pattern worth recording for the independent reviewer.** Three of these five (SELF-1, SELF-2, SELF-3) are the *same* defect at three scales: a claim asserted from a stale observation rather than re-derived from the artifact at the moment of claiming. SELF-1 mis-stated a hash that a check could have compared; SELF-2 declared work unbuilt that a re-check would have found; SELF-3 attributed layers from probe instances that the new contract had already invalidated. Each was caught by an external signal (the generated state file; the owner surfacing an agent record; a subagent's independent re-derivation) rather than by self-review. **The reviewer should assume this run's unaided self-assessment carries that failure mode and weight external verification accordingly.**
