# Primary ancestry and source-return record

Checked 8 October 2026 UTC. This is an elementary specialization and synthesis of established interpolation, binomial factorial moments, concentration, mean-value bounds, and two-point testing. No general novelty claim is made. The rational controls check finite instances; they do not establish any general theorem or new formal verification result.

## 1. Frozen predecessor

Read the complete `RESULT.md`, `PROCESS_AND_ORACLE_BOUNDARIES.md`, `SOURCE_AUDIT.md`, and `MANIFEST.json` in `../grouped-mixture-identification/`. Independently verified the manifest's SHA-256 as

`baf29c6df8ba1047782a03f794409bf03a0bfe8394f04845bb2b876b6bcc75f6`.

All six payload hashes listed by that manifest were also recomputed successfully. No file in that stage was altered. Imported content is the finite eligible base4 histogram code, its injection, the common-latent grouped-binomial interpretation, the factorial-moment identity, and the earlier process/oracle/ownership boundaries. This stage does not reprove the imported primitive-prime injection.

The predecessor's ordinary classical Lagrange/Vandermonde argument is used directly for the known catalogue. Its source audit points to standard finite-atomic moment and Prony ancestry. Moving from a known catalogue to a noisy finite sample is the bounded question pursued here, rather than a claim to invent polynomial inversion.

## 2. Concentration: Hoeffding's original paper

Wassily Hoeffding, **Probability Inequalities for Sums of Bounded Random Variables**, *Journal of the American Statistical Association* 58(301), 13–30 (1963), [publisher record and abstract](https://www.tandfonline.com/doi/abs/10.1080/01621459.1963.10500830), DOI `10.1080/01621459.1963.10500830`.

The publisher's primary record and abstract were inspected. They identify independent bounded summands and range-dependent tail bounds. The direct publisher PDF returned HTTP 403. The author's May 1962 precursor, UNC Institute of Statistics Mimeo Series No. 326, was located in the [NC State institutional archive](https://repository.lib.ncsu.edu/bitstreams/d0e6ed15-3e1c-432f-8419-e55ffb6f3171/download), but attempts to open its full text encountered a bot-verification page. Search indexing exposed its title and abstract; this is not recorded as a full-paper or theorem-page reading. The [collected-works publisher page](https://link.springer.com/chapter/10.1007/978-1-4612-0865-5_26) supplied another primary publication record and the same abstract, not the full proof.

The exact inequality used here is the standard two-sided bounded-summand Hoeffding inequality. `RESULT.md` gives its exponential-tilting variance proof, so no uninspected theorem text is needed to justify its constant. Applying the bound to finitely ranged contrasts and taking a union bound are straightforward specializations. We do not transfer a dependent-sample extension merely because the original paper also discusses such settings.

## 3. Polynomial/binomial ancestry: Bernstein

S. Bernstein, **Démonstration du théorème de Weierstrass fondée sur le calcul des probabilités**, *Communications de la Société mathématique de Kharkow*, second series 13(1), 1–2 (1912). Primary archive: [article and full-text link](https://www.mathnet.ru/eng/khmo107); [original two-page PDF](https://www.mathnet.ru/php/getFT.phtml?jrnid=khmo&option_lang=eng&paperid=107&what=fullt).

The full two-page extracted text was retrieved and read. The opening page expresses a binomially weighted polynomial as the expected payoff after repeated Bernoulli experiments; the ending restates the binomial polynomial representation used for approximation. This is primary ancestry for interpreting Bernstein-basis polynomials through binomial counts. The retrieved text has imperfect mathematical OCR, so no transcription of its exact formula or claim of a visual full-page audit is used as evidence here.

The present estimator's coefficients `b_i(s)` are obtained by **exact inversion** of a degree-`R` polynomial into the Bernstein basis. They are not generally `L_i(s/R)`, and ordinary Bernstein approximation must not be mistaken for exact reproduction of arbitrary degree-`R` polynomials. The factorial proof and adjacent-difference derivative identity are proved explicitly in `RESULT.md`. We do not claim Bernstein's paper states this catalogue estimator or its statistical guarantee.

## 4. Grouped-mixture primary context

Robert Vandermeulen and Clayton Scott, **An Operator Theoretic Approach to Nonparametric Mixture Models**, *Annals of Statistics* 47(5), 2704–2733 (2019), [primary author preprint](https://arxiv.org/pdf/1607.00071), DOI [10.1214/18-AOS1762](https://doi.org/10.1214/18-AOS1762).

Fresh targeted inspection covered the abstract, introductory random-group formulation, and Section 3 setup, printed pp.1–3. It explicitly draws one component and then conditionally independent identically distributed samples from that component. This confirms the classical grouped-data setting inherited from the predecessor. The predecessor records a wider inspection of its identification thresholds; this stage does not claim to have repeated that full inspection or derive a new threshold.

The familiar distinction between population identifiability and finite-sample stable recovery is retained. The unknown-label counterexample in the present report uses a directly proved coupling and two-event testing inequality, not a claimed new general mixture lower-bound theorem.

## 5. Evidence and accounting limits

All finite computations use Python integer/fraction arithmetic and exhaustive sums over small count laws. No observations were collected, no random simulation was run, and no empirical calibration or process premise was validated. No Lean file or theorem was added. Source discoveries, analytic derivations, and exact controls are different evidence layers.

`ACTIVE_RESEARCH.jsonl` contains only prospective starts and milestones for this worker's work. Initialization before its recorded start is not credited; no elapsed-time total is offered as a substitute for active time. Waiting, packaging, and other workers' concurrent work are excluded from research credit. This is an author checkpoint, not independent review or final integration.
