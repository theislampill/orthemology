# Audit-aware continuation: exact predictive state and posterior-only tensor test

10 October 2026 UTC. Scratch-only substantive T20 continuation. No protected source, adopted theory, repository integration, actual-warrant judgement, or programme status is changed. Written mathematics with exact rational controls; no kernel certification or field-wide novelty claim.

## Result first: what was inherited and what was actually added

The proposed row-span construction is already **H-Continuation Theorem 2**, including finite action–observation instruments, event probabilities, target numerators, normalization on positive branches, invariant closure, and its full-simplex continuous-coordinate lower bound. H-ICS already supplies feasible-support fibre criteria and observation congruence. Reproving those as a new Bayesian theorem would duplicate inherited work.

The missing bridge supplied here is concrete:

1. Realize the existing source/audit countermodel as a finite instrument with the correct latent history and distinguish a reread of one fixed verifier result from a new independent verifier experiment.
2. Push this instrument through an explicit joint target–audit statistic. In the original 16-state realization, eight masses of (target, future audit) suffice after the report; four masses suffice in the known-Bad slice. This is an exact commuting update construction, not a claim that the transcript must literally be retained.
3. Show that retaining the current target posterior **and all next-audit event probabilities** can still fail: the missing quantities are target–audit joint numerators. The two neutral report histories have the same target and audit marginals but give posteriors 4/5 and 1/5 after the same audit.
4. For the strictly weaker posterior-only contract, give a finite **paired tensor test plus a separate feasibility-language test**. The invariant span of cross-products decides equality of all conditional target answers. Its tensor dimension is not the memory of a one-belief filter.
5. Calculate the exact posterior-only quotient for the fixed binary audit: it is injective away from target–audit independence and collapses different audit frequencies on the independence locus.

The posterior-only lift and binary quotient were proposed by the parent during this investigation. This packet supplies the source comparison, explicit instrument transport, proofs in a single convention, and exact executable controls. The independent review is a separate artifact if supplied; this report does not confer that status on itself.

## 1. Inherited ownership was checked first

The exact local inputs and hashes are in INPUT_BINDINGS.json.

- **H-Continuation**, “Continuation completion, including observations and feedback,” Theorem 2 and its proof, especially source lines 217–292, already treats the finite substochastic instrument requested here. Its row-law convention becomes the column-law convention below by transposition. It expressly preserves probabilities and numerators, only normalizes positive branches, and distinguishes the full simplex from a restricted reachable family. Its conditional-error section already warns about vanishing conditioning margins.
- **H-ICS v5**, probability and transition sections, Proposition “Output determination on the feasible support,” observation congruence, and the finite labelled-belief construction, already owns support-sensitive factorization and operation-relative state sufficiency. Support alone forgets weights. The deterministic sure-decision construction is not a Bayesian-filter theorem and is not relabelled as one here.
- **Reset/guarded revision** and **provenance-learning transport** already prove exact continuation statements for their declared Boolean and named fixed-factor operations. Their own warnings exclude silent extension to new observation channels, arbitrary source revisions, or erasure of actual knowledge. Their general continuation reasoning is inherited.
- **Source-audit revision** and **TRIPLE_INTERACTION** already supply the audit-selection counterexample, its pair-marginal collision, the posterior 1/5, and the warning that a neutral report can matter to a later audit. This packet adds an actual finite instrument quotient and the posterior-only comparison; it does not claim a new parity counterexample.

The inspected H-Continuation and H-ICS passages do not state the paired normalized-output criterion or the binary posterior-only quotient below. This is a bounded source comparison, not an exhaustive priority claim. The finite-span and tensor-product mechanisms have established automata/filter ancestry.

A concurrent change to Source-audit RESULT was detected by the first replay's final hash check. The parent confirmed the expected correction adding “at least two target states” to the null-audit nonuniqueness statement. That exact revised passage was inspected and the revised result copied into inputs/SOURCE_AUDIT_RESULT.md. The old binding, detected new hash, and reason remain recorded. The packet does not claim the original moving file remained unchanged.

## 2. Declared finite instrument and target

Let X have n latent states. States r are nonnegative **column** vectors, with mass u r where u=(1,…,1). A live unnormalised state has u r>0. A finite explicitly supplied alphabet Σ consists of authorized action–observation symbols, with nonnegative matrices M_a. Each is column-substochastic; where several symbols are outcomes of one action, their sum is column-stochastic. A deterministic permitted intervention is a one-outcome stochastic matrix.

