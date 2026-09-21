# Adversarial comparison: what survives the novelty test?

This is a theorem-level comparison, not a claim of exhaustive literature coverage.
References and read-depth limitations are in SOURCES.json. New proofs appear in
../mathematics. No independent referee or expert endorsement was obtained.

## A — Observation-refinement defect calculus (CV-R)
**Exact statement.** For coherent measurable refinements with measurable
singletons, d_n=d_0+Σ_{k≤n}Σ_y w_{k,y}d(ρ_{k,y}). At the complete infinite
observation add J=μ({all finite cells have positive mass, limiting cell has zero
mass}). Every increment and J is nonnegative. The formula characterises exactly
when a fixed error budget remains true.

**Closest facts and hypotheses.** Decomposing a measure into positive singleton
masses, continuity from above for decreasing measurable cells, and bounded
conditional-expectation convergence supply the proof. The required positive
fibres are restrictions, not a new disintegration theorem. The martingale
formulation is an application of the established Lévy upwards theorem; Mathlib
already formalises that convergence machinery [S6].

**Conclusion-by-conclusion.** Finite telescoping is an immediate corollary of Q1.
The cocycle is a coboundary d(final)−d(initial), not a new cohomological invariant.
The infinite residual is a precise accounting of the failure of point-positivity
to persist under decreasing cells. Fair-prefix counterexamples are standard
probability phenomena. Our formula organises these facts for the declared task;
it does not supersede standard measure theory or Shannon entropy.

**Disposition.** A useful exact lemma/application. The elementary proof defeats
a claim that the finite chain rule alone is a foundational breakthrough. The
specific infinite accounting notation has no demonstrated priority. At most a
short lemma in a larger contribution until independently compared.

## B — Exact certificate-revision accounting (CV-R + CV-O)
**Exact statement.** With fixed tolerance ε and exact initial defect, finite
semantic survival is equivalent to ΣΔ≤ε−d_0; infinite survival requires ΣΔ+J≤ε−d_0.
An old version-bound licence nevertheless fails after any relevant version change.
A new transport certificate can establish the new bound and receive a new licence.

**Closest facts.** The arithmetic equivalence is substitution in A. Proof-carrying
code already separates supplied executable code, explicit host safety policy and
finite proof checking [S7]. Dependency stamps and monotone generations provide
ordinary freshness/ABA protection; we prove the relevant finite-key theorem
rather than claiming it is an unprecedented security primitive.

**Hypothesis differences.** Our risk assertion is the full measurable conull-event
intersection bound on a declared observation law. That is narrower than general
PCC safety and stronger in event expressiveness than a countable predicate list.
The code-revision theorem additionally needs complete read sets, including absence
and vocabulary guards, and revision-consistent dispatch. Merely renaming a result
"certificate" supplies none of these premises.

**Disposition.** A particular application/integration, not a new inference law.
It could become a useful verification case study if the actual implementation
refinement is completed. No mathematical novelty follows from the risk terminology.

## C — Productive-observer defect complexity (CV-C)
**Exact statement.** In the specified total primitive-recursive synchronous
observer language, zero defect is Π3-complete and positive defect Σ3-complete;
for 0<q<1 rational, <q is Σ2-complete, ≥q Π2-complete, ≤q and =q Π3-complete,
and >q Σ3-complete. The original one-switch Q8 family remains Π1/Σ1. Finite
synchronous Mealy observers admit exact rational defect computation.

**Closest known objects.** Porter studies computable measures concentrated on
positive atoms ("trivial measures") and uses tally functionals to turn logical
behaviour into infinite streams [S4]. The definition is therefore old, and our
bounded-simulation/copying technique belongs to an existing tradition. His
selected Section 3 constructions and Theorem 3.2 address randomness structure,
not this presentation-index threshold table. This observation does not establish
that another theorem in the literature fails to contain the table.

Kaminski–Katoen prove Π2-completeness for almost-sure termination and exact
expected-outcome predicates, with related strict-bound classifications [S5].
Their programs may fail to terminate; our observers are productive at every
index and our question concerns the atomic/diffuse split of an infinite output
law. Thus "Π3 instead of Π2" is not an improvement of their theorem: the index
sets differ. Their geometric input selection is also a close methodological
precedent for our weighted row construction.

**Conclusion comparison.** The full upper/lower-bound match is genuinely stronger
than the inherited Q8 single halting reduction. It is not obtained merely by
unfolding realisability. The finite-state theorem adds a structural exception:
atomic mass equals hitting probability of deterministic-output states. But the
method uses standard relation refinement and finite Markov reachability.

**Disposition.** The exact table for this explicit total numbering is the strongest
plausibly publishable ordinary theorem in this packet. Priority remains OPEN.
The bounded search did not locate an exact equivalent statement, but that fact
is not positive novelty evidence. Specialist verification must compare effective
atomic-mass decompositions, descriptive complexity of purely atomic measures and
indices of truth-table functionals. A prior equivalent result would reduce this
to an effective-presentation application; no foundational claim survives merely
because the notation or compiler language differs.

