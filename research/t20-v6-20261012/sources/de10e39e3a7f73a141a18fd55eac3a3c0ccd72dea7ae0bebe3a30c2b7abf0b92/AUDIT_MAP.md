# Declaration meaning / source correspondence map

All theorem bodies are in external new research files. No frozen source declaration is silently edited, renamed, or claimed compiled by this project.

## Relational continuation (§11 of frontier-programme.md)

- `liftedRank_step`: derives destination maximum-rank contraction from every successor alternative having a source predecessor (C4) and actual source rank descent. It does not assume destination rank descent.
- `liftedRank_run_bound`: induction over arbitrary selected-policy runs, giving `rank(run n) ≤ rank(run 0)-n`.
- `liftedRank_zero_iff`: zero of the finite maximum is equivalent to every represented alternative having zero rank.
- `target_after_liftedRank`: conservative target transfer C1 turns the derived zero rank into target membership, for every n past the initial maximum.
- `matched_run`: C3 constructs an infinite source path from every related initial source state; destination choices remain fixed by the given run/policy.
- `restoration_transport`: combines actual rank transport and matched readout path under a complete `ContinuationContract`; safety and license predicates are supplied and visibly assumed. Its proof does not confer real-world permission.
- `exists_policy_run`: nonblocking is an explicit contract field, and produces an infinite run, preventing a dead-end-only universal-run theorem from being the claimed result.
- `RankFixtures`: non-singleton/overlapping positive fibres and an alternating-match-without-coverage failure. The latter is a genuine stale source alternative, not an arbitrary contradictory axiom.

## Partial-equivalence refinement (cvc-research.md §3)

- `PER.completion`: on S×Bool, relate x,y exactly when x=y or R(x.state,y.state). Symmetry/transitivity of R establish a total equivalence; no reflexivity of R is assumed.
- `PER.coarseMap`: a finer completion quotient maps surjectively to a coarser one.
- `PER.coarseMap_not_injective`: a removed R-pair is represented with opposite tags, preventing equality from masking a lost diagonal.
- `PER.potential_strict`: finite surjective noninjective maps force the strict cardinal increase. This is the substantive combinatorial mechanism.
- `PER.potential_le`: completed quotient cardinal is at most 2m.
- `PER.potential_universal`: starts at one for nonempty S.
- `PER.strict_chain_length`: derives, rather than assumes, the 2m−1 limit.
- `PER.stabilization_bound`: adds deterministic recurrence, converting any equality into permanent stationarity and proving equality at the uniform bound.
- `PER.potential_formula`: constructs an actual quotient equivalence and cardinal decomposition establishing exactly `2(m−|D|)+c`, including empty D.

## Actual binary Mealy semantics (pinned DEFECT_COMPUTABILITY.md §5)

- `Mealy.refine`: forall independent b,c, compare immediate output and successor relation. The proof of transitivity picks a common middle input false. This is the literal universal-input condition, not same-input bisimulation.
- `Mealy.approx_decreasing`: from top and actual recurrence, all iterations refine.
- `Mealy.stabilization_bound`: instantiates the generic PER theorem; finite nonempty S is explicit.
- `Mealy.bound_iff_infinite`: finite bound equals every finite approximant, not a hand-chosen postfixed subrelation.
- `Mealy.approx_iff_words`: independently relates the operator to actual recursive finite output execution on all pairs of length-n words.
- `Mealy.distinguishing_words`: failure of the infinite diagonal yields two differing actual output words at uniform length 2m−1.
- `MealySharpness`: a countdown reindexing of the original sharpness family, plus a one-state copy-input machine. Every m≥1 has an actual m-state machine surviving 2m−2 and failing at 2m−1. All-size optimality is a separate theorem from the upper bound.

## Quantitative finite words

- `BoundedPaths.words`: a finite set of actual lists of input blocks, constructed by admissible first block and recursively computed suffix. Different heads give injective list construction.
- `card_words_succ`, `mem_words_succ`: cardinal and semantic recurrences proved from that set construction.
- `card_words_le_pow`: derives an exponential path count from the local branching bound.
- `Mealy.exists_mismatch_block`, `card_matchingBlocks_le`: apply actual distinguishing words to exclude one of the 2^L input blocks for any requested output target.
- `deterministic_domain_closed`: the infinite-output diagonal is transition closed, directly from the universal operator.
- `surviving_input_words_bound`: puts the local mismatch bound into the genuine path-count recurrence, retaining domain-avoidance conditions.
- `surviving_uniform_fraction_bound`: rational normalisation of those counts, yielding `(1−1/2^L)^j`. No infinite measure, IID product construction, almost-sure limit, or atomic-mass theorem is hidden in this statement.

## Reviewer challenge questions

1. Can opposite-tag completion conflate deletion with equality? The noninjectivity proof explicitly rules this out.
2. Are empty fibres or dead ends manufacturing success? They are prohibited in the bundled contract, and run existence is independently proved.
3. Is a source witness chosen after an inaccessible destination action? The destination relation already fixes one selected policy; C3 quantifies over every source alternative and every destination branch.
4. Is full-fibre coverage inferred from alternating matching? No, it is a distinct field with a compiled deletion counterexample.
5. Does a finite count get called an infinite probability theorem? No; the README and declaration types retain the boundary.
6. Is the upper bound called universally sharp only from small examples? No; the all-cardinality constructive family is separately compiled.

## Concrete-simulation lower envelope

- `lowerRank_step`: chooses a minimum witness from an explicitly nonempty finite fibre. C3 supplies a matching successor for the same destination step; pairwise bad reflection bounds the destination bad indicator; the next fibre minimum is no larger than the matched source rank. C4 coverage is not assumed.
- `badVisits_add_rank_le`: prefixes count bad states at times `[0,n)`, plus the rank at n; induction proves this stays below initial rank.
- `eventually_no_bad_of_budget`: the sequence attains a globally least natural rank. Future nonincrease prevents any further bad-rank drop. This gives an existential cutoff, with no fixed delay claim.
- `lowerRank_preserves_eventual_good`: combines the derived lower budget with bad-visit counting and eventual goodness for each supplied infinite destination run. It does not synthesize a policy, establish observation-uniform implementation, supply authority, or prove nonblocking.
- `arbitrarily_late_bad_visit`: a nonvacuous rank-one run has its single bad state at any chosen delay, proving why a bad-visit bound is not a time-to-target bound.
- `stale_bad_reflection_fails`: blocks applying the new minimum theorem to the original failed universal-information target contract.

An additional semantic readback of both rank transports found the statements and hypothesis directions correct. It specifically confirmed the source/destination dynamics, public observability, authorization, safety, and readout adequacy remain model obligations. This review is separate from the compiler receipts and is not external refereeing.
