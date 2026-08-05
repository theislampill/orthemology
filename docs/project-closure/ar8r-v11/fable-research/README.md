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

> **Corrected after independent review.** Commit `f0e386a` was reviewed
> independently and returned **BLOCK**. Several round-1 claims were withdrawn or
> narrowed; the Lean results survived. Read
> `AR8R-FABLE-R1-CORRECTION-RECEIPT-V1.md` alongside this page — where the two
> disagree, the correction receipt governs.

| Artifact | Content |
|---|---|
| `AR8R-FABLE-R1-CORRECTION-RECEIPT-V1.md` | Withdrawal and correction record following independent review. **Read first.** |
| `AR8R-FABLE-R1-LEAN-RECEIPTS.yaml` | First executed Lean toolchain custody and kernel check in the program. 0 `sorry`, standard axioms only. |
| `AR8R-FABLE-R1-T299-SPECIFICATION-DEFECTS.md` | Fifteen underdetermined places in the T299 packet, four classified as defects beyond notation, one claim withdrawn. |
| `AR8R-FABLE-R1-NEGATIVE-RESULTS.md` | Failed candidates, interpretation firewalls, and a reaffirmed gate. N1's target attribution was withdrawn. |
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
mathlib pinned, clean build, and a **repaired, scoped interpretation** of AR8R-T299
kernel-checked with no `sorry` and no axiom beyond Lean's standard three. Nine queue
items were blocked behind this.

The historical T299 packet itself was **not** machine-checked end to end. What was
checked is a formalization of a reading of it, with the interpretive repairs
recorded in the specification-defects packet. This distinction was blurred in the
original round-1 wording and is corrected here.

**2. Formalizing T299 exposed real underdetermination in the packet.** Fifteen
places were found where the informal packet does not fix the formal content; four
are defects beyond notation. The sharpest concerns the word "requires": stating
only necessary conditions leaves `L_b` underdetermined, so the packet's separate
claim that the matched profile `B*` is sufficient "by construction" is not
established under that reading.

*Corrected:* round 1 said the **characterization** is false under the literal
reading. It is not — `Certifiable P l ↔ FibreConst P l` is proved for an arbitrary
label and does not depend on how `L_b` arises. The casualty is the `B*` sufficiency
remark, not the characterization. Round 1's claim of five genuine defects is also
withdrawn; D4 (A14) was induced by a formalization choice, not by the packet.

**3. A valid combinatorial firewall — but its original target attribution was
false.** A minimum transversal cannot in general be replaced by a maximum
root-disjoint packing (`τ ≠ ν`), and "pairwise root-disjoint" need not form a
matroid.

*Corrected:* round 1 presented this as refuting the Round-20 restorative-cutset
result and milestone candidate MEN-2. It refutes neither. Round 20 V1 and V2 both
state and prove the transversal condition `κ_root > f` and cite hypergraph
transversal theory; MEN-2 is `NOT_ADOPTED` and asserts no matroid axioms. The
attribution is withdrawn, the Round-20 statement is unaltered, and the surviving
content is an interpretation firewall plus a constraint on any future MEN-2
definition. Round 1's "sharp threshold" — that both properties fail as soon as one
item requires two roots — is **false** and is withdrawn, with counterexamples
preserved.

**4. The convergence gate stays closed, correctly.** The OSM source does not clear
it — principled nonidentity at the section/warrant layer, with the source-level
readings marked `SOURCE_LEVEL_UNVERIFIED` because the paper was outside the
independent review boundary. The separation index
clears the gate weakly at the typed-model level but fails at the theorem-transfer
level: it carries a type, not a theorem. Recording the weak pass without the
failure would be the exact overclaim the gate exists to prevent, so the honest
disposition is that the gate remains unsatisfied.

## Method note

Every positive claim here is machine-checked, exhaustively finite-checked from a
committed checker, or explicitly downgraded to a guarded, unverified, or negative
disposition. **Zero general mathematical novelty is claimed** — see the prior-art
table.

The round-1 version of this note claimed nothing was accepted because it was
plausible. Independent review found otherwise in three places: a target attribution
with no repository instantiation, a false `iff`, and a defect induced by the
formalization rather than found in the packet. Those are withdrawn above. The claim
that this round's method was self-correcting is retained only as corrected by
external review, not as a property round 1 demonstrated on its own.

## What round 2 should do

In dependency order:

1. Do **not** re-express the cutset result: Round 20 already uses the correct
   transversal condition. If the interpretation firewall is worth formalizing,
   formalize `τ ≠ ν` as a standalone lemma, not as a correction to PRRC-1.
2. Formalize the certificate survival radius and the MIN law; the six-clause
   landing conjunction is a live application.
3. Resolve the CI decision recorded in the Lean receipts before adding any Lean
   job to the workflow.
4. Perform the real prior-art search for Candidate 1 in the promise/query model —
   still the program's only genuinely non-trivial piece of mathematics, and still
   unadjudicated.
5. Decide whether the two rival cores answer one question or two. Round 1's
   evidence says two.
