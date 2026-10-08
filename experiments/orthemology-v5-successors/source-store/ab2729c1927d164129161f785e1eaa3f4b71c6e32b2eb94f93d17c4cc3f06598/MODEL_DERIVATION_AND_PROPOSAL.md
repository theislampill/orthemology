Historical-stage notice: the original opening status and proposal describe the written/preimplementation stage. Later author implementation and independent scoped PASS are in README.md and review/REVIEW.md. No frozen historical verdict has been rewritten.

# Deletion traces: content recovery and the limits of its credit

Status: written model and proof plan, with a small exact-rational illustrative enumeration already performed before the coordinator’s later instruction to await an implementation decision. No Lean implementation, upstream execution, kernel replay, empirical study, or adoption. The useful contribution is an Orthemology applicability and model audit of established statistical principles, not a new trace-reconstruction theorem.

## 1. Pinned source and exact scope

All repository citations use commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

- `preprints/Uniform-quasipolynomial-time-trace-reconstruction-October-5-2026/uniform-trace-reconstruction.pdf`, Theorem 1.1 (pp. 1–2), exact observation definition (pp. 1, 4), statistical event and decoder (pp. 22–27). All 29 pages were read, including proofs and references. This supplies a manuscript claim about one fixed binary word of known length, known rational retention probability, and independent ordinary deletion traces. Its runtime counts received bits but treats trace generation as an external operation. The decoded word need not carry a per-instance certificate of correctness.
- `preprints/quantitative-lower-bounds-for-trace-reconstruction-September-24-2026/paper.pdf`, Theorems 1.1–1.2 (pp. 1–2), complete-trace channel and statistical scope (pp. 1–4). Opening pp. 1–5 read; the full 42-page proof has not been credited as read.
- `lean/docs/122.md` names only that lower-bound manuscript. `lean/ComparatorChallenges/TraceReconstruction.{json,lean}` specifies three lower-bound endpoints, not the October 5 decoder. The implementation is `lean/OAI/Probability/TraceReconstruction.lean`, importing the 30-file same-named directory. Source acquisition and static closure inspection are separate from a successful check.

The elementary results below do not depend on either claimed new upper or lower bound.

## 2. Shared content is intended; repeated observations are different

Fix one unknown word x. A single deletion trace retains each position independently with probability p, then concatenates retained bits in their original order. Throughout this note **p is retention probability** and q = 1 - p is deletion probability.

Fresh M traces mean independent masks conditional on the same x. Sharing that latent x is exactly the intended reconstruction model. It does not invalidate independence conditional on x.

Copied observations mean one mask is sampled once, yielding Z, followed by the deterministic replication Z -> (Z,...,Z). Every individual coordinate still has the correct one-trace marginal. Their joint law is not the product law. Counting these as M fresh masks changes an essential premise.

No blanket statement about all shared-provenance evidence follows: actual dependence must be established from the channel model.

Copies can improve availability, durability, and fault tolerance. The information calculation concerns ideal repeated access to the same realised trace, with no additional observational content; it does not deny those practical benefits.

## 3. Exact two-word experiment

Restrict the possible content to x = 00 and y = 01, with equal prior probability for this diagnostic experiment. For 0 <= p <= 1 the complete one-trace laws are:

- Under 00: empty has mass q^2; 0 has mass 2pq; 00 has mass p^2.
- Under 01: empty has mass q^2; 0 has mass pq; 1 has mass pq; 01 has mass p^2.

Absent outputs have mass zero. The laws include the empty trace and its length. Their total-variation distance, half the sum of absolute mass differences, is pq + p^2 = p.

For any randomized binary decision rule h(z) in [0,1], interpreted as the chance of reporting y, equal-prior success is

S(h) = (1 + E_y h - E_x h)/2 <= (1 + TV(P_x,P_y))/2.

The inequality follows directly by separating positive and negative terms in the finite signed mass difference. Choosing h=1 on positive differences and h=0 on negative differences attains the bound. Randomization cannot improve it.

### 3.1 Copies of one realised trace

For M >= 1, the replication map is injective, and the first-coordinate map recovers its input. Summing pushforward masses over its image therefore gives

TV(rep_M(P_x), rep_M(P_y)) = TV(P_x,P_y) = p.

Thus copied traces have optimal equal-prior binary success (1+p)/2 for every positive M. At p=1/4 this is 5/8. In particular, no rule can have success at least 2/3 under both x and y, since its equal-prior mean would then be at least 2/3.

For M=0 there is no observation, both observation laws are the same point mass, and optimal equal-prior success is 1/2. The injectivity claim is not made in that case.

### 3.2 Fresh independent traces: positive information gain

Use the test: report 01 if at least one trace contains a 1; otherwise report 00. Under 00 the test is always correct. Under 01 the final 1 is independently retained in each trace, so the test is correct with probability 1-q^M. Its equal-prior success is therefore 1-q^M/2.

For this particular pair the expression is also optimal, as a separate calculation shows. On the one-trace alphabet A = {empty,0,00}, P_x is pointwise at least P_y; outside A, P_x is zero. Hence on A^M the product P_x^M is pointwise at least P_y^M, while outside A^M P_x^M is zero. The common mass is exactly P_y^M(A^M) = q^M. Thus TV(P_x^M,P_y^M) = 1-q^M, and the finite decision-rule bound above is attained by the stated test.

