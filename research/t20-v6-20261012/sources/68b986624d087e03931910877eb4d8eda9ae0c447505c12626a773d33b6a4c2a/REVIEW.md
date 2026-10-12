# Independent rational-threshold review

11 October 2026 UTC. Additive review only; author sources and protected repositories are not edited. Verdict: PASS within the stated additive formal-upper-normal-form scope. Fresh independent replay and axiom inspection passed at the exact hashes below.

## Original semantics recovered

The 77 baseline source files match every source-member SHA256 in the author's ACQUISITION.json. Archive binding: Orthemology_v5_Frontier_Research_Return_20260930.zip, SHA256 866c6ff6e74a67f2bc452b49a0ada05311c0c2601585ea166404719172bd8086. This check establishes extracted-source agreement with the recorded manifest, not an independent provenance audit of the archive.

CodecProgram.evaluateIndex is the actual total decoded P02-L1 LOOP evaluator. Decode failures and decoded programs of arity other than 2 yield zero. Valid arity-2 programs execute on registers n,word,0,... and return the designated register modulo 2. FiniteOutputTable.indexTable uses this evaluator, and its proved exactness is against fairCantor.map(output(evaluateIndex e)), a probability measure. No new machine semantics or assumed approximation is substituted.

P02A2.MeasureCore defines positive μ={x | 0<μ{x}}, mass μ=μ(positive μ) in ENNReal, and defect μ=1−(mass μ).toReal in Real. Probability gives finite mass in [0,1], so passing through toReal and real subtraction is valid. HeavyCylinders proves M=sup_k inf_n H(k,n), H the measure of cylinders of mass at least 2^-k.

NumericMembership.rationalOfCode decodes natural-pair numerator/denominator through NNRat.divNat. Zero denominators decode as zero, and redundant fractions are allowed. membershipMatrix e i k n is the implication r_i<1 -> r_i<=H(k,n); it is deliberately vacuous at r_i>=1. The extension's lowerCutMatrix explicitly conjoins r_i<1, preventing that vacuity from producing false strict witnesses. upperCutMatrix uses r_i<q -> membershipMatrix, sound for q<=1.

## Cut and slack review

For nonnegative rational q, lowerCutMatrix yields M>q iff exists i,k forall n L_q(e,i,k,n), using q<r_i<1. Density supplies a margin strictly above q and below M; all finite horizons then bound r_i non-strictly. The reverse bounds the infimum and supremum by r_i. This does not exchange strict comparison with an infimum.

For 0<=q<=1, upperCutMatrix yields M>=q iff forall i exists k forall n U_q(e,i,k,n). Every r_i<q receives its own k, and density rules out M<q. This does not assert the supremum is attained. Negations correctly give M<=q as forall i,k exists n not L and M<q as exists i forall k exists n not U.

With D=1−M, for q in [0,1]:
- D<q has an exists-exists-forall computable matrix (ordinary Sigma-2 upper normal form).
- D>=q has a forall-forall-exists computable matrix (ordinary Pi-2 upper normal form).
- D<=q has a forall-exists-forall computable matrix (ordinary Pi-3 upper normal form).
- D>q has an exists-forall-exists computable matrix (ordinary Sigma-3 upper normal form).
- D=q is the conjunction of the displayed closed cuts; ordinary upper bound Pi-3.

These are inherited ordinary hierarchy interpretations of exact quantifiers, not newly proved lower reductions, completeness at every rational threshold, or a new classification. The baseline already includes the primitive-recursive reduction from each fixed jointly PR forall-exists-forall matrix to zero defect, and uniformly Computable membership normal form. No claim of a universal primitive-recursive interpreter is licensed.

Direct comparison was made with user-checkpoints/extracted/P02/proofs/CV_C_HIERARCHY.md C2-09–C2-12, its actual compile_shift implementation in P02/code/prcodec.py lines 293–310, and the retained PRIOR_DEFECT_COMPUTABILITY.md. These already state the complete ordinary rational threshold table. The formal increment uses the inherited hard-cylinder mass formula rather than the ordinary excess-cylinder formula; both compute the same original mass. It does not newly establish the ordinary classification.

## Boundary controls and scope

At q=0, D<0 is false, D>=0 is true, D<=0 is D=0 (old zero-defect index set), and D>0 is its complement. At q=1, D<=1 is true, D>1 is false, D<1 means positive atomic mass, and D>=1 means atomlessness. Thus positive defect and atomlessness remain distinct. The new upperCutMatrix at mass threshold 1 simplifies to original membershipMatrix; at 0 it is true. The lower matrix at mass threshold 1 is false.

For signed rational thresholds below zero, D<q and D<=q are false, while D>q and D>=q are true. Above one these truth values reverse. Such signed out-of-range defect cuts are ordinary consequences of the probability bounds; the current API takes NNRat and its defect theorems require q<=1. Do not claim they have been supplied as signed-rational Lean theorems. The mass gt/le results cover nonnegative q without an upper-bound hypothesis and correctly degenerate above one; mass ge/lt require q<=1.

