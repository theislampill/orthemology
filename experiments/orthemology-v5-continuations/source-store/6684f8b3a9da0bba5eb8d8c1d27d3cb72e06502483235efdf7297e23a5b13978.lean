/- New exact-rational finite pushforwards and common couplings for fixed seeds.
   No quantifier exchange, external probability oracle, or unrestricted bind. -/
import P01EffectSeeds
import Mathlib.Algebra.Order.Field.Rat
import Mathlib.Algebra.BigOperators.Field
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Fintype.BigOperators
namespace P01Probability
open scoped BigOperators

universe u v w

def support {Ω : Type u} {X : Type v} [Fintype Ω] [DecidableEq X] (f : Ω → X) : Finset X :=
  Finset.univ.image f

def pushMass {Ω : Type u} {X : Type v} [Fintype Ω] [DecidableEq X]
    (weight : Ω → ℚ) (f : Ω → X) (x : X) : ℚ :=
  ∑ s, if f s = x then weight s else 0

def jointMass {Ω : Type u} {X : Type v} {Y : Type w}
    [Fintype Ω] [DecidableEq X] [DecidableEq Y]
    (weight : Ω → ℚ) (f : Ω → X) (g : Ω → Y) (x : X) (y : Y) : ℚ :=
  ∑ s, if f s = x ∧ g s = y then weight s else 0

theorem support_mem {Ω : Type u} {X : Type v} [Fintype Ω] [DecidableEq X]
    (f : Ω → X) (s : Ω) : f s ∈ support f :=
  Finset.mem_image.mpr ⟨s,Finset.mem_univ s,rfl⟩

theorem push_nonnegative {Ω : Type u} {X : Type v} [Fintype Ω] [DecidableEq X]
    (weight : Ω → ℚ) (hw : ∀s, 0 ≤ weight s) (f : Ω → X) (x : X) :
    0 ≤ pushMass weight f x := by
  apply Finset.sum_nonneg
  intro s hs
  by_cases h : f s = x <;> simp only [h,if_true,if_false] <;> first | exact hw s | exact le_rfl

theorem joint_nonnegative {Ω : Type u} {X : Type v} {Y : Type w}
    [Fintype Ω] [DecidableEq X] [DecidableEq Y]
    (weight : Ω → ℚ) (hw : ∀s, 0 ≤ weight s) (f : Ω → X) (g : Ω → Y) (x : X) (y : Y) :
    0 ≤ jointMass weight f g x y := by
  apply Finset.sum_nonneg
  intro s hs
  by_cases h : f s = x ∧ g s = y <;> simp only [h,if_true,if_false] <;>
    first | exact hw s | exact le_rfl

theorem push_total {Ω : Type u} {X : Type v} [Fintype Ω] [DecidableEq X]
    (weight : Ω → ℚ) (f : Ω → X) :
    ∑ x ∈ support f, pushMass weight f x = ∑s, weight s := by
  unfold pushMass
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro s hs
  rw [Finset.sum_ite_eq]
  simp only [support_mem,if_true]

theorem joint_left_marginal {Ω : Type u} {X : Type v} {Y : Type w}
    [Fintype Ω] [DecidableEq X] [DecidableEq Y]
    (weight : Ω → ℚ) (f : Ω → X) (g : Ω → Y) (x : X) :
    ∑ y ∈ support g, jointMass weight f g x y = pushMass weight f x := by
  unfold jointMass pushMass
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro s hs
  by_cases h : f s = x
  · simp only [h,true_and,if_true,Finset.sum_ite_eq,support_mem]
  · simp only [h,false_and,if_false,Finset.sum_const_zero]

theorem joint_right_marginal {Ω : Type u} {X : Type v} {Y : Type w}
    [Fintype Ω] [DecidableEq X] [DecidableEq Y]
    (weight : Ω → ℚ) (f : Ω → X) (g : Ω → Y) (y : Y) :
    ∑ x ∈ support f, jointMass weight f g x y = pushMass weight g y := by
  unfold jointMass pushMass
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro s hs
  by_cases h : g s = y
  · simp only [h,and_true,if_true,Finset.sum_ite_eq,support_mem]
  · simp only [h,and_false,if_false,Finset.sum_const_zero]

theorem joint_positive_has_seed {Ω : Type u} {X : Type v} {Y : Type w}
    [Fintype Ω] [DecidableEq X] [DecidableEq Y]
    (weight : Ω → ℚ) (f : Ω → X) (g : Ω → Y) {x y}
    (h : 0 < jointMass weight f g x y) : ∃s, f s = x ∧ g s = y := by
  by_contra hn
  have hz : jointMass weight f g x y = 0 := by
    apply Finset.sum_eq_zero
    intro s hs
    have hnot : ¬ (f s = x ∧ g s = y) := fun q => hn ⟨s,q⟩
    exact if_neg hnot
  rw [hz] at h
  exact (lt_irrefl 0) h

