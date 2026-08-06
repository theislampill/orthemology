# PMR-007 Deep Round AN V2 — predictive surplus, representation-relative simplicity, and Candidate G P6

```text
identity: PMR-007-ABPD-1
round: PMR-007-DEEP-AN
version: V2
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_task: state the exact evidential gate for explanatory-unification claims
```

## 1. Frozen finite comparison model

Let `Ω` be a finite registered evidence space.  Let architectures `A` and `R`
induce probability distributions `P_A` and `P_R` on `Ω` under one explicitly
frozen measurement and sampling model.  Let prior odds be

\[
O_0 = \pi_A/\pi_R.
\]

For evidence `D`, posterior odds are

\[
O_D = O_0\,\frac{P_A(D)}{P_R(D)}
\]

whenever the denominator is positive.  Dependence, intervention, adaptive
sampling, and selection are not silently represented by an iid product; each
requires its own declared likelihood.

## 2. ABPD-1A — likelihood-parity theorem

If

\[
P_A(D)=P_R(D)>0,
\]

then

\[
O_D=O_0.
\]

Thus evidence on which the two architectures have equal likelihood supplies no
Bayesian update between them.  This does not make their priors equal and does
not establish global observational equivalence.

## 3. ABPD-1B — finite predictive-discriminator characterization

For finite `Ω`, the following are equivalent:

```text
P_A != P_R;
there exists an event E⊆Ω with P_A(E) != P_R(E);
total-variation distance TV(P_A,P_R) > 0.
```

Hence an integrated architecture supplies a testable evidential advantage only
if it creates at least one independently identified event with a different
predicted probability.

The strongest form is a preregistered, held-out cross-domain restriction or
counterfactual prediction that was not used to define the architecture.

## 4. ABPD-1C — representation-relative description ranking

For any two named hypotheses, there are valid finite prefix codes in which `A`
is shorter and valid finite prefix codes in which `R` is shorter.  Therefore
raw description length, primitive count, or bearer count does not yield a
representation-invariant evidential ordering.

A complexity penalty may be used only after independently fixing:

```text
hypothesis language;
primitive vocabulary;
code or prior;
allowed auxiliaries;
data representation;
and comparison class.
```

This does not deny every MDL, Bayesian, or simplicity argument.  It blocks an
untyped move from `one ground` or `fewer labels` to truth.

## 5. ABPD-1D — predictive-surplus criterion for Candidate G

Candidate G's derivational unification becomes evidence-bearing only when the
unified architecture yields a **predictive surplus**:

```text
an independently motivated cross-domain restriction, probability assignment,
or intervention response;
not already encoded in the comparison target;
fixed before held-out evaluation;
with likelihood different from the strongest matched rival;
and evaluated under a source, representation, and sampling contract common to
both candidates.
```

If the unified-personal architecture and the strengthened impersonal rival
induce equal likelihood on all current evidence, P6 remains unestablished and
posterior preference is prior-driven.

## 6. Positive construction and controls

### AN-POS1 — independently fixed support restriction

If `A` is uniformly distributed over an independently motivated proper subset
`S⊂Ω` and `R` is uniform over `Ω`, then observing `x∈S` has Bayes factor

\[
|Ω|/|S|
\]

under the frozen iid model.  This is genuine predictive discrimination only if
`S` was not selected after seeing `x` and the zero probabilities are warranted.

### AN-CM1 — equal-current-evidence architectures

A personal and an impersonal architecture assign equal probability to every
currently registered observation.  Current evidence supplies no update.

### AN-CM2 — code reversal

Two prefix codes reverse which architecture is shorter.  Unfixed code length
cannot carry P6.

### AN-CM3 — simple false model

A syntactically shorter architecture makes a false held-out prediction; a
longer architecture succeeds.  Simplicity is not an entailment of truth.

### AN-CM4 — ad hoc support restriction

`A` excludes exactly the already known counterexamples.  Its apparent
compression is target import rather than prediction.

### AN-CM5 — source-prior migration

Track-N source commitment raises `π_A` but does not change a neutral likelihood.
This is a source-relative prior, not neutral evidence.

### AN-CM6 — misspecified zero

A finite model assigns zero probability to an observation omitted from its
registry.  The observation refutes the frozen model but does not by itself
identify the correct metaphysical architecture.

### AN-CM7 — shared hidden assumption

Both A and R inherit the same hand-authored profile representation.  Their
agreement may reflect the representation rather than world structure.

## 7. Candidate-G and architecture disposition

Deep AL found no robust champion under current evidence.  Deep AN identifies
what can change that result:

```text
A-only predictive event or intervention;
held-out evidence with a nonunit likelihood ratio;
an independently warranted prior or coding policy;
and survival of representation and model-misspecification controls.
```

Derivational unity remains a legitimate explanatory virtue, but P6 is not a
formal consequence of unity.  It is a meta-epistemic bridge requiring either
independent defense or predictive success.

The strongest current impersonal rival survives because it can share all
registered neutral likelihoods, semantic anchors, causal guidance, and source-
conditional role predicates while withholding personal realization.

## 8. Bitter-Lesson and empirical design implication

Any future comparison of Architecture A against learned or impersonal rivals
must freeze:

```text
hand-authored, learned, and minimal/raw representations;
matched information and compute;
common train/validation/held-out splits;
likelihood or scoring rule;
preregistered retirement conditions;
and analysis of selection bias and model misspecification.
```

This is a test contract, not evidence that learned representations win.

## 9. Theorem-family and novelty

The formal results are direct consequences of standard Bayesian odds, finite
probability separation, and finite prefix-code constructions.

```text
general_mathematical_novelty: 0
historical_identity: NONE
repository_status: PROPOSAL_EVIDENCE_ONLY
external_review: OPEN
owner_adoption: PENDING
```

## 10. Nonclaims

No result establishes:

```text
a canonical prior or description language;
Bayesianism as the unique epistemology;
the metaphysical truth of any candidate;
that personal architecture is false;
that the impersonal rival is actual;
source-to-world identity;
proper function, Wisdom, or Speech;
integrated champion;
meniscus;
or natural closure.
```