For a chronological word w=a1…ak, including the empty word ε,

    M_w = M_ak … M_a1,       M_ε = I.

The tested repertoire is all finite words Σ*. If permissions or one-shot availability are restricted, include an explicit finite controller/phase in X and its observables before applying this all-word construction, or supply a separately proved language-restricted construction. Do not silently substitute a smaller or history-dependent language into an all-word claim. A modeled refusal is an observation, not permission to perform the refused action.

Let C be a fixed column-stochastic target readout. Its rows are target indicators in the examples. It reads the declared current latent state. If the intended target is about an initial state that later transitions mutate, retain that initial label in X; a changing target cannot silently share this fixed C. For normalized r, the branch probability and posterior are

    p_w(r) = u M_w r,
    q_w(r) = C M_w r / p_w(r), when p_w(r)>0.

For unnormalised live r, divide p_w(r) by u r for the probability conditional on the current history. The target posterior formula is unchanged. At p_w(r)=0, the output is an explicit impossible-observation status. Because M_w r is nonnegative, zero total mass implies M_w r=0. No posterior is invented at that branch.

The model/version, source meaning, and legal repertoire are premises of this construction. Changing the joint probability law, adding new audits, or changing the target can change the sufficient statistic. Finite latent state is a justified modelling requirement here, not a theorem that arbitrary real audit histories always admit one.

## 3. The inherited predictive construction, with its admissible cone explicit

Put

    W0 = span({u} ∪ rows(C)),
    W_(h+1) = W_h + Σ_(a∈Σ) W_h M_a.

Because C is a complete target marginal, u is already the sum of its rows; retaining it explicitly makes the normalization contract visible. The ascending sequence stabilizes in dimension k≤n. Choose a full row-rank basis B of the stable space W. Then there are uniquely determined matrices T_a and readout coefficients ν,L with

    B M_a = T_a B,       u = ν B,       C = L B.

These equalities are the structure-preserving transport. Retain z=B r. Its unnormalised update is z′=T_a z. From normalized z with νz=1, the branch probability is νT_a z. If positive, the next normalized state and target are

    z′ = T_a z / (νT_a z),       q′ = L z′.

The admissible unnormalised state space is the finitely generated cone

    K = B R_+^n = cone{B e_i : i∈X}.

Its normalized slice is Z={z∈K:νz=1}=BΔ(X). This cone, not the whole coordinate space and not necessarily its coordinatewise nonnegative orthant, is the domain of the reduced filter. The matrices T_a may have signed entries in a chosen basis while preserving K exactly. Indeed T_a B r=B M_a r∈K for r≥0. Also νz≥0 on K, and νz=0 implies z=0, since every representing nonnegative r then has zero mass. K is pointed for the same reason. For rational data, membership may be checked by the finite feasibility system B r=z, r≥0; an explicit inequality elimination is unnecessary.

This positivity makes the impossible-branch behavior faithful: if νT_a z=0 for z∈K, then T_a z=0. One may keep that zero as an absorbing impossible-history marker, but not normalize it. This gives a status, not a regularized posterior or repair of an incompatible model.

**Exact equivalence.** For normalized r,s, B r=B s iff every future word has equal probability and, when possible, equal target posterior. Sufficiency follows from the commuting equations. Conversely equal probabilities and positive-branch posteriors give equal target numerators; both numerators vanish on impossible branches. Thus r−s annihilates every uM_w and cM_w, and hence W. For arbitrary live unnormalised r,s, conditional future probabilities and posteriors instead correspond to

    B r/(u r) = B s/(u s).

Retaining absolute evidence mass is a stronger requirement. Confusing it with normalized predictive equivalence would incorrectly separate merely rescaled copies of the same belief.

Minimality is inherited and carefully scoped. W is the least sufficient invariant **linear observable space** for the probability-plus-target contract over all laws. H-Continuation also proves that k−1 continuous real coordinates are necessary and sufficient on the full normalized simplex, even with arbitrary decoders. Neither statement is a bit count, a literal transcript requirement, a bound for discontinuous real encodings, or automatically valid for a fixed finite reachable history set. It is also not a minimality statement for posterior-only outputs.

## 4. A faithful realization of the actual audit countermodel

