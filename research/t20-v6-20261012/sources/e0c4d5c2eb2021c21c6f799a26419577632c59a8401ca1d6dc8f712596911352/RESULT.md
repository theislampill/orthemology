# An actual source-level graph invariant, with exact projection boundaries

10 October 2026. **The literal `HasE [] c3 (W q)` remains OPEN.** This pass does construct a nontrivial dependent graph iteration in the original source grammar. It does not turn semantic standardness into a source proof, prove noninhabitation, or claim a new general mathematical theorem.

## The gained judgement

Let S be the unchanged source pair-state type `Sigma N N`, Delta the actual retained `diagonalStep`, and z0 its actual `diagonalZero`. In the scalar context `Gamma = [alpha, alpha -> alpha, N]`, write n, f, a for variables 2, 1, 0. Define

    h(s) = snd(s) f a
    G = Sigma s:S. Sigma x:alpha. Id_alpha(x, h(s)).

The new checked construction is the strong graph step

    g(s,x,e) = (Delta s, f x, ap(f,e) ; computation),

where `e : Id_alpha(x,h(s))`, `ap(f,e)` is derived with the actual source `Has.j`, and the second identity comes from the unchanged raw computation

    h(Delta s) converts to f(h(s)).

This step genuinely advances the old scalar coordinate by f. It is **not** the weaker recomputing assignment `x := h(Delta s)`. The seed is the source pair

    b = (z0, h(z0), reflexivity),

whose scalar coordinate converts to a. Formation of G, typing of b and g, impredicative instantiation of n at G, and both Sigma projections are all checked in the actual grammar.

For `r = n g b`, the final gained source judgement is

    HasE Gamma (snd(snd r))
      (Id_alpha(fst(snd r), h(fst r))).

This is `literal_graph_invariant`, not merely a semantic graph membership assertion. Its general precursor `iterated_invariant` assumes original `Has Gamma n N`, `Has Gamma f (alpha -> alpha)` and `Has Gamma a alpha`; the derivation is first constructed in original Has and then included into HasE. The literal variable context meets these premises. No general theorem over arbitrary HasE-only input derivations is claimed.

## What was actually built and tested

`InternalGraph.lean` imports the original source objects and adds only scratch definitions/proofs:

- `graph_form`, `graph_pair_has`: the exact dependent Sigma graph and its constructors
- `congr_app_has`, `trans_has`: congruence and identity composition using explicitly formed, two-coordinate source J motives
- `delta_has`, `zero_has`: the unchanged compiler's actual state step and seed are typed at S
- `poly_beta`, `delta_beta`, `succ_beta`, `image_delta`: positive raw computations using only the inherited seven-constructor PolyConv, without eta or a new conversion rule
- `strong_step_body_has`, `strong_step_has`: the actual f-on-old-scalar graph lift
- `graph_run_has`, `iterated_invariant`: the actual Church instantiation and extracted source identity

`ProjectionBoundary.lean` additionally checks all four algebra-morphism computations:

    fst(g z) converts to Delta(fst z)
    fst(snd(g z)) converts to f(fst(snd z))
    fst(b) converts to z0
    fst(snd b) converts to a.

Thus the construction has the intended step and seed compatibility; this is not a proposal that quietly assumes the difficult preservation obligation. `original_scalar_computation` invokes the imported `redundant_closed_exact` to bind the original q, establishing

    (q n) f a converts to h(n Delta z0).

No compiler replacement or formula-only mirror is substituted for q.

## The two exact remaining judgements

A sufficient route for projecting this graph iteration back to the two external iterations would supply evidence of the following *formed* identity types in Gamma. These are not claimed to be necessary for every scalar-fusion proof:

    stateTransport = Id_S(fst(n g b), n Delta z0)
    scalarTransport = Id_alpha(fst(snd(n g b)), n f a).

`state_transport_formed` and `scalar_transport_formed` check their actual source formation. They are legitimate candidate proof goals, unlike the earlier malformed Raw-endpoint J motive. Neither is assumed, postulated, or proved here.

