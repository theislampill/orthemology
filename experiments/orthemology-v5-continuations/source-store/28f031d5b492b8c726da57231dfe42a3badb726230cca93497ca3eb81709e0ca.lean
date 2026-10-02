import EmpiricalTailBounds
import FiniteWordDeviation

noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Exponential
open HiddenParity.Empirical CentredBernoulli BernoulliWord
universe u v
variable {A Y : Type u} {R : Type v}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

def symbolWord (a : A) (y : Y) (n : ℕ) (z : R × FlatStack A Y) : Fin n → Bool := by
  classical
  exact fun i => decide (seededStackCoordinate a i.val z = y)

lemma symbolWord_measurable (a : A) (y : Y) (n : ℕ) :
    Measurable (symbolWord (R := R) a y n) := by
  classical
  apply measurable_pi_lambda
  intro i
  exact (measurable_of_finite (fun t : Y => decide (t=y))).comp
    (seededStackCoordinate_measurable a i.val)

lemma row_probability_le_one (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (a : A) (y : Y) : P a y ≤ 1 := by
  rw [← hN a]
  exact Finset.single_le_sum (fun t _ => hP a t) (Finset.mem_univ y)

lemma symbolWord_probability
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (a : A) (y : Y) (n : ℕ) (w : Fin n → Bool) :
    (ρ.prod (stackMeasure P hP hN)) (symbolWord a y n ⁻¹' {w}) = weight n (P a y) w := by
  classical
  let sets : Fin n → Set Y := fun i => if w i then {y} else {y}ᶜ
  have hs : ∀ i, MeasurableSet (sets i) := by
    intro i
    dsimp [sets]
    split
    · exact measurableSet_singleton y
    · exact (measurableSet_singleton y).compl
  have hi : iIndepFun (fun i : Fin n => seededStackCoordinate (R := R) (Y := Y) a i.val)
      (ρ.prod (stackMeasure P hP hN)) := by
    exact (seededStackCoordinates_independent ρ P hP hN).precomp
      (show Function.Injective (fun i : Fin n => (a,i.val)) from by
        intro i j h
        exact Fin.ext (congrArg Prod.snd h))
  have he : (symbolWord (R := R) a y n ⁻¹' {w}) =
      ⋂ i : Fin n, seededStackCoordinate a i.val ⁻¹' sets i := by
    ext z
    simp only [Set.mem_preimage, Set.mem_singleton_iff, Set.mem_iInter]
    rw [funext_iff]
    apply forall_congr'
    intro i
    cases hw : w i <;> simp [symbolWord,sets,hw]
  rw [he]
  have hind := hi.measure_inter_preimage_eq_mul Finset.univ (sets := sets) (fun i _ => hs i)
  simp only [Finset.mem_univ, iInter_true] at hind
  rw [hind,weight_prod n (hP a y) (row_probability_le_one P hP hN a y)]
  apply Finset.prod_congr rfl
  intro i _
  have hm : MeasurableSet (seededStackCoordinate (R := R) (Y := Y) a i.val ⁻¹' {y}) :=
    (measurableSet_singleton y).preimage (seededStackCoordinate_measurable a i.val)
  have hp : (ρ.prod (stackMeasure P hP hN))
      (seededStackCoordinate a i.val ⁻¹' {y}) = ENNReal.ofReal (P a y) := by
    rw [← Measure.map_apply (seededStackCoordinate_measurable a i.val) (measurableSet_singleton y),
      seededStackCoordinate_law ρ P hP hN,actionMeasure_singleton]
  cases hw : w i
  · dsimp [sets]
    simp only [hw,Bool.false_eq_true,ite_false,Set.preimage_compl]
    rw [measure_compl hm (measure_ne_top _ _),hp,measure_univ]
    rw [ENNReal.ofReal_sub 1 (hP a y)]
    norm_num
  · simpa [sets,hw] using hp

lemma symbolWord_law
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (a : A) (y : Y) (n : ℕ) :
    (ρ.prod (stackMeasure P hP hN)).map (symbolWord a y n) =
      (distribution n (P a y) (hP a y) (row_probability_le_one P hP hN a y)).toMeasure := by
  apply Measure.ext_of_singleton
  intro w
  rw [Measure.map_apply (symbolWord_measurable a y n) (measurableSet_singleton w),
    symbolWord_probability,PMF.toMeasure_apply_singleton _ _ (measurableSet_singleton w)]
  rfl

#print axioms symbolWord_law
end HiddenParity.Exponential