Use the original latent state

    X=(Θ,T,Y,V), all four binary, with T=0 Good and T=1 Bad.

The original law has Θ and T independent and uniform; Y has accuracy 9/10 conditional on Good and 1/2 conditional on Bad; V has accuracy 4/5 and is conditionally independent of Y given (Θ,T). Put D=1[V≠Y] and A=(T,D).

Reading Y=y is a diagonal projector. Reading A=a is the diagonal projector

    M_a(x,x) = 1[A(x)=a].

These audit projectors form an instrument. They describe learning or rereading a **single fixed audit result**, as in the original joint law. They are idempotent; distinct audit results multiply to zero. This is materially different from redrawing V after every audit.

After Y has been read, suppose the admitted future observations are readings of this A. Let G send a law on X to its eight joint masses

    μ(θ,t,d) = Σ_(x: (Θ,T,D)(x)=(θ,t,d)) r(x).

Let P_a be the corresponding diagonal selector on these eight coordinates. Then exactly

    G M_a = P_a G,
    target marginal of μ = C r.

The observable closure has rank eight: target rows multiplied by the four audit selectors give all eight indicators 1[Θ=θ,A=a]. Thus G is an explicit sufficient quotient of the 16-state latent law for this future contract. It can forget the literal Y,V coordinates while retaining their target–audit dependence. That is not the same operation as keeping only the target marginal.

If future reading of Y is also included over the unrestricted 16-state domain, closure has rank sixteen: (Θ,T,Y,D) determines V, so the joint indicators separate every latent state. If Y is already fixed and known, that is a restricted domain rather than the whole 16-state simplex. Both the operation family and the admissible law family matter.

For the original prior and observed Y=1, this realization reproduces

    P(Θ=1|Y=1)=7/10,
    P(A=(Bad,1)|Y=1)=1/4,
    P(Θ=1|Y=1,A=(Bad,1))=1/5.

### Known-Bad slice: target and audit marginals still lose the answer

Condition on T=Bad and the report Y=y. A sufficient future state is the four masses π_y(θ,d) of (Θ,D). At verifier accuracy α, put ρ=2α−1. The joint law is

    π_y(θ,d) = [1+ρ(−1)^(θ+y+d)]/4.

At α=4/5, in order (Θ,D)=(0,0),(0,1),(1,0),(1,1),

    π_0 = (2/5, 1/10, 1/10, 2/5),
    π_1 = (1/10, 2/5, 2/5, 1/10).

Both have target marginal (1/2,1/2) and audit marginal (1/2,1/2). Nevertheless observing D=1 yields target-one probabilities 4/5 and 1/5, respectively. The mixed numerator P(Θ=1,D=1) is missing from the two marginals. Adding audit-event prediction alone therefore does not repair the target-only state.

The four-state closure is the full space, with rank progression 2→4. A useful basis is

    (1, τ, δ, τδ), where τ=(−1)^Θ and δ=(−1)^D.

For retained moments z=(m,t,d,h), a fixed audit reading D=b with s=(−1)^b gives

    m′=(m+s d)/2,       t′=(t+s h)/2,
    d′=s m′,           h′=s t′.

Normalize by m′ when positive; the target-one posterior is (1−t′/m′)/2. In the two neutral histories z=(1,0,0,(−1)^yρ). The already-owned triple interaction has become exactly the retained two-slot target–future-audit cross-moment after conditioning on the report. It is not a symmetric tensor power, tensor rank claim, metric, or gradient.

The cone requirement is visible. The moment vector (1,0,0,2) has apparently valid target and audit marginals but reconstructs the signed masses (3/4,−1/4,−1/4,3/4). On D=0 it would produce target probability −1/2. Excluding it is part of a valid state domain, not optional numerical cleanup.

For fixed α≠1/2 there are only **two neutral pre-audit histories** in this example, distinguished by one report bit or an equivalent sufficient statistic. The rank-four/three-normalized-coordinate statement concerns arbitrary laws on the four latent outcomes; it is not a lower bound of three continuous coordinates for those two histories.

### A reread is not a fresh source

After Y=1,Bad,D=1, reading the same D again leaves posterior 1/5 and has conditional probability one. Reading the opposite D has probability zero. Alternatively, a model that draws a new independent 4/5-accurate verifier for each audit uses diagonal likelihood matrices on (Θ,Y):

    F_b(θ,y;θ,y) = [1+ρ(−1)^(θ+y+b)]/2.

