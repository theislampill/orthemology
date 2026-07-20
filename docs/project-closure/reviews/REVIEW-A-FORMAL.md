# Review A — formal reviewer (assume the framework is wrong)

**Date:** 2026-07-20 · **Reviewer stance:** adversarial; every finding below was either FIXED in this revision or is recorded as a standing limitation. This is a fresh pass performed after the full R2 implementation, over and above the three-pass audit (`../FORMAL-AUDIT-R2.md`).

| # | Attack | Finding | Disposition |
|---|---|---|---|
| A-1 | Equivocation on "analysis-relative" (relativism smuggling) | §2.6's anti-relativism paragraph now pins the index as declared/public/versioned; no passage predicates truth of an actor's belief state | CLEAR |
| A-2 | Undefined types | Swept against the notation registry; the two genuine gaps found in R2 (Π_A definition site; informal `Reach(m)`) were fixed (Definition 10; explicit `Reach` at both Compat/Conflict sites). No further undefined current symbol found (validator-enforced) | FIXED (this revision) |
| A-3 | Circularity in the pathway core | `PathwayAdequate` is defined from statuses over `ReqPath`, `ReqPath` from governance inputs, none from `PathwayAdequate`; V2b-P's reference class is fixed pre-outcome, blocking the rescue-circle | CLEAR |
| A-4 | Vacuous applicability (adequacy by exclusion) | Blocked three ways: governance-derived `ReqPath` (no discretionary list), mandatory `not-applicable` reasons, and "missing assessment = undetermined" (F5). Fixture-checked | CLEAR |
| A-5 | Impossible profile comparisons | The R2 item-11 repair typed `Compat_m`/`Conflict_m` through per-analysis evaluation of one shared occurrence; no remaining cross-space set operation found in the corpus | FIXED (this revision) |
| A-6 | False independence claims | The old "none entails another" is gone; the implication table declares the sole entailment and explicitly refuses pairwise-independence claims | CLEAR |
| A-7 | Hidden result-factivity in the pathway core | Checked verdict-by-verdict: V2b-P non-factive by construction; V3e decision-time; V6 quantifies over neighborhood V1 rates *of other episodes* — the only subtlety: V6's tolerance references RESULT failure rates of *perturbed* episodes, which is neighborhood-factive but not THIS-episode-factive; recorded as a definitional feature (robustness is about the neighbors), not a leak | CLEAR (with note) |
| A-8 | Token/type collapse | Four layers (μ / π_μ / μ̄ / execution) with per-layer verdicts (V3a/V3b/V3c/V3d); `MetaInst` types tokens without a second ground-truth primitive | CLEAR |
| A-9 | Analysis/task collapse | Shorthand convention + multi-analysis prohibition, machine-checked by the notation validator's context rule | CLEAR |
| A-10 | Claim/burden collapse | 𝒬 vs δ separation stated at the signature and in Definition 12/13; the R2 precedence rule removed the owner-assigned/transferred ambiguity | FIXED (this revision) |
| A-11 | Counterexamples | 16-pattern ledger, all representable; two needed new fixtures (F6, F7) | CLEAR (see `../COUNTEREXAMPLE-LEDGER-R2.md`) |

**Standing formal limitations (not defects, acknowledged):** the five items in `FORMAL-AUDIT-R2.md` §"Acknowledged remaining theoretical limitations" (evidence-class exhaustiveness as hypothesis; no closed-form `RequiredBy` calculus; Δ_A's inherited idealizations; non-unique fusion rules; zero empirical validation).
