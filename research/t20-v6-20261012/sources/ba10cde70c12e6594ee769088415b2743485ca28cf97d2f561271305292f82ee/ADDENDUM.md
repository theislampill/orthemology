# Posterior-equivalent continuations can disagree on almost-sure exact stopping

10 October 2026 UTC. Separate bounded follow-through to the frozen stochastic exact-inquiry result. The main packet is unchanged. Ordinary proof plus exact rational controls; no kernel or empirical claim.

## Result

**The current posterior-only continuation quotient preserves every finite conditional answer and the possibility of every finite receipt history, but can still identify an almost-surely solvable exact-stopping problem with an unsolvable one.** The failure is probability-one eventual completion, not correctness of any finite posterior. It is stronger than the already established failure to preserve a chosen expected score: here existence of any lawful zero-error almost-surely terminating policy changes.

The positive alternative is precise. Full predictive equality, including branch probabilities and target numerators, preserves each shared history policy's finite stopped-verdict laws. With matching legal menus and terminal-report permissions, continuity from below carries that equality to almost-sure finite stopping. No hidden-state isomorphism is needed. A weaker sufficient repair is uniform domination of finite-history laws; same finite initial support supplies mutual domination for a fixed instrument. The original eight-mass audit quotient meets that contract and passes the direct support-transition check below.

## 1. The exact existing posterior-only interface

The 10 October audit-continuation result defines r≈post s by equality of feasible finite action/receipt words and equality of the target posterior after every such word, including the empty word. It explicitly discards word probabilities. It proves a paired-tensor criterion plus a separate feasible-language test, and identifies a set-theoretic partial continuation quotient.

The subsequent inquiry-value result already demonstrates that this quotient need not preserve expected proper-score gain or the resulting audit-versus-skip choice. It does not test a probability-one exact-stopping objective. The present counterexample applies the existing quotient to that stronger temporal contract; it neither corrects its equivalence theorem nor reinvents its tensor mechanism.

The exact-stopping theorem compares policies for a declared finite immutable initial answer label. Stopping at a posterior point mass is allowed; a finite mixed-label posterior cannot justify a zero-error declaration. This is a model-relative certificate requirement, not a claim that all human knowledge or practical warrant demands probability one.

## 2. One instrument, two posterior-equivalent starting laws

There are four static latent states, ordered

    (0,R), (1,R), (0,N), (1,N).

The first coordinate Theta is the requested answer. R means the instrument may reveal it; N means it never reveals it. One universally permitted repeatable observation has receipts w, r0, r1, with diagonal likelihoods

    M_w  = diag(1/2, 1/2, 1, 1)
    M_r0 = diag(1/2, 0,   0, 0)
    M_r1 = diag(0,   1/2, 0, 0).

The matrices sum to the identity. They are a single fixed valid finite instrument, not two changed experiments. In R each use is a fresh chance to reveal the same fixed answer. In N the receipt is always w. Once a reveal is seen, the target is known; later readings, if taken, cannot reveal the opposite label. Terminal stopping is available and permitted.

Compare

    p = (1/2, 1/2, 0,   0)
    q = (1/4, 1/4, 1/4, 1/4).

Both have current target probability (1/2,1/2).

### All-word posterior and feasibility proof

A word containing both r0 and r1 is impossible under both laws. Every word containing only w and one reveal type is possible under both, as is every all-w word. Thus the two laws have the same feasible-word language exactly.

An all-w word weights the two target labels symmetrically within each surviving mode. Its target posterior remains (1/2,1/2) under both laws, at every finite length. A word containing rk and no opposite reveal eliminates all states except (k,R), so its posterior is the point mass at k under both laws. These cases exhaust all finite words. Hence p≈post q under the existing definition.

No finite-depth testing is used to prove the all-word statement. The executable paired-tensor closure provides a second exact finite algebraic check: its row-space dimensions are 1→2→3, it is closed under all same-word tensor operators, and each basis row annihilates p⊗q. The separate feasible-language proof remains essential.

### Different exact-stopping existence

Under p, stop at the first reveal. Every verdict is correct, and

    P_p(no reveal in the first n uses) = 2^(-n).

The limit is zero, so this policy terminates almost surely. It has no sure finite depth because each w^n is possible and ambiguous; the all-w infinite path remains supported even though its probability is zero.

