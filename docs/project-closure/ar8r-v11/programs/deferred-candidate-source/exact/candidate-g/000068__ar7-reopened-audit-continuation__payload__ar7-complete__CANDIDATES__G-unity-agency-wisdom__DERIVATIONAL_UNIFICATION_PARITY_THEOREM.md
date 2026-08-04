# Candidate G — derivational-unification parity theorem

## Neutral theorem

Let an explanatory profile theory be a tuple

```text
T = <Θ, E, F, I>
```

where:

- `Θ` is the admissible space of primitive profiles;
- `E = E₁×...×Eₙ` is the joint explanandum space;
- `F:Θ→E` gives the explanandum profile fixed by a primitive profile;
- `I` records which coordinates of `Θ` are independently variable.

Let a plural theory have independent primitive coordinates

```text
Θ_P = Θ₁×...×Θₙ
```

and let a proposed one-ground theory merely place the same coordinates in one bearer `g`:

```text
Θ_B = {g}×Θ₁×...×Θₙ.
```

Suppose:

1. projection `π(g,θ₁,...,θₙ)=(θ₁,...,θₙ)` is a bijection;
2. `F_B = F_P∘π`;
3. the same primitive-coordinate interventions are admissible under `π`;
4. no additional cross-coordinate law, restriction, or derivation is introduced.

Then the theories are **derivationally equivalent** relative to `E`: they permit the same primitive profiles, fix the same explanandum profiles, preserve the same intervention/dependence structure, and differ only by carrier packaging.

Therefore:

> Reducing many primitive bearers to one bearer does not by itself reduce primitive explanatory freedom or supply metaphysical unification.

## Proof

The projection `π` is a bijection by condition 1. Condition 2 preserves every explanandum profile. Condition 3 preserves every permitted primitive-coordinate variation and therefore every counterfactual dependence relation between primitive and explanandum coordinates. Condition 4 rules out any further shared derivation or cross-domain constraint. Hence `π` is an isomorphism of the explanatory profile structures after deletion of the idle carrier label. No explanatory contrast represented by the theory distinguishes the two structures.

## Product-decomposition corollary

If

```text
Θ = Πᵢ Θᵢ
F(θ₁,...,θₙ) = (F₁(θ₁),...,Fₙ(θₙ))
```

and each coordinate remains independently recombinable, then the theory decomposes into `n` independent explanatory modules even when every coordinate is called an intrinsic feature of one thing.

## Genuine-unification condition

Carrier unity can become explanatory only if at least one of the following obtains:

1. **shared derivation:** a non-conjunctive explanans or argument pattern contributes to multiple explananda;
2. **cross-profile restriction:** the admissible joint profile space is a proper subset of the product of independently admissible marginal spaces;
3. **cross-domain counterfactual dependence:** variation in one domain constrains another by a law not reconstructed as independent coordinate facts;
4. **primitive reduction:** some alleged primitive coordinates are derived from fewer independently motivated primitives;
5. **novel constraint:** the unified account rules out joint configurations that its plural rival permits.

Calling the conjunction of independent attributes a “nature,” “essence,” “mind,” “law,” or “ground” does not satisfy these conditions by itself.

## Orthability application

Let the target explananda be:

```text
M = modal admissibility and identity
A = concrete obtaining and causal efficacy
S = determinate content and truth conditions
N = correctness, fittingness, and reason-giving authority
```

A proposal that posits one bearer `g` with four primitive and freely recombinable features `m(g)`, `a(g)`, `s(g)`, and `n(g)` is derivationally equivalent to positing four primitive facts `M`, `A`, `S`, and `N`. It does not yet explain why these dimensions coordinate in actual correction episodes.

A serious unified-ground hypothesis must derive at least some of their coordination from a smaller, independently motivated architecture. Rational agency is one candidate architecture because representation, evaluation, alternative-sensitive selection, and efficacy are systematically linked. But merely defining a bearer as “intellectual, willing, powerful, and wise” recreates the boxing problem unless the links are separately defended.

## Limits

The theorem does not show that:

- ontological unity has no value;
- all theoretical virtues reduce to derivational structure;
- explanatory profile isomorphism is full metaphysical equivalence;
- a unified ground is false;
- plural primitives are preferable;
- rational agency cannot unify the target.

It establishes a parity burden: **carrier-count reduction alone is not explanatory compression**.

## Finite executable witness

```text
ar7-work/experiments/candidate_g_carrier_boxing_checker.py
ar7-complete/VALIDATION_EVIDENCE/candidate_g_carrier_boxing_results.json
```

The checker exhaustively verifies, for one through eight binary coordinates, that plural and carrier-boxed models have identical profile counts, outputs, and coordinate-dependence structures. A parity-constrained model illustrates a genuine cross-profile restriction. The computation illustrates the general bijection proof; it does not replace it.

## Source-critical disposition

This theorem is closely anticipated by:

- Kitcher’s derivational account of explanatory unification;
- Kovacs’s metaphysical unificationism, which evaluates derivation of many explananda from meager explanantia and few patterns;
- Cowling’s distinction between ontological and ideological parsimony;
- McIntyre’s argument that exchanging ontology for ideology does not reduce brute-fact cost.

The exact carrier-boxing formulation and its orthability application are useful, but the mechanism is a direct synthesis of established unification and parsimony principles.

```text
CORRECT_EXPLANATORY_PARITY_THEOREM
DIRECT_SYNTHESIS_OF_ESTABLISHED_UNIFICATION_AND_PARSIMONY_MECHANISMS
NO_STANDALONE_NOVELTY_MENISCUS
LOAD_BEARING_REPAIR_TO_ANY_UNITY_ARGUMENT
```
