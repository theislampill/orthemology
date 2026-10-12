# Independent review: calibrated pairwise corroboration bounds

Date: 11 October 2026 UTC.

## Outcome and authority

No blocking mathematical, custody, or stated-scope defect found. The packet is acceptable as the bounded ordinary mathematical research result it claims to be. No author revision is requested.

This is an independent research review, not an ImplementAudit assessment, release, integration, historical authentication, programme acceptance, or T20/T21 closure. The parent explicitly confirmed this review's ordinary research scope. Review work and replay outputs are confined to this separate directory; author bytes are unchanged.

Reviewed author result:

- `pairwise-corroboration-bound-20261011/RESULT.md`
- SHA-256 `a86cced3f856527cbfab677458c2792e36bab1a89dc0684f3c5a0447c8ef0eb2`
- The associated `verify.py`, `CONTROL_RESULTS.json`, `INPUT_BINDINGS.json`, and `MANIFEST.json` were inspected and checked.

## 1. Independent derivation

### Exhaustive cell law and exchangeability

For eight atoms q_c of a binary correctness triple, normalization, three singleton moments p, and three pair moments p² impose seven independent affine constraints. The independent control script constructs their evaluation matrix and verifies rank seven by exact rational Gaussian elimination. Its one-dimensional null direction, in binary lexicographic order, is

    (-1, +1, +1, -1, +1, -1, -1, +1).

Taking t=q_111 as the free coordinate determines q_110=q_101=q_011=p²−t, q_100=q_010=q_001=p−2p²+t, and q_000=1−3p+3p²−t. Thus equality of masses for patterns with equal Hamming weight is a consequence of the declared equal first and pair moments. Exchangeability is not a hidden added premise. This fact is special to the declared three-bit, equal-calibration setting; no general exchangeability inference is warranted.

For arbitrary p in [0,1], nonnegativity is equivalent to

    max(0, 2p²−p) ≤ t ≤ min(p², 1−3p+3p²).

On the author's p in (1/2,1), these endpoints become L=p(2p−1) and K=1−3p+3p², with K−L=(1−p)². The endpoint exclusions and the interior full-support statement in RESULT lines 31–52 are correct.

### Sharp posterior range

Under the author's truth symmetry, the two likelihoods of E={Y=111} are t and K−t. For prior alpha in (0,1),

    f_alpha(t) = alpha*t / [alpha*t+(1−alpha)*(K−t)].

Its denominator is positive throughout [L,K]; its derivative is alpha*(1−alpha)*K divided by the squared denominator, hence strictly positive. The exact closed range is therefore

    [ alpha*L / (alpha*L+(1−alpha)*(1−p)²), 1 ].

Both endpoints are realized. With strictly positive cells, t lies in (L,K) and the posterior range is correspondingly open. The Bayes factor has lower endpoint L/(1−p)² and extended upper endpoint +infinity. A zero false-state likelihood is permitted at t=K because the conditioning event still has positive unconditional probability alpha*K.

The lower Bayes factor is at least one precisely when p²+p−1≥0, or p≥(sqrt(5)−1)/2 on this domain. At equality the lower boundary is neutral; all interior models are favorable. Below the threshold, the set L<t<K/2 is nonempty and consists of full-support reversals. All of these claims in RESULT lines 58–78 are correct. At alpha=1/2 the range simplifies to [L/K,1].

The p=3/5 controls independently yield posteriors 3/7, 13/28, 5/7, 27/35, and 1 for the packet's five t values. The product channel is exactly t=p³, and its eight recovered atoms equal the product Bernoulli probabilities. The 13/100 and 1/5 channels have strictly positive atoms and opposite evidence directions.

## 2. Symmetry, report frequencies, and all proper marginals

Truth symmetry is substantive, and the packet correctly says so in RESULT lines 31–37. Pairwise truth-conditioned independence with the same accuracy alone permits two interaction parameters t_0 and t_1. Requiring the correctness vector to be independent of truth identifies them. The packet never silently derives that identification from pairwise independence.

For its shared t and equal prior, q_y and q_complement(y) have opposite free-coordinate coefficients. Their average cancels t exactly. The entire unlabelled law is K/2 on each unanimous pattern and p(1−p)/2 on each other pattern. Separately, each (X,Y_i,Y_j) marginal is fixed by the prior and pairwise calibration. These are all four three-coordinate projections of (X,Y_1,Y_2,Y_3), so every proper marginal is fixed. The claim is about the complete report distribution, not merely pairwise report statistics.

This equality extends to every finite iid sample by taking products. The independent script additionally checks all 64 ordered two-sample outcomes. The claim does require fresh independent target instances under the same balanced stationary experiment. The packet states those conditions and explicitly excludes changed sampling and calibration experiments.

With known unequal alpha in the same truth-symmetric model,

    P(Y=111)=(1−alpha)K+(2alpha−1)t

has nonzero slope, so its population frequency identifies t. RESULT lines 104–108 correctly prevent transporting the balanced nonidentifiability claim to that setting. This is population identification, not a finite-sample exact-estimation guarantee.

### Additional adversarial boundary control, not a requested extension

The sharp posterior bound before supplying unlabelled frequencies actually survives relaxing truth symmetry. With separate t_0,t_1 in [L,K], the posterior is

    alpha*t_1 / [alpha*t_1+(1−alpha)*(K−t_0)].

It increases in both parameters. Its minimum is attained at t_0=t_1=L; its maximum is one whenever t_0=K. The independent controls check this across 81 asymmetric models.

