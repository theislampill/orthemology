# A total integer report protocol with non-tight resources

Twelfth Orthemology research supplement • 4 October 2026 UTC

Ordinary mathematical and abstract computational argument, pending independent exact readback. No implementation, physical-realisation claim, sampler, Gaussian acquisition algorithm or canonical change. The v3 bounded-access article is preserved unchanged.

## Result and why it matters

The accepted integer ±1 history supports a completely described report protocol that terminates on every finite anchor input and every Bernoulli tape. It requires no exact-real floor oracle and does not discard the all-tails tape. The protocol preserves the positive-report conditional probabilities, two-transaction arithmetic, and finite-deadline/Brier calculations of the bounded-access article.

This answers a specific objection positively. For this integer analogue, mere noncomputability of the report is not an available objection once its stated finite-input representation is supplied. The remaining access burden is the warranted supply of that input and the maintenance of the channel, clock, stored information and action opportunities through a non-tight duration. These are substantive operational commitments, not an undiscovered arithmetic algorithm. They remain distinct from a physical implementation, generation of the finitely additive anchor, or the actual programme's source-realisability bridge.

## 1. Accepted law and inherited ownership

Use the integer version in `tranche12/reviews/finitely-additive-concentration/INDEPENDENT_REVIEW_PUBLIC_v1.md`, §3, “Integer version.” Its fixed sample space has integer anchor X₀ and a two-sided ordinary iid fair-sign noise sequence (ξ_j). The finitely additive history law μ gives every finite position set mass zero and retains the entire countably additive noise marginal. Its recurrence holds pointwise, and the accepted full past–future independence properties are unchanged.

No new law is sampled or silently substituted. The finite input below is a representation of the existing anchor coordinate. The independent bits come from the existing noise coordinates. In particular, an external coin product extension is unnecessary.

Prior computational ownership remains explicit. P02 `CV_C_CODEC_AND_CORRESPONDENCE.md`, C2-01–C2-07, already distinguishes valid finite input, total abstract computation and resource-limited execution. Its C2-06 treatment of a geometric selector explicitly preserves an exceptional all-ones stream rather than confusing almost-sure termination with total productivity. Tenth `finite-limit-warrants/ASSESSMENT.md`, §§1–4, already separates representation, effective acquisition and a uniform advance resource guarantee. The present increment is the total capped report inside this exact integer law and its hidden-information timing contract, not a new general computation theorem.

## 2. Finite input and private information

For each integer anchor x, supply the reporting machine with a private, read-only finite representation consisting of a sign bit and a magnitude tape

1^{|x|}0.

The magnitude tape's zero is an end marker, not an infinite padding convention. Its length is

N=1+|X₀|.

Every sample therefore supplies a finite, valid input word. Each event {N≤m} is a finite position event and has μ-probability zero. No algorithm generating X₀ according to μ is asserted. Saying that the machine receives this representation is an input contract, not a proof of how an actual observer obtains the world's state.

The trader does not see the word, its sign, its length, or its loading history. The private input is supplied before the public protocol begins. Any real setup channel that reveals its duration or length would require a new information analysis; such leakage is excluded by the stated abstract interface, not proved absent in nature.

Before reading the branch coin ξ₀, the trader makes the first A-ticket transaction, where A={ξ₀=+1}. The reporting machine then reads ξ₀ privately and stores that one bit. Thus μ(A)=1/2. At each later public round j≥1, ξ_j supplies one fresh private fair-sign bit. Its value is not announced to the trader.

## 3. Total causal report rule

Let K∞ be the first j≥1 with ξ_j=+1, with K∞=∞ if every such bit is −1. The usual untruncated waiting rule is only almost surely terminating. Here it is used only to describe the following total stopping variable:

K*=min(K∞,N).

Define

R=N on A;     R=K* on Aᶜ.                      (1)

The machine realises (1) using these bounded local operations, rather than first performing an unbounded hidden preprocessing of N:

1. In round j, read the next magnitude-tape cell and the bit ξ_j. Do this on both branches.
2. If that cell is the end marker, mark completion for this round.
3. Otherwise, if the stored branch bit says Aᶜ and ξ_j=+1, mark completion for this round.
4. Otherwise advance the tape head one cell and continue to the next round.
5. When completion is marked, emit the pulse at the same fixed final phase of the padded round and halt, regardless of which trigger marked it. No earlier sub-round signal is exposed.

Each round requires one input-cell read, one coin-bit read, a fixed finite-state conditional and a possible pulse. A round can be implemented by a fixed bounded block of elementary transducer steps, padded equally across the branches. The publicly observed rounds therefore do not hide an unbounded unit-cost arithmetic instruction.

On A the end marker is the only stopping trigger, so R=N. On Aᶜ the first head or end marker stops the machine, so R=min(K∞,N). In every sample, R≤N<∞. Even the all-tails tape halts at the end marker. No sample-space restriction, conull-domain promise, infinite physical portfolio or real-number equality oracle is used.

The protocol is causal: the decision at round j uses only the finite supplied input prefix, ξ₀ and ξ₁,…,ξ_j. It never consults a future bit to decide whether to stop now. A numeric report need not be computed privately in advance: the pulse's public round identifies R. An ordinary finite counter may record that number if required; its possible size is unbounded across inputs.

