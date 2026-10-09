# Independent review: weighted certificate completion

Status: completed independent mathematical review of `RESULT.md` at SHA-256 `71551ae962a17ec72709b6d36cfb58ed99237a2ef776339709a43b8d3b436d28`.

Disposition: no remaining blocking mathematical defect was found in the stated restricted model. This is a revision-bound mathematical assessment, not repository integration, scientific adoption, programme closure, a novelty determination, or certification of the source-trust and philosophical premises.

## Overall finding

The core theorem is correct for a fixed, finite, monotone certificate-admissibility contract with finite real verification costs. Its cleanest formulation is an exact, canonical antichain representation of the per-verdict continuation-cost function. The residual-update law, cost-preserving planning quotient, and complete-menu characterization all follow. The conclusions are conditional computational claims, not a derivation of source trust or human epistemic basing.

No mathematical counterexample was found within that stated model. The principal qualifications are the meaning of canonical uniqueness, the separation of an abstract control state from concrete proof witnesses, and the persistence of warrant assumptions rather than merely token objects.

## 1. Exact inverse and canonical uniqueness

For a verdict v, let

    f_K^v(U) = min { κ_π : v_π = v and S_π ⊆ K ∪ U },

where min ∅ = +∞, all catalogue costs κ_π belong to the finite real interval [0,∞), and U ranges over every subset of the fixed token universe E. Let R_v(K) be the nondominated set of residual pairs (S_π \ K, κ_π), using the product order of support inclusion and ordinary cost order.

The exact inverse is

    R_v(K) = { (D, f_K^v(D)) :
                  f_K^v(D) < ∞ and
                  f_K^v(D \ {d}) > f_K^v(D) for every d ∈ D }.

For D = ∅, the last condition is vacuous. Checking immediate predecessors suffices because f is antitone under inclusion.

Proof: if (D,c) is nondominated, a certificate with residual contained in D and lower cost would dominate it; therefore f(D)=c. If any proper subset U⊊D had f(U)≤c, a minimizing residual contained in U would also dominate it. Conversely, if the displayed condition holds, any minimizing residual at D must equal D, and no distinct support-cost pair can dominate it. Finiteness of the catalogue gives minimizer attainment.

Consequently, two evidence states have equal weighted frontiers for every verdict if and only if their per-verdict continuation-cost functions agree for every U. Any exact summary of all those functions must distinguish inequivalent frontier classes. Thus this is the coarsest cost-observational quotient and the unique normalized antichain representation. It is not the sole possible encoding or literally the only sufficient summary.

If +∞ is allowed as a certificate’s own verification cost, the inverse and uniqueness statements fail without adjustment: a catalogue containing only an infinite-cost certificate and the empty catalogue have the same all-infinite cost function. Require finite κ_π, or discard infinite-cost certificates from the cost quotient while treating licence separately.

## 2. Persistent update and quotient

For any admitted token set T,

    f_{K∪T}^v(U) = f_K^v(T∪U).

Therefore continuation-cost equivalence is a congruence under token addition. At the representation level,

    R_v(K∪T) = Pareto-min { (D \ T,c) : (D,c) ∈ R_v(K) }.

A previously dominated pair remains dominated after subtracting T: support inclusion is preserved and verification costs do not change. Duplicate resulting pairs are identified as set elements.

The minimality claim is relative to all per-verdict costs under all U⊆E. A particular test menu can make some distinguishing U unreachable, or a particular objective can ignore verdict identity, so this need not be the coarsest quotient of that restricted planner.

The quotient is valid for the proposed planner while retaining B and Q. It is not a claim that the frontier alone captures all future test behavior. Test availability, outcome partitions, token emissions, and costs must depend only on the retained planning state and the fixed test model, not on forgotten details of the original evidence history.

## 3. Bellman exactness

For nonempty candidate set B and unused test set Q, define the terminal cost by taking the minimum over certificates for allowed substantive verdicts whose support lies in K. It is +∞ if none exists. A verdict meaning “unresolved” must not be included as an always-available substantive success.

The exact worst-case value is

    D(K,B,Q) = min(
        terminal_cost(K),
        min over q∈Q of [c_q + max over o with B_{q,o}≠∅
            D(K∪τ(q,o), B_{q,o}, Q\{q})]
    ).

Empty candidate branches must be excluded. The inner test minimum is +∞ when Q is empty. The objective must be deterministic-policy worst-case cost, or pathwise worst-case cost maximized over policy random bits. Deterministic test behavior alone does not impose deterministic policies. Worst-case expected cost under private randomization is a different objective. For example, take two scenarios and two unit-cost tests: the first yields a required certificate token only in the first scenario, and the second only in the second scenario; other outputs yield no usable tokens. Deterministic worst-case cost is 2, whereas a uniformly random test order has worst-case expected cost 1.5.

