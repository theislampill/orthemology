# Independent review: repair/evidence commutation

10 October 2026 UTC. Active T20, separate read-only mathematical review. **PASS at the stated scope; no revision requested.** This disposition supplies evidence to the parent only, with no closure, integration, release, protected-edit, or formal-certification authority.

## Bound object and executed evidence

The reviewed author `RESULT.md` has SHA-256 `3b55fa93bdfc680be53ebc80cc30308f4db9bddb8a8ffae65898200e97a69c4c`. Its verifier has SHA-256 `f80b578ea22f3f052655fdbd1dabe500947d4584df0fb116b6fea400305e2367`; its author receipt has SHA-256 `922add6ac8a031f7eb24f6b9a8326cf4138ee9da00ea3c0acb7be1b3575fb769`.

- Read the complete author report and verifier. Examined the inherited classifier's definitions, compact-convex generation proof, Theorem 1 and limiting cases; the Bayes-feasibility report §§5–6; the nonseparable report's definitions and main normalization statement; the channel-natural report's main contract; and the face-stratified report's Theorem 2, preservation statement and product controls. This is a bounded local comparison, not a complete re-review of every predecessor or its external literature.
- Verified every author-manifest entry and all five bound predecessor hashes. Replayed the author verifier in `author-replay/`, never in the original directory. All 12 author groups pass; the reproduced receipt and stdout match the preserved author bytes exactly.
- Independently wrote `verify_review.py`, importing no author module. Nine exact symbolic/rational review groups pass with Python 3.12.14 and SymPy 1.14.0. `SOURCE_BASELINE.json` and the final check bind and preserve all original author files, including pre-existing cache bytes, plus the five predecessor reports.

## Mathematical assessment

1. **Well-posedness and orientation:** finite positive second argument, compact nonempty C and strict convexity of the continuous first-argument objective give a unique KL(q||p) minimizer even on boundary-only C. No gradient at a forced zero is used.
2. **Inherited classification:** normalization gives the convex Bayes-plausibility decomposition of each extreme c. All-outcome invariance forces each posterior to equal c, so every supported state has the same entire channel column. The predecessor's finite-dimensional extreme-point generation proof then yields the block join. Conversely a join is invariant by independent block reweighting. Neither a single selected likelihood nor merely current-prior feasibility supplies this argument.
3. **Constructive sufficiency:** the disjoint-block KL chain rule minimizes conditionals first, then gives the exact gap KL(w||w*)−log Z, with w*_a=s_a exp(−d_a)/Z. Input masses on selected blocks need not sum to one. Every selected block retains positive projected weight, though coordinates within it may vanish. Block-constant evidence changes only those weights, proving commutation at every positive off-model input and the value identity (5).
4. **Boundary necessity:** the proposed p_e=(1−e)c+eu is positive; optimality gives D(q_e||p_e)≤−log(1−e). Pinsker plus p_e→c proves q_e→c. Thus B_y(q_e) lies in C by commutation and converges to B_y(c) by strict positivity of the channel. Closedness closes the argument. This does not assume continuity of a boundary-second-argument projection, or that C has any strictly positive member.
5. **Operator separation:** the moment-fibre selector minimizes D(q||r) on an input-dependent fibre. For positive inputs its opposite-orientation interpretation over the fixed exponential-model closure is correctly justified by moment matching. That generally nonconvex range is not this theorem's fixed convex C. Preserving that range does not imply its selector commutes off-model. The ambient normalization and cross-dimensional divergence-contraction predecessors likewise have distinct codomains/contracts.

No defect found in the author curved-disk, omitted-block, fixed-marginal, Euclidean or zero-channel-entry controls. Their stated limits are necessary to interpret them; they do not establish a uniqueness theorem for KL or an extension to undefined zero branches.

## Fresh exact controls

The new combined example differs from the author's symmetric control. Its selected blocks have three coordinates each, plus one omitted singleton block.

- A: disk centered at (1/3,1/3,1/3), squared radius 1/18; input conditional (192,16,1)/209; unique repair (1/2,1/3,1/6); cost log(209/96). Its gradient equals a constant vector minus 18 log(2) times the disk's outward normal. Cauchy–Schwarz and convexity certify the global minimum without a symmetry argument or numerical optimizer.
- B: {(t,1−t,0): 3/4≤t≤1}; input conditional (3,16,45)/64; repair (3/4,1/4,0); cost log 8. The one-variable derivative is positive throughout the allowed segment. This forces a zero *inside an active block*, separately from omitting the third block.
- Block input masses: (1/2,1/3,1/6). Three outcome columns: A=(1/2,1/3,1/6), B=(1/4,1/4,1/2), omitted D=(1/3,1/2,1/6). Each is positive and normalized.
- Z=1361/5016 and the repair is (576/1361,384/1361,192/1361,627/5444,209/5444,0,0). All three outcomes commute exactly and satisfy both the cost formula and value identity.

Additional checks include an all-boundary noninvariance witness, approximation to an endpoint of a proper boundary segment, Pinsker's binary curvature bound, the author scope-discriminator arithmetic, and a fresh asymmetric positive product-completion countercontrol. For prior (1/2,1/6,1/12,1/4), unary positive evidence yields completed means (1/5,1/10), whereas evidence after completion yields (1/5,−1/6); both outputs are product laws. The opposite-orientation Pythagorean identity is checked independently.

## Additional consequence and limitations

`SAMPLING_LAW_COROLLARY.md` records the parent's post-freeze suggestion, verified separately: expected reverse-KL repair cost increases by KL(a||b) under original outcome probabilities a, but decreases by KL(b||a) under repaired probabilities b. A finite forward-KL chain rule has a separate orientation and support requirement. This adds no change to the frozen author packet and claims no field novelty.

The universal theorem is supported by ordinary proof review; finite exact checks are supplemental, not a proof-assistant certificate. No external literature survey, statistical test, general minimization algorithm, normative justification of C, source reliability, evidence availability, actual warrant, or psychological conclusion is established. T20 remains active under the parent's authority.

Two initial review-harness issues were corrected locally and their logs retained: an equivalent logarithm normal form not simplified under a symbolic domain bound, and SymPy's construction of huge integer log powers. The final verifier uses an exact additive prime-log normal form and unchanged mathematical test targets. These were review-harness issues, not author-source findings.

## Reproduction

From this review directory, with the original sibling inputs present and SymPy installed:

    python3 -B prepare_replay.py
    python3 -B verify_review.py

The first command refuses changed original baseline bytes and verifies manifest bindings before replaying the copy. The second produces `CHECK_RESULTS.json` and prints nine PASS groups. Preserved final output is `verification.txt`; copied-author results are `AUTHOR_REPLAY.json` and `AUTHOR_REPLAY.stdout.txt`. `MANIFEST.json` hashes the review files and copied inputs. No original author or predecessor bytes are changed by either command.
