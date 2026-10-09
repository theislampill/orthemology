# A checked relevant factive ground derivation

→R is relevant implication. P and N are arbitrary formulas. B abbreviates P ∧ (P →R N).
Each line is an instance of a source-listed axiom or modus ponens from prior lines.

1. ((P ∧ (P →R N)) →R P)    [A6]
2. ((P ∧ (P →R N)) →R (P →R N))    [A7]
3. ((P →R N) →R (((P ∧ (P →R N)) →R P) →R ((P ∧ (P →R N)) →R N)))    [A2]
4. (((P →R N) →R (((P ∧ (P →R N)) →R P) →R ((P ∧ (P →R N)) →R N))) →R (((P ∧ (P →R N)) →R P) →R ((P →R N) →R ((P ∧ (P →R N)) →R N))))    [A4]
5. (((P ∧ (P →R N)) →R P) →R ((P →R N) →R ((P ∧ (P →R N)) →R N)))    [MP 4, 3]
6. ((P →R N) →R ((P ∧ (P →R N)) →R N))    [MP 5, 1]
7. (((P →R N) →R ((P ∧ (P →R N)) →R N)) →R (((P ∧ (P →R N)) →R (P →R N)) →R ((P ∧ (P →R N)) →R ((P ∧ (P →R N)) →R N))))    [A2]
8. (((P ∧ (P →R N)) →R (P →R N)) →R ((P ∧ (P →R N)) →R ((P ∧ (P →R N)) →R N)))    [MP 7, 6]
9. ((P ∧ (P →R N)) →R ((P ∧ (P →R N)) →R N))    [MP 8, 2]
10. (((P ∧ (P →R N)) →R ((P ∧ (P →R N)) →R N)) →R ((P ∧ (P →R N)) →R N))    [A3]
11. ((P ∧ (P →R N)) →R N)    [MP 10, 9]
12. (¬N →R ¬N)    [A1]
13. ((¬N →R ¬N) →R (N →R ¬¬N))    [A15]
14. (N →R ¬¬N)    [MP 13, 12]
15. ((N →R ¬¬N) →R (((P ∧ (P →R N)) →R N) →R ((P ∧ (P →R N)) →R ¬¬N)))    [A2]
16. (((P ∧ (P →R N)) →R N) →R ((P ∧ (P →R N)) →R ¬¬N))    [MP 15, 14]
17. ((P ∧ (P →R N)) →R ¬¬N)    [MP 16, 11]
18. (((P ∧ (P →R N)) →R ¬¬N) →R (¬N →R ¬(P ∧ (P →R N))))    [A15]
19. (¬N →R ¬(P ∧ (P →R N)))    [MP 18, 17]

The checker verifies the syntactic derivation and rejects a mutated final consequent.
This is a logical theorem. Calling B the actual epistemic basis additionally requires the subject to know and use its components.
