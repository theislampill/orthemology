# Finite moment recovery kernel verification plan

Prospective work began 2026-10-09 21:59:49 UTC. This work formalises an already established ordinary result, with no research-discovery or external-validation credit.

## Scope and constraints
- Create only this additive isolated package; preserve original result and all previous proof packages.
- Prove moment recovery for every finite N over a field from pairwise distinct support, rather than assuming interpolation or injectivity.
- Derive equality of all higher moments and the existence of a fixed linear recovery map.
- Kernel-check the exact four-point positive probability control.
- No sorry, admit, new axioms, repository integration, protected edits, or T20/T21 closure.

## Work
1. Inspect installed dependencies and pin official Lean/mathlib versions. Log acquisition and builds.
2. Use mathlib's proved Vandermonde determinant identity and nonsingular inverse identities to derive the actual weight-recovery theorem.
3. Prove exact support distinctness, positivity, normalisation, equal degrees 0–2 and third-moment difference 1/54 for the displayed rational/real four-point laws.
4. Rebuild all local modules fresh, inspect #print axioms, run controls, hash every delivered source, and describe the precise kernel boundary.

## Edge cases
N=0 must remain valid without inventing a support point; N=1 uses its degree-zero total. Weights are arbitrary field elements for the recovery theorem. Counterexample positivity is a separate real ordered-field fact. No ODE, analytic observation, tensor projection existence, or epistemic claims receive kernel credit here.
