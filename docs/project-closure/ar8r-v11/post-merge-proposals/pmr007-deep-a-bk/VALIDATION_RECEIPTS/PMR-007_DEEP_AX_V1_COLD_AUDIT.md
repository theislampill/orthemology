# PMR-007 Deep AX V1 cold audit

```text
disposition: REPAIR_REQUIRED
frozen packet: PMR-007_DEEP_AX_V1_FROZEN_HASHES.sha256
review relation: same-session procedural cold audit
external independence: NOT CLAIMED
```

## Blocking findings

### AX-F01 — conditional independence was silently assumed

V1 multiplies marginal root likelihood ratios.  That is valid only when the
complete root vector factors conditionally on each architecture.  The primary
checker found 24,608 joint-table outcomes where the product of marginal ratios
differed from the exact joint likelihood ratio.  The theorem must begin with
the full joint distribution and state factorization as a corollary.

### AX-F02 — zero-probability and support cases were not typed

Likelihood ratios require extended values or a common-support guard.  Posterior
updates must distinguish impossible-under-A, impossible-under-R, and impossible
under both.  Repair using the exact joint Bayes rule on positive-probability
observations and an extended likelihood convention elsewhere.

### AX-F03 — displayed sources were too close to actual provenance roots

Books, translations, editions, commentaries, and summaries are not automatically
independent roots.  Root identity and conditional independence require separate
custody and causal evidence.  Copies and translations within one lineage must
not receive extra factors.

### AX-F04 — source compatibility was conflated with source reliability

A source-role statement may be compatible with both architectures.  A
nonunit likelihood ratio requires an independently specified source-generation
or reliability model.  Compatibility, authority, and truth are different
coordinates.

### AX-F05 — translation data processing was overread

A common candidate-independent channel contracts distributional discrimination
such as total variation, but an individual realized output can have a larger
pointwise likelihood ratio than a particular input.  State only the correct
distribution-level contraction and exact pushforward likelihood rule.

### AX-F06 — source-to-world interpretation was not separated from evidence

Source bearer identity, interpretation-family admissibility, world referent,
actual-world selection, and architecture likelihood are separate.  A restricted
interpretation family can hide the preferred-world anchor.

### AX-F07 — posterior preference was overread as world truth

A Bayesian update is conditional on the candidate set, priors, and likelihood
model.  It does not establish that the selected architecture is actual, that the
model class is complete, or that the source is true.

### AX-F08 — tawatur and qualitative source warrant were not firewalled

The finite likelihood model is not a reconstruction of Ibn Taymiyyah's broader
fiṭrah/tawatur epistemology.  The source literature treats qualitative,
conventional, pan-human, and normative factors that are not reduced to iid
Bayesian roots here.

### AX-F09 — hidden target labels and candidate-dependent channels remain live

A source predicate, translation, coding policy, or referent map chosen because
it favors Architecture A violates the Deep AQ/AN/AO candidate-independence
requirements.  Add explicit relabeling and hidden-anchor controls.

### AX-F10 — ancestry and novelty ceiling were incomplete

The abstract result is Bayes likelihood, conditional-independence
factorization, and data processing, specialized to source/provenance custody.
It receives no general mathematical novelty or historical identity.

## Required repair

1. Replace the marginal product theorem with the exact joint-likelihood theorem.
2. Add conditional factorization only under an explicit independence guard.
3. Separate compatibility, reliability, source authority, referent mapping, and world truth.
4. State translation effects at distribution level.
5. Preserve correlated-root, copy, hidden-anchor, version, and candidate-dependent-channel controls.
6. Run a distinct exact-rational rereview over ternary joint source alphabets and stochastic channels.
