# Deep CO V1 cold audit

## Disposition

```text
REPAIR_REQUIRED
```

## Blocking findings

### CO-F01 — “computed from E0” was under-typed

The theorem holds for a common deterministic function or common stochastic
kernel applied to the same complete profile law. It does not cover an
architecture-specific algorithm, hidden side channel, differently trained
model, or changed experiment.

### CO-F02 — completeness is relative to the frozen interface

`E0` is complete only for the declared neutral observation/intervention
interface. Internal interventions, additional sensors, new source evidence, or
longer horizons can enlarge the experiment.

### CO-F03 — latent-parameter wording was too broad

A latent parameter inferred solely by common postprocessing of `E0` cannot
split the collision. A latent variable introduced with architecture-specific
prior structure or new data is not covered.

### CO-F04 — target-dependent corrections must be classified, not merely noted

A target oracle or architecture-specific correction can separate U/I, but is
ineligible as neutral evidence. The repaired theorem must make target
independence a formal guard.

### CO-F05 — equal laws do not imply metaphysical equivalence

The result is statistical/experiment-relative nonidentifiability, not
metaphysical identity, equal prior probability, or equal explanatory merit.

### CO-F06 — deterministic and stochastic scopes must be separated

The proof for deterministic functions is a pushforward equality; the stochastic
case is equality under one common Markov kernel. Candidate-specific kernels do
not satisfy the theorem.

### CO-F07 — model-class restrictions are not postprocessing

An independently defended restriction may remove one model even when it is not
measurable from `E0`. Deep CB only blocks restrictions determined by the same
profile. The repaired packet must retain that distinction.

### CO-F08 — theorem-family and novelty ceiling were missing

The mathematical core is a compositional corollary of Deep AO data processing,
Deep CB evidence-determined restriction, Deep BV fibre constancy, and standard
pushforward equality. It receives no independent general novelty credit.

## Required repair

Freeze one common-profile measurable family, state completeness and target
independence, preserve changed-experiment and external-anchor exits, separate
statistical from metaphysical conclusions, and classify ancestry.