theorem joint_zero_off_support {Ω : Type u} {X : Type v} {Y : Type w}
    [Fintype Ω] [DecidableEq X] [DecidableEq Y]
    (weight : Ω → ℚ) (f : Ω → X) (g : Ω → Y) (x : X) (y : Y)
    (ho : x ∉ support f ∨ y ∉ support g) : jointMass weight f g x y = 0 := by
  apply Finset.sum_eq_zero
  intro s hs
  apply if_neg
  intro h
  rcases ho with hx | hy
  · exact hx (h.1 ▸ support_mem f s)
  · exact hy (h.2 ▸ support_mem g s)

theorem push_positive_iff {Ω : Type u} {X : Type v} [Fintype Ω] [DecidableEq X]
    (weight : Ω → ℚ) (hw : ∀s, 0 < weight s) (f : Ω → X) (x : X) :
    0 < pushMass weight f x ↔ ∃s, f s = x := by
  constructor
  · intro h
    by_contra hn
    have hz : pushMass weight f x = 0 := by
      apply Finset.sum_eq_zero
      intro s hs
      exact if_neg (fun q => hn ⟨s,q⟩)
    rw [hz] at h
    exact (lt_irrefl 0) h
  · rintro ⟨s,hs⟩
    apply Finset.sum_pos'
    · intro z hz
      by_cases h : f z = x <;> simp only [h,if_true,if_false] <;>
        first | exact le_of_lt (hw z) | exact le_rfl
    · exact ⟨s,Finset.mem_univ s,by simpa only [hs,if_true] using hw s⟩

theorem observations_same_law {Ω : Type u} {X : Type v} {Y : Type w} {O : Type*}
    [Fintype Ω] [DecidableEq O]
    (weight : Ω → ℚ) (f : Ω → X) (g : Ω → Y) (leftObs : X → O) (rightObs : Y → O)
    (h : ∀s, leftObs (f s) = rightObs (g s)) :
    ∀o, pushMass weight (leftObs ∘ f) o = pushMass weight (rightObs ∘ g) o := by
  intro o
  apply Finset.sum_congr rfl
  intro s hs
  simp only [Function.comp_apply,h s]

end P01Probability

namespace P01R
open OrthemologyV2 OrthemologyV3 P01D
open scoped BigOperators
open P01Probability

def seedWeight (e : EExpr) (_ : Seed e) : ℚ := 1 / (Fintype.card (Seed e) : ℚ)

theorem seed_weight_positive (e : EExpr) (s : Seed e) : 0 < seedWeight e s := by
  apply one_div_pos.mpr
  exact Nat.cast_pos.mpr Fintype.card_pos

theorem seed_weight_total (e : EExpr) : ∑s : Seed e, seedWeight e s = 1 := by
  have hn : (Fintype.card (Seed e) : ℚ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr Fintype.card_pos)
  simp only [seedWeight,Finset.sum_const,Finset.card_univ,nsmul_eq_mul,one_div]
  exact mul_inv_cancel₀ hn

def outputMass (e : EExpr) (θ : P01D.Env) : Term → ℚ := pushMass (seedWeight e) (run e θ)
def outputSupport (e : EExpr) (θ : P01D.Env) : Finset Term := support (run e θ)
def outputCoupling (e : EExpr) (θ η : P01D.Env) : Term → Term → ℚ :=
  jointMass (seedWeight e) (run e θ) (run e η)

theorem output_mass_nonnegative (e : EExpr) (θ : P01D.Env) (t : Term) : 0 ≤ outputMass e θ t :=
  push_nonnegative (seedWeight e) (fun s => le_of_lt (seed_weight_positive e s)) (run e θ) t

theorem output_mass_total (e : EExpr) (θ : P01D.Env) :
    ∑t ∈ outputSupport e θ, outputMass e θ t = 1 := by
  rw [outputSupport,outputMass,push_total]
  exact seed_weight_total e

theorem output_mass_support_exact (e : EExpr) (θ : P01D.Env) (t : Term) :
    0 < outputMass e θ t ↔ Outcome (erase e θ) t :=
  (push_positive_iff (seedWeight e) (seed_weight_positive e) (run e θ) t).trans
    (seed_support_exact e θ t)

