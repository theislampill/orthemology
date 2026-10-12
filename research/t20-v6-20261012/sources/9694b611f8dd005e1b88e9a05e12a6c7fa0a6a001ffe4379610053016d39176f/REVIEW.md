# Independent review: exact decision-profile representation

11 October 2026 UTC. Verdict applies to decision_representation/RESULT.md SHA-256 **d91e0dfb49154a17ca8173d7a344b3aae51ae0e02aea843b092d29bc26010323**, and the exact companion/source hashes in READ_LEDGER.json. This reviewer did not author or revise the candidate. No author, source, projection, or repository edits were made.

## Verdict

**PASS, with bounded scope.** The narrow corollary correctly distinguishes exact per-model loss preservation, the fixed-game answer, finite tags, and the actual deterministic/rationally seeded source owners. It is an explicit application and comparison of inherited machinery, not a new general minimum theorem or a new source compiler.

The author's 278-check verifier passes freshly both normally and under optimization. All three false-claim guards reject in both modes. The independent 44-check symbolic/exact verifier imports none of the author's code; it and its three guards have the same normal/optimized dispositions. CHECKS.json records all 16 commands and outcomes. General topology/cardinality arguments were reviewed as proofs, not inferred from the finite controls.

## 1. Algebra and contract

Starting independently with moments (1,1/2,1/3,t,s), inclusion–exclusion assigns a specified k-one word mass sum_j (-1)^j binom(4-k,j)m_(k+j). Summing all words gives one; summing history 11 gives 1/3. Directly evaluating the six reporting plans on those words yields exactly the claimed profile.

The Jacobian rows for skip1 and invert form the matrix [[-3,0],[-6,6]], determinant -18. Their displayed inverse is therefore correct for every fixed known c. The affine full profile separates (t,s), and those moments reconstruct the complete four-bit exchangeable law with the stipulated earlier moments. A private mixture adds no new coordinates because its expectation is the same mixture of these entries. Conversely it includes all six pure plans. Neither argument lets a policy inspect Nature's model label.

Important limit: this recovers the four-bit law, not the complete latent mixing measure in C4. Distinct mixing measures can share these moments. The candidate confines its claim to the experiment and correctly excludes missing semantic costs, authority and provenance.

## 2. Full dimensionality and topological necessity

The inherited simplex theorem cannot merely have its numerical dimension copied onto C4. The candidate supplies the needed independent restricted-domain argument. Here are explicit additional interior controls:

- C4 contains a square of half-width delta=1/1000 around (1/4,29/144). At t=1/4, each vertical margin is 1/144. Under |h|<=delta, the lower boundary varies by at most 2delta+12delta² and the upper by at most 2delta+6delta²; 3delta+12delta²<1/144. The square also stays strictly between 2/9 and 5/18 in t.
- E4 contains a square of the same half-width around its barycenter (1/4,7/36). All three barycentric coefficients equal 1/3 there; their changes are bounded by 12delta,36delta,24delta, respectively, all less than 1/3.

Thus each domain contains a circle. Exact recovery and injectivity of the profile force an encoder to be injective. If a continuous real-valued encoder were injective on that circle, its distinct minimum and maximum points would divide the circle into two arcs. The intermediate value theorem on each arc produces two different preimages for any value strictly between the extrema, a contradiction. Zero coordinates cannot distinguish points; two coordinates suffice by the identity. No decoder regularity is needed.

Two countercontrols expose the exact scope. On the lower-boundary curve s=L(t), a single t coordinate continuously determines all six losses despite the ambient affine profile having rank two. With only skip policies, the loss map has rank one even on the full domains. Thus both the actual domain and the declared menu matter. Without encoder continuity, arbitrary exact real encodings can inject two real coordinates into one: rescale to a bounded interval, select canonical binary expansions and interleave their digits in a ternary 0/2 expansion. This is outside the theorem and supplies no finite-precision implementation. The candidate states these limits accurately.

## 3. Posterior fibres and tags

At q=3/4 the C4 s interval is [7/36,5/24]; the E4 interval is [1/6,1/4], obtained either from triangle edges or its barycentric inequalities. Both are nondegenerate. Invert loss has derivative 6 in s at fixed t; copy has derivative -6. The C4 endpoints differ by 1/72 in s and by 1/12 in these losses, while posterior/skip losses agree.

Therefore q alone cannot recover the profile, and adding the continuous scalar s succeeds. A finite tag alphabet of size M cannot distinguish M+1 points on this exact fixed-q fibre, irrespective of tag or decoder regularity. A countable alphabet cannot distinguish its uncountably many points either. This stronger cardinality observation is not an illicit extension of D2's finite-state theorem.