This is ordinary finite-depth minimax induction: a successful policy either stops with a currently enabled certificate or chooses a first test, after which the adversary selects a feasible output and the continuation is an instance with one fewer test. The induction also proves equality of values at states having equal frontiers, B, and Q, because terminal costs and all successor quotient states agree.

For a standard finite algorithm, state a finite scenario set or finite effectively represented outcome partitions. With infinite output alphabets the recursion can still be mathematically meaningful, but finite menu size alone does not make all branches algorithmically enumerable. Using sup instead of max is the generally safe formulation when attainment is not established. In the particular fixed-cost, finite-catalogue, one-use menu model, only finitely many path-cost sums can occur, which can supply attainment even when there are infinitely many outcomes.

All proof-cost optimality statements are relative to the fixed admitted catalogue Γ. Soundness of the rules does not imply that a finite selected catalogue contains every rule-derivable proof. If an implementable exact algorithm is claimed, costs and outcome partitions also need effective finite representations and comparisons.

The cost model charges the stipulated test costs and one terminal certificate-checking cost. It does not automatically include search for a proof, token admission/authentication, storage, querying the catalogue, or retained/cached checking work. These must be excluded explicitly or modeled separately.

## 4. Complete-menu criterion

The criterion is correct under all of the following:

- A finite total menu of tests, each executable until used.
- Each test has a fixed deterministic outcome for each candidate scenario.
- Its token emission depends only on the test and its observed outcome.
- Token accumulation, certificate admissibility, and the trust/rule/scope contract are monotone.
- Every test and verification has finite cost.
- A full transcript is feasible for at least one candidate scenario; it is not an arbitrary cross-product combination of individually possible outcomes.

Necessity: follow a guaranteed-resolving policy on a scenario x. The support of its terminal certificate is contained in the evidence obtainable from the whole menu on x. By persistence the same certificate is present in the complete transcript.

Sufficiency: execute every test in any fixed order. The full-transcript condition supplies an enabled substantive certificate at each leaf. Since the catalogue is finite, an available certificate can be chosen by finite search. The total cost is bounded by the sum of all test costs plus the largest catalogue verification cost.

The theorem establishes solvability under the stipulated warrant contract. A complete transcript with no admitted certificate does not establish that the target claim is false, unknowable in every stronger model, or impossible to resolve with new tests or new rules.

## 5. Witness reconstruction and epistemic scope

A numerical frontier is sufficient to choose future tests and calculate optimal costs. It is not by itself a usable proof packet. Actual proof delivery needs a realizing catalogue certificate and the authenticated evidence objects that discharge its support. A safe implementation keeps a representative certificate identifier for each frontier pair, together with the underlying evidence store. When residual pairs merge or dominate one another, keep a representative of the surviving pair. If the complete original evidence set is retained, a witness can instead be reconstructed by searching the finite catalogue.

Authentication establishes provenance under its assumptions. It does not establish truth of testimony. Inference-rule validity and source trust must be supplied and scoped independently. Moreover, persistence of authenticated objects alone does not ensure persistence of warrant: trust revocation, expiry, contradictory defeaters, or changing target time can invalidate earlier licences. The present theorem needs a fixed monotone validity contract; a defeasible extension requires additional state and cannot inherit the subtraction law without proof.

The existence or successful execution of a computational proof-production/checking procedure is not sufficient to establish human epistemic basing. The model should make no such identification.

## 6. Sharpness and examples

### Distinguishable residual states

One certificate with support E and fixed finite cost yields 2^n pairwise inequivalent evidence states when |E|=n: the residual support E\K identifies K, and a suitable continuation U enables one of two unequal residuals but not the other. The current licence bit distinguishes only the fully enabled state from the other 2^n−1 states.

This establishes 2^n state classes, hence an n-bit lower bound for an arbitrary exact state encoding. It does not by itself prove that each state needs an exponentially large representation.

### A genuinely exponential frontier

For every D⊆E, include one same-verdict certificate of support D and cost n−|D|. Every one of the 2^n pairs is nondominated: smaller support always has larger cost. Thus a weighted frontier can contain 2^n pairs. This is the largest possible cardinality because, for a fixed residual support, only its least cost survives.

With equal verification costs, supports instead form an ordinary inclusion antichain, whose maximal size is the central binomial coefficient.

### Why cost-blind dominance fails

