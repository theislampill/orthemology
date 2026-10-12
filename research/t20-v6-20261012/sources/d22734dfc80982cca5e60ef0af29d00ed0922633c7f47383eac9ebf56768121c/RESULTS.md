# Canonical carrier projection for the P01 dependent fragment

## Result

This is a separate post-seal extension of the raw-index dependent successor. It proves exact equalities of unary canonical `Code` values for the lawful Pi/Sigma/Id cases, and source-preserving admission corollaries. It does not rewrite the predecessor's sealed report or claim equality for the entire recursive model.

The canonical constructor source owners are `InternalPolymorphism.lean` and `EffectsAndDependence.lean`. Qualification checks their bytes against the actual canonical checkout at 03e2604dfcef278b01c60d19b05370fcec4194b6, not just against a shadow file with a similar name.

## Construction and exact squares

`carrierCode P` forgets a PER's relational equality and retains exactly its domain `P(t,t)`. Raw-conversion saturation proves this is a canonical `Code`. The raw PER's carrier is canonical `Code.top`.

For a family B with derived raw-conversion coherence:

- `raw_pi_carrier_square`: the carrier of PiPER(rawPER,B) equals canonical dependentPi(carrier(rawPER), carrier(B))
- `raw_sigma_carrier_square`: the carrier of represented SigmaPER(rawPER,B) equals canonical dependentSigma with those carriers
- `raw_identity_carrier_square`: the carrier of IdPER(rawPER,x,y) equals canonical equalityCode(carrier(rawPER),x,y)

The Sigma theorem is also proved for an arbitrary domain PER P when both P-relational coherence and global raw-conversion coherence of the fibre family are explicitly supplied. The raw-index syntax supplies both from its already-checked transport theorem.

`syntax_pi_carrier_square`, `syntax_sigma_carrier_square`, and `syntax_identity_carrier_square` instantiate these equalities with the actual recursive syntax interpretation. The corresponding canonical admission theorems send every relevant `Has` derivation to membership in the unchanged canonical constructor **with the exact same evaluated source polynomial**.

These are equalities of Code values, not just unnamed existence results. The proof does not add raw eta, conversion reflection, a new canonical constructor, or an approximation of the encoded pair.

## Why the Pi restriction matters

A PiPER tests every pair of related inputs, whereas canonical dependentPi asks only unary membership at each input. For rawPER inputs, related arguments are canonically convertible, so application congruence and fibre saturation derive the cross-input condition from the unary one. This is the substantive reason the square is exact.

For an arbitrary domain PER, the reverse implication fails. The checked counterexample uses the universal PER as domain and rawPER as codomain. I preserves both unary carriers, but would have to send all related inputs to raw-convertible results in the relational arrow. I and SKK refute that requirement. General arrow projection is proved only in the lawful relational-to-unary direction.

## Why the identity restriction matters

Canonical equalityCode requires raw Conv of its endpoints. General IdPER requires only the domain PER's relation. Thus canonical equality always implies PER identity after forgetting, but the reverse implication can fail. The checked example uses the inhabited polymorphic identity PER, where I and SKK are related despite not being raw-convertible. Its PER identity is inhabited while canonical equalityCode is empty.

No equality between arbitrary AllPER and canonical unary All is claimed. No syntax-wide equality obtained by recursively replacing every PER constructor with canonical constructors is claimed: arrows, arbitrary identity, and polymorphic quantification retain independent obligations.

## Scope and preservation

This closes a real part of the previous source-projection obligation: top-level raw-index Pi/Sigma/Id constructions and their compiled inhabitants now have exact canonical carrier squares. It does not close full U11, arbitrary typed dependent contexts, universal frontend refinement, full normalization, or canonical adoption.

The predecessor ZIP `P01_Raw_Index_Dependent_Successor_2026-09-30.zip` remains byte-identical with SHA256 dec5951de21c2ef0918f9eb6da130907e4dba4df213dd84ef04209aa251840cc. The original recursive successor and canonical checkout also remain unchanged.

The final qualification rebuilt 30 local modules before the audit and checked 19 declarations, including 16 theorem declarations. Its axiom union is only propext, Quot.sound and Classical.choice.

The authoritative evidence is `qualification-final/QUALIFICATION.json`: fresh local dependency rebuilding, exact-pin compiler and package checks, source/driver/artifact identities, full target type/axiom readback, and source-hygiene checks. Main-module diagnostics must be empty. No novelty or external expert-review claim is made.