For a nonempty finite selected model set Q, fibrewise labelling gives precisely max_t #{s:(t,s) in Q}. The refreshed candidate explicitly says “nonempty finite selected model set,” resolving the original review’s sole minor convention about the maximum over an empty family. D1's joint transition contract is stronger than merely this selected loss menu; the candidate expressly preserves that distinction.

## 4. Fixed-game output is weaker

The independent symbolic E4 saddle control returns primal losses (2/5+c/5,2/5+c/5,1/5+c/5). With dual weights ((3+4c)/5,(2-4c)/5,0), the six dual gaps are ((1-2c)/5,0,(1+3c)/5,(1+8c)/5,0,c). For 0<c<1/2 this forces the two supported pure plans, and balancing the first two vertices forces invert weight 1/5. C4's conditional least-favourable Bernoulli(2/3) model has unique optimal skip1 at positive cost.

These agree with the independently reviewed uncertainty-inquiry owner. Once the family, c, history, information and menu are fixed, a constant output can return that certified minimax result. A constant is not injective and cannot preserve the varying per-model loss profile. The report properly distinguishes a candidate law, a set of such laws, and one minimax output; it neither grants hidden model information to the policy nor claims that two real numbers encode arbitrary uncertainty sets.

## 5. Actual PT19/PT20 ownership and source boundary

The actual PT19 and PT20 RESULT.md owners were inspected, along with SourceSidecarController.lean and SeededSourceLookup.lean declarations. PT19's State is Sigma N (Sigma N Evidence), with ordinary natural coarse/tag observations and a fixed trivial identity-proof slot. Its controller_has and controller_observes establish typed deterministic computation, with HasE/HasJ inclusions. PT20 adds an explicit natural seed in Input, and sampler_has/sampler_observes compute the entire outcome/next-state reply from the same seed and state. No probabilistic primitive is thereby introduced.

PT20's written counting and conditional seed-law argument already supplies exact finite rational joint-law transport. Rational four-bit rows for a finite Q can use a common denominator and a pre-drawn hidden complete word; subsequent coordinate reads are deterministic. Alternatively, the finitely many positive-history conditional rows are rational. The model/word must remain hidden from the policy, and the private plan coin must retain its independent timing. The candidate calls this an application, not a newly compiled implementation or a source-implemented optimizer, which is the correct credit.

A fixed D-point uniform source yields n/D probabilities. It cannot span an interval of posterior values, nor all rationals of unbounded reduced denominator. This is an architecture-specific limitation. Natural source carriers are unbounded; finite program description is not finite-state capacity, and rational numerators/denominators admit finite but unbounded natural codes. No impossibility for original Has or alternative variable-denominator/random-bit/nonuniform-seed interfaces follows. Conversely these owners do not deliver an evaluator for every arbitrary real model. All those distinctions are retained.

## Evidence limits and custody

All seven inherited ledger hashes and every author-manifest size/hash match. READ_LEDGER.json distinguishes actual text/declaration reading from digest verification. No Lean build or renewed kernel audit was performed; the source inspection confirms interface ownership, not a new kernel certification. The separate uncertainty-inquiry review owns its broader body/game/horizon assessment; this review independently checks the narrow representation bridge and the displayed certificates.

During construction of the review controls, a reviewer-only gap-factor expression had an erroneous factor 2 and failed immediately. It was corrected to the directly expanded identity U-L=-18(t-2/9)(t-5/18) before the recorded final runs. This was not a candidate defect. The final script uses explicit RuntimeError checks that survive optimization.

No new field-wide priority, psychological storage bound, warrant estimate, metaphysical conclusion, arbitrary-horizon invariant filter, source integration, or programme closure is certified. No blocking error was found within the stated narrow result.

## Prose-only revision rebind

The current author revision inserts only the word “nonempty” into section 5’s finite-Q hypothesis. Removing that single insertion exactly recovers the previously reviewed RESULT.md digest 2be505cd04c6a6d3bd4cf37e6c40f24eb122498bf319af3d424a5376cf2f1617. PROSE_REVISION.diff records the comparison. The author manifest was updated consistently; check_exact.py, CHECKS.json and READ_LEDGER.json remain byte-identical. All owner pins still match. The exact execution receipts in this review are reused from the preceding reviewed bytes because neither verifier nor mathematical content changed; no new replay is claimed. The review binding and its manifest have been refreshed, and the empty-Q note is resolved.
