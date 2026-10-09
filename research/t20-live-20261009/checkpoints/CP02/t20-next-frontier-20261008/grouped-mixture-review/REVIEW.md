# Independent grouped-mixture review

Reviewed 8 October 2026 UTC. Author checkpoint: `grouped-mixture-identification/MANIFEST.json`, SHA-256 `baf29c6df8ba1047782a03f794409bf03a0bfe8394f04845bb2b876b6bcc75f6`. All six listed file lengths and hashes were checked before and after the review. The author files were read without alteration. Their frozen copies and a fresh replay are included here.

## Result

No mathematical blocker was found in the scoped claims. The classical finite-mixture moment argument transfers correctly to the previously established injective base4 code of finite unguarded histograms. The sharp examples use eligible histogram codes and positive rational weights. The process and oracle restrictions are substantive premises, not consequences of the identification theorem.

The strongest new reviewer control is that **equal observable endpoint marginals and the entire persistent-looking pair law do not establish the latent equal-second-marginal premise**. It strengthens the author's nonstationarity example without invalidating the stated theorem. Its complete exact law is below.

This is a mathematical and code review, not a Lean proof of the mixture stage, empirical validation, novelty/priority certification, source-level original-efficacy bridge, or owner acceptance. The earlier scalar result remains an imported theorem with its own receipt and assumptions.

## Proof assessment

### Finite mixtures and sharpness

1. Distinct finite unguarded histograms have distinct scalar codes by the preceding stage. For two mixtures with at most `k` components each, the signed difference has at most `2k` nodes. Its first `2k` moments, including normalization, annihilate every Lagrange polynomial of degree at most `2k−1`; each signed coefficient is therefore zero. Positive real weights are allowed for uniqueness.
2. For `2k` decreasing eligible nodes `(3/4)^j`, reciprocal Vandermonde denominators have alternating signs. Their normalized positive and negative parts each have exactly `k` atoms, agree through order `2k−2`, and disagree next. The coefficient comparison proof is correct, including `k=1`. Multiplying every node by `3/4` makes all inventories nonempty without changing the moment-equality orders.
3. With `2k+1` such nodes the same construction gives a `k` versus `k+1` ambiguity through `2k−1`. Hence the competitor bound cannot be discarded.
4. The complete length-`R` binary group law is equivalent to moments through `R`: expand `z^t(1−z)^(R−t)` in powers, then recover moments by marginalization. The exchangeable count law suffices, using normalized falling factorials. A single all-no-effect probability of order `R` alone does not provide lower moments.
5. Accordingly the sharpness is for this fixed-calibration grouped/moment instrument and maximum group length. It is not a sample-size lower bound, nor a lower bound for unrestricted interventions.

### Constructive and unknown-order claims

The Gram/Hankel rank is the number of distinct positive-weight nodes; its leading block of that size is positive definite. The displayed linear system recovers the annihilator uniquely, and Vandermonde inversion recovers weights. Under explicitly represented rational moments and the promised rational-node model, finite rational-root enumeration gives a terminating procedure. This is a valid existence-of-algorithm statement.

The supplied code is appropriately narrower: it tests a recovered polynomial against known fixture roots and then reconstructs weights. It does not implement generic polynomial factorization or an end-to-end histogram mixture decoder. Neither its tests nor this review should be described as such an implementation.

For an existing positive representing measure, equality through order `2s` forces the integral of the squared `s`-node annihilator to vanish. The competing measure is then supported on its roots. The first singular `(r+1)`-square Hankel matrix occurs at `r=s`; positive definiteness before that follows because a lower-degree polynomial cannot vanish at all `s` nodes. An infinite-support positive law has no such finite singularity. These arguments correctly retain the representing-measure promise and exact zero-testing contract. They do not turn arbitrary approximate moments or a merely positive-semidefinite truncated array into a certified measure.

A finite scalar-support certificate also does not certify finite actual route inventories: the preceding infinite-product mimics share every power of the same scalar code. All per-component finitude, visibility, unguardedness, calibration and independence assumptions survive composition.

### Process, continuation, and oracle claims

Conditionally independent repetitions from a held-fixed latent histogram produce power moments. Fresh independent latent draws within a group instead produce powers of the first moment. Holding the latent state fixed without independent emissions is insufficient; the copied-single-Bernoulli example preserves only the mean. Drawing the latent state once forever does not empirically sample the population mixture weights.

