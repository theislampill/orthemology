# Independent internal review: shared proof overlap information

9 October 2026. Review of the superseding frozen `shared-proof-overlap-information-20261009` packet. This review and its receipt are outside the author's directory.

## Disposition

Accept the corrected bounded written transport at its declared scope. No unresolved mathematical or executable-control defect was found. One overbroad information-loss statement was reported, supported by a concrete counterexample, and corrected before acceptance. The unit-weight parity obstruction was unaffected.

This is an independent internal review of written mathematics, inherited source mapping, and bounded execution. It is not external human review, a new kernel theorem, formal certification, source warrant, an optimization advance, integration, adoption, or T20 closure. Acceptance binds only the exact bytes in `REVIEW_RECEIPT.json`.

## Finding preserved and resolved

The first frozen report said the full scalar record does not reconstruct node identities or unused weight. This needed two qualifications:

1. With a known finite inventory having weights 1, 2, 4, and so on, the singleton intersection scalar uniquely identifies that branch's footprint by binary expansion. The scalar map is not generally injective on labelled footprints, but some declared inventories make it injective.
2. The report already declares N and w known. Their sum gives total inventory weight, so `h(empty) = total weight - union cost` is recoverable in this interface. It is undetermined only from the nonempty scalar record alone when the total is unavailable.

`INITIAL_FINDING.json` preserves the initial report digest, exact disputed passage, an eight-subset separating-weight counterexample, and the scope of the correction. The superseding report explicitly states both qualifications. No change to the script or the unit-weight counterexample was necessary. This was a scope correction, not a defect in inclusion–exclusion or the no-decoder proof on its stated unit-weight family.

## Source-to-target mapping

I read the actual inherited real typed-word and free-basis definitions, the finite-record channel, Theorem 4.2/Corollary 4.3, Theorem 5.1/Corollary 5.2, and the basis-dependent contraction passages in `INHERITED_GRADED_INTERFACE.md`. I also inspected the relevant identity-alignment and arithmetic-versus-Boolean discussion in the qualitative tensor report, Theorem 2 and its raw-data warning in `productive-identifiability/THEOREMS.md`, and the predecessor proof-DAG contract and implementation. The previously reviewed shared-cost report supplies the synthesis/validation boundary.

The mapping respects these sources:

- Each branch role has a free real vector space on the same explicitly aligned paid-node inventory. The vector coefficients are Boolean incidence values; arithmetic remains real addition and multiplication. No real sum is identified with Boolean OR.
- Footprints map bijectively to coefficient-one supports in the role vectors. This is faithfulness at the footprint level only. It neither reconstructs proof structure nor manufactures a semantic identity alignment.
- The diagonal covariant tensor carries each node's weight once. Contracting with a selected role product therefore computes the weighted intersection. Weighting every input vector instead would incorrectly multiply the weight repeatedly.
- The inherited fibre theorem applies once the input domain is supplied valid proof bundles, the representation is the restricted list of scalar intersection costs, and the target is union cost. Equal summaries and unequal costs then forbid a decoder of that representation.
- The inherited parity theorem supplies equality of proper probability marginals. The report establishes the new union-cost target separately by counting the zero word. It does not assume that an obstruction for parity expectation automatically proves an obstruction for every observable.
- The histogram inverse is the standard Boolean-lattice inversion already used in the productive-identifiability source. None of that source's causal or intervention assumptions is imported into this proof-cost application.

No new external-source claim was needed to evaluate these elementary identities and the supplied inherited passages. I did not repeat the author's bounded local priority search or claim historical exhaustiveness.

## Identity and validity contract

The union-price equation is correct for compatible supplied branches of a globally identified acyclic proof graph. A shared identity must have the same rule application, ordered references, scope, and price. Equal local indices, judgement labels, rule names, or evidence tokens are insufficient on their own. The report explicitly retains these restrictions.

Positive-price nodes form the cost footprint; zero-price structure remains part of the valid proof. A parent's own positive charge is additional because acyclicity prevents the parent from occurring below itself. Empty footprints and an empty bundle give zero cost. The extraction is an observable-specific view, not a validator or a complete provenance representation.

The script's constructed grammar uses a unique paid leaf per inventory identity. Its label-based footprint extraction is sound for those constructed witnesses. It is not presented as a generic identity-merging algorithm for arbitrary separately numbered DAGs. The separate duplicated-leaf control correctly shows that two occurrences of the same admitted rule can cost two, while one shared occurrence costs one.