After two fresh disagreeing verifiers, the posterior is 1/17. Its closure has rank four for ρ≠0, but these matrices do not represent repeated readings of the old observation. The difference is source/event identity in the model, not a failure of Bayes or of the closure theorem.

## 5. The genuinely different posterior-only question

Define r≈_post s for live nonnegative states when:

- the same words are possible from r and s;
- for every possible word w, q_w(r)=q_w(s).

Word probabilities need not be equal. The empty word is included. This is the behavior of a filter that must give every conditional target answer and correctly flag impossibility, but is not required to predict audit frequencies.

The full predictive quotient can be strictly finer. Let the latent state be (Θ,S), keep Θ and S fixed, and observe source-only likelihoods f(S) with f(0)=1/4,f(1)=3/4 and complementary likelihood 1−f. Take Θ uniform and independent of S in both beliefs, with P_r(S=0)=3/4 and P_s(S=0)=1/4. Every finite word has positive probability and every target posterior remains (1/2,1/2) in both beliefs. Yet the next first-outcome probabilities are 3/8 and 5/8. The full predictive closure has rank four; it is not a minimality theorem for these posterior-only equivalence classes.

### Paired tensor criterion

For each target row c of C, put

    d_c = c⊗u − u⊗c,       N_a = M_a⊗M_a.

Let U be the least row space containing the d_c and invariant under right multiplication by every N_a. It is computed by finite span closure. It lies in the antisymmetric two-slot space, because swapping tensor factors changes the sign of each d_c and commutes with each M_a⊗M_a. Thus dim U≤n(n−1)/2, although an n²-coordinate implementation suffices.

**Proposition.** For nonnegative live r,s,

    r≈_post s

iff their feasible-word languages agree and every row of U annihilates r⊗s.

**Proof.** For a word possible from both states, equality of its target component is equivalent to cross multiplication:

    (cM_w r)(uM_w s) − (uM_w r)(cM_w s)=0.

The left side equals d_c(M_w⊗M_w)(r⊗s). The mixed-product identity for Kronecker matrices gives N_w=M_w⊗M_w, with exactly the same word on both factors. The generators for all words span U. Thus annihilating U is equivalent to all cross-products vanishing. On a jointly impossible word both unnormalised vectors vanish, so these equations still hold. Conversely, with common feasibility, divide the equations only on common positive branches. This proves both directions. ∎

The same-word synchronization is load-bearing: replacing M_a⊗M_a by arbitrary independent symbol pairs would test a different question. Right multiplication of a row by N_a **prepends** a to its tracked chronological word under the chosen column convention; it still generates exactly all words. A witness-producing implementation must preserve that labeling convention.

This is a tensor transport of a nonlinear normalized-output comparison into a finite linear zero test. It is not a linear statistic of one belief, an optimal one-state filter construction, a dimension lower bound for posterior memory, or a new general tensor-product theorem. The quotient by ≈_post is a well-defined partial continuation quotient because a common feasible first symbol preserves all continuation comparisons; existence of that set-theoretic quotient does not supply a convenient finite-dimensional parameterization.

### Why zero-branch feasibility cannot be omitted

If M_w r=0 but M_w s≠0, every cross-product at that word is still zero. The tensor equations alone therefore erase the distinction between an impossible observation and a live posterior.

For example, let two states have the same target Θ=0 but different source bits S=0 and S=1. A perfect source-bit observation has diagonal projectors onto S=0 and S=1. All target cross-products vanish, including after every word, but the first S=0 observation is possible from only the first state. The feasibility test rejects their equivalence.

Because M_a≥0, supports update deterministically by

    F_a(S)={i : some j∈S has M_a[i,j]>0}.

Compare initial supports by exploring pairs under (F_a,F_a). A reachable pair with exactly one empty component is a distinguishing word; absence of such a pair establishes equal feasible-word languages. There are at most 4^n pairs, including empty supports. Equal initial positive supports imply the same language, but equal support is sufficient, not necessary. Rational explicitly supplied M,C,r,s make both this procedure and row-span closure exact algorithms. Arbitrary uncomputable real coefficients do not.

## 6. Exact posterior-only quotient for one fixed binary audit

For a joint law π of binary Θ,D, suppose 0<t=P(D=1)<1. Write

    q=P(Θ=1),       q_b=P(Θ=1|D=b).

