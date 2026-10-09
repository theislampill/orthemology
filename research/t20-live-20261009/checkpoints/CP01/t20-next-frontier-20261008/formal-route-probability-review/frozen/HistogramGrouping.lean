import CalibratedPanels

/-!
# Grouping labelled route occurrences by their anonymous histogram

Each occurrence carries one class and a finite output set. Summing histogram
entries that hit a query counts exactly the corresponding labelled occurrences.
Consequently, a product over those occurrences can be grouped by class.
-/

namespace RouteProbability

open scoped BigOperators

variable {R K E : Type*}
variable [Fintype R] [DecidableEq R]
variable [Fintype K] [DecidableEq K]
variable [Fintype E] [DecidableEq E]

/-- Multiplicity of a class/output pair among the labelled route occurrences. -/
def routeCount (kind : R → K) (outputs : R → Finset E) (k : K) (T : Finset E) : ℕ :=
  (Finset.univ.filter (fun r => kind r = k ∧ outputs r = T)).card

omit [DecidableEq R] [Fintype K] in
/-- The hit transform of a class histogram counts its occurrences hitting the query. -/
theorem hit_routeCount (kind : R → K) (outputs : R → Finset E) (k : K) (U : Finset E) :
    CalibratedIdentification.hit (routeCount kind outputs k) U =
      (Finset.univ.filter (fun r => kind r = k ∧ (outputs r ∩ U).Nonempty)).card := by
  unfold CalibratedIdentification.hit routeCount
  rw [← Finset.sum_filter]
  simpa only [Finset.filter_filter, Finset.mem_filter, Finset.mem_univ, true_and] using
    Finset.sum_card_fiberwise_eq_card_filter
      (Finset.univ.filter (fun r => kind r = k))
      (Finset.univ.filter (fun T : Finset E => (T ∩ U).Nonempty)) outputs

omit [DecidableEq R] in
/-- Regrouping a product over hitting routes requires neither positivity nor
nonempty output sets. -/
theorem product_grouped_by_histogram (kind : R → K) (outputs : R → Finset E)
    (U : Finset E) (f : K → ℚ) :
    (∏ r ∈ Finset.univ.filter (fun r => (outputs r ∩ U).Nonempty), f (kind r)) =
      ∏ k : K, f k ^ CalibratedIdentification.hit (routeCount kind outputs k) U := by
  rw [← Finset.prod_fiberwise'
    (Finset.univ.filter (fun r => (outputs r ∩ U).Nonempty)) kind f]
  apply Finset.prod_congr rfl
  intro k _
  rw [Finset.prod_const, hit_routeCount]
  congr 1
  apply congrArg Finset.card
  ext r
  simp [and_comm]

omit [DecidableEq R] [Fintype K] [Fintype E] in
/-- Nonempty route outputs imply the histogram's empty-output coordinate vanishes. -/
theorem routeCount_empty (kind : R → K) (outputs : R → Finset E)
    (h : ∀ r, (outputs r).Nonempty) (k : K) : routeCount kind outputs k ∅ = 0 := by
  apply Finset.card_eq_zero.mpr
  apply Finset.eq_empty_iff_forall_not_mem.mpr
  intro r hr
  exact (h r).ne_empty (Finset.mem_filter.mp hr).2.2

end RouteProbability
