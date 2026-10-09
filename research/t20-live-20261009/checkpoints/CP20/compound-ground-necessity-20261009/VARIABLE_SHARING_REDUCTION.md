# Conditional derivation exposing variable sharing

P and Q are distinct propositional atoms. N = Q →R Q; C = P ∧ ¬P; B = P ∧ (¬P ∨ N).
Lines1–9 are R theorems. Line10 is the hypothesis being refuted, not an R theorem.
No claim is made that a subject knows C or that C is actual.

1. ((P ∧ ¬P) →R P) [A6]
2. ((P ∧ ¬P) →R ¬P) [A7]
3. (¬P →R (¬P ∨ (Q →R Q))) [A10]
4. ((¬P →R (¬P ∨ (Q →R Q))) →R (((P ∧ ¬P) →R ¬P) →R ((P ∧ ¬P) →R (¬P ∨ (Q →R Q))))) [A2]
5. (((P ∧ ¬P) →R ¬P) →R ((P ∧ ¬P) →R (¬P ∨ (Q →R Q)))) [MP 4, 3]
6. ((P ∧ ¬P) →R (¬P ∨ (Q →R Q))) [MP 5, 2]
7. (((P ∧ ¬P) →R P) ∧ ((P ∧ ¬P) →R (¬P ∨ (Q →R Q)))) [Adjunction 1, 6]
8. ((((P ∧ ¬P) →R P) ∧ ((P ∧ ¬P) →R (¬P ∨ (Q →R Q)))) →R ((P ∧ ¬P) →R (P ∧ (¬P ∨ (Q →R Q))))) [A8]
9. ((P ∧ ¬P) →R (P ∧ (¬P ∨ (Q →R Q)))) [MP 8, 7]
10. ((P ∧ (¬P ∨ (Q →R Q))) →R (Q →R Q)) [H: suppose this were an R theorem]
11. (((P ∧ (¬P ∨ (Q →R Q))) →R (Q →R Q)) →R (((P ∧ ¬P) →R (P ∧ (¬P ∨ (Q →R Q)))) →R ((P ∧ ¬P) →R (Q →R Q)))) [A2]
12. (((P ∧ ¬P) →R (P ∧ (¬P ∨ (Q →R Q)))) →R ((P ∧ ¬P) →R (Q →R Q))) [MP 11, 10]
13. ((P ∧ ¬P) →R (Q →R Q)) [MP 12, 9]

The final implication has antecedent atoms {P} and consequent atoms {Q}.
R has variable sharing, as verified by the two closed M0 subalgebras and cross-implication table.
Therefore H cannot be an R theorem. The direct M0 countervaluation independently rejects H and sensitivity.