Under q,

    P_q(no reveal in the first n uses) = 1/2 + 2^(-n-1).

Its limit is 1/2, the initial N mass. On an N path the observer receives w forever. A zero-error policy cannot stop on any finite w^n with positive probability because both target labels still have positive conditional probability there. This also excludes randomized stopping: a common positive-probability stopping choice at such a history produces a positive error under an opposite-label possibility. Consequently **no** zero-error policy can terminate almost surely under q. Nontermination probability is at least 1/2; waiting until the first reveal attains that bound.

The instrument and permitted actions are identical. Only the initial distribution changes, exactly as in the posterior-continuation equivalence problem. The initial supports are different: supp(p)={(0,R),(1,R)} and supp(q) contains all four states. This is necessary for this example and consistent with the main theorem that qualitative almost-sure winningness depends only on support for one fixed finite instrument. The example does not refute same-support invariance, and does not assert an all-positive-state collision.

## 3. What the weaker quotient still preserves

With common history-based legal menus and terminal permissions, posterior-only equivalence does preserve any **sure finite** exact decision protocol. The same finite action/receipt tree has exactly the same feasible branches under both starting laws. Its terminal target posteriors agree, so a correct point-mass leaf in one remains correct in the other. An everywhere-terminating finitely branching protocol has a finite uniform depth by the inherited sure-stopping argument. Thus existence of a sure finite exact protocol transfers in both directions.

The counterexample separates sure finite decision from almost-sure finite decision rather than declaring the posterior-only quotient useless. The missing datum is the probability of an unbounded continuation event. Every finite prefix can have positive probability without the infinite unresolved continuation having the same probability under the two starting laws.

## 4. Precise positive transport condition

Suppose two representations of a fixed initial problem have the same observable action and receipt alphabets, the same target-label meanings, and, for every finite word w,

    P(w) agrees,
    P(w, Theta=k) agrees for every target label k.

These are the full predictive probability/target-numerator identities already established by H-Continuation and the audit-continuation construction. In addition assume:

1. Histories correspond by their actual observed action/receipt sequence; neither policy is given an unobserved hidden state or new private information.
2. The same action menu is permitted at each reachable corresponding history, including any robust live-state permission requirement.
3. The same terminal reporting choices are permitted and have the same meaning. In the main theorem, reporting the common label at a homogeneous support is always permitted.

For every shared adaptive randomized history policy, its probability of each finite history and target label is obtained from the fixed-word likelihood by multiplying the same policy-choice factors. The factors for stopping and reporting at a finite history are also the same. Therefore, for every integer n and label k, the joint law of “stop by n, output k, target label l” agrees in both representations. Arbitrary independent private randomization can equivalently be integrated over its common law or represented behaviorally, as in the main theorem.

Now {tau<infinity}=union_n{tau<=n}. By continuity from below,

    P(tau<infinity) = lim_n P(tau<=n).

The error event is likewise the increasing union of finite-horizon stopped-error events. Thus stopping probability and total error probability agree for each corresponding policy. The equality of legal policy classes then gives equivalence of existence of a zero-error almost-surely finite policy.

This is an elementary infinite-horizon consequence of the inherited finite-history law contract; no new general stochastic-process theorem is claimed. Posterior-only equality cannot run this proof because P(w) is omitted, as §2 exhibits.

### A weaker sufficient repair: uniform prefix domination

Full predictive equality is sufficient, not necessary. Suppose posterior-only equivalence and the same lawful history-policy class hold, and there is a finite constant C such that, for every feasible finite action/receipt word h,

    Q(h) <= C P(h).

The same policy-choice factors multiply each word likelihood. Summing over the finite histories on which a shared policy has not stopped by n therefore gives

    Q(tau>n) <= C P(tau>n).

Consequently a policy that terminates almost surely under P also terminates almost surely under Q. Zero-error declarations transfer because the finite stopped-label posteriors agree. Mutual uniform domination gives a two-way transfer of zero-error almost-sure solvability. This is an elementary bounded-density argument, not a new probability theorem or a claim that such domination is necessary.

For a single fixed finite instrument, initial laws p and q with the same support automatically satisfy the stronger *labelled* finite-history bounds

    m P(h, Theta=k) <= Q(h, Theta=k) <= M P(h, Theta=k),
    m = min_x q(x)/p(x) > 0,    M = max_x q(x)/p(x) < infinity,

