import IndexedControls
set_option pp.universes true
set_option format.width 120
#check @Orthemology.CertifiedObserver.Indexed.literal_state
#print axioms Orthemology.CertifiedObserver.Indexed.literal_state
#check @Orthemology.CertifiedObserver.Indexed.source_output_exact
#print axioms Orthemology.CertifiedObserver.Indexed.source_output_exact
#check @Orthemology.CertifiedObserver.Indexed.certified_index_defect
#print axioms Orthemology.CertifiedObserver.Indexed.certified_index_defect
#check @Orthemology.CertifiedObserver.Indexed.certified_index_error
#print axioms Orthemology.CertifiedObserver.Indexed.certified_index_error
#check @Orthemology.CertifiedObserver.Indexed.tick_sound
#print axioms Orthemology.CertifiedObserver.Indexed.tick_sound
#check @Orthemology.CertifiedObserver.Indexed.search_tick_exact
#print axioms Orthemology.CertifiedObserver.Indexed.search_tick_exact
#check @Orthemology.CertifiedObserver.Indexed.uniform_tick
#print axioms Orthemology.CertifiedObserver.Indexed.uniform_tick
#check @Orthemology.CertifiedObserver.Indexed.scheduled_tick_success
#print axioms Orthemology.CertifiedObserver.Indexed.scheduled_tick_success
#check @Orthemology.CertifiedObserver.Indexed.runtime_output_exact
#print axioms Orthemology.CertifiedObserver.Indexed.runtime_output_exact
#check @Orthemology.CertifiedObserver.Indexed.runtime_law_exact
#print axioms Orthemology.CertifiedObserver.Indexed.runtime_law_exact
#check @Orthemology.CertifiedObserver.Indexed.runtime_finite_solver
#print axioms Orthemology.CertifiedObserver.Indexed.runtime_finite_solver
#check @Orthemology.CertifiedObserver.Indexed.Fixtures.split_decode
#print axioms Orthemology.CertifiedObserver.Indexed.Fixtures.split_decode
#check @Orthemology.CertifiedObserver.Indexed.Fixtures.splitSimulation
#print axioms Orthemology.CertifiedObserver.Indexed.Fixtures.splitSimulation
#check @Orthemology.CertifiedObserver.Indexed.Fixtures.runtime_split_defect
#print axioms Orthemology.CertifiedObserver.Indexed.Fixtures.runtime_split_defect
#check @Orthemology.CertifiedObserver.Indexed.Controls.undersized_horizon_loses_tick
#print axioms Orthemology.CertifiedObserver.Indexed.Controls.undersized_horizon_loses_tick
#check @Orthemology.CertifiedObserver.Indexed.Controls.same_runtime_law_distinct_source
#print axioms Orthemology.CertifiedObserver.Indexed.Controls.same_runtime_law_distinct_source
set_option pp.universes false
#eval P02.Codec.encodeBytes Orthemology.CertifiedObserver.Indexed.Fixtures.splitProgram
#eval Orthemology.CertifiedObserver.Indexed.Fixtures.splitIndex