## D — OWOU + internal self-instantiation + no full Girard capability (CV-O)
**Exact achieved statement.** A specified nonempty finite-plan calculus has typed
execution, useful primitives/composition/source certificates and version-bound
licences; its source model has All(B)∈C with legal self-instantiation; exported
same-level full-section/beta operations would imply the Girard package and hence
cannot be supplied by a consistent interpretation.

**Girard/Hurkens [S1].** The hypothesis is universe-compressing dependent products
with abstraction/application for every ambient section and the beta equation.
The conclusion is False. Our negative part is an adaptation/application, not an
alternative proof of consistency for those same hypotheses. Our internal All
uses uniform program realisers and does not supply full ambient abstraction.

**Lietz–Streicher [S2].** For the typed-PCA-induced models covered by their theorem,
impredicativity is equivalent to existence of a universal realiser type, and the
structure then induces an equivalent untyped realisability model. We already use
an untyped program carrier. There is no evasion of this theorem. A universal
realiser type/partial retract structure is not the full ambient Girard universe.
Our bare-predicate model is not automatically identified categorically with their
exact construction; proving such an equivalence is unnecessary to refute a
"new impredicativity" claim, and no such equivalence is asserted here.

**Pistone [S3].** Theorem 7.1 relates realisability, logical-relation invariance,
dinaturality and typability for positive types under specified closure and
normal-form hypotheses. It also discusses incompleteness beyond the positive
fragment. Our finite-source logical-relations induction and identity/Boolean/
numeral instances are narrower; they do not establish his hypotheses for every
new dependent/effectful constructor. There is no stronger parametricity result.

**Speight–van der Weide [S8].** Their Example 23 constructs an impredicative PER
universe with Cartesian and linear decoders, using closure of modest types under
large dependent products. Example 18 supplies tracked dependent products; their
Section 5 treats refined impredicative list encodings. Sections 3–4 have an
author-reported Rocq/UniMath formalisation. This is substantially richer dependent
structure and assurance than our uncompiled candidate. It does not claim full
ambient set-theoretic section abstraction, so it is compatible with Girard too.

**Universal-type/PCA comparison [S9].** Longley's PCTS framework already has typed
partial application, products, tracked morphisms and applicative equivalences
connecting programming-language term models and PCAs. Our interface vocabulary
is not a new categorical universality notion. We have not proved a universal
property or full abstraction beyond the declared plan grammar.

**Adversarial derivation.** The generic-wrapper construction in CV-O attaches the
same dependency/version registry to ANY suitable sound finite fragment without
changing its realisability model. This shows that the conjunction, by itself,
is a modular integration result. It does not reveal a new foundational calculus.
A stronger prior model can receive the same operational wrapper.

**Disposition.** No foundational novelty established. The distinctive output is
a concrete bounded engine and its specific evidence discipline, not a capability
proved absent from earlier models. Kernel checking the preserved modules would
improve assurance but would not alter this historical conclusion.

## E — Integrating D with probabilistic revision obligations
**Exact statement.** The engine's declared-law grammar computes defect evidence;
licences bind laws/vocabularies and risk requirements; relevant changes force
rechecking. CV-R specifies exact multi-stage debt and the infinite residual,
while CV-C rules out a complete effective certifier for arbitrary productive
observers. Countable finite realiser outputs remain zero-defect throughout.

**Closest work and relationship.** This combines existing realisability/PCC ideas
with an exact observation-law application. Nonzero defects concern a different
outcome object (continuum or infinite stream), not the unchanged countable term
carrier. No theorem yet interprets every measurable event as a source type.
Neither finite reference tests nor a semantic fixed point close that gap.

**Disposition.** Potentially useful integration with a precise non-completeness
boundary. It is not proved impossible or awkward in all prior frameworks, and
no benchmark against a prior implementation is supplied. Publication significance
would depend on verified refinement and a genuinely needed application, not the
number of successful demonstration scenarios.

## Read-depth and historical limits
Primary full-text theorem passages were inspected for S1, S3, S4, S5, S8 and S9;
S6 is primary formal-library documentation; S7 is the original publication and
author seminar abstract. For S2 the publisher abstract and author's exact theorem
summary were read; its linked compressed PostScript failed to load. No claim of
having rechecked that entire proof is made. PDF screenshots for S3/S4 returned
internal errors; text was available and the cited statements did not require an
unseen diagram. No expert peer review occurred.

The smallest defensible result is a typed revision-certificate application with
an ordinary exact defect-index theorem candidate. The principal remaining barrier
to a foundational-breakthrough claim is the absence of an independently validated
non-derivative foundational result. The immediate engineering barrier remains the
missing actual Lean build; these are separate barriers, not interchangeable.