where extrema range over their common support. Indeed each word-and-label likelihood is a nonnegative linear combination of the initial masses. These bounds also hold after multiplying common adaptive policy factors. They preserve both probability-one termination and zero error, even when p and q do not have equal numerical target posteriors. With the same robust legal menus this recovers the main theorem's same-support qualitative invariance directly. It does not extend that invariance to different initial supports.

In the counterexample of §2,

    Q(w^n) / P(w^n) = 2^(n-1) + 1/2,

which is unbounded. Thus the lost probability-one guarantee is visible exactly as failure of this proposed weaker repair. This comparison is a sufficient transport diagnostic, not an optimization problem. The root suggested the domination repair; this addendum supplies its explicit policy and initial-law proof and rational controls.

### Permissions are an independent part of the contract

Observation/target intertwining alone does not encode legality. Identical potential observation kernels and target laws can accompany permission to make a perfect read in one system and no permission to make it in the other. One allows immediate exact decision and the other may not allow any inquiry. This is the already inherited H-ICS access-versus-admission distinction, now stated at this transport boundary.

For one-way controller transfer, it is enough that every reduced permitted action lifts to a permitted fine action with the stated history law. That yields safe transfer of the reduced controller, but not necessarily the reverse existence implication if the reduced menu omitted useful fine actions. Matching legal menus gives the two-way result above. The theorem does not require literal equality of hidden state spaces or full transcripts stored inside the controller.

One sufficient route to robust menu preservation is retaining the relevant permission predicates as observables: for a given action, all supported states permit it exactly when the expectation of its forbidden-state indicator is zero. This is a finite support statement under the current positive supported weights. H-Continuation already instructs the user to include authorization prerequisites in the retained contract; merely preserving answer probabilities does not establish them.

## 5. Actual eight-mass audit transport

The existing map G sends the original 16-state law on (Theta,T,Y,V) to eight masses of (Theta,T,D), D=1[V!=Y]. Reading A=(T,D) commutes with G and retains the target label. After the observed report Y=1, the fine and reduced instruments each have exactly five reachable supports. The direct checker establishes:

- each fine reachable support maps to the corresponding aggregate support;
- all four audit-receipt support updates commute;
- both models have no homogeneous target goal in the reachable family;
- both sure and almost-sure exact-stopping criteria therefore reject.

Here the one audit action is universally permitted in the declared model, and the terminal-report contract is the same. Hence the permission/history conditions are actually satisfied. The eight-mass quotient is safe for this stopping question; the posterior-only quotient need not be.

This uses the actual retained audit instrument rather than inventing a new source audit. It does not add a substantive claim about whether any real person or source is reliable or should be treated as known.

## 6. Evidence, ancestry and credit

The inherited main inputs are audit-continuation-transport-20261010/RESULT.md (posterior-only equivalence and full predictive contract), posterior-inquiry-value-20261010/RESULT.md (distinct expected-score obstruction), H-Continuation Theorem 2 and its contract discussion, and the frozen stochastic-exact-inquiry-20261010/RESULT.md (exact stopping semantics and criterion). The immutable input identities are recorded in INPUT_BINDINGS.json.

The root supplied the R/N counterexample and all-word proof outline, retained in posterior-stopping-boundary-root-20261010/DERIVATION.md. This worker checked the proof, supplied the paired-tensor closure check and actual solver realization, executed the eight-mass support transport, and stated the positive law/permission transfer. Root/worker overlap is shared development rather than independent corroboration.

Run:

    python3 check_transport.py
    python3 check_posterior_tail.py

The first checks the actual eight-mass support map and a permission-sensitive control. The second checks all 9,841 words through length eight, 30 exact survival and likelihood-ratio prefixes, 9,841 same-support word/target domination cases, the entire closed three-dimensional paired-tensor span, and the two different almost-sure winning decisions. Finite words corroborate rather than establish the all-word proof. The scripts depend on the exact bound solver in the adjacent frozen main packet. Independent review is a separate artifact and must identify this addendum's actual final bytes.

No protected input, main packet or earlier theorem has been changed. The newly learned boundary is specific: exact finite conditional continuation does not settle probability-one completion, while the stronger predictive law contract does once lawful policy correspondence is retained.
