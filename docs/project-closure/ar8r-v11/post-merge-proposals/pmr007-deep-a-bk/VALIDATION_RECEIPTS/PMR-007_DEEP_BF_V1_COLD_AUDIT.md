# PMR-007 Deep Round BF V1 — cold audit

```text
candidate: PMR-007-ILRC-1 V1
disposition: REPAIR_REQUIRED
review relation: same-program procedural cold audit; not external review
frozen-hash verification: PASS 4 / 4
```

## Audit target

The frozen V1 packet proposes to identify the minimum width of a finite
bivariate latent product mixture with matrix nonnegative rank and then use that
quantity as a discriminator against a width-restricted impersonal rival. The
central equality is mathematically standard; the audit focuses on field,
semantics, scope, comparison fairness, and metaphysical nontransfer.

## Blocking findings

### BF-F01 — factorization field was not part of every formal symbol

The prose defines `rank_+(P)` without a field superscript while the model owner
fixes `nonnegative_reals` and the checker operates over exact rationals. For
rational matrices, minimum real and minimum rational nonnegative rank can
differ. The canonical theorem must be over `R_+`; a rational variant requires a
separate symbol and no field equality may be inferred from the checker.

### BF-F02 — zero terms and the width convention were under-specified

The normalization proof skips a component when either factor has zero total
mass. This is valid only because nonnegativity makes that rank-one term
identically zero. Width must count positive-weight/nonzero terms and zero terms
must be explicitly removable.

### BF-F03 — the stochastic-channel claim lacked a typed kernel formula

V1 states that common deterministic or stochastic coarse-graining cannot
increase width, but does not type the two Markov kernels or matrix orientation.
The repair must define `P' = K_X P K_Y^T`, fix a stochastic convention, and
separate mathematical monotonicity from the methodological requirement that
architecture comparisons use one preregistered common channel.

### BF-F04 — observational and interventional realization were conflated

One observational matrix can have a latent product representation even when no
single latent causal model reproduces a family of interventions. The theorem
must remain one-law and observational. Shared-latent interventional families,
dynamics, and counterfactuals need additional compatibility constraints.

### BF-F05 — the matrix result does not extend unchanged to tensors

For three or more observed blocks, a nonnegative tensor factorization or a
family of compatible flattenings is required. Matrix nonnegative rank of one
flattening can forget genuinely multiway structure.

### BF-F06 — latent width was at risk of ontological overreading

A mixture component is a factorization term, not thereby a bearer, subject,
agent, acquisition root, causal source, or metaphysical ground. One impersonal
randomizer can implement many latent states; one personal agent can implement
the same law.

### BF-F07 — factorization nonuniqueness and latent-label orientation were not formalized

The observed matrix generally does not identify a unique factorization,
semantics, or orientation of latent labels. Permutation is only the simplest
ambiguity. `LRC` is a minimum-cardinality invariant, not an identification
theorem for factors.

### BF-F08 — candidate-specific representations can manufacture comparison differences

Although width is monotone under each fixed channel, processing rivals through
different, outcome-selected, or source-biased maps is not a fair comparison.
The discriminator requires a common frozen experiment/channel or an explicit
selection model.

### BF-F09 — unrestricted-rival saturation needed exact formal wording

Every finite bivariate law has a product-mixture realization of width at most
`min(|X|,|Y|)`. This proves saturation of a formal model class, not physical or
metaphysical possibility, causal adequacy, explanatory parity, or
source/world compatibility.

### BF-F10 — computational hardness and checker coverage were omitted

The primary checker verifies algebraic normalization, canonical upper bounds,
2×2 rank classification, and factor pushforward on rational examples. It does
not compute minimum nonnegative rank beyond 2×2 except for
ordinary-rank-tight witnesses and cannot certify generic real-field optima.

### BF-F11 — theorem-family and novelty ceilings were incomplete

Product-mixture width equals nonnegative rank by standard nonnegative
rank-one decomposition after probability normalization. The rank bounds and
monotonicity are standard. Project-specific value is the typed Candidate-G/R5
burden relocation. General mathematical novelty is zero.

## Nonblocking findings

### BF-N01 — support rectangles offer an independent rereview route

Every nonnegative rank-one term has rectangular support, so the support
rectangle-cover number lower-bounds nonnegative rank. It is not a complete
characterization but gives independent sparse-witness checks.

### BF-N02 — common channels may strictly lower width

Monotonicity is one-sided; equality is not promised.

### BF-N03 — rational exact checks remain useful at their declared scope

They validate explicit constructions, zero-term normalization, support lower
bounds, and channel pushforward without floating error; they do not erase the
real/rational distinction.

## Required repair

1. Introduce explicit real-field notation and a separate rational-field scope note.
2. Define positive-weight width and zero-term deletion.
3. State the Markov-kernel theorem with orientation.
4. Add observational/interventional and matrix/tensor firewalls.
5. Add the support-rectangle lower bound.
6. Add explicit bearer/subject/causal/source/world nonclaims.
7. Add common-channel comparison guards.
8. Record ancestry, computational scope, and zero novelty.
9. Freeze V2 and conduct an independently implemented rereview.
