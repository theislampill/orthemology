# Independent review: fixed-count skyline-area concentration

8 October 2026 UTC. Scratch-only mathematical/source review. Historical floor remains UNVERIFIED.

## Verdict

PASS within the stated scope. No blocking mathematical or source-mapping defect was found. The area MGF/tail, positive-integer raw-moment bounds, and localized residual-square consequence follow for both declared hard-pair worlds. This verdict does not certify a fixed-count CLT, cancellation-sensitive fourth moment, likelihood information rate, physical observation contract, kernel proof, protected integration, or closure.

The verdict is bound to these exact author files:

- RESULT.md: `ff663eca1abe6b680ef9ed615eb8978484e78ff6a3c2debc13b9cc0e0ddaa945`
- SOURCE_AUDIT.md: `a297002371f620dcf0233f0e5d494b617b3b406ed4d7be4299630cd0aad69ba7`

The supplied MANIFEST.json is also recorded in VERIFICATION_MANIFEST.json. No author or predecessor file was changed.

## Checks that carry the verdict

1. **Exact geometry and finiteness.** With all Borel subsets of the compact square in the localizing ring, configurations are finite. Their Pareto generator retains every minimal support point with its multiplicity. The hull is the union of upper rectangles minus the minimal support points; consequently the complementary stopping set contains precisely K observed points but has route-law mass V=μ(E). Retaining the minima and replacing all hull points cannot create or remove a minimum. This proves the source stopping identity, including the empty configuration. Finite coordinate comparisons give measurability. The generator axioms also hold. Absolute continuity removes the vertex/boundary mass without incorrectly removing those points from the count.

2. **Actual source theorem and proof.** I read the local PDFs through freshly regenerated text, which was byte-identical to the supplied extracts, and visually checked the key formula pages. [Efron type identities](https://arxiv.org/abs/2608.06038), Section 2 and Theorem 2.1, make this finite stopping set a Markov set. Theorem 4.7 and its full proof on printed pages 8–9 require λ(1−e^(−f))<∞. For intensity λμ and constant f=t≥0 this is automatic and yields exactly E exp[−tK+(1−e^(−t))λV]=1. Corollary 4.8, including its coefficient-comparison proof, gives the stated falling-factorial identity because the entire square belongs to the localizing ring. Example 8.4 agrees with the Pareto order used here. No infinite-hull extension is needed.

3. **Poisson compensation.** [Poisson hulls](https://arxiv.org/abs/2212.02150), Example 2.15, Theorem 3.2 and proof, Lemmas 4.3–4.4, and Theorem 5.1 and proof give F̂=λ(1−V)+K, mean λ, and variance λEV=EK. Constant functions are integrable and square-integrable under the finite intensity, even for the unbounded Joe density. The uniform void-probability integral gives the stated logarithmic asymptotic. The separate skyline-density Poisson mixing calculation has the correct ordered-stratum factor and empty-stratum mass; its intensity-ratio argument independently verifies the specialized exponential identity.

4. **Conditioning and Cauchy–Schwarz.** The alternative route law μ_c is held fixed at c=n/(n+1) while the auxiliary Poisson total varies. Conditioning on N=m−1 or N=m therefore gives precisely the intended two laws. The ratio of the two Poi(m) masses is m/m=1. For A=exp[−(log 2)K+Z_j/2], nonnegativity gives E_j A≤1/p_m. The decomposition exp(Z_j/4)=A^(1/2)2^(K/2) gives the stated Cauchy–Schwarz bound without any independence assumption.

5. **Inherited inputs.** The hashed density packet proves f_c≥c, so mμ_c(E)≥mcU=nU. The hashed count packet's TP2/conditional-quantile argument correctly couples every Joe lower-record indicator below the corresponding iid-uniform record indicator. Thus E_j 2^K≤m+1, by the exact telescoping record MGF. The baseline uses R_n and has the slightly stronger bound n+1. Together these facts prove (1) with its displayed constant.

6. **Tail, moments and localization.** Markov gives (2) with B_m=2 log((m+1)/p_m); Stirling yields 3 log m+O(1). Domination by B_m+4 Exp(1) proves the finite binomial-sum bound for each positive integer r. The analogous count tail and m/n≤2 give E_j(K+mU)^r=O_r((log m)^r). On the score packet's domain K/m≤1/2 and U≤1/2, K≤m−1, so common support is automatic. Squaring its deterministic bound gives 1600(K/m+U)^6; integration proves (11). Outside that domain the residual has not been defined or bounded, and the indicator is correctly retained.

## Scope and source-audit boundaries

The actual source has the claimed theorem, hypotheses, proof and Pareto examples. The official arXiv records independently confirm the two versions and dates. The audit distinguishes the 2026 preprint from the published earlier work, identifies the indirect spatial-Markov dependency, and does not claim to have read the supplementary normal-approximation proofs or Zuyev's original equation. I checked the Section 7 statements: their application-specific error terms remain unevaluated here.

The limited secondary checks also support the stated exclusions: Fill–Naiman's exponential-coordinate record region maps to area through the weight exp(−x−y), and Baldin's Proposition 4.3 concerns the named volume estimators and minimax risk, not arbitrary mixed centered moments. No new broad search was performed. This review does not retrospectively certify how much an author read or spent researching, and it does not independently verify the journal body or all recursively cited proofs.

The packet explicitly withholds fixed-count CLT/KL/Hellinger rates, sharper compensated fourth moments and global likelihood-tail control. Those boundaries are necessary and are respected.

## Verification record

VERIFICATION_MANIFEST.json records the exact inputs, actual read scopes, PDF/text consistency checks, source-page visual checks, and supplementary exact-arithmetic/finite-grid controls. These controls test consistency; the written source mapping and arguments above carry the general result.