With those bridges, ordinary identity congruence/composition would connect the gained graph invariant to `Id_alpha(n f a, (q n) f a)`. This paragraph identifies the remaining proof structure; this package does not assert a checked conditional reduction theorem from arbitrary HasE proofs of the two bridges to W(q).

The ordinary graph-parametricity argument would supply precisely these bridges because both projections commute with the step and seed. It is not enough to instantiate n at G and project: that produces `fst(n g b)` and `fst(snd(n g b))`, not the external `n Delta z0` and `n f a`. The source allElim constructor changes the instantiated type while retaining the same polynomial; it does not add an identity relating these projected applications. The source piExt/allExt schemas compare endpoints at a common displayed type and require actual pointwise identity evidence. They do not consume the checked commuting squares as a graph-fusion premise. An application of J also needs a supplied identity; the source J uses already constructed graph-coordinate evidence in the strong step, but does not itself provide either bridge.

These statements describe where this concrete construction stops. They do not classify every possible J motive, every proof of the two bridges, or every alternative proof of scalar fusion.

## Projection-specific conversion obstructions

Both temptations to close the remaining bridge by raw conversion are now refuted against the actual PolyConvPlus, including its atom/application bridge. These tests are different from the inherited nonconversion of the original p/q or scalar endpoints.

For the state projection, use the arbitrary **untyped** raw valuation assigning n the constant-two-argument operation `K(K I)` and f,a the raw I. Both `n g b` and `n Delta z0` reduce to I. Their compared endpoints therefore reduce to K and I:

    fst(n g b) -> K
    n Delta z0 -> I.

They are distinct raw normal forms. `state_projection_not_conversion` proves the precise open PolyConvPlus nonconversion.

For the scalar projection, instead assign n the raw `K(K K)`. Both graph and scalar iteration results reduce to K. The compared endpoints reduce to K I and K:

    fst(snd(n g b)) -> K I
    n f a -> K.

Again distinct normal forms. `scalar_projection_not_conversion` checks the second exact open PolyConvPlus nonconversion.

These valuations are used only because source raw conversion is sound under every raw valuation. They are **not** asserted to satisfy the typed Church context; they are not new nonparametric N elements, Henkin models, or separators of HasE. Consequently the tests rule out identityIntro's raw-conversion shortcut for these two displayed endpoints, not their possible typed identities obtained through J/extensionality. The earlier warning against introduction inversion remains intact.

## Verification and immutable inputs

Both files compile under Lean 4.19.0, `--trust=0`. The displayed main theorem axioms are only ordinary Lean `propext`, `Classical.choice`, and `Quot.sound`; the two J helper theorems omit Classical.choice. There are no admitted proofs, custom axioms, or unsafe implementations. The classical dependencies arise in the imported proof infrastructure and are not an added object-language axiom.

The existing 83-module pinned closure comes from `theislampill/orthemology` commit `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`, as recorded in the predecessor acquisition manifest. The unchanged `ScalarFusionCore.lean` SHA-256 is `975e2220158cf6b285cc994e36c408389a908c77e0f63bfa028c8cb416319618`. Existing verified prerequisite objects are reused read-only; this is a new-file replay, not another claimed reconstruction of the entire closure. No original source, compiler, conversion relation, previous evidence, or protected repository state was modified.

From the workspace root, run:

    bash hase-internal-graph-20261010/check.sh -o hase-internal-graph-20261010/InternalGraph.olean hase-internal-graph-20261010/InternalGraph.lean
    bash hase-internal-graph-20261010/check.sh -o hase-internal-graph-20261010/ProjectionBoundary.olean hase-internal-graph-20261010/ProjectionBoundary.lean

check.sh establishes the exact existing import paths. Author replay logs are under validation. Independent review is reported separately.

## Conclusion

The useful progress is an actual source-level strong graph invariant and exact compiler-bound commuting squares. The concrete construction isolates two legal typed projection goals, and both direct raw-conversion shortcuts fail. The original literal scalar-fusion identity remains unproved, as does its negation. No semantic-completeness principle, parametricity axiom, numerical induction for a source Church variable, proof-search closure, or universal impossibility conclusion is introduced.