On a **nonempty** finite known candidate set, the diagonal instrument gives `K_0^j 1=q^j`; the horizon span has Vandermonde dimension `min(h+1,|X|)`. The inherited full-simplex continuous-coordinate theorem applies on that full domain. It supplies no automatic lower bound on the different sparse unknown-support domain. The source's nonempty-state condition is retained in this reading.

For equal latent second marginals and conditionally independent emissions given the pair, expansion gives `E[(Q−R)^2]=2(m_2−c)`. Equal full latent marginals are sufficient, while reversibility and the Markov property are unnecessary. Zero deficit gives anonymous-histogram equality only where scalar injection applies. The finite known-support gap bound follows directly by restricting the squared difference to changes. Unknown countable supports have no uniform positive separation. The certificate concerns the observed transition, not unobserved intermediate histories or bearer identity.

The finite-transcript Cauchy-oracle obstruction is valid: a sufficiently rare added high-index route keeps every finitely requested moment inside the given positive tolerance. The same continuity argument handles finitely many grouped-word probabilities. It concerns arbitrary valid enclosures at the prescribed calibration, not exact rational representations, canonical stronger encodings, or arbitrary new rate interventions.

## Stronger independent nonstationarity counterfeit

Let `H_j` denote `j` copies of the `{0}` route, so `q(H_j)=(3/4)^j`. At the first time let the histogram always be `H_1`, with `Q=3/4`. At the second time independently choose `H_0` with probability `3/7` and `H_2` with probability `4/7`. Thus `R` takes `1` and `9/16`; it never equals `Q`, so the anonymous histogram changes with probability one.

Given the two histograms, draw endpoint indicators independently with means `Q,R`. Then

- `E[R]=E[Q]=3/4`;
- `E[Q^2]=E[QR]=9/16`;
- `E[R^2]=39/64`, not `9/16`;
- `E[(Q−R)^2]=3/64`.

The complete observed pair probabilities, in order `(11,10,01,00)`, are exactly

`(9,3,3,1)/16`.

This is the pair law of independent repeats from the genuinely persistent point mass at `H_1`. Both observed one-time marginals agree. Even an independently known **first-time** scalar second moment would produce the spurious zero difference `E[Q^2]−E[UV]=0` if latent second-marginal equality were silently assumed. The theorem avoids the error by explicitly requiring that equality. Conditional emission independence holds in this counterexample; only the latent stationarity premise is removed. If nonempty inventories at both times are required, adding a common route to every component scales all scalar nodes and preserves the counterexample structure.

The separate author's stationary swap with correlated emissions removes the other key premise and also counterfeits the complete pair law. These two counterexamples isolate different failures; neither disproves the correctly conditional stationary identity.

## Replays and independent controls

Fresh frozen-author replay: all ten control families pass. Independent standard-library script: five control families pass:

- Twelve sharpness constructions through `k=6`, using signed maximal minors rather than the author's reciprocal-product formula, all components nonempty, comparing complete count laws.
- Thirty-six independently generated eligible mixtures of sizes one through four, checked by determinants/Cramer's rule: first singular Hankel section, annihilator, weights, nonnegative squared-polynomial certificate, and factorial-count moment recovery.
- Thirty-two stationary transition laws formed from weighted permutations, verifying both equal marginals, the square identity, and the gap-based change bound.
- The stronger nonstationarity full-pair counterfeit above.
- Independent corroboration of the correlated-emission stationary counterfeit.

These are finite exact checks supporting a separately read arbitrary-parameter proof. They do not establish its universal quantifiers by enumeration. All arithmetic in these controls is rational; no Monte Carlo inference, floating equality, generic root solver, or probability-oracle implementation is used.

## Replay and dependency instructions

From this review directory:

`PYTHONDONTWRITEBYTECODE=1 PYTHONOPTIMIZE=0 python frozen/exact_controls.py`

`PYTHONDONTWRITEBYTECODE=1 PYTHONOPTIMIZE=0 python independent_checks.py`

`python verify_receipt.py`

Runtime: Python 3 standard library only. The scripts run entirely from the review directory and do not need the predecessor code, network, external packages, or Lean. The mathematical import is separately bound to countable-author manifest `43681d0c2d070e30200afb7b3dc557396150bff9c8012e75bd0a72328a27a974` and countable-review receipt `40be03d0d6b9b983ed7b3c09edbbecc59a17ea56bc92695fff78c49e98cd5556`.

Only this review and its independent controls were produced here. The author stage and all previous frozen reviews were left unchanged. Work and source checks are prospective; no elapsed-time floor, historical active-work claim, final integration, or closure is certified.
