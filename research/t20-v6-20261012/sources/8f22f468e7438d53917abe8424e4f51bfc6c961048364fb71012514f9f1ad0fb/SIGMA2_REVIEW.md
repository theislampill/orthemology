# Additive independent Sigma2/Pi2 lower-reduction review

11 October 2026 UTC. PASS for the separately bound fifth module, Sigma2ThresholdRealisation.lean. The four-module REVIEW.md and its BINDINGS.json remain unchanged; this supplement extends that scope.

The new theorem `exists_primrec_sigma2_threshold_reduction` takes each fixed jointly primitive-recursive ternary predicate R. It applies the established rational-shift compiler to the existing jointly primitive-recursive SurvivorPrimrec.prefixFunction at a/b=0/1. Thus the resulting actual numeric-code family has the same defect as Sigma2RowLaw.rowLaw. It does not assert equality of the two measures or observers: the outer unary tagging remains, but the zero shift preserves defect exactly.

The baseline Sigma2RowLaw proves defect zero iff ∃s∀t R and defect one iff no such witness. These two alternatives exhaust parameters. For every real threshold r with 0<r≤1, zero is below r, while one is at least r. Consequently the single PR map f, selected before e and r, simultaneously reduces the Sigma2 predicate to D<r and its Pi2 negation to D≥r at every threshold in this interval. There is no dependency of the compiler on r and no assumption that r is computable; specializing to rational r gives the requested ordinary lower-cut applications.

The endpoints are correct. At r=1 the 0/1 distinction still works. At r=0 the strict cut is empty, so the positive hypothesis is indispensable. For r>1 both defect alternatives are below r, so the upper bound is indispensable. Independent false endpoint controls reject these overextensions. Existing Pi3 Eq/Le/Gt reductions retain a<b; this fifth module does not relax that restriction.

The proof only uses inherited 0/1 row semantics and the checked fixed-family numeric bridge. No universal PR evaluator, Python compile_shift verification, new ordinary classification, or hierarchy-library completeness instance is introduced. Protected and author sources were not edited.

The fifth module was independently compiled with Lean 4.19.0 --trust=0 against the reviewer's fresh four module objects and the unchanged original dependency cache. Its final theorem's axiom readback is exactly propext, Classical.choice, Quot.sound. The four earlier source hashes were rechecked before this replay. SIGMA2_REPLAY.json and kernel/Sigma2ThresholdRealisation.log preserve the compilation and axiom evidence; two expected-rejection logs preserve the endpoint checks. SIGMA2_BINDINGS.json binds the supplement and its relation to the preceding exact review.