However, unequal-prior identification fails in that broader class. An exact countercontrol at p=3/5 and alpha=2/3 compares

    A: (t_0,t_1)=(1/5,1/5), posterior 5/6;
    B: (t_0,t_1)=(11/50,21/100), posterior 7/8.

Both joint laws have full support and identical every proper marginal, including the entire unlabelled report law. This follows because alpha*delta(t_1)=(1−alpha)*delta(t_0). This control confirms why the packet's common-parameter premise must remain attached to its unequal-prior identification sentence. The current text already supplies that premise; the control is not a defect or an instruction to expand the author packet.

## 3. Endpoint and tensor checks

The exclusions p>1/2, p<1, and 0<alpha<1 avoid real singular or degenerate regimes:

- At p=1/2 and interior prior, the interval becomes [0,1]. The strict L>0 reasoning must be replaced, though the event remains positive for the author's symmetric family.
- At p=1 the only channel is perfectly correct. The posterior on E is one for alpha>0, but the displayed lower-bound ratio in its limiting form cannot be evaluated as 0/0.
- At alpha=0, every possible E has posterior zero; E is impossible at t=K. At alpha=1, the posterior is one whenever E is possible. When p=1/2 and t=0 it is impossible.
- An impossible event has no posterior. The independent controls return an explicit absence of a posterior for these cases rather than silently treating it as an endpoint value.

The author makes no extension to these excluded regimes, and no correction is needed.

For signs S=2X−1 and W_i=2C_i−1, Z_i=S*W_i. Therefore S*Z_1*Z_2*Z_3=W_1*W_2*W_3 and expansion gives tau=8t−12p²+6p−1. Its nonzero coefficient identifies t, hence the full joint law within the declared family. At equal prior, the ordinary three-report interaction is already fixed and is not this missing quantity. The packet correctly distinguishes correctness order three from the truth/report interaction order four. It does not equate tensor grade with historical authentication or causal independence.

## 4. Custody, inheritance, and conclusion ceiling

Every four-entry author manifest binding matches both byte count and SHA-256. All 17 records in INPUT_BINDINGS also match, covering 14 unique prior files. The three Library-input records remain bindings of normalized local read projections. The recovered INPUT_PROVENANCE explicitly distinguishes those projections from original download bytes and records the prior completed reading; this review does not establish fresh remote Library custody or assign fresh complete-attachment-reading credit.

Credit checks used the full bound Deep AX V2 source, the opening inheritance/result sections of the provenance-learning, tensor-likelihood-closure, and historical-source-revision packets, relevant scope passages of the supplement and the communication/content-access reports, and the full local CONTEXT_ADDITION projection. Targeted inspection agrees with the claimed inherited ownership:

- Deep AX already states joint Bayesian updating, conditional root factorization, and possible evidence reversal from marginal multiplication.
- Provenance learning already separates duplicate-root identity from numerical evidence and warranted factorization.
- The graded-interface parity mechanism is explicitly credited by the bound tensor-likelihood and historical-source-revision reports. Tensor-likelihood closure owns its stronger passive-update no-go statements under its own full-simplex and support conditions.
- The new packet does not rebrand parity, all-proper-marginal insufficiency, root factorization, or a generic tensor no-go as newly discovered mathematics. Its increment is the calibrated family, sharp positivity-constrained interval, and evidence threshold.

No exhaustive project or literature priority search was performed or certified. The inherited repository pin was read as provenance metadata, not freshly remotely authenticated. Upstream full proofs were not re-reviewed wholesale.

The philosophical application remains properly bounded: no actual source accuracy, scripture comparison, causal provenance, prior warrant, absence of all epistemic warrant, theological verdict, or change to affirmative appraisals is inferred. The historical admissibility, meaning attribution, communication purpose, temporal access, and warrant obligations are retained. The mathematical countercontrol is relevant to the supplied research connection without pretending to discharge those obligations.

## 5. Executed verification

Execution order was independent controls first, copied author replay second.

1. `python3 pairwise-corroboration-independent-review-20261011/independent_controls.py`
   - PASS, 14,163 exact assertions.
   - Independent Gaussian-elimination derivation; 365 general-accuracy models including p=0, p=1/2, p=1; 81 truth-asymmetric models; prior endpoint guards; tensor and proper-marginal checks; all stated custody bindings.
   - Does not import or execute author code.
2. Copy of author `verify.py`, run only under this review's `author_replay/` directory.
   - PASS, 39,280 exact rational assertions, 1,296 grid models.
   - Replayed CONTROL_RESULTS is byte-identical to the author's retained result.
   - The copied script is byte-identical to the bound author script.
3. Before/after hash comparison of all five author files.
   - No author-byte change. Only review-local files were created.

Portable mathematics-only replay: `python3 independent_controls.py --mathematics-only`. This performs 14,120 mathematical assertions and explicitly skips all upstream custody reads. It writes a distinct `MATHEMATICS_ONLY_RESULTS.json`; it must not be represented as replaying the custody checks. The original full replay requires the author packet plus the 14 locally bound prior files at the relative paths in INPUT_BINDINGS.

At the parent's request, the truth-asymmetric boundary above is also preserved separately in `pairwise-corroboration-asymmetric-supplement-20261011/SUPPLEMENT.md`, with a standalone `verify.py`. That reviewer-authored supplement does not silently amend the independently reviewed symmetric author theorem and does not claim independent review of itself.

The controls corroborate the ordinary general proof and targeted source/scope inspection; they are not universal formal-kernel certification. `RECEIPT.json` binds the inspected author snapshot, executed control outputs, and this review. No unresolved blocking finding or required edit remains within this review's stated scope.