The original root mixed-law strict-infimum guard is collaborative input, not independent invention: (1/2)delta_0+(1/2)fair law has H(1,n)>1/2 at every finite n but inf_n H(1,n)=1/2. The author's hidden-mixture program controls check finite counts only, not a new theorem identifying its full output law or atomic mass.

Independent supremum-attainment guard: give distinct Cantor atoms x_j mass 2^-j for j>=1. Total atomic mass is 1, while the mass of each heavy level k is 1−2^-k (k=0 gives zero). Hence replacing forall rational margins exists k with one k attaining total mass is unsound. This is an ordinary mathematical guard, not a proved P02 realization.

Independent exact Fraction tests check 20,808 numerator/denominator/threshold cases, including zero denominators and redundant codes, against both cross-multiplication formulas. They also check 100 finite geometric sums for the supremum guard. The final joint-code controls add 28,561 comparison cases and 169 complement cases, all passing. These are controls, not proofs of the universal identities.

## Effectivity

The final RationalThresholdUniform module strengthens the initial fixed-q results: lowerCutMatrix_code_computable and upperCutMatrix_code_computable prove one joint Computable relation in the threshold code plus e,i,k,n. rationalCodes_lt_primrec handles both total division conventions, including zero denominators. complementCode_primrec and rationalOfCode_complement transport the truncated NNRat complement, including denominator-zero codes mapping to one. lowerDefectMatrix_code_computable and upperDefectMatrix_code_computable prove joint effectivity of both defect matrices. Full defect semantic equivalence still requires q<=1; computability of a truncated expression alone does not extend that equivalence out of range. The proof uses inherited membershipMatrix_computable, not mere Decidable instances.

## Final verification and exact bindings

The reviewer compiled all five final sources independently into this review directory with Lean 4.19.0 --trust=0, using the author-rebuilt 77 original modules and original mathlib pin c44e0c8ee63ca166450922a373c7409c5d26b00b. No duplicate dependency acquisition or full baseline rebuild was performed by the reviewer. All 77 baseline source and object hashes were independently rechecked against the successful BASELINE_REBUILD.json, and all 77 source hashes against ACQUISITION.json. The five extension sources were checked unchanged after replay.

All 38 theorem declarations were independently queried with #print axioms. Every target lists exactly propext, Classical.choice, Quot.sound. No sorryAx, custom axiom, or native-decide reduction axiom is present in these dependency readbacks. Literal source scanning found no sorry/admit/native_decide; a matched baseline prose line says “axiom is used” inside a comment, not a declaration. REPLAY.json gives the source/object hashes, exact theorem list, dependency search path, and baseline manifest digest; kernel/AXIOMS.log contains the readbacks.

Final source SHA256:
- RationalThresholdCuts.lean: b8e57f1e5e4bd851c3e0b2faaa755c2bab6c48c4c3c5be0ebef7dcd849069bbf
- RationalThresholdComputable.lean: 30d00bbcf2e54f38d11ab6f163a58953b72ec029da97a6cba4b52b9dd9c26838
- RationalThresholdUniform.lean: 6f270a77065244b86f2db671936db03a3587cf2157dcf653e629dc8361f886dc
- RationalThresholdDefect.lean: cb654b071db716f97d40a7ee3e4949915a04f29627326dcca33bc3e1e2771da0
- RationalThresholdControls.lean: d231c64f2ed5b548a410d159653727625cb709128c6cae1b9e5ff72a419a8583

BINDINGS.json additionally binds all ordinary comparison documents, the root collaborative guard, acquisition and baseline evidence. The review does not transfer acceptance to unbound later edits.

## Residuals and limits

- The ordinary full classification was inherited. No new classification or historical-priority claim is accepted.
- Formal rational-shift hardness and integration into a hierarchy-library completeness interface remain outside this increment.
- Signed/out-of-range defect thresholds are explained by ordinary order bounds; the Lean defect API intentionally states q : NNRat with q<=1.
- The hidden mixture’s all-horizon law and exact half atomic mass are an ordinary derivation backed by the actual evaluator formula and finite kernel checks, not a new kernel theorem of the infinite-law identity.
- This is an additive review verdict, not owner integration, general repository acceptance, T20 closure, or a philosophical consequence. Protected repositories and author source bytes were not edited.

## Expected-rejection controls

All four author negative controls were independently rerun with --trust=0 against the reviewer's fresh objects and rejected specifically as false propositions: zero-denominator complement incorrectly equal to zero, hidden-mixture horizon-4 count incorrectly equal to eight, exact threshold incorrectly accepted as strict slack, and vacuous mass-one code incorrectly accepted as a strict witness. NEGATIVES.json records their exact source hashes and nonzero exits; kernel/*.negative.log retains diagnostics. These negative tests supplement the universal proofs and do not substitute for them.
