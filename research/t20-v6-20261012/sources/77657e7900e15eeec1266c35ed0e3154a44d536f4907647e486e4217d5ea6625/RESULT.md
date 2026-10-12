# Actual effective source presentation, candidate evidence

This additive candidate proves an unconditional `Primrec₂` and `Computable₂` total checker on natural claim/certificate codes, its equality to the retained actual finite source checker on canonical source encodings, soundness of every accepted pair of natural inputs, and completeness for all six actual Joint/E judgment families.

`SourceProofSearch.lean` proves `REPred DerivableCode`, actual Mathlib `Partrec` and `Nat.Partrec` least-certificate search, exact termination domain, least-witness characterization, and source-instance domain equivalences for `CtxJ`, `FormJ`, `HasJ`, `CtxE`, `FormE`, and `HasE`. No source `Primcodable` instance is presumed and no executable-Lean-to-Computable shortcut is used. The checker has no abstract or unproved rule/checker-computability arguments.

`TypeInhabitationSearch.lean` separately projects closed Joint type inhabitation through an actual paired term-code/certificate-code witness. It explicitly checks canonical Ty and Poly images, uses the proved actual `hasCode` transport, proves the candidate checker PR, and proves exact partial-search domain and recursive enumerability for `∃ p, HasJ [] p A`.

## Preservation and rejection behavior

Serial certificate nodes and lists are traversed simultaneously with the exact expected ordered premise list. Nil rejects leftover expectations; cons rejects an empty expected list. All 63 rule maps and all unused type-image formation premises are preserved. Explicit finite, lookup, reduction, and conversion evidence is retained by the actual side-checker bridge. A canonical-domain gate rejects malformed claim/certificate codes before accepting a result; arbitrary malformed decoder behavior need not match the old decoder.

Controls prove valid acceptance, missing/extra children rejection, swapped distinct-claim children rejection, wrong-root rejection, false conversion rejection, full unused-image formation order, dropped-image rejection, malformed-domain rejection, and undefined search at an invalid claim. They do not claim that interchanging two certificates of the same claim must fail. Four small supplied-certificate runtime tests pass; larger attempted runtime tests have `RESOURCE_INCONCLUSIVE` status recorded separately and receive no passing, rejection, or counterexample credit.

## Verification and scope

Author replay uses fresh selected Lean 4.19.0 `--trust=0` outputs with sources and retained imports pinned before and after. It rebuilds the needed additive computability/validity/rule-map chain, not the huge protected baseline. Endpoint audits permit only `propext`, `Classical.choice`, and `Quot.sound`, and reject semantic `FullPER`/`JointCompletion.fundamental` dependencies. False semantic controls must fail in the kernel.

The unbounded search result is a certified mathematical partial recursive function. It is not a freshly extracted machine listing, a practical theorem prover, a total decider, or an efficiency/resource-bound claim. Code numbers can be very large. This establishes a constructive effective source presentation; previous semantic/source separation and `no_re_sound_complete_acceptance` results already existed. It is not first-ever incompleteness, a metaphysical conclusion, source adoption, or T20 closure. Independent review remains required.