## Same-grammar realization

The three-branch example is valid. In the common grammar, q1 uses p2/p3, q2 uses p1/p3, and q3 has the two alternatives p1/p2 and p0/p3. All structural charges are zero and all paid leaves cost one. Thus both bundles have individual costs 2 and pairwise intersection costs 1. Their triple intersections have costs 0 and 1, yielding total costs 3 and 4.

Both are actual admitted, root-reachable, acyclic proof DAGs. The even certificate does not store unused p0 as an unreachable node; p0 remains an available rule in the common grammar. This distinction is essential and correctly implemented. Every extracted branch is remapped into its own valid premise-first sub-DAG. Shared identities refer back to the original paid leaves.

The general construction uses one paid leaf per inventory member, branch rules for the requested footprints, and a parent requiring every branch. Any finite set of footprint alternatives can be represented in a suitable common synthetic grammar. It does not assert that they are realizable in an arbitrary independently fixed grammar. Natural weights lie within the written predecessor contract; exact rational controls use the actual Python interface's admitted extension, as the report now explicitly states.

## Algebra and information restrictions

For each nonempty role set J, the diagonal contraction is the sum of weights whose incidence product is one. Weighted inclusion–exclusion follows by expanding `1 - product(1 - a_i)` for Boolean incidences and summing nodewise. Each node used by at least one branch contributes exactly once.

The transforms `m(J) = sum_{K superset J} h(K)` and its alternating upper-set inverse are mutually inverse on nonempty incidence histograms. Substituting one into the other leaves the usual alternating interval sum, zero except on the diagonal. On realizable records h is nonnegative. Algebraic invertibility does not make every formal scalar array realizable with a prescribed finite inventory. Known total mass supplies the empty coordinate; proof edges and node identities are not generally recovered.

Full aligned incidence vectors already suffice to compute the union directly. The failed representation is specifically the retained scalar intersection coordinates, even with total inventory size and weight. The report does not claim failure of full uncontracted vectors or arbitrary lower-order tensor encodings. A single already-computed cost is sufficient for this one target, so there is no minimality claim for the complete intersection panel.

For general b at least 2, indexing identities by their first b-1 bits aligns the even and odd rows. The first b-1 footprint rules coincide and only the final branch needs two alternatives. Fixing the coordinates of a proper J to one leaves one parity constraint on at least one remaining bit, giving `2^(b-|J|-1)` rows in either table. Zero incidence occurs only on the even side. The union costs are consequently `2^(b-1)-1` and `2^(b-1)` on the same known unit-weight inventory. These unequal costs inhabit one proper-intersection-summary fibre.

Choosing b larger than any fixed retained order proves the stated no-decoder result in this family. It is not a time, memory, tensor-rank, minimal-encoding, or unavoidable-high-degree lower bound. The report explicitly notes exponential parity inventory size and degree-one sufficiency when raw incidences are retained.

## Bounded execution and currentness

I executed an exact copy of the frozen script with Python bytecode writes disabled. The copy ran in a temporary tree with read-only symlinks to the six actual predecessor inputs. Its check output was confined to that temporary tree, then compared byte-for-byte with the author's recorded output.

All 369 assertions passed. They cover parity sizes 2 through 6, same-grammar paid footprints and valid branch sub-DAGs, equal proper intersection summaries, union values 1/2, 3/4, 7/8, 15/16, and 31/32, diagonal formulas, both histogram round trips, and four additional weighted/empty/repeated bundle cases plus identity controls. All six frozen input hashes and byte counts matched before and after execution. `EXECUTION.json` records the bound report, script, manifest, output equality, and checks.

The final receipt separately binds all authored manifest entries, the six current predecessor inputs, and the reviewer artifacts. The reviewer did not modify authored files or predecessors. These finite controls corroborate the written derivation; the general parity and algebraic arguments were reviewed directly rather than inferred from enumeration.

## Significance and stopping boundary

The bounded addition is a valid-proof realization and cost-observable interpretation of inherited overlap-information loss. Fibre sufficiency, parity cancellation, contractions, and inversion remain inherited/classical. No general originality, faster evaluation, optimal bundle selection, escape from Set Cover hardness, source authentication, cross-context reuse licence, physical runtime model, or source-warrant result follows. The report's significance and stopping claims respect these limits.
