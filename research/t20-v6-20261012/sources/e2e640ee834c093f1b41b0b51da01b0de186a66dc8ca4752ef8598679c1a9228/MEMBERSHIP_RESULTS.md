# Atomic membership from exact finite observations

## Main advance

The actual positive-singleton mass of any finite measure on Cantor space now has a kernel-checked hard-threshold cylinder representation. The formula supplies an alternative to the repository's ordinary cylinder-excess integral argument; it does not claim to have formalised that original formula.

Let C_n(x) be the length-n cylinder containing x, and H(k,n) the set of x whose cylinder mass is at least 2^-k. Then

    atomic_mass(μ) = sup_k inf_n μ(H(k,n)).

The threshold is fixed before the infimum over depth. Inclusive comparison is intentional. Each H(k,n) is a finite disjoint union of cylinders, so its mass is exactly the sum of the masses of those cylinders. Nested cylinders separate every Cantor point, and finiteness permits continuity from above. The union of all positive thresholds is exactly the set of positive-mass singletons.

## Actual program binding

FiniteOutputTable enumerates all N-bit input words, executes the actual causal prefix evaluator at each output position using only the available prefix, and counts preimages of an output word. Its nonnegative rational table is count divided by 2^N. The kernel identifies this table with the actual fair-Cantor output-law cylinder mass, including N=0, malformed numeric codes and nonbinary arity under the explicit zero fallback.

RationalNormalForm converts the heavy-set masses into exact rational finite sums. NumericMembership supplies a concrete natural-number matrix: decode a nonnegative rational by unpairing the outer natural into numerator and denominator, test whether it is below one, and compare it with the finite rational heavy sum. Every nonnegative rational has such a code. The kernel proves

    e has zero defect iff for every i there exists k such that for every n,
    membershipMatrix(e,i,k,n).

It also proves the complementary exists-forall-exists normal form. The matrix definition evaluates no measure or infinite stream; it uses decoded finite syntax, finite Boolean word enumeration and exact rational arithmetic.

## Evidence levels and classification

The actual measure identity, finite-table identity, rational comparison conversion, rational-code surjectivity, and natural quantifier equivalences are Lean theorems. A separate sealed source-driven argument shows that the actual decoder, finite syntax evaluator and finite table terminate uniformly and are effective. This is ordinary mathematical reasoning about the executable definitions, not a complete Mathlib Computable certificate for universal evaluation.

Together, the natural normal form and that uniform algorithm establish ordinary Π^0_3 membership for the exact total numeric presentation. The independently checked primitive-recursive reduction from every fixed jointly primitive-recursive Π3 normal-form matrix supplies the lower bound. With the standard arithmetical-hierarchy normal-form theorem, the ordinary consequence is Π^0_3-completeness of zero defect and Σ^0_3-completeness of positive defect under computable many-one reductions. This reconciles and strengthens the evidence for the repository's existing ordinary classification; it is not a historical novelty claim or a single fully mechanised hierarchy-library completeness theorem.

## Boundaries

- This is positive-singleton mass; general measurable-space atom terminology must not silently replace it
- Cantor separation and finite total measure matter; reversing the quantifier order admits diffuse fair measure
- The rational comparison uses q<1, not q=1; the supremum need not be attained at one finite threshold
- A total computable universal LOOP evaluator is not uniformly primitive recursive
- Mathematical termination does not promise host runtime, memory, stack or execution-budget acceptance
- No canonical programme cell is adopted or closed by these shadow results

The final receipt and independent review, rather than draft source compilation, control the qualification status.
