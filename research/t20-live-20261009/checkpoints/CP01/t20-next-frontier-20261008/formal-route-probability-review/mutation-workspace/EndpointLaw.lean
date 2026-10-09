import GenerativePanels

namespace RouteProbability

open scoped BigOperators

variable {R E : Type*} [Fintype R] [DecidableEq R] [Fintype E] [DecidableEq E]

/-- The full joint endpoint law is the finite pushforward of assignment weights. -/
def endpointProbability (M : Model R E) (S : Profile) (V : Finset E) : ℚ :=
  ∑ ω : R → Bool, if endpoint M S ω = V then
    bernoulliWeight (fun r => failure (M.kind r)) ω else 0

/-- A joint-absence coordinate is a marginal of the actual endpoint law. -/
theorem absence_from_endpointLaw (M : Model R E) (S : Profile) (U : Finset E) :
    (∑ V : Finset E, if ¬(V ∩ U).Nonempty then endpointProbability M S V else 0) =
    absenceProbability M S U := by
  calc
    _ = ∑ V : Finset E, ∑ ω : R → Bool,
        if ¬(V ∩ U).Nonempty then
          (if endpoint M S ω = V then bernoulliWeight (fun r => failure (M.kind r)) ω else 0)
        else 0 := by
          apply Finset.sum_congr rfl
          intro V _
          by_cases hV : ¬(V ∩ U).Nonempty <;> simp [hV, endpointProbability]
    _ = ∑ ω : R → Bool, ∑ V : Finset E,
        if ¬(V ∩ U).Nonempty then
          (if endpoint M S ω = V then bernoulliWeight (fun r => failure (M.kind r)) ω else 0)
        else 0 := Finset.sum_comm
    _ = absenceProbability M S U := by
      unfold absenceProbability
      apply Finset.sum_congr rfl
      intro ω _
      rw [Finset.sum_eq_single (endpoint M S ω)]
      · simp
      · intro V _ hV
        simp [Ne.symm hV]
      · simp

/-- The endpoint distribution has total mass one. -/
theorem endpointProbability_normalized (M : Model R E) (S : Profile) :
    (∑ V : Finset E, endpointProbability M S V) = 1 := by
  simpa [absenceProbability, sum_bernoulliWeight] using absence_from_endpointLaw M S ∅

omit [Fintype E] in
/-- Every endpoint probability is nonnegative. -/
theorem endpointProbability_nonneg (M : Model R E) (S : Profile) (V : Finset E) :
    0 ≤ endpointProbability M S V := by
  apply Finset.sum_nonneg
  intro ω _
  split
  · exact (assignment_distribution M).1 ω
  · rfl

variable {R' : Type*} [Fintype R'] [DecidableEq R']

/-- Equality of the three full generated endpoint laws identifies the complete
anonymous route histogram, even when occurrence types and counts differ. -/
theorem endpoint_law_identification (M : Model R E) (N : Model R' E)
    (h : ∀ S : Profile, ∀ V : Finset E,
      endpointProbability M S V = endpointProbability N S V) :
    histogram M = histogram N := by
  apply generative_model_identification
  intro S U _
  rw [← absence_from_endpointLaw, ← absence_from_endpointLaw]
  apply Finset.sum_congr rfl
  intro V _
  rw [h S V]

end RouteProbability
