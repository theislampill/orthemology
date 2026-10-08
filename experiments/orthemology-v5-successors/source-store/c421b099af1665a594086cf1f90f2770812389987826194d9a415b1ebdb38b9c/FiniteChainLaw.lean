import FiniteChainHitting

/-! Bind the finite-chain recurrence to an actual PMF constructed from the
normalized rows. Absorbing a goal records whether it has been hit by the finite
horizon. This is a law construction, not a supplied hitting-probability law. -/
noncomputable section
open MeasureTheory
open scoped BigOperators ENNReal
namespace HiddenParity.Cost.FiniteChainHitting
variable {Q : Type*} [Fintype Q]

def rowPMF (P : Rows Q) (s : Q) : PMF Q :=
  PMF.ofFintype (fun t => ENNReal.ofReal (P.row s t)) (by
    rw [← ENNReal.ofReal_sum_of_nonneg (fun t _ => P.nonneg s t),P.normalized]
    simp)

@[simp] theorem rowPMF_apply (P : Rows Q) (s t : Q) :
    rowPMF P s t = ENNReal.ofReal (P.row s t) := PMF.ofFintype_apply _ _

/-- A genuine normalized finite-horizon Markov law, with goals made absorbing.
A path ends in a non-goal exactly when it has avoided goals through this time. -/
def absorbedLaw (P : Rows Q) (goal : Q → Prop) [DecidablePred goal] : ℕ → Q → PMF Q
  | 0, s => PMF.pure s
  | n+1, s => if goal s then PMF.pure s else (rowPMF P s).bind (absorbedLaw P goal n)

variable [MeasurableSpace Q] [MeasurableSingletonClass Q]

/-- The numerical finite-chain survival recurrence is exactly the measure of
the avoiding event under the constructed law. -/
theorem absorbedLaw_survival (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (n : ℕ) (s : Q) :
    (absorbedLaw P goal n s).toMeasure {t | ¬ goal t} = ENNReal.ofReal (survive P goal n s) := by
  have hset : MeasurableSet {t : Q | ¬ goal t} := (Set.toFinite _).measurableSet
  induction n generalizing s with
  | zero =>
      simp only [absorbedLaw,survive]
      rw [PMF.toMeasure_pure]
      by_cases hs : goal s <;> simp [hs,Measure.dirac_apply' _ hset]
  | succ n ih =>
      by_cases hs : goal s
      · simp only [absorbedLaw,if_pos hs,survive]
        rw [PMF.toMeasure_pure]
        simp [hs,Measure.dirac_apply' _ hset]
      · simp only [absorbedLaw,if_neg hs,survive]
        rw [PMF.toMeasure_bind_apply _ _ _ hset,tsum_fintype]
        simp_rw [rowPMF_apply,ih,← ENNReal.ofReal_mul (P.nonneg s _)]
        symm
        apply ENNReal.ofReal_sum_of_nonneg
        intro t _
        exact mul_nonneg (P.nonneg s t) (survive_nonneg P goal n t)

/-- Actual finite-horizon probability bound, derived from positive graph paths
and minimum positive transition probabilities. -/
theorem absorbedLaw_geometric_survival (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ s t, 0 < P.row s t → p ≤ P.row s t)
    (D : ℕ) (hpaths : ∀ s, ∃ t n, goal t ∧ n ≤ D ∧ Path (fun u v => 0 < P.row u v) s t n)
    (k : ℕ) (s : Q) :
    (absorbedLaw P goal (k*D) s).toMeasure {t | ¬ goal t} ≤ ENNReal.ofReal ((1-p^D)^k) := by
  rw [absorbedLaw_survival]
  exact ENNReal.ofReal_le_ofReal (geometric_survival_bound P goal p hp hp1 hmin D hpaths k s)

end HiddenParity.Cost.FiniteChainHitting
