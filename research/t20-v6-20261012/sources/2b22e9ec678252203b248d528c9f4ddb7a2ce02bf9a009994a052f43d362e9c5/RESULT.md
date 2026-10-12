# Constructive source Sigma completion equivalence

## Verified theorem

`SigmaCompletion.eta_iff_elimination` proves an exact equivalence of source-rule schemas, without changing or extending HasE:

1. At every original-source typed dependent pair z : Sigma(A,B), there exists a HasE identity proof z = pair(fst z)(snd z).
2. For every original-source formed motive P over Sigma(A,B), and every original-source branch d : P(pair(a,b)) in the dependent context b:B,a:A,Gamma, there exists a HasE result of type P(z). The result is also raw PolyConv-convertible to d with fst z and snd z substituted for the branch variables.

`eta_iff_weak_elimination` proves the same equivalence when the elimination schema asks only for a typed result, without computation. Thus computation is not smuggled into the converse as an eta-like premise.

## Exact scope

These are metatheoretic schemas, not new constructors, adopted axioms, internal equivalence types, or a proof that either schema holds in the present calculus. They quantify over all source telescopes, domain and dependent codomain types, arbitrary motives, and branches. Ctx, Form, the branch, and the scrutinee use the original Has calculus. The eta witness and resulting elimination use actual HasE.

The result does not assert elimination for arbitrary HasE-formed motives, HasE branches, or HasE-only scrutinees. Extending to those would require corresponding verified structural lemmas. The already frozen SigmaRaw countermodel is untouched.

## Construction and obligations

- `pair_substitution` constructs the actual MixedSubstitution for replacing the two branch variables by a and b, including dependent lookup cancellation and the tail context.
- `branch_type_at` proves the exact syntactic equality of the substituted branch type with P(pair(a,b)).
- `branch_has` applies the existing original-source mixed-substitution theorem; no general HasE substitution rule is assumed.
- `reconstruction_has` derives the reconstructed pair from source projection and introduction rules.
- `identity_sym` derives the required orientation of the explicit HasE eta witness using J and an original-source formed identity motive.
- `elim_of_eta` applies J to transport the instantiated original branch from P(reconstruction(z)) to P(z). The arbitrary motive is genuine dependent elimination, not a renamed eta type.
- Conversely, `eta_motive_formed` constructs the original-source motive Id z reconstruction(z), and `canonical_eta_branch` supplies its original-source branch using raw pair beta conversion. Applying the elimination schema to this fully checked motive/branch yields eta.

All motive formation, context weakening, dependent lookup, and substitution equations are discharged in the file. The imported `RigidityInitiality.transport_source` is a proved source-derived J helper; none of the constructive theorems assumes Rigidity.

## Computation and no UIP

`elim_pair_computation` proves the expected canonical-pair equation in raw source PolyConv:

elim d (pair a b) e = d[b/0,a/1]

The actual source J polynomial erases to its branch for any equality proof. Consequently `elim_erases` proves a stronger raw equation at every z. This does not assert raw pair eta, raw equality of identity proofs, equality reflection, or UIP.

`elim_pair_identity` separately derives a typed HasE identity witnessing canonical computation, with both endpoints independently typed in P(pair a b). Raw computation is established first, not inferred from propositional identity.

## Validation

Run `bash hase-sigma-elimination-equivalence-20261010/check.sh` in the retained workspace. Lean 4.19.0, --trust=0. All printed proof dependencies are at most propext and Quot.sound; canonical raw computation is axiom-free. No sorry, extra axiom, or protected edit is used.

Frozen candidate source: Constructive.lean SHA256 254b95f0b02765d1b3018f256299af432083ac7f2bcdd0d4d99f538e50c861c7.

Independent review is separate. INPUTS.json records candidate and retained source/object hashes. Existing campaign baseline objects are reused without rebuilding them.
