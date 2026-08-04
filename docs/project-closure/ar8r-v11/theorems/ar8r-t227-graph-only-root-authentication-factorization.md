# AR8R-T227 — graph-only root-authentication factorization boundary

Status: validated at repaired scope; canonical identity fixed by theorem-origin authority V5; no general mathematical novelty.

## Typed setting

Let `G=(V,E)` be a finite directed record graph, `R⊆V` a declared set of origin-root records, and `r↝v` reflexive-transitive reachability. Let `Λ⊆{0,1}^R` be a nonempty, independently specified class of admissible authentication assignments. Define

```text
AuthSupp_λ(v) = {r in R : λ(r)=1 and r↝v}.
```

A graph/profile-only classifier `s_{G,R,Λ}:V→P(R)` may use fixed `G`, `R`, and `Λ`, but may not inspect which `λ∈Λ` is actual.

## Theorem

The following are equivalent:

1. one graph/profile-only classifier returns `AuthSupp_λ(v)` for every `v` and every admissible `λ`;
2. for every `v`, the map `λ↦AuthSupp_λ(v)` is constant on `Λ`;
3. every root authentication bit `λ(r)` is constant on `Λ`.

Hence fixed graph/profile input determines authenticated support exactly when the admissible class has already fixed every root's authentication status.

## Proof

The first clause immediately implies support constancy. For support constancy to imply bit constancy, evaluate at root `r`: reflexive reachability gives `r∈AuthSupp_λ(r)` exactly when `λ(r)=1`. Conversely, if every bit is constant, let `A` be the roots assigned one by every admissible profile and define `s(v)={r∈A:r↝v}`.

## Boundaries

Conditional on an independently fixed authentication assignment, SCC condensation preserves support by ordinary reachability preservation. Reachability does not authenticate roots. A signature, certificate, or independently checked identifier changes the input or restricts `Λ`; it is not recovered from the unlabeled graph.

Availability and copying do not establish authentication, truth, translation accuracy, historical attribution, evidential independence, grounding, realism, or a Necessary Being.

This is a standard fibre-factorization/identifiability application plus the reflexive-root corollary. The orphaned predecessor labeled T223 is historical custody only and receives zero additional theorem or novelty credit.