/-- Explicit finite rational matrix, exact marginals, and a SINGLE witness before
    quantification over every admissible relation environment. -/
theorem common_coupling {Γ e A} (h : EHas Γ e A) (θ η : P01D.Env) :
    ∃κ : Term → Term → ℚ,
      (∀t u, 0 ≤ κ t u) ∧
      (∀t, ∑u ∈ outputSupport e η, κ t u = outputMass e θ t) ∧
      (∀u, ∑t ∈ outputSupport e θ, κ t u = outputMass e η u) ∧
      (∀t u, t ∉ outputSupport e θ ∨ u ∉ outputSupport e η → κ t u = 0) ∧
      ∀r, ValRelated Γ r θ η → ∀t u, 0 < κ t u → (interpret A).rel r t u := by
  refine ⟨outputCoupling e θ η,?_,?_,?_,?_,?_⟩
  · intro t u
    exact joint_nonnegative (seedWeight e) (fun s => le_of_lt (seed_weight_positive e s)) _ _ t u
  · intro t
    exact joint_left_marginal (seedWeight e) (run e θ) (run e η) t
  · intro u
    exact joint_right_marginal (seedWeight e) (run e θ) (run e η) u
  · intro t u ho
    exact joint_zero_off_support (seedWeight e) (run e θ) (run e η) t u ho
  · intro r hv t u hp
    obtain ⟨s,rfl,rfl⟩ := joint_positive_has_seed (seedWeight e) (run e θ) (run e η) hp
    exact shared_seed_fundamental h r θ η hv s

/-- Any specified relation-respecting observation gives exactly equal observed
    distributions, not merely equal positive support. -/
theorem related_observations_equal {Γ e A} (h : EHas Γ e A) {O : Type*} [DecidableEq O]
    (r : REnv) (θ η : P01D.Env) (hv : ValRelated Γ r θ η) (obs₀ obs₁ : Term → O)
    (ho : ∀t u, (interpret A).rel r t u → obs₀ t = obs₁ u) :
    ∀o, pushMass (seedWeight e) (obs₀ ∘ run e θ) o =
      pushMass (seedWeight e) (obs₁ ∘ run e η) o := by
  apply observations_same_law
  intro s
  exact ho _ _ (shared_seed_fundamental h r θ η hv s)

end P01R

namespace P01R
open OrthemologyV2 OrthemologyV3 P01D
open scoped BigOperators
open P01Probability

/-- At the exact original closed effect grammar, every relational environment
    is admitted; there is no hidden or potentially empty valuation premise. -/
theorem original_common_coupling {e A} (h : EffectDerives e A) (θ η : P01D.Env) :
    ∃κ : Term → Term → ℚ,
      (∀t u, 0 ≤ κ t u) ∧
      (∀t, ∑u ∈ outputSupport (embed e) η, κ t u = outputMass (embed e) θ t) ∧
      (∀u, ∑t ∈ outputSupport (embed e) θ, κ t u = outputMass (embed e) η u) ∧
      (∀t u, t ∉ outputSupport (embed e) θ ∨ u ∉ outputSupport (embed e) η → κ t u = 0) ∧
      ∀r t u, 0 < κ t u → (interpret A).rel r t u := by
  refine ⟨outputCoupling (embed e) θ η,?_,?_,?_,?_,?_⟩
  · intro t u
    exact joint_nonnegative (seedWeight (embed e))
      (fun s => le_of_lt (seed_weight_positive (embed e) s)) _ _ t u
  · intro t
    exact joint_left_marginal (seedWeight (embed e)) (run (embed e) θ) (run (embed e) η) t
  · intro u
    exact joint_right_marginal (seedWeight (embed e)) (run (embed e) θ) (run (embed e) η) u
  · intro t u ho
    exact joint_zero_off_support (seedWeight (embed e)) (run (embed e) θ) (run (embed e) η) t u ho
  · intro r t u hp
    obtain ⟨s,rfl,rfl⟩ := joint_positive_has_seed (seedWeight (embed e))
      (run (embed e) θ) (run (embed e) η) hp
    exact original_seed_relational h θ η s r

theorem original_positive_support {e} (θ : P01D.Env) (t : Term) :
    0 < outputMass (embed e) θ t ↔ Outcome e t := by
  simpa only [erase_embed] using output_mass_support_exact (embed e) θ t

theorem coupling_total (e : EExpr) (θ η : P01D.Env) :
    ∑t ∈ outputSupport e θ, ∑u ∈ outputSupport e η, outputCoupling e θ η t u = 1 := by
  simp only [outputCoupling,outputSupport,joint_left_marginal]
  exact output_mass_total e θ

end P01R
