# Independent review of same-threshold replay

8 October 2026 UTC. Verdict: **PASS within the explicitly declared probability and observation model.** No substantive mathematical, boundary, attribution, or source-scope defect was found. This is a review receipt, not integration authority or T20 closure.

The reviewed author manifest is ../same-threshold-replay/MANIFEST.json, SHA-256 f58c75e855e51be1bf4818b2b4ea6a91b1b5e685cbd45cfe304e9c3627fcbf53. All ten payloads match its recorded hashes and lengths. Six bound source inputs, three predecessor manifests, and their 27 payload entries also match. Author and predecessor bytes were checked again after the isolated author-script replay. No author or predecessor file was edited.

## 1. Independent work and review sequence

The proof in independent_derivation.md and the separate rational controls in verify_controls.py were written before the frozen author packet was read. Their hashes and lengths were recorded in preinspection_manifest.json at 16:05:19 UTC. The author supplied the frozen manifest at 16:07:36 UTC, after which its full contents were inspected. The independent derivation file has SHA-256 509e3cf6a45f05c80f3393e1145339ceb5dd61d3a079869c656670dba6b5f3f3 and remains unchanged.

The parent supplied the conjecture and candidate small-command/AM-GM strategy. Independence here means independent checking, derivation, and controls, not independent discovery of that strategy. Before the freeze the reviewer additionally derived the full three-bit strengthening of the high-command alias and communicated it to the author, whose frozen result attributes it accurately.

The preinspection derivation's final section records its then-pending frozen-payload inspection. That is a retained historical status; this report and the receipt record the completed inspection.

## 2. Scoped verdicts

1. **PASS: observation-law derivation.** Uniform marginal threshold pairs and one marginal calibration per coordinate, shared across all route occurrences, imply D_j(a,1)=alpha(a) and D_j(1,b)=beta(b). Mutually independent route vectors give the fresh and replay products. Reuse of the same threshold vector across the two distinct face commands supplies the intersection event represented by J. Separately readable outputs, correct pairing, and no query-induced state change or output latch are explicit premises.
2. **PASS: count and calibration rigidity.** The face laws give c=n/m and alpha=beta=H_c. Probability inequalities and scalar log estimates determine the coefficient of t^2 in log J as -nc without differentiating any unknown copula. The target coefficient -n forces c=1. Every finite m is covered; no unjustified uniform-in-m remainder or finite-panel conclusion is used.
3. **PASS: individual within-route factorization.** For any interior point the two prescribed products are positive. AM-GM applied separately to R_j and S_j has nonnegative gaps whose sum is zero. Both equality cases therefore hold, giving every K_j(a,b)=ab. Copula boundary identities handle the closed square and avoid logarithms of zero.
4. **PASS: Joe separation control.** Substitution into the inherited joint command-space CDF gives the stated replay law. At n=1,m=2,a=b=1/2 its value is 11/4-sqrt(6), strictly greater than 1/4. The formula is derived directly; no fresh external naming or novelty claim is needed.
5. **PASS: persistence distinctions.** Independently refreshed thresholds give products of face marginals. Held thresholds at an unchanged command duplicate one deterministic bit. Held thresholds at different commands yield the new joint statistic. Neither inventory persistence nor conditional-independent grouped-mixture semantics can be substituted for this additional contract.
6. **PASS: fixed finite-grid global-factorization obstruction.** The polynomial perturbation has a globally positive density by a coefficient-norm bound, retains uniform margins, agrees at every finite-grid vertex, and differs off-grid. Vertex agreement implies all cell masses agree. A full within-grid replay response is determined by those cells, so all stated transcript laws agree. Keeping m=n suffices for this obstruction; no count impossibility is inferred.
7. **PASS: explicit high-command count alias.** The two stated valid copulas, with shared H_(1/2) calibration, match the two face marginals, fresh interior law, paired-face law, and the entire three-bit held transcript at t=3/4. Agreement is not claimed outside that panel.
8. **PASS: bounded source and semantic claims.** The packet identifies its inherited mathematics, limits its reading claims, distinguishes probabilistic from original-source independence, and makes no physical replay, psychological manipulability, finite-sample certification, integration, owner-acceptance, or T20-closure claim.

## 3. Proof audit details

### Marginal premise and face argument

Endpoint preservation alone would not identify each route's face response if route marginals were unrelated. The frozen author avoids that gap by using uniform-marginal copulas and shared alpha,beta. Homeomorphism regularity is stronger than the independent proof needs but introduces no problem. The theorem can instead begin from the explicit common-marginal identities; its face equations then force the required regular form. The empty-inventory case is excluded; it would in any event contradict the nonconstant target for n>=1.

### Remainder control without copula derivatives

For d_j(t)=D_j(t,t), the product identity gives 0<=d_j(t)<=1-(1-t^2)^n=O(t^2). This finite family bound makes sum d_j^2=O(t^4). Applying log(1-z)=-z+O(z^2) to the fresh factors proves sum d_j=nt^2+O(t^4). With u=ct+c(1-c)t^2/2+O(t^3), the replay log expansion has terms -2u+d_j-2u^2; all omitted mixed terms are O(t^3) or smaller. Summation gives -2nt-nct^2+O(t^3). The proof needs neither differentiability nor absolute continuity of any K_j, so singular comonotone or lower-bound copulas are admissible.

