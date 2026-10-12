# Independent review and revisions

The initial contract reviewer replayed eight tests and identified real gaps:
certificate conclusion/state binding and nonvacuity; actual applicability versus
implication-validity; dropped event state; indirect proof branches mistaken for
unique route lineage; and incomplete epistemic-wrapper fields. The reviewer also
requested the strongest common-law comparison and coupled certificate/productive
route-cut test. These were addressed, and initial code/tests remain in results.

The continuation reviewer independently checked the typed tensor query and the
indirect supplied-history projection, replaying eighteen checks. They confirmed
that route co-membership differs at equal contractions, and that the indirect
histories are extra refinements rather than alternative deterministic-closure
executions. A nondefault-state certificate helper defect was fixed and tested.

A second contract review reproduced a remaining applicability defect using normal
constructors: a sound B certificate could qualify against an A-only ledger if a
caller supplied an inconsistent AB active profile. The failure is recorded in
PROFILE_BINDING_RED.log. Ledger now retains issued roots; applicability checks
profile equality. PROFILE_BINDING_GREEN.log records all nineteen checks passing.
The report also states that execute_program guarantees Run/rule coherence, whereas
adapt_run trusts that precondition for manually supplied inputs.

The independent root review's eighteen-test bindings describe the version before
the final issued-profile fix. They are not silently re-labelled as final nineteen-
test approval. Final local and isolated replay is separately recorded in
results/VERIFICATION.json. The contract reviewer independently replayed all nineteen checks after the last fix and confirmed the original profile-substitution counterexample now returns False.

None of these reviews validates the metaphysical interpretation or closes T20.
