# Source scope and provenance

Read on 8 October 2026 UTC. This records access and continuous read boundaries, not a certificate of active research duration. Historical floor remains UNVERIFIED. The deliverable contains no complete copyrighted source bodies. Temporary local PDFs/text extracts used for reading are outside this sibling and are not part of the deliverable.

## Primary texts used

1. Günter Last and Ilya Molchanov, Poisson hulls.
   - Author preprint: https://arxiv.org/abs/2212.02150 ; https://arxiv.org/pdf/2212.02150
   - Read artifact: arXiv:2212.02150v4, 1 February 2024, 42 PDF pages, including supplement.
   - Publication identity independently cross-checked at the author's KIT publication list https://stoch.math.kit.edu/english/72.php : Bernoulli 31(1) (2025), 359–387, DOI 10.3150/24-BEJ1731. The DOI web open failed, so no journal-body read is claimed.
   - PDF SHA-256: 40532db7351b7fc7b35f093239f0e18cabeef138e8511c3ec64fcb1c19ea1f14.
   - Continuous reading: main-text Sections 2–4 and Section 5 through the higher-moment discussion before Section 6 (printed pages 3–14). This includes generator axioms and proofs of Lemmas 2.3–2.9, prime property, Example 2.15, Theorem 3.2 and its proof, Lemmas 4.3–4.4 and their proofs, Theorem 5.1 and its proof, Proposition 5.2, and the surrounding examples/qualifications.
   - Additionally read the end of Section 6/Example 6.3 and all of Section 7 (printed pages 16–18). The normal-approximation statements delegate their proofs to the supplement; those supplementary proofs were NOT read. No verified CLT rate is claimed in this packet.
   - Theorem 3.2's proof invokes another paper's spatial strong Markov theorem; no recursive source-proof verification is claimed. The elementary Poisson skyline-density derivation in RESULT independently verifies the specialized exponential identity.
   - Role: exact finite-Poisson model match, compensated variance, identification of usable further moment and normal-approximation machinery.

2. Günter Last and Ilya Molchanov, Efron type identities for stopping sets and Poisson hulls.
   - Primary author preprint: https://arxiv.org/abs/2608.06038 ; https://arxiv.org/pdf/2608.06038
   - Read artifact: arXiv:2608.06038v1, submitted 6 August 2026; document title page dated 7 August 2026; 25 PDF pages.
   - PDF SHA-256: 1d10a0c740aae2b062f1c59e4917e8ef66ce878d2fec279ceda44b154f979a5f.
   - Continuous reading: Sections 1–5 and Section 6 through Corollary 6.2 (printed pages 1–13), including all hypotheses, proofs of Theorem 4.7/Corollary 4.8, the conditional Poisson formulation, and distinctions among stopping/Markov sets. Separately read complete Example 8.4 (page 19), Appendix A through complete Lemma A.1 proof (pages 21–22), and relevant references (pages 24–25).
   - Appendix A's further Lemma A.2 was only partly read and is not a dependency. We verify the finite-Pareto stopping property directly.
   - Role: directly stated exponential identity and general mixed factorial-moment identity, with explicit Pareto example. The cited antecedent Zuyev (1999) was checked bibliographically/at abstract level only; its Eq. (12) was not independently read, so attribution of that antecedent is explicitly mediated through Last–Molchanov.
   - Status: preprint, not represented as peer-reviewed.

## Narrow secondary routes screened and bounded

3. James Allen Fill and Daniel Q. Naiman, The Pareto Record Frontier.
   - Primary author preprint: https://arxiv.org/abs/1901.05620 ; https://arxiv.org/pdf/1901.05620
   - Artifact: arXiv:1901.05620v2, 25 January 2019, 28 pages.
   - PDF SHA-256: d2305f1d75330ed9e891564e4320535b1e4804fe4d18e61aca723391bcfef649.
   - Read definitions and main-result statements in Section 1; continuously read Sections 3.1–3.3 (pages 11–13), including geometric lemma, its proof, finite empty-orthant covering argument, and Proposition 3.2. Stopped at start of Section 3.4.
   - Mapping assessed: fixed n and independent coordinates match after order-reversing exponential-to-uniform transformation, but frontier widths/product extrema are not U. Its geometric localization machinery may be useful, but no direct area-moment or joint likelihood result was imported.

4. Nicolai Baldin, The wrapping hull and a unified framework for volume estimation.
   - Primary author preprint: https://arxiv.org/abs/1703.01658 ; https://arxiv.org/pdf/1703.01658
   - Artifact: arXiv:1703.01658v2, 20 December 2017; document dated 22 December 2017; 25 pages.
   - PDF SHA-256: be8d564da21e01abd15b963a7a1315905a39237455195ccb4443069db838ebf2.
   - Read abstract and continuously read Section 4.1 (including Proposition 4.3 and its displayed proof) plus Section 4.2 through its binomial inequality proof and beginning of Poisson transfer, printed pages 12–14.
   - Exact failed inference: a risk-transfer statement for a particular volume estimator is not a theorem transferring arbitrary cancellation-sensitive mixed moments. We use no such transfer from this paper.

Searches also screened primary abstracts/titles on maximal-point counts, random-polytopes volume CLTs, generating Pareto records, and exponential–uniform record identities. These were not followed into a broad bibliography; no negative existence or exhaustive-search claim follows. Third-party search snippets were discovery aids only, not mathematical authorities.

## Local dependencies

- retained-skyline-likelihood/RESULT.md: e5dce85e41eaf41e69c373c26793478fa057de293502c22eb0a133f85221b345. Exact fixed-count skyline density, family definition, f_c≥c, boundary limitation.
- skyline-count-information/RESULT.md: b96715873d240787ea6343538b4df54d94dc4bd7a52b79615fcaa9b2d34c2e4d. Count record law and Joe stochastic domination.
- skyline-likelihood-score/RESULT.md: ba6345d03e5fe9d2735f221ee45f5ee6b6f05508ce4d96f8ba9a86ceb3da5b5f. Local deterministic residual bound and no-global-remainder caveat.
- baseline-skyline-moments/RESULT.md: b7bdcfa8b7288d69d569b6ed904c314fe58e4795c92549a6d525c433ad7c139f. Read after it became available; background consistency, not needed for the exponential-tail proof.

The new fixed-count area MGF/tail and local residual-square bounds are this packet's elementary deductions from the stated source identity and already-proved local count/density facts. They are not results claimed verbatim from the source authors. Independent review must distinguish those deductions from the original published/preprint results.
