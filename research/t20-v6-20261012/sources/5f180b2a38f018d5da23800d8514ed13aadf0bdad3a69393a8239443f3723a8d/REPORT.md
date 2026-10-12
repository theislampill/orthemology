# Author report: radial quartic gradient reverse lift

## Outcome

The proposed unrestricted-rank theorem is valid under the precise normalization, full square positivity, exact hierarchy, and C¹-through-zero hypotheses in RESULT.md. A new additive packet was warranted after checking that the polynomial-automorphism theorem was already complete and did not apply to this nonpolynomial, non-surjective characteristic map.

The decisive estimate is

    A_t(|x|^(2n)) ≤ L_0(|x|²)(2t)^(1−n), n≥1, t>0.

It is derived before representation. Nussbaum–Carleman then supplies a compact determinate positive-time law. The subsequent polynomial-to-PDE passage, compactly supported backward tests, and tight initial-limit recovery identify exactly the weighted nonlinear characteristic evolution. No full-path finite-rank promise or pre-existing initial law is used.

The finite-rank consequence is now stronger for this model: initially finite full rank forces constant full path rank and the unique inherited atomic negative-gradient dynamics. General coercive nonlinear gradients remain outside the theorem. The initial full moment record can still have several admitted paths precisely when its representing-law fibre has several laws.

## Evidence and reading boundaries

Eight files are directly bound in INPUT_BINDINGS.json: six ancestor reports and the inherited primary Nussbaum–Carleman PDF plus its p.24 extraction. Earlier files were not changed. The previously reviewed polynomial-automorphism result was identified as inherited and was not reproduced as a purported new theorem.

The primary external statement used is Putinar–Schmüdgen, *Multivariate Determinateness*, https://arxiv.org/pdf/0810.0840v1, printed p.24, Theorem 25 and the following attribution to Nussbaum. That page, including its proof, was read from the existing extraction, and the current primary web PDF statement was cross-checked. This is the only imported specialized existence theorem. Standard Fourier inversion, Stone–Weierstrass approximation, tightness compactness on Euclidean space, and finite measure uniqueness are used with the needed local estimates written out. This is not a new literature survey or a field-priority claim.

check_exact.py was actually executed successfully. EXACT_CHECKS.json gives its exact count and names, and check_exact.log retains the execution output. Its eight source-integrity checks confirm preservation of all bound old inputs. Remaining checks are finite symbolic identities and explicit scope controls. The factorial, semigroup, backward-test, quotient, and inverse formulas are not inferred from floating-point samples. The lognormal sine controls retain the algebraic integer cancellation from the inherited fibre example; they do not independently rederive Gaussian integration or turn finite checks into proof of every integer.

The scope-control checks deliberately reject closed-ball boundary and exterior points as members of the forward image. They do not constitute an exhaustive negative theorem. The written proof distinguishes a law carried by an open ball from its possibly boundary-meeting topological support.

## Terminal scope

- New report/proof and exact controls: completed as an author deliverable.
- Every bound old input: unchanged at the final integrity check.
- Independent review: separate work by the parent's assigned reviewer; no self-awarded review status here.
- Universal proof-kernel verification, protected changes, broad campaign, integration, and programme closure: not performed or claimed.

No follow-up is required to complete this author deliverable. The parent may use the frozen receipt for its separately assigned review and preservation decisions.
