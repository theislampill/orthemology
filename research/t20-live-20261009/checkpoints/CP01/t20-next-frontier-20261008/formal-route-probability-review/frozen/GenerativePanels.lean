import Model
import BernoulliAssignments
import HistogramGrouping

namespace RouteProbability

open scoped BigOperators
open CalibratedIdentification

variable {R E : Type*} [Fintype R] [DecidableEq R] [Fintype E] [DecidableEq E]

/-- The actual route-occurrence inventory induces its anonymous five-class histogram. -/
def histogram (M : Model R E) : Histogram E where
  a := routeCount M.kind M.outputs .a
  b := routeCount M.kind M.outputs .b
  c := routeCount M.kind M.outputs .c
  d := routeCount M.kind M.outputs .d
  e := routeCount M.kind M.outputs .e
  a_empty := routeCount_empty M.kind M.outputs M.outputs_nonempty .a
  b_empty := routeCount_empty M.kind M.outputs M.outputs_nonempty .b
  c_empty := routeCount_empty M.kind M.outputs M.outputs_nonempty .c
  d_empty := routeCount_empty M.kind M.outputs M.outputs_nonempty .d
  e_empty := routeCount_empty M.kind M.outputs M.outputs_nonempty .e

/-- Probability is defined by summing normalized independent assignment weights
whose generated endpoint contains no member of the queried bundle. -/
def absenceProbability (M : Model R E) (S : Profile) (U : Finset E) : ℚ :=
  ∑ ω : R → Bool, if ¬(endpoint M S ω ∩ U).Nonempty then
    bernoulliWeight (fun r => failure (M.kind r)) ω else 0

omit [Fintype E] in
/-- The declared assignment model is a normalized nonnegative finite distribution. -/
theorem assignment_distribution (M : Model R E) :
    (∀ ω : R → Bool, 0 ≤ bernoulliWeight (fun r => failure (M.kind r)) ω) ∧
    (∑ ω : R → Bool, bernoulliWeight (fun r => failure (M.kind r)) ω) = 1 := by
  constructor
  · exact bernoulliWeight_nonneg _ (fun r => failure_nonneg (M.kind r))
      (fun r => failure_le_one (M.kind r))
  · exact sum_bernoulliWeight _

omit [DecidableEq R] [Fintype E] in
/-- Disabled classes contribute a unit factor; active classes retain calibration. -/
lemma relevant_product (M : Model R E) (S : Profile) (U : Finset E) :
    (∏ r ∈ relevant M S U, failure (M.kind r)) =
    ∏ r ∈ Finset.univ.filter (fun r => (M.outputs r ∩ U).Nonempty),
      if enabled S (M.kind r) then failure (M.kind r) else 1 := by
  unfold relevant
  rw [Finset.prod_filter, Finset.prod_filter]
  apply Finset.prod_congr rfl
  intro r _
  by_cases he : enabled S (M.kind r)
  · simp [he]
  · simp [he]

/-- The no-hit probability factorization is derived from the assignment-level
model and the generated endpoint; it is not the definition of probability. -/
theorem absence_probability_factorisation (M : Model R E) (S : Profile) (U : Finset E) :
    absenceProbability M S U =
    ∏ k : Kind, (if enabled S k then failure k else 1) ^
      hit (routeCount M.kind M.outputs k) U := by
  unfold absenceProbability
  simp_rw [endpoint_absent_iff]
  rw [sum_bernoulliWeight_all_false, relevant_product]
  exact product_grouped_by_histogram M.kind M.outputs U
    (fun k => if enabled S k then failure k else 1)

/-- The A panel is derived from the finite stochastic route model. -/
theorem absence_A (M : Model R E) (U : Finset E) :
    absenceProbability M .A U = panelA (histogram M) U := by
  rw [absence_probability_factorisation, univ_kind]
  simp [enabled, failure, panelA, histogram, pow_add]

/-- The B panel is derived from the finite stochastic route model. -/
theorem absence_B (M : Model R E) (U : Finset E) :
    absenceProbability M .B U = panelB (histogram M) U := by
  rw [absence_probability_factorisation, univ_kind]
  simp [enabled, failure, panelB, histogram, pow_add]

/-- The AB panel is derived from the finite stochastic route model. -/
theorem absence_AB (M : Model R E) (U : Finset E) :
    absenceProbability M .AB U = panelAB (histogram M) U := by
  rw [absence_probability_factorisation, univ_kind]
  simp [enabled, failure, panelAB, histogram, jointCode, mul_assoc]

variable {R' : Type*} [Fintype R'] [DecidableEq R']

/-- Full forward-model/inverse composition. Occurrence types and inventory sizes
may differ. Exact observational agreement identifies their anonymous histograms. -/
theorem generative_model_identification (M : Model R E) (N : Model R' E)
    (h : ∀ S : Profile, ∀ U : Finset E, U.Nonempty →
      absenceProbability M S U = absenceProbability N S U) :
    histogram M = histogram N := by
  apply calibrated_panels_identify
  intro U hU
  constructor
  · simpa only [absence_AB] using h .AB U hU
  constructor
  · simpa only [absence_A] using h .A U hU
  · simpa only [absence_B] using h .B U hU

end RouteProbability