Supports {a} at cost 10 and {a,b} at cost 1 must both be retained. The first is the only available proof after receiving a alone; the second becomes cheaper after receiving b too. Inclusion-only minimization would erase the cheaper future option.

### Display-equal histories

An authenticated assertion from an admitted source and an unauthenticated copy can have identical rendered text while differing in admissible token identity. The example is valid if the display map erases provenance and the licence contract distinguishes the typed authenticated token. It should not imply that all authenticated testimony is true.

## 7. Independent mechanical checks

A standalone Python exhaustive check, without modifying the manuscript, verified:

- All 65,536 assignments of absent/0/1/2 costs to the eight supports on a three-token universe: direct Pareto reduction agrees with the inverse recovered from the continuation-cost function.
- All 4,096 combinations of catalogue, current evidence, and added evidence on a two-token universe: residualizing the old frontier and re-minimizing agrees with directly constructing the new frontier.

All checks passed. These finite checks supplement the proofs; they do not replace them.

## Final manuscript consistency review

The first complete manuscript was read in full. Its theorem proofs agree with this review. The following precise corrections were sent to the author and are now incorporated in the reviewed revision:

1. **Guaranteed checking success.** The manuscript calls Γ members “candidate proof objects” and initially says their verdict follows only “if π passes” the checker, while the Bellman terminal action assumes certain success. State that Γ consists of admissible, valid rule/scope derivations whose checks succeed when their support is available. This does not assert that operational checking has already occurred. Uncertain check success requires an additional transition/outcome model or restriction to a valid subcatalogue.
2. **Authenticated inventory consistency.** The display-equal example initially put an unauthenticated copied report r into K₂={r,b}, contrary to K’s definition. Raw r can remain in the display/history while K₂={b}, or r can instead be an authenticated copy-artifact token that lacks the required primary-source entitlement.
3. **Residual coordinates.** At K={a}, the larger-support/cheaper-proof example has residual pairs (∅,10) and ({b},1). The original pairs ({a},10) and ({a,b},1) describe K=∅.
4. **Optimal choices versus proof identities.** Equal frontiers preserve optimal test actions and abstract terminal verdict-cost choices, not necessarily the same concrete certificate identifier. A proof needing {a} and an equal-cost same-verdict proof needing {b} yield equal frontiers at inventories {a} and {b}, while only the respective certificate is enabled. Reconstruction selects a local witness.
5. **Monotone negative diagnoses.** “Currently unsupported” and no-certificate conclusions must refer to a fixed inventory/time or completed bounded-search snapshot. An unqualified current-state absence claim can be invalidated by future evidence and therefore falls outside the persistence contract.
6. **Randomized objectives.** The deterministic-policy/pathwise-worst-case convention is now explicit.

The final minor clarifications are also incorporated: costs are finite nonnegative reals; executable exact planning requires effective representation and comparison; witness-search proofs share a fixed terminal price k; and the expiry counterexample starts from empty active inventory.


### Final independent rerun and remaining scope

The final exact `verify.py` was read and independently rerun. Its sole output write was intercepted in memory, so the rerun changed no manuscript, code, or check-result files. All assertions passed, and the captured JSON exactly matches the supplied `CHECK_RESULTS.json`.

Revision binding:

- `RESULT.md`: `71551ae962a17ec72709b6d36cfb58ed99237a2ef776339709a43b8d3b436d28`
- `verify.py`: `bdd29fd57418db2327983bf2cb7e4c40632c9140637ae6df5d0d990ff28481b2`
- `CHECK_RESULTS.json`: `429fc2e93da069d5ac61b7527860f74ecb83e73e9d780e6caf85a51b9e60a602`

The manuscript’s concrete checks now cover 256 inverse-frontier catalogues, 4,096 recovery evaluations, 4,096 residual updates, 120 distinguishing continuation pairs, 1,024 full-transcript feasibility models, priced verification, witness search, provenance distinction, scope transport, derivation/support checking with a rejected wrong-premise/scope mutation, an expiry counterexample, and the deterministic/randomized-expected objective distinction.

The final precision edits were directly checked in the hash-bound manuscript: finite real costs and the effective-comparability qualification are present, and §6.1 now identifies an untagged proof-availability summary that can merge distinct scope-entitlement histories while expressly noting that tag erasure alone need not erase a separately retained transport token. The common witness-check price and empty initial inventory are explicit. No review correction remains outstanding. The verification script and result hashes are unchanged, so the independent successful rerun remains applicable.

No general claim of literature originality was independently verified. No conclusion was drawn about the truth of a specific philosophical application, the adequacy of its semantics, the honesty of a source, or a human’s operative epistemic basing.
