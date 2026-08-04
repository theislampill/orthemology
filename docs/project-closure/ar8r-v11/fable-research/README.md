# AR8R Fable research — round 1 checkpoint

Bounded research output produced under
`docs/project-closure/ar8r-v11/programs/AR8R-FABLE-INTEGRATED-ORTHEMOLOGY-MENISCUS-RESEARCH-PROMPT-V2.md`.

## Status block (unchanged by this round)

```text
historical AR8R substantive duration: 09:41:25.405101139
historical latest segment: 357
theorem-origin authority: V5
integrated champion: NONE
meniscus: NOT_REACHED
natural campaign closure: NOT_REACHED
```

This round adopts no theorem, selects no champion, completes no milestone,
validates nothing empirically, and establishes no metaphysical or theological
claim. Two of its four substantive results are negative.

## What round 1 produced

| Artifact | Content |
|---|---|
| `AR8R-FABLE-R1-LEAN-RECEIPTS.yaml` | First executed Lean toolchain custody and kernel check in the program. 12 declarations, 0 `sorry`, standard axioms only. |
| `AR8R-FABLE-R1-T299-SPECIFICATION-DEFECTS.md` | Five specification defects in the T299 packet, found by formalizing it. |
| `AR8R-FABLE-R1-NEGATIVE-RESULTS.md` | Five refutations and a failed-candidate ledger. The most load-bearing artifact here. |
| `AR8R-FABLE-R1-TYPED-CORE-CANDIDATES.md` | Two rival typed cores, their battery outcomes, and a finite scenario where they disagree. |
| `AR8R-FABLE-R1-SEPARATION-INDEX-AND-INTERPRETATION-MAPS.md` | One invariant, three interpretation maps, split convergence verdict. |
| `AR8R-FABLE-R1-OSM-TYPED-EXTRACTION.md` | Typed extraction of the OSM source and four countermodel classes. |
| `AR8R-FABLE-R1-PRIOR-ART-AND-NOVELTY-CEILING.md` | Correspondence table placing every round-1 object in its classical home. |
| `AR8R-FABLE-R1-REMAINING-BURDENS.yaml` | What is still open, and who can close it. |
| `lean/` | The Lean sources, toolchain pin, and dependency manifest. |

## The four results that matter

**1. Lean Q0 is done.** The formalization queue recorded parse, elaboration,
kernel check, and axiom report as `NOT_PERFORMED`, all gated on a toolchain custody
step that had never been executed. It has now been executed: Lean 4.32.2 pinned,
mathlib pinned, clean build, and AR8R-T299 machine-checked end to end with no
`sorry` and no axiom beyond Lean's standard three. Nine queue items were blocked
behind this.

**2. Formalizing T299 exposed five specification defects.** This is exactly the
outcome the research prompt predicted formalization would produce, and it is the
strongest argument for continuing to formalize. The sharpest: the packet says
landing "requires" its six clauses, which states only necessary conditions — and
under that literal reading the characterization is **false**. It holds only if the
label is *defined as* the conjunction. That failure is itself machine-checked. The
packet's celebrated causal/spontaneous twin, separately, is not statable in the
packet's own declared vocabulary and is not formally an instance of its own
theorem.

**3. A premise the program had been relying on is false.** "Provenance
independence" is not a matroid rank, and the restorative-cutset condition is not a
Menger duality. The exact condition is a minimum transversal, not a maximum packing
of independent routes; the two differ, unboundedly, and the exchange axiom fails as
soon as any item requires two roots. **This was derived twice independently**, from
a proof-theoretic and a model-theoretic direction. The program's existing positive
witness happens to live in the single-root regime, which is why the wrong intuition
survived. Milestone candidate MEN-2 cannot be stated as a rank.

**4. The convergence gate stays closed, correctly.** The OSM source does not clear
it — principled nonidentity at the section/warrant layer. The separation index
clears the gate weakly at the typed-model level but fails at the theorem-transfer
level: it carries a type, not a theorem. Recording the weak pass without the
failure would be the exact overclaim the gate exists to prevent, so the honest
disposition is that the gate remains unsatisfied.

## Method note

Nothing in this round was accepted because it was plausible. Every positive claim
is either machine-checked, exhaustively finite-checked, or explicitly downgraded to
a guarded or negative disposition. Every object was checked against classical
literature before any novelty was considered, and **zero general mathematical
novelty is claimed** — see the prior-art table.

## What round 2 should do

In dependency order:

1. Formalize the transversal-versus-packing correction in Lean and re-express the
   cutset result with its correct condition.
2. Formalize the certificate survival radius and the MIN law; the six-clause
   landing conjunction is a live application.
3. Resolve the CI decision recorded in the Lean receipts before adding any Lean
   job to the workflow.
4. Perform the real prior-art search for Candidate 1 in the promise/query model —
   still the program's only genuinely non-trivial piece of mathematics, and still
   unadjudicated.
5. Decide whether the two rival cores answer one question or two. Round 1's
   evidence says two.
