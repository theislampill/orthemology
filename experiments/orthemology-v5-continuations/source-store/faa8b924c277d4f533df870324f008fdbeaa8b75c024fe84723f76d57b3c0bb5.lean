import CanonicalBlockPolicy
import BlindGuessSharpness
import Mathlib.Probability.ProductMeasure

noncomputable section
open MeasureTheory ProbabilityTheory Filter Set
open scoped Topology BigOperators ENNReal

namespace Orthemology.Tranche2.IntegratedBinary

def alpha (e : ℝ) (θ : Bool) : ℝ := if θ then 1/2+e else 1/2-e
def repair (e : ℝ) (a : Bool) : ℝ := 1/2 + alpha e a * e
def law (e : ℝ) (θ _a y : Bool) : ℝ := if y then alpha e θ else 1-alpha e θ
def support (θ : Bool) : Finset Bool := {θ}

def good (e : ℝ) (θ : Bool) : Finset Bool := by
  classical
  exact Finset.univ.filter (fun a => BinaryGood (alpha e θ) e (repair e a))

lemma alpha_bounds (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ : Bool) :
    0 < alpha e θ ∧ alpha e θ < 1 := by
  cases θ <;> simp [alpha] <;> constructor <;> linarith

lemma exact_action_good (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ : Bool) :
    BinaryGood (alpha e θ) e (repair e θ) :=
  exact_parameter_repair _ _ (alpha_bounds e he0 he1 θ).1.le
    (alpha_bounds e he0 he1 θ).2.le

/-- The target labels are derived from actual score inequalities, not supplied
as a hand-labelled diagonal relation. -/
lemma good_iff_same (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ a : Bool) :
    BinaryGood (alpha e θ) e (repair e a) ↔ a = θ := by
  constructor
  · intro hg
    by_contra hne
    have own := exact_action_good e he0 he1 a
    cases θ <;> cases a
    · exact hne rfl
    · exact binary_symmetric_success_disjoint e (repair e true) he0 he1 ⟨hg,own⟩
    · exact binary_symmetric_success_disjoint e (repair e false) he0 he1 ⟨own,hg⟩
    · exact hne rfl
  · intro h
    subst a
    exact exact_action_good e he0 he1 θ

lemma good_eq_support (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ : Bool) :
    good e θ = support θ := by
  ext a
  simp [good,support,good_iff_same e he0 he1]

lemma law_positive (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) :
    ∀ θ a y, 0 < law e θ a y := by
  intro θ a y
  have h := alpha_bounds e he0 he1 θ
  cases y <;> simp [law] <;> linarith

lemma law_normalised (e : ℝ) (θ a : Bool) : ∑ y, law e θ a y = 1 := by
  simp [law, Fintype.sum_bool]

lemma law_identifies (e : ℝ) (he : 0 < e) (θ σ a : Bool)
    (h : law e θ a = law e σ a) : θ = σ := by
  have hh := congrFun h true
  cases θ <;> cases σ <;> simp_all [law,alpha] <;> linarith

lemma supports_self_verifying (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) :
    ∀ θ, SelfVerifying (good e) (fun η ζ a => law e η a = law e ζ a)
      θ (support θ) := by
  intro θ
  constructor
  · rw [good_eq_support e he0 he1 θ]
  · intro σ h
    have heq := law_identifies e he0 θ σ θ (h θ (by simp [support]))
    subst σ
    rw [good_eq_support e he0 he1 θ]

/-- A single explicit history-based controller eventually satisfies the actual
binary repair inequalities, under the declared fresh observation contract.
Singleton blocks mean each block is exactly one physical repair action. -/
theorem canonical_repairs_eventually_good
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ initial : Bool)
    (X : Bool → ℕ → Ω → Bool)
    (hX : ∀ a n, Measurable (X a n))
    (hindep : iIndepFun (fun an : Bool × ℕ => X an.1 an.2) μ)
    (hident : ∀ a n, IdentDistrib (X a n) (X a 0) μ μ)
    (hLaw : ∀ a y, (Measure.map (X a 0) μ).real {y} = law e θ a y) :
    ∀ᵐ ω ∂μ, ∀ᶠ n : ℕ in atTop,
      BinaryGood (alpha e θ) e
        (repair e (canonicalSelected (law e) support X initial ω n)) := by
  have h := canonical_block_policy_eventually_good (law e) (good e) support θ initial X
    (law_positive e he0 he1) (law_normalised e)
    (fun σ => by simp [support]) (supports_self_verifying e he0 he1)
    hX hindep hident hLaw
  filter_upwards [h] with ω hω
  apply hω.mono
  intro n hn
  have hg := hn.2 (show canonicalSelected (law e) support X initial ω n ∈
      support (canonicalSelected (law e) support X initial ω n) by simp [support])
  simpa [good] using hg

end Orthemology.Tranche2.IntegratedBinary

#print axioms Orthemology.Tranche2.IntegratedBinary.good_iff_same
#print axioms Orthemology.Tranche2.IntegratedBinary.canonical_repairs_eventually_good
