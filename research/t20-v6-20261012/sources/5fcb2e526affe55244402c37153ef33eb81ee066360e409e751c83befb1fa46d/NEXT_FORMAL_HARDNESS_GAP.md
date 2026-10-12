# Feasibility check: the remaining rational-shift lower reduction

This is a bounded source inspection after freezing the accepted upper-cut Lean sources. It makes no additional theorem or completion claim.

## Finding

A real compiler/law bridge remains absent in the inspected current formal sources. This is **not just composition of already proved rational-shift theorems**. The ordinary lower-bound proof is already owned by C2-12; its exact Python `compile_shift(observer,a,b)` exists at `user-checkpoints/extracted/P02/code/prcodec.py:293–310`.

The formal `P02A2.ObserverCore.shift_eq_threshold`, `shift_le_threshold` and `shift_gt_threshold` prove only real affine algebra about q+(1−q)d. Their arguments do not mention `compile_shift`, a program index, an output law, stopping prefixes, or fair-source mass. They cannot supply the missing premise that the compiled observer's actual defect equals that affine expression.

The retained final archive was searched only within its Lean sources for `compile_shift`, `compileShift`, `shiftProgram`, `rationalSelector`, `stoppingWords` and prefix-free selector names. No corresponding implementation/law bridge was found. Targeted current repository searches for those formal identifiers were also empty; searching `shift_eq_threshold` returns the same affine-only declaration and its qualification records. SEARCH_SHIFT_FORMAL_RESIDUAL.json retains those results. This bounded negative search is not an exhaustive proof that no equivalent theorem exists under an unrelated name.

## Existing reusable pieces and their exact limits

- `FiniteSelector.selector` scans for the first zero, choosing the unary tag 1^i0. Its correctness theorems are `selector_on_tag`, `selector_before_tag`, and `selector_allTrue`. It does not implement comparison of arbitrary dyadic prefix cells with a rational cut.
- `TaggedRows.tagged_mixture_law` identifies the actual unary-selector observer law with a countable mixture weighted by 2^(-i-1). `selector_cover_ae` handles its sole all-true exceptional input.
- `TaggedMass.tagged_mass`, `tag_mass`, and the general `P02A2.mass_mixture` supply the atomic-mass transport machinery. The missing object is not an abstract mixture identity.
- `PrefixObserver.pi3PrefixValue_output` and `Pi3Program.numeric_observer_eq` connect the existing unary row construction to the actual old output/evaluator semantics.
- `PRCoverage.exists_program_of_primrec`, `CodecParameter.exists_parameterIndex_of_primrec`, and `CodecIndexPrimrec` supply actual compilation and primitive-recursive numeric specialization for a fixed jointly primitive-recursive family.
- `Pi3IndexReduction.exists_primrec_zero_defect_reduction` supplies the already formalized lower reduction to zero defect. It does not instantiate an arbitrary-rational shift of the resulting observer.

## If the target is the literal existing compile_shift

The substantive missing chain is:

1. Formalize/bind the compiler's bounded prefix scan and fresh/reset base-program invocation to its exact old Expr/Stmt and numeric codec. Prove the stagewise output equation, including the stopping prefix itself, unresolved boundary input, endpoint conventions, and untouched fresh tail.
2. Establish that the minimal stopping prefixes are prefix-free, that the below/above prefix events have fair masses q and 1−q, and that the unresolved event is null. Neither almost-sure resolution nor arbitrary measurable branching can substitute for total productivity on every input.
3. Use the existing restricted-tail, injective-prefix, and mixture mass lemmas to prove the actual compiled law's defect q+(1−q)d. Prove the required effective numeric index transformer.
4. Only then compose with the existing zero-defect reduction and the existing affine order lemmas. That last step really is short.

## A potentially smaller source-faithful route

If the goal is arbitrary-rational hardness in the **same original L1 evaluator**, rather than literal identification with Python compile_shift, the already proved unary-tag architecture can be reused. For fixed q=a/b in [0,1), let its binary digits select which unary-tag rows carry a fair diffuse copy and which carry the original base observer. The weights are already 2^(-i-1).

A new exact weighted-binary-expansion theorem must show that the diffuse-row weights sum to q, and a primitive-recursive mixed-row family must be connected through the retained compiler to the actual numeric law. For a<b, the digit formula floor(a*2^(i+1)/b) mod2 has partial weighted sum floor(a*2^N/b)/2^N and residual below 2^(-N). Use a fixed jointly primitive-recursive lower-reduction family; the arbitrary-index evaluator is only uniformly Computable and cannot be silently treated as Primrec. Then tagged_mass and the existing numeric-family machinery would yield the affine defect identity. This avoids reproving a general arbitrary-prefix stopping partition, but it is still a genuine new compiler/law and weighted-series proof. It must be credited as an alternative reduction, not as verification of Python compile_shift.

No accepted upper-cut source was modified to pursue either route. The literal compiler's semantics, endpoint behavior and previous ordinary proof keep their original ownership. T20 remains active.