Both logs are used only near zero where all factors tend to one. Equality of the all-command laws permits taking t down to zero with the fixed alternative m. Dividing the coefficient difference by t^2 leaves a vanishing O(t) remainder. No empirical derivative estimation or finite sample passage is implied.

### Complementary-product equality

At an interior command pair, R_j+S_j=2-a-b. Their geometric means are respectively 1-ab and (1-a)(1-b), whose sum is the same constant. The sum of the two AM-GM gaps is exactly zero, not merely bounded. Equality forces each family constant. The proof then extends via the exact boundary margins, with no hidden continuity or division-at-zero step. It also holds when n=1.

### Finite-grid interpretation

The density certificate is global: M=sum k|f_k| bounds |f'| for every x in [0,1], not merely sampled x. Epsilon<=1/(2MN) therefore gives density at least 1/2 everywhere. Integrating obtains xy+epsilon f(x)g(y); endpoint roots ensure the two uniform margins and total mass one.

A fixed grid partitions each route's threshold square into cells. Every command response, every ordered word of retained-threshold responses, and the aggregate endpoint word are deterministic functions of those cells. Independent route vectors have product cell distributions; independent fresh batches likewise preserve equality. This is why the result concerns complete transcript laws rather than isolated marginal probabilities.

The packet correctly limits its conclusion to fixed finite panels and does not assert a universal adaptive/randomized impossibility. As an optional mathematical extension, the same argument covers a bounded deterministic binary-outcome adaptive decision tree whose union of coordinates across all branches is finite; that extension is in the independent derivation and is not needed for the frozen packet's claims.

### High-command control

At calibrated threshold 1/2, route 1 has gate table p00=p11=1/2 and p10=p01=0. Route 2 has p00=p11=1/8 and p10=p01=3/8. Independent composition gives the held endpoint-bit law

- 000 with probability 1/16
- 100 with probability 3/16
- 010 with probability 3/16
- 111 with probability 9/16

These are exactly the one-route independent probabilities at threshold 3/4. The alternative's first route either supplies both face hits and the interior hit, or supplies none; in the latter case route 2 alone determines the three bits. Therefore the interior bit equals the AND of the two aggregate face bits. This verifies the claimed stronger transcript equality, without extrapolating it to asymmetric or off-panel commands.

## 4. Evidence and reproducibility

### Independently written controls

verify_controls.py uses Python Fraction arithmetic only and imports no author code. It checks:

- Exact Q=7/16, J=1/16, and each face no-hit=1/4 for the count alias.
- Exact equality of the full held three-bit laws by route-cell enumeration.
- A different explicit finite-grid perturbation on {0,3/4,1}, with f(x)=x(1-x)(x-3/4), epsilon=1/128, global density lower bound 1207/2048>1/2, all four unchanged grid-cell masses, and off-grid copula difference 1/32768 at (1/2,1/2).
- Exact coefficient arithmetic over 121 independently chosen m,n pairs; this is an arithmetic diagnostic, not the proof of the universal theorem.

The preinspection source and exact result JSON were reverified after frozen-payload inspection.

### Isolated author replay

The author script was copied byte-for-byte into this review's replay directory and executed there. Its relative output writes therefore stayed in the review, never in the frozen author packet. It completed with exit code zero and passed 16,598 assertions in 29 families. Its generated JSON and stdout matched the frozen results byte-for-byte. These checks are supplementary evidence; global claims rest on the written proof and density certificate, not finite enumeration.

verify_evidence.py verifies the author manifest, all ten author payloads, all six explicit source inputs, the actual three predecessor manifests and their 27 payload entries, the independent preinspection file identities, and output equality. It repeats external binding checks after replay. Its complete record is evidence_verification.json.

## 5. Source inspection scope

All ten frozen author payloads and the author manifest were read in this review, including the script, output records, source audit, source bindings, and milestone events. The predecessor RESULT.md, SEMANTIC_GUARD.md, SOURCE_AUDIT.md and dependent-gate-transport-review/REVIEW.md were read in full. The grouped-mixture PROCESS_AND_ORACLE_BOUNDARIES.md was read in full. The grouped-calibration RESULT.md was read only through its initial 100 lines, matching the declared targeted source use.

Predecessor manifest payloads were mechanically hash-verified; that is not a claim that every script, web-response record, or ancillary output in those manifests was substantively reread or executed. The preceding independent review is evidence of its own scoped checks, not authority to expand this review's coverage. No predecessor control script was rerun.

No new external paper, software package, or web source was read in this review. The Joe family attribution is inherited from the bound prior primary-source records; the formula needed here is also directly rederived from the prior joint CDF. Original-paper full-text reading, historical priority, field-wide novelty, and source-level causal warrant are not claimed.

## 6. Receipt boundary

This review establishes mathematical consistency, correctness of the scoped derivations and explicit controls, source-accounting consistency, and byte-bound reproducibility for this particular frozen packet. It does not review or depend on the separate finite-panel-replay count-certificate task. It does not certify empirical replay availability, finite-sample identifiability, route-pair independence from data, metaphysical original-source independence, or source-domain perfection/complete-willing premises. It authorizes no integration or closure.
