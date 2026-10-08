# Nonuniform completion: checked scope and exact frontier

3 October 2026 UTC. Separate authorized mathematical extension. The earlier four-module packet and manifest are preserved unchanged.

## Checked result

All four new Lean 4.19.0 modules and 33 theorem dependency readbacks passed a clean final replay. There are no proof holes, custom axioms, resource increases, or final compiler warnings. The only dependency axioms are standard `propext`, `Classical.choice`, and `Quot.sound`.

The theorem family uses an arbitrary dependent family `X : Nat -> Type u` and bonding maps `f_i : X_(i+1) -> X_i`. Neither the spaces nor the maps are required to be constant. No injectivity, surjectivity, quantitative contraction, or common metric bound is assumed.

### General indexed composition

`IndexedCompletionCore.lean` defines actual finite composites by natural-number recursion. Identity, one-step, composition, right-extension, and leftmost-bonding-map laws are proved. It defines compatible full paths, finite-depth survival at each coordinate, all-coordinate singleton survival, and exact uniqueness including existence. Every compatible path supplies every finite-depth predecessor. The finite-path construction and continuity of finite composites are also checked.

### Compact Hausdorff inverse-limit projection

`IndexedCompletionCompact.lean` proves, for each nonempty compact Hausdorff coordinate space and continuous bonding map:

- A compatible infinite realization exists.
- For every coordinate i and every value y in X_i, y survives every finite extension if and only if some compatible full realization has i-th coordinate y.
- Singleton survival at every coordinate is equivalent to exactly one compatible full realization.

The proof uses the compact product of all coordinate spaces and decreasing closed sets of finite compatibility constraints. To realize a prescribed survivor, it adds the closed constraint that coordinate i equal that survivor. Nonemptiness of each finite constraint set is proved from an actual sufficiently remote predecessor. This is standard compact inverse-limit mathematics implemented directly through Mathlib compact intersection, rather than a compatibility-extension assumption.

The topological result genuinely earns compact Hausdorff generality. No metric is needed in this module. Classical choice and product compactness are disclosed and are not presented as effective construction algorithms.

### Compact metric forgetting equivalences

`IndexedCompletionForgetting.lean` specializes to arbitrary nonempty compact metric coordinate spaces. It proves:

- All-coordinate singleton survival gives uniform attraction to a compatible path b, separately at each fixed coordinate i.
- This attraction implies pairwise shrinking of each finite-extension range.
- Pairwise shrinking forces singleton survival at every coordinate.
- Coordinatewise shrinking is equivalent to uniform remote-boundary forgetting at every fixed finite horizon.
- Coordinatewise attraction to b is equivalent to finite-horizon attraction to b.
- Exact uniqueness is equivalent to finite-horizon attraction to a compatible path.

The finite-horizon predicate is explicitly:

For every H and epsilon > 0, there is N such that, for every j >= N with H <= j, for every i <= H and every pair u,v in X_j, the distance between their transported i-th values is below epsilon.

The one N covers all coordinates in the chosen finite horizon and all admissible boundary values. H is fixed before N is selected. The attraction version compares each transported value with b_i; the b_i may differ, and no common fixed point is inferred.

`IndexedCompletionDiameter.lean` further checks ordinary real-valued `Metric.diam` convergence. It verifies that the pairwise epsilon condition is equivalent to the diameter of each fixed coordinate's extension range tending to zero. Each such range is compact and bounded, so Mathlib's convention assigning diameter zero to unbounded sets cannot cause a spurious result.

The packaged theorem `nonuniform_four_way` proves:

1. All-coordinate singleton survival iff exact uniqueness.
2. Exact uniqueness iff every fixed coordinate's range diameter tends to zero.
3. Those diameter limits iff fixed-finite-horizon forgetting.

### Technical indexing convention

`extensionRange f i j` is the actual finite-composite range whenever i <= j. For j < i it is padded by all of X_i solely to obtain a decreasing sequence indexed by every natural number. `extensionRange_of_le` and `survival_iff_all_ranges` verify the connection to the original survivor definition. The finite early prefix cannot affect a limit at infinity. This does not identify different coordinate spaces or narrow the admissible remote boundary values.

## Precise frontier

The approved equivalence and inverse-limit projection targets are checked. No proof gap is hidden behind an ordinary-only label.

The finite-horizon uniform statement is mechanised in its exact epsilon/all-coordinates/all-boundary-values form. A separately named scalar expression involving a real supremum over boundary pairs of a finite maximum, and the identity exchanging that supremum with a finite maximum of diameters, are not formalised here. No claim is made that those particular scalar-expression identities have been checked. The actual coordinate diameter limits and their equivalence to the uniform finite-horizon predicate are checked.

The following remain ordinary-only in the proposal:

- The example separating fixed-horizon forgetting from uniformity over all starting times.
- Arbitrarily slow convergence and absence of a general effective rate.
- The observer-quotient example and its explanatory interpretation.
- Quantitative Lipschitz-rate corollaries.
- Source-domain applicability, modal adequacy, metaphysical possibility, concrete existential actuality, and original-source claims.

No global mathematical novelty is claimed. These are standard inverse-limit/compactness results applied at a precise indexed interface. No runtime extension, publication, canonical edit, or source exposition is included.

## Evidence and preservation

Final evidence directory: `logs/final-validation-20261003T1245Z/`.

- Core: 5.212 seconds, exit 0
- Compact inverse limit: 5.983 seconds, exit 0
- Metric forgetting: 6.063 seconds, exit 0
- Diameter equivalence: 4.080 seconds, exit 0
- Readback: all 33 theorem dependency checks passed

Each compiler call uses `timeout 180 lean -j1`; heartbeat and recursion-depth settings remain default. Only one compiler lane was used. Earlier unsuccessful development diagnostics are retained separately and are not treated as final-source validation evidence.

`validate.sh` performs a fresh sequential rebuild and readback and writes a source-bound validation report. `readbacks/IndexedCompletionReadback.lean` also prints exact definitions to expose quantifier order and dependent-space interfaces. `environment.txt` records the existing trusted Lean/Mathlib input identities; this is not a bootstrap verification claim.

The design input is `../NONUNIFORM_COMPACT_EXTENSION_PROPOSAL.md`, SHA-256 e225a2105081eb08b75e656dbd88352177b973636e69892c4316ff77598238eb. The original packet manifest remains SHA-256 5d7b52d653a818641b2fd818a95fc3a13a159dd89cd75bb597435b818f0a55d4, and all 33 artifacts bound by it still match. Preservation evidence is in `ORIGINAL_PACKET_PRESERVATION.json`.

Independent review has been requested and is not represented as already accepted.
