import IntegratedBinaryRestoration
import ProductObservationLaw

noncomputable section
open MeasureTheory ProbabilityTheory Filter Set
open scoped Topology BigOperators ENNReal

namespace Orthemology.Tranche2.IntegratedBinary

/-- An explicitly normalised observation mass, coupled by specification to the
hidden score parameter. This is a supplied model, not a derivation of authority. -/
def coin (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ : Bool) : PMF Bool :=
  PMF.ofFintype (fun y => ENNReal.ofReal (law e θ false y)) (by
    rw [Fintype.sum_bool]
    rw [← ENNReal.ofReal_add (law_positive e he0 he1 θ false true).le
      (law_positive e he0 he1 θ false false).le]
    simp [law])

def coinMeasure (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ : Bool) : Measure Bool :=
  (coin e he0 he1 θ).toMeasure

instance coin_probability (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ : Bool) :
    IsProbabilityMeasure (coinMeasure e he0 he1 θ) := by
  unfold coinMeasure
  infer_instance

lemma coinMeasure_real (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ y : Bool) :
    (coinMeasure e he0 he1 θ).real {y} = law e θ false y := by
  unfold Measure.real coinMeasure
  rw [PMF.toMeasure_apply_singleton _ y (measurableSet_singleton y)]
  change (ENNReal.ofReal (law e θ false y)).toReal = _
  exact ENNReal.toReal_ofReal (law_positive e he0 he1 θ false y).le

abbrev Experiment := (Bool × ℕ) → Bool

def experimentLaw (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ : Bool) : Measure Experiment :=
  Measure.infinitePi (fun _ : Bool × ℕ => coinMeasure e he0 he1 θ)

instance experiment_probability (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ : Bool) :
    IsProbabilityMeasure (experimentLaw e he0 he1 θ) := by
  unfold experimentLaw
  infer_instance

def observation (a : Bool) (n : ℕ) (ω : Experiment) : Bool := ω (a,n)

def selectedRepair (e : ℝ) (initial : Bool) (ω : Experiment) (n : ℕ) : ℝ :=
  repair e (canonicalSelected (law e) support observation initial ω n)

/-- End-to-end positive crosswalk: actual product observation laws, literal
binary score targets, one causal shared controller, and eventual good actions.
No independence, identical-law, maximisation or target-labelling oracle is assumed
in this final theorem. The selected controller does not receive the true θ. -/
theorem generated_experiment_eventually_repairs
    (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ initial : Bool) :
    ∀ᵐ ω ∂experimentLaw e he0 he1 θ, ∀ᶠ n : ℕ in atTop,
      BinaryGood (alpha e θ) e (selectedRepair e initial ω n) := by
  apply canonical_repairs_eventually_good (experimentLaw e he0 he1 θ)
    e he0 he1 θ initial observation
  · intro a n
    exact measurable_pi_apply (a,n)
  · exact infinite_product_coordinates_independent
      (fun _ : Bool × ℕ => coinMeasure e he0 he1 θ)
  · intro a n
    constructor
    · exact (measurable_pi_apply (a,n)).aemeasurable
    · exact (measurable_pi_apply (a,0)).aemeasurable
    · rw [show observation a n = fun ω : Experiment => ω (a,n) from rfl,
        show observation a 0 = fun ω : Experiment => ω (a,0) from rfl,
        experimentLaw, infinite_product_coordinate_law, infinite_product_coordinate_law]
  · intro a y
    rw [show observation a 0 = fun ω : Experiment => ω (a,0) from rfl,
      experimentLaw,infinite_product_coordinate_law]
    exact coinMeasure_real e he0 he1 θ y

end Orthemology.Tranche2.IntegratedBinary

#print axioms Orthemology.Tranche2.IntegratedBinary.generated_experiment_eventually_repairs
#check Orthemology.Tranche2.IntegratedBinary.generated_experiment_eventually_repairs
