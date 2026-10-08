# Independent acceptance of the nonuniform completion implementation

3 October 2026 UTC. **Accepted within the exact scope below. No implementation or theorem-target defect found.** This is a distinct receipt for the nonuniform packet; it does not amend the earlier uniform receipt.

The reviewer authored the ordinary nonuniform derivation, `NONUNIFORM_COMPACT_EXTENSION_PROPOSAL.md`, but did not author this Lean implementation. The independence claimed here concerns implementation, mathematical-interface comparison, and validation. It is not independent discovery of the underlying argument. The mathematics is standard inverse-limit compactness.

## Bound inputs and fresh validation

The admitted nonuniform manifest is SHA-256 `e7e1eab2d7055f81738cec7515d34b7b3bd7d39bcb2a02411099695151662c18`. All 35 manifest members match, including the four Lean source modules. The design input remains SHA-256 `e225a2105081eb08b75e656dbd88352177b973636e69892c4316ff77598238eb`.

The original uniform manifest remains SHA-256 `5d7b52d653a818641b2fd818a95fc3a13a159dd89cd75bb597435b818f0a55d4`; all its 33 members were independently rehashed before and after this review and remain unchanged.

The four sources and author readback were copied into this new review directory without author-generated module objects. The initial reviewer object count was zero. Every module was rebuilt sequentially, with this review directory first on `LEAN_PATH`, using the existing Lean 4.19 / Mathlib environment. Commands used `timeout 180 lean -j1`, default heartbeat and recursion limits, and one compiler lane. No unrelated Ninth proofs were rerun.

| Fresh check | Seconds | Result |
|---|---:|---|
| IndexedCompletionCore | 12.428 | Pass |
| IndexedCompletionCompact | 5.885 | Pass |
| IndexedCompletionForgetting | 6.934 | Pass |
| IndexedCompletionDiameter | 4.096 | Pass |
| Author readback | 9.180 | 33 checks passed |
| Reviewer controls | 5.032 | 10 checks passed |

All final invocations returned exit 0 without warnings. Source inspection found no proof holes, custom axioms, unsafe proof shortcuts, or resource-limit increases. The 43 axiom readbacks depend only on `propext`, `Classical.choice`, and `Quot.sound`; two reviewer controls require no axioms. The existing compiler, kernel, operating environment, and Mathlib inputs remain trusted. This is not a compiler-bootstrap or independent-library verification claim.

## Exact mathematical scope

1. **Actual varying coordinate spaces and maps.** Core lines 10–46 define an arbitrary dependent family `X : Nat → Type u`, total bonding maps `X (i+1) → X i`, and actual finite composites using natural-number recursion. Identity, one-step, composition, and leftmost-map laws are proved. No fixed common carrier, stationary map, onto map, or quantitative contraction is hidden in the signatures.

2. **Survival and realization are distinct definitions.** Core lines 48–57 define compatibility, finite-extension survival, all-coordinate singleton survival, and exact uniqueness using `ExistsUnique`. Survival quantifies over all values of every remote declared carrier through an existential preimage. Exact uniqueness includes existence. These predicates are not renamed versions of one another.

3. **Projection equality is earned.** Compact lines 43–104 prove realization existence, realization of each survivor, exact projection equality, and all-coordinate singleton survival iff exact unique realization. Readbacks retain nonempty compact Hausdorff coordinate spaces and continuous bonding maps. The proof uses closed finite-compatibility sets in the compact product. For prescribed survivor y at coordinate i, each finite constrained set is populated by an actual predecessor at coordinate max(i,n). It never assumes that an arbitrary predecessor is itself a survivor. Metric structure is absent from these topological theorem signatures.

4. **Range indexing matches the ordinary statement.** Forgetting lines 14–54 pad ranges below i by the full carrier solely to obtain a natural-indexed decreasing family. At every relevant j≥i, the range equals the image of the actual finite composite. The checked survival equivalence and the finite irrelevant prefix prevent the padding from changing survival or asymptotic claims.

5. **Uniformity has the intended order.** Forgetting lines 56–75 choose each coordinate i, or each finite horizon H, and epsilon before the bound N. The bound then covers every sufficiently remote j, every i≤H, and every admitted pair of boundary values in X_j. It is not selected separately for each boundary value or each coordinate within the chosen horizon. Lines 150–180 prove the coordinate/finite-horizon equivalences by taking a finite maximum of coordinate bounds. There is no bound uniform over every starting time, no common limiting state across unlike carriers, and no supplied convergence rate.

6. **Diameter is the genuine bounded-range quantity.** Diameter lines 14–57 prove ordinary real-valued diameter convergence and the packaged four-way equivalence. The reverse diameter implication explicitly uses compact bounded extension ranges, avoiding Mathlib's zero-diameter convention for unbounded sets. The complete theorem retains nonempty compact metric coordinate spaces and continuity. Forgetting lines 193–203 also prove exact uniqueness iff finite-horizon attraction to a compatible, possibly varying path.

These are the ordinary proposal's main equivalence and projection targets. The compact-product proof is an alternative to the proposal's surviving-predecessor construction and supplies the same conclusion under the stated hypotheses.

## Independent interface controls

`ReviewerControls.lean` contains ten checked lemmas supporting three groups of controls:

- A generic dependent-family constant-map system has exactly one full path and the expected survivors. Instantiating it at `X_i = Fin(i+1)` checks changing coordinate cardinalities. The map at coordinate 1 is proved non-surjective while the full system is uniquely completed. This is a positive interface control, not an added hypothesis.
- The Boolean system with a constant first map and identity later maps has singleton survival at coordinate zero but two explicit compatible paths. The all-coordinate premise cannot be replaced by determination of the first coordinate alone.
- With empty carriers, fixed-horizon forgetting is vacuous; an empty coordinate zero precludes any full realization. These are generic checked statements under explicit emptiness hypotheses. They expose why the final equivalence must preserve an existence resource.

The earlier complete bounded discrete countercontrols remain covered by the separate uniform acceptance. This review does not pretend these new interface controls newly mechanise every ordinary example or establish necessity of every displayed sufficient hypothesis.

## Acceptance boundary

The scalar supremum of a finite maximum and its separately named equality with the maximum of coordinate diameters remain ordinary-only. The exact epsilon formulation of finite-horizon forgetting and its equivalence to actual coordinate diameter limits are checked. This distinction is accurately stated in the packet.

Time-uniform separation, arbitrarily slow convergence, numerical or effective rates, Lipschitz corollaries, and the observable-quotient example remain ordinary-only. No determination of one query is treated as determination of the complete state. Uniform Control C, eventual compactness, and contraction claims are not newly included by this receipt.

Applicability to explanatory laws requires justification of the declared carriers, total maps, compactness, continuity, and the relation between all algebraic paths and any selected class of worlds. None is supplied by successful compilation. No physical actuality, metaphysical possibility, productive efficiency, existential source, or source-wide philosophical result is certified.

This receipt makes no publication-status determination and adds no source exposition. Any later attribution remains to the inspected proof-marked witness unless a final version is separately verified. No external contact, publication, or canonical edit occurred.

Evidence: `REVIEW_VALIDATION.json`, `INPUT_VERIFICATION.json`, `logs/AuthorReadback.log`, `logs/ReviewerControls-01.log`, the four fresh build logs, copied source modules, and `logs/environment.txt` in this directory.
