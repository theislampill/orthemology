import EndpointLaw

open RouteProbability

#check @bernoulliWeight_nonneg
#check @sum_bernoulliWeight
#check @sum_bernoulliWeight_all_false
#check @endpoint_absent_iff
#check @absence_probability_factorisation
#check @absence_A
#check @absence_B
#check @absence_AB
#check @generative_model_identification
#check @endpointProbability_normalized
#check @endpointProbability_nonneg
#check @endpoint_law_identification
#print axioms sum_bernoulliWeight_all_false
#print axioms endpoint_absent_iff
#print axioms absence_probability_factorisation
#print axioms generative_model_identification
#print axioms endpointProbability_normalized
#print axioms endpointProbability_nonneg
#print axioms endpoint_law_identification

/-- Different occurrence counts and arbitrary finite effect catalogues are covered. -/
example (routes routes' effects : ℕ)
    (M : Model (Fin routes) (Fin effects)) (N : Model (Fin routes') (Fin effects))
    (h : ∀ S V, endpointProbability M S V = endpointProbability N S V) :
    histogram M = histogram N := endpoint_law_identification M N h

/-- An empty route inventory is a valid normalized model. -/
example (p : Empty → ℚ) : (∑ ω : Empty → Bool, bernoulliWeight p ω) = 1 :=
  sum_bernoulliWeight p

/-- The real-number interpretation of the calibrated rational probabilities
is unnecessary for the exact finite model: rational masses already normalize. -/
example (M : Model (Fin 3) (Fin 2)) (S : Profile) :
    (∑ V : Finset (Fin 2), endpointProbability M S V) = 1 :=
  endpointProbability_normalized M S