The complete posterior-only signature is (q,q_0,q_1). Matching rereads add nothing; contradictory rereads are impossible. The total-probability identity is

    q=(1−t)q_0+t q_1.

If q_0≠q_1, it recovers t=(q−q_0)/(q_1−q_0), and hence every joint mass. If q_0=q_1=q, Θ and D are independent and all t∈(0,1) give the same posterior-only signature. Therefore the quotient is injective off independence but collapses the audit-marginal fibres on independence. At t=0 or t=1, feasible-language information identifies which audit value is possible; the target marginal then determines the supported joint law.

This is a genuine nonlinear quotient distinction. It also shows why “posterior-only is coarser” need not yield a smaller universal continuous coordinate count: away from independence the signature is injective on an open three-dimensional set. The same invariance-of-domain reasoning already used in H-Continuation precludes a globally exact continuous encoding into fewer than three real coordinates. That is a full-law statement, not the size of the two-history example.

## 7. Classical ancestry and the bounded increment

[Littman, Sutton and Singh, *Predictive Representations of State*](https://proceedings.neurips.cc/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf) is direct ancestry for finite predictive state and normalized updates. This worker opened the primary proceedings PDF; the inherited manuscript already credits it. No new filter-observability mechanism is claimed.

[Kiefer, Murawski, Ouaknine, Wachter and Worrell, *On the Complexity of Equivalence and Minimisation for Q-weighted Automata*](https://people.mpi-sws.org/~joel/publications/Q_weighted_automata13.pdf), inspected §§2.2–3 through Proposition 3.1, explicitly supplies Kronecker composition and finite-span zero/equivalence testing. The bound on a distinguishing weighted-automaton word is inherited machinery, not a discovery here.

The parent independently read [Droste–Kuske, *Weighted automata*](https://www.informatik.uni-leipzig.de/theo/pers/droste/papers/Droste-Kuske-AutoMathA-neu.pdf), Lemma 4.3 and adjacent qualification plus §8 through Theorem 8.3 and Corollary 8.4 statement. It supplies the standard product construction for pointwise products and finite invariant-span equivalence. That targeted reading, rather than a claimed complete-paper review, supports the ancestry comparison.

[Tzeng's 1992 paper](https://epubs.siam.org/doi/pdf/10.1137/0221017) was accessed only as publisher abstract and metadata; no full-proof reading is claimed. It is further historical context for probabilistic-automata equivalence.

The paired posterior criterion is a short cross-multiplication specialization of this established product/zero-test machinery, with an essential separate zero-event guard. The claimed new-to-this-packet contribution is the audit-specific commuting model, its source-identity distinction, the mixed-numerator obstruction, and the precise posterior-only interface/classification. It does not establish that no prior literature or uninspected project artifact contains the same specialization.

## 8. Verification, preservation, and limits

Run `python3 verify.py`. Only Python standard-library Fractions are used. CONTROL_RESULTS.json records exact results, including:

- the original 16-state source model, its audit-only rank-eight quotient, rank-sixteen report-plus-audit closure, and original 7/10→1/5 posterior;
- the four-mass known-Bad quotient, equal target/audit marginals, differing conditional targets, idempotent same-audit reread and impossible contradictory reread;
- fresh-versus-fixed verifier controls, including 1/17 after two fresh disagreeing verifiers;
- a positive-support posterior-only collision with different event probabilities;
- the false positive obtained by omitting the feasibility guard;
- an inadmissible moment vector giving a negative posterior;
- the fixed-binary-audit signature compared against the tensor/support criterion on all 4,225 ordered pairs of 65 distinct normalized rational laws;
- exact seeded generic instruments, closed-update/normalization identities, shared-word tensor identities, finite-horizon checks at the antisymmetric dimension bound, and projective scale invariance;
- support-language comparison for all 729 combinations of two partial deterministic two-state maps and three nonempty initial support laws in each slot;
- rehashing of the eight bound inherited inputs, including the reviewed immutable source-audit snapshot.

Finite controls corroborate the written universal arguments; they do not prove those arguments by enumeration. Exact arithmetic does not authenticate a source, establish its empirical calibration, grant authorization, determine actual cognitive basing, or turn a possible model revision into justified knowledge. The positive result is conditional on the declared finite channel, target, state domain, and future-operation scope. No sample-complexity optimization or generic model-discovery campaign is added.
