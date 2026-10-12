# Rigidity and generic source recursor uniqueness are interderivable

## Strongest completed result

`InternalUniqueness.rigidity_implies_internal_uniqueness` (actual namespace `RigidityInitiality`) is a closed derivation in the unchanged original source judgement:

`HasE [] (abstract uniqueUniformProof) (arr SourceRigidity.Rigidity InternalRecursorPrinciple.Uniqueness)`.

The conclusion is the **literal pre-existing internal Uniqueness proposition**, including its `All` carrier quantifier, seed, scalar step, candidate recursor, zero/successor identity hypotheses, and pointwise uniqueness conclusion. It is not a replacement proposition, a semantic theorem, a parameter-only schema, or a new typing rule. All hypothesis variables, six Pi introductions, type weakening, All introduction, outer implication, formation and scope premises are explicitly checked.

The converse is also source-checked in `UniquenessConverse.lean`:

`internal_uniqueness_implies_rigidity : HasE [] (abstract (abstract (abstract (abstract ident)))) (arr InternalRecursorPrinciple.Uniqueness SourceRigidity.Rigidity)`.

Thus the exact two internal propositions are interderivable by **closed source proofs in both directions**. This does not assert that either proposition has a closed inhabitant. The converse directly instantiates the internal All proposition at N, applies it to both an arbitrary Peano endomorphism and identity, composes the resulting pointwise equalities, and invokes the existing source `piExt` rule with all formation and scope premises. A routine derivation-to-scope lemma for HasE is proved by constructor induction; no general HasE weakening or substitution theorem is assumed.

The exact internal formula says: given a carrier A, seed a:A, step f:A→A, and u:N→A satisfying u(0)=a and u(succ n)=f(u n), every n:N satisfies u(n)=n f a. Rigidity is a hypothesis throughout. No closed inhabitant of Rigidity is asserted.

## Exact inhabitation boundary

`UniquenessIndependence.lean` proves both `(¬ ∃p, HasE [] p Uniqueness)` and `(¬ ∃p, HasE [] p (arr Uniqueness bottom))`, together with the corresponding original-Has exclusions. These transfer the existing RigidityDiscriminator independence through the two checked source implications. The negative-U transfer uses explicit source S/K composition to build a hypothetical negative-R proof, avoiding arbitrary HasE weakening/substitution. No closed Rigidity evidence or semantic reflection is introduced. Unlike the positive implication modules, this consequence deliberately depends on the existing noninhabitation/model discriminator.

## Other completed source results

1. `dependent_section_from_rigidity`: for every original-source formed dependent family P over N, typed seed p:P0, and typed total-space step, arbitrary `HasE` rigidity evidence gives P(n) for every original-Has n:N.
2. `dependent_section_explicit` and `dependent_section_curried`: the proof polynomial is literally `snd (n D (pair zero p))`; the ordinary curried step is fully converted into the typed total-space step. No opaque witness choice is needed.
3. `rigidity_implies_section`: an actual source implication `Rigidity → Πn:N.P(n)` for every original-Has formed family/seed/curried step. The rigidity assumption is bound as an ordinary hypothesis, avoiding a need for unrestricted HasE weakening.
4. `section_zero_law`: original-Has identity at P0 between the section's zero value and p. The equality also holds by raw conversion.
5. `section_successor_law`: genuine HasE identity at P(succ n) between the section's successor value and `s n (section n)`, conditional on arbitrary HasE rigidity evidence. It is **propositional**, not asserted as unrestricted raw conversion.
6. `section_application_beta`: the uniform Pi witness applied to n raw-converts to the same explicit pointwise section polynomial used in the computation laws.
7. `recursor_unique_source`: the full fixed-polynomial source identity-family specialization at carrier parameter A. `rigidity_implies_internal_uniqueness` then packages this into the existing internal All proposition, removing the parameter-only limitation of the standalone schema.

## Construction and exact assumptions

- Form E = Σ n:N.P(n) using the actual Sigma constructor.
- Type `(zero,p)` and `(n,x) ↦ (succ n,s n x)` in original Has.
- Instantiate original Church N at E and fold those data.
- Its first projection is a genuinely typed N→N endomorphism. Original conversion supplies its zero/successor identities.
- Eliminate the internal Rigidity hypothesis to identify that projection with identity.
- Use source J to obtain the pointwise return-to-input equality and transport the dependent second projection.
- Existing erased-J conversion yields the exact polynomial `snd(n D a)` at P(n); although the polynomial erases rigidity evidence, its typing remains conditional on that evidence.
- For successor computation, form a two-variable dependent J motive with both endpoints explicitly typed. Transport/application coherence, plus raw total-fold beta, gives the identity in P(succ n). Neither UIP nor an implicit endpoint-type conversion is used.
- For uniqueness, specialize P(n) to Id_A(u n,n f a). Source zero evidence, source congruence/transitivity, and Church beta construct the total-space algebra. Bind all ordinary hypotheses and quantify the carrier using the existing All constructor.

Original-Has family/seed/step premises remain the scope of the dependent-family metatheorem. No arbitrary HasE-family/seed/step structural theorem is asserted. The internal uniqueness implication itself binds its assumptions in the source and can be eliminated with existing HasE rules; it does not assume general HasE substitution as a metatheorem.

No arbitrary-value graph naturality, semantic reflection, full-PER completeness, q-specific equation, new source rule, proof irrelevance, UIP, identity reflection or universe resizing is used. Families are quantified metatheoretically in the dependent schema; the existing internal Uniqueness proposition uses its actual source All carrier quantifier.

## Categorical relation and remaining bounds

The standard categorical fact is valid: with equalizers, weak initiality plus identity-only endomorphisms implies initiality. For f,g:X→A, let e:E→X equalize them. Weak initiality gives h:X→E; rigidity gives eh=id_X; then f=feh=geh=g. This needs only an equalizing arrow admitting a lift, not its full universal property.

The source proof takes the total-space route and never needs to identify Sigma points or morphism proof fields. It establishes generic source recursor uniqueness and dependent elimination with the stated computation laws without defining a whole category of proof-relevant source algebras. A formal category-level initiality theorem and arbitrary-HasE-premise dependent induction remain outside this packet. The converse does include the necessary source function-equality packaging via piExt. No novelty is claimed for the standard categorical or total-space argument; the contribution here is the checked transport through this original calculus.

## Reproduction and files

Run `bash hase-rigidity-initiality-20261010/check.sh` from the workspace root. It uses pinned Lean 4.19.0, `--trust=0`, and inherited compiled pins captured by the generic-rigidity independent review.

- Initiality.lean: total-space construction and conditional dependent section
- SectionCorollaries.lean: exact erased polynomial and curried step
- UniformSection.lean: uniform source implication
- ComputationLaws.lean: fully typed dependent coherence and zero/successor laws
- SectionApplication.lean: uniform/pointwise polynomial beta connection
- SourceUniqueness.lean: actual identity-family recursor uniqueness
- InternalUniqueness.lean: closed implication to the literal existing internal proposition
- UniquenessConverse.lean: closed converse, yielding exact source interderivability
- UniquenessIndependence.lean: transferred noninhabitation of U and its internal negation

All source modules are frozen for independent review. All printed new theorem axiom dependencies are standard Lean foundations (`propext`, `Classical.choice`, `Quot.sound`), with no `sorryAx` or new axiom. Author replay logs and source SHA256 values are in validation. Independent reviews are maintained separately by the reviewer.