This is binary discrimination under a declared equal prior, not a guarantee for arbitrary words or a posterior authenticity certificate. A finite two-word control does not establish the new quasipolynomial decoder.

## 4. Source identity remains outside the content channel

Let worlds w0 and w1 have distinct historical source identities or distinct utterance-event identities but the same content c(w0)=c(w1)=x. Suppose observations depend on a world only through x and the specified deletion-mask law. Then their complete observation laws are equal for every number of fresh traces. Any randomized observation-only decision rule has the same output law in both worlds. If required to distinguish those two identities, its equal-prior success is at most 1/2.

The proof is simple substitution of equal x into the channel, followed by postprocessing. It does not depend on copying masks. Even exact content recovery leaves this identity ambiguity intact. Resolving it requires additional observations or warranted restrictions that distinguish the worlds. This says nothing against ordinary content agreement as evidence where those additional premises already hold.

The same statement applies to truth or authority only when the declared comparison worlds agree on all observations yet differ on that property. It does not assert that any actual source is false, unauthenticated, or unauthorized. Content correctness, actual truth, occurrence, attribution, and normative standing remain separately typed targets.

## 5. Even a known word need not identify a retained token occurrence

For known word 00, conditional on a trace equal to 0 and 0<p<1, the two possible masks (retain first, delete second) and (delete first, retain second) each have probability pq. Each therefore has conditional probability 1/2. The word can be completely known while the trace's original-position attribution remains unresolved. Fresh other traces, conditional on the known word, do not reveal this particular mask without an additional cross-mask observation.

This distinguishes source/utterance-event identity from the narrower alignment of a retained character to a position. It must not silently replace a programme-specific occurrence predicate.

## 6. Exact transfer obligations to Orthemology

An actual application needs all of the following, rather than importing a paper title:

1. A lossless finite binary encoding of the declared content target, with known original length. If the target is a structured reading, specify decoding and which content equivalence it preserves.
2. Evidence that received records are ordinary order-preserving deletion traces, including the empty record. Substitution, insertion, reordering, editing, translation, selection bias, or changing originals require new modelling and proofs.
3. A known rational retention probability for the claimed uniform decoder, or an explicit separately proved parameter-estimation/robustness result. The lower-bound statement instead quantifies over arbitrary real deletion probabilities.
4. The full conditional joint law of masks. Fresh corruptions of one word are allowed. Copies of a realised corruption are not new independent samples. A shared random environment also needs explicit conditioning and calibration.
5. An actual sampling/resource contract: retained access to the same original and a trace-generating channel is continuing support. Trace generation is not paid for by the manuscript's internal bit-operation bound.
6. A selected mathematical result with exact statement correspondence and adequate verification. The new upper algorithm has no matching Comparator endpoint in this pinned family scope document, and its directory contains manuscript sources rather than an executable decoder implementation.
7. Separate predicates/evidence for historical origin, intended occurrence, source-owned assertion, truth, and authority. A successful content decoder does not instantiate those predicates.
8. A declared probabilistic service. The manuscript's success bound is over channel draws for each fixed word. It is not a universal success assertion for every well-formed trace stream and not, by itself, a posterior probability for this particular output. Its fallback output exists even on bad data.

Relevant avenues are 4 (specified restoration), 5 (provenance-resilient restoration with support counted), 7 (content equality versus continuation/source identity), 8 (exact observation contract), 10 (sampling and effective resource bounds), and 11 (occurrence-sensitive interpretation). Nothing here advances necessary-bearer, attribute, or norm-ground premises in avenues 1–3, and no participant/statistical inquiry is reopened.

## 7. Historical bounded verification proposal

Use the existing approved Lean 4.19 environment and only finite probability vectors, if the coordinator decides that a new formal control adds value beyond the inherited information-composition theory. Do not import the 4.34.1 OpenAI library or execute its Lake configuration.

Proposed scope: one small module defining the length-two deletion channel, rational probability vectors for p=1/4, deterministic replication, and the finite randomized decision-rule inequality. Prove exact one-trace TV=1/4, replication invariance for M>=1, the 5/8 decision bound, the separate zero-data case, and equality of channel laws for identical encoded content. The fresh-trace formula can either be a second small finite-product lemma or remain a written contrast if its formal cost does not serve the current programme.

Controls: p as retention versus deletion; M=0 versus M>=1; fresh product sampling versus diagonal copied sampling; same content with two distinct source labels; known 00 with two possible masks; and no promotion from a randomized content service to an authentication predicate.

Stopping condition: a source-bound result/receipt at exactly this scope, or a finding that the inherited information-composition theory already provides the needed consequence. No universal trace decoder, asymptotic new lower bound, empirical reproduction, or public integration is proposed.

`check_copy_controls.py` and `COPY_CONTROL_RECEIPT.json` record the pre-instruction exact-rational illustration: four masks for each length-two word, all 32 deterministic binary decision rules on the union trace support, and copied-law checks for M=1,...,16. The written injectivity proof establishes all positive M; those finite repetitions alone do not. This receipt is not a Lean/kernel proof.
