# Bounded controls

semantic_controls.py independently represents finite sets with Python frozensets and evaluates complete action/reply traces. It performs no proof search and imports no author Lean semantics. Explicit checks raise RuntimeError and remain active with python -O.

Passed counts: 21,845 complement pairs; 2,136 portfolio families; 4,838 nonmaximal-taint checks; 741 fixed-map actual-root realizations; 1,624 adaptive history checks, including receipt present/absent and complete preparation/cancellation payload; 96 uniform-permutation seed/world pairs; 126 identity/repair target-state cases.

Controls detect: wrong complement direction; checking only smaller/empty worlds; removing opaque replies; confusing expected attempts with an almost-sure cap; counting repeated supports as distinct; a one-too-small minimum cover; and incorrectly forcing attempts when the target is initially correct.

A richer revealing interface on m=4,q=3,k=1 succeeds in at most two attempts: first test {0,1,2}; on failure receive the actual bad label; then test its complement. This is excluded by opacity, and NegativeControls.lean proves that the revealing observation cannot satisfy Opaque for any common failed reply.

Uniform random permutations of the four minimum paths have mean 5/2 attempts for each fixed world, while their almost-sure worst cap is still four. Every fixed world has failure probability 1/4 by a cap of three. These finite calculations corroborate the cap/expectation distinction; the generic randomization result comes from the separate measure-theoretic kernel proof.

mutation_controls.py compiles six deliberately false/under-specified variants in disposable output files: wrong complement; wrong family cardinality; opacity replaced by a reflexive equality (well-typed but information-free); a strict-too-small attempt inequality; removal of the probability-measure premise; and binomial cap minus one. Each must produce a nonzero compiler exit and an error. Rejected mutants are not part of the trusted proof modules.
