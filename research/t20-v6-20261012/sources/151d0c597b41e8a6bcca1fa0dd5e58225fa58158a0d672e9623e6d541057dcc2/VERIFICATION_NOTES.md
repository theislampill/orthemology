# Verification record and limits

11 October 2026 UTC. Author checks only. Independent review is separately owned.

The first executable run stopped at the same-support mixture's second-moment equality. Diagnosis identified Python's integer default zero divided by 2, which introduced floating-point SymPy weights at formerly absent atoms. The exact equality assertion correctly detected the resulting roundoff. Replacing both defaults by SymPy Integer(0) restored exact rational arithmetic. A rational-type regression assertion for every mixed weight was added. No theorem or reported witness value was changed.

The final full run writes CONTROL_RESULTS.json and verification.txt to an explicitly selected output directory. Its finite controls include all retained source snapshot hashes, binomial annihilation through M=18, degree pairs D,K=1 through 5, the displayed quadratic pair, common-support positive mixtures, a separate five-node finite-evaluation/Jordan witness, multivariate cases, constant-objective and constant-descriptor negative boundaries, a drift-only positive countercontrol, and Gaussian square completion and differential equations. The check count is recorded by the executed output rather than inferred from this prose.

For the separate evaluation witness, with F=x^2/2 and retained x,x^2,x^3, the script obtains mu=(delta_1+delta_3)/2 and nu=(delta_0+6 delta_2+delta_4)/8. The signed functional before normalization annihilates 1,x,x^2,x^3,F and takes B_F(x^3) to 1; its positive mass is 1/15. Thus the normalized derivative gap is 15. This supplements the six-node binomial witness with the dimension-based construction.

The written proofs establish the arbitrary-dimension and arbitrary-degree statements. The checks do not enumerate all real polynomials, certify local ODE existence in a kernel, or mechanically prove the finite evaluation lemma. Local existence and positive weighting are justified directly in RESULT.md. Exact checks are supporting controls, not independent assessment or universal formal verification.

The frozen manifest binds the author packet and its copied inputs. A digest identifies retained bytes; it does not authenticate the original mathematical sources, declare integration, or close T20. Replays should write outside the frozen packet. The bounded search and primary-source reading are recorded separately from the mathematical proof.
