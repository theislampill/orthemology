# Exact effective membership matrix for numeric observer laws

## Qualified terminal result

Six new modules (MembershipWords, MembershipComputableCore, MembershipComputable, MembershipHeavyBridge, MembershipMatrixComputable, MembershipWitnesses) contain 35 public theorem targets. They were freshly rebuilt and individually type/axiom audited at the exact Lean4.19/Mathlib pins. The baseline and positive controls pass; wrong strict-threshold and unweighted-class-count assertions are rejected as false. Only propext, Classical.choice and Quot.sound occur.

Receipt: receipts/computable-matrix-20260930T173131Z/COMPUTABLE_MATRIX_RESULT.json.
SHA-256: 4b19312debc1d20ff5cb709817a6bc4aecd1a22cd172ed7dfce1144a97e3162c.

P02.Codec.UniformComputability.membershipMatrix_computable proves Mathlib Computable for decide(AtomicMembership.membershipMatrix(e,i,k,n)) jointly in all four natural inputs. The target is the unchanged predicate from the separately sealed NumericMembership module. membershipMatrix_nat_computable uses explicit nested Nat.unpair projections, and membershipMatrix_characteristic_computable provides a standard Nat-to-Nat 0/1 characteristic function. Neither endpoint carries a remaining effectivity premise.

The effective_membership_normal_form theorem pairs that certificate with the already proved actual zeroDefectIndices equivalence:

    e is in zeroDefectIndices iff forall i, exists k, forall n,
      membershipMatrix(e,i,k,n).

Thus the upper normal form now has an internally checked uniform computational matrix, rather than relying only on the ordinary total-algorithm argument. The prior primitive-recursive lower reduction for every fixed jointly PR forall-exists-forall matrix remains a separate immutable stage.

## Exact finite computation and measure bridge

allWords enumerates each length-N Boolean list exactly once. The proof establishes exact membership, no duplicates and a generic summation equality with the original finite-function words Fin N -> Bool. outputList runs the actual numeric evaluator at each output position on that position's available sentinel prefix. outputList_ofFn identifies it with the original finiteOutput; wordCount_exact identifies its filter length with the original preimageWords cardinality.

For each output word w, c(w) counts its N-bit source preimages. heavyCount(e,k,N) sums c(w) when 2^N <= c(w)*2^k and zero otherwise. It is an integer mass numerator, not a count of output classes. rationalHeavyMass_heavyCount proves that the existing rationalHeavyMass(indexTable e,k,N) is exactly heavyCount(e,k,N)/2^N.

The root's frozen MatrixArithmetic module then converts the original rational implication without approximation. For rational code i with Nat.unpair i=(a,d), the matrix is exactly:

    d=0 or d<=a or a*2^N<=d*heavyCount(e,k,N).

Zero denominators, rational codes at or above one, redundant fractions and inclusive threshold ties retain their original meanings. No bound on H was inserted as a premise to the arithmetic bridge.

## Computational certificate

Word enumeration, sentinel coding and variable list take are primitive recursive. outputList, wordCount and heavyCount are uniformly Computable using the previously sealed actual universal evaluator certificate. They are not claimed uniformly primitive recursive. General computable list mapping is proved through bounded range mapping and exact indexed lookup, so no unproved closure oracle is used.

All source-level local opacity annotations only control elaborator normalization of existing definitions. They change neither executable definitions nor theorem targets. The final proofs explicitly connect the integer algorithm back to the original rational predicate.

## Controls and boundaries

Kernel controls include invalid-index zero laws, identity-bit output above/below an inclusive dyadic threshold, zero observation horizon, zero denominator and vacuous rational one. Negative controls distinguish inclusive from strict thresholds and probability mass from merely counting distinct output classes. The independent reviewer is separately replaying richer mixed-output, redundant-fraction and numerical comparisons; those results have their own receipt.

This is this tranche's terminal computational extension. It completes the concrete numeric evaluator, actual finite-cylinder law, and uniformly effective membership-matrix proof obligations for the stated zero-defect normal form. It introduces no new threshold-mixture families or general arithmetical hierarchy framework. Interpreting the matched upper/lower normal forms as the conventional Pi3 classification uses the stated standard normal-form convention; no new library definition of hierarchy completeness is asserted here.

Full Python host-runtime/resource equivalence, canonical adoption and novelty are not claimed. Earlier seals remain unchanged, including their time-bounded statements of gaps that this later extension closes.
