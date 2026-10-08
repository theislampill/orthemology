import HiddenChangeSemanticEndpoint
open HiddenChange
#print axioms policyLawful_iff_allHistoryLawful
#print axioms LawfulMeasurableWinner
#print axioms DeterministicWinner
#print axioms positive_compiled_semantics
#print axioms seeded_winner_has_positive
#print axioms positive_iff_deterministic_winner
#print axioms bound_positive_compiled_semantics
#print axioms seeded_winner_has_bound_positive
#print axioms bound_positive_iff_deterministic_winner
#print axioms bound_negative_excludes_seeded_winner
#print axioms bound_negative_iff_no_deterministic_winner
#print axioms signed_semantic_alternatives

set_option pp.universes true in
#check @policyLawful_iff_allHistoryLawful
set_option pp.universes true in
#check @LawfulMeasurableWinner
set_option pp.universes true in
#check @DeterministicWinner
set_option pp.universes true in
#check @positive_compiled_semantics
set_option pp.universes true in
#check @seeded_winner_has_positive
set_option pp.universes true in
#check @positive_iff_deterministic_winner
set_option pp.universes true in
#check @bound_positive_compiled_semantics
set_option pp.universes true in
#check @seeded_winner_has_bound_positive
set_option pp.universes true in
#check @bound_positive_iff_deterministic_winner
set_option pp.universes true in
#check @bound_negative_excludes_seeded_winner
set_option pp.universes true in
#check @bound_negative_iff_no_deterministic_winner
set_option pp.universes true in
#check @signed_semantic_alternatives