## 4. Why the same probability equations survive

For every n≥1, the events {K*=n} and {K∞=n} can differ only where N≤n. That set is μ-null. Therefore

μ(K*=n)=μ(K∞=n)=2^(−n)=q_n,
μ(A∩{K*=n})=μ(A∩{K∞=n})=q_n/2.                (2)

The second equality uses only the ordinary iid noise marginal: ξ₀ is independent of the cylinder defining the first head at n. It does not infer causal autonomy from the cap's statistical effect.

The geometric distribution statement is not merely a list of unspecified finite-dimensional values. For every m, {K*>m} differs from {K∞>m} only on {N≤m}, so μ(K*>m)=2^(−m). These tight tails and finite additivity determine μ(K*∈B)=Σ_(n∈B)q_n for every set B of positive integers, by bounding the remainder after m by 2^(−m). The same tail bound applied to A∩{K*∈B} gives independence of A and K* at their entire countable event domains.

K* uses the finite anchor bound in its definition, so it is not literally a function of the noise alone. Its ordinary geometric marginal and independence from A are conclusions of (2) and the tail argument. They must not be described as a new causally independent random source.

Now let H_n={R=n}. These events partition the whole sample space because R is pointwise finite. Under (1),

μ(A∩H_n)=μ(A∩{N=n})=0,
μ(H_n)=μ(A∩{N=n})+μ(Aᶜ∩{K*=n})=q_n/2>0.

Consequently

μ(A|H_n)=0 for every n;     μ(A)=1/2.          (3)

The null cap does not alter the report probabilities. It repairs computational totality on exceptional tapes and large inputs while preserving the same exact nonconglomerability calculation.

## 5. The trader's adaptive information

The trader's public observations are a common start, a round clock, silence at every earlier round, and a pulse at round R. A transcript ending with the pulse at n is exactly the event H_n; the previous silence is already implied. At trade two, the trader receives no branch bit, private input cell, coin value, setup timing or other state-dependent message.

At a fixed deadline m with no pulse, the information is D_m={R>m}, not an exact report. Writing Q_m=Σ_(n≤m)q_n=1−2^(−m), the same finite-additive calculation gives

μ(D_m)=1−Q_m/2,
μ(A∩D_m)=1/2,
μ(A|D_m)=1/(2−Q_m).

Waiting itself therefore supplies information. The protocol does not pretend that the trader's belief stays at 1/2 while no pulse appears. Its specified trading policy makes no intervening trade and uses the exact-report posterior only after the pulse.

The second transaction takes place in a designated phase immediately after the pulse. The branch coin is revealed for settlement only after that transaction. Whether the trader ought to follow the local conditional-price policy is unchanged from the main assessment: computational feasibility alone does not establish that normative commitment.

## 6. Consequences and precise resource limit

For 0<ε<1/4, the policy buys the A-ticket at 1/2−ε before the branch coin is read and sells it at ε after the pulse. At the corresponding information states each transaction has conditional expected gain ε. In every sample the combined payoff is −1/2+2ε. Each execution makes two bounded transactions and terminates after finitely many rounds.

Similarly, the exact-report forecast is zero in every H_n, with prior quadratic loss 1/2 rather than the constant prior forecast's 1/4. A fixed-deadline posterior retains D_m and has prior loss (1−Q_m)/[2(2−Q_m)]. The prior mathematical review of those formulas is not automatically a review of this new protocol construction; the latter requires its own exact readback.

The magnitude-input length N, and the total representation length N+1 including the sign bit, each have zero probability of meeting every fixed finite bound. The report runtime has

μ(R≤m)=Q_m/2,     μ(R>m)=1−Q_m/2→1/2.

Thus its marginal is non-tight, although R is finite in every sample. It would be incorrect to say that every finite bound on the report's runtime itself is null: the Aᶜ branch often finishes early. Bounds on the full anchor input length are null; runtime bounds have the displayed positive probabilities. On A the runtime equals N and misses every fixed deadline with conditional probability one.

The elementary reporting transducer needs only a fixed finite control plus the supplied input tape and sequential coin access. Unbounded working memory is not required just to emit a pulse. An unbounded input repertoire, indefinitely maintained channel and opportunities, and an unbounded clock/counter repertoire if exact integer timestamps must be stored are nevertheless part of the complete operational contract. These distinct resource requirements must not be merged into a generic claim that the algorithm consumes infinite memory in an actual run.

The gain is therefore exact and limited: a total abstract finite-input protocol is available for the accepted integer analogue. The Gaussian exact-real acquisition question remains separate. No physical sampler for μ, actual indefinite service, original productive source or metaphysical impossibility follows. The remaining objection to this integer protocol must address its input and maintained-resource contract, its operative-prevision/update norm, or the actual support realisability bridge; it cannot simply assert that the displayed report is only measurable and no computation has been supplied.

## Inspection scope

This supplement introduces no new historical primary-source exposition or quotations. Its standard computational and probabilistic ingredients remain inherited. The source-neutral increment is their fully specified, all-tapes-total application to the accepted integer history and its trading-information interface. v3 is not amended by this separate candidate.
