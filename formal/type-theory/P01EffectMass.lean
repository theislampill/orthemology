/- Exact quantitative laws for the shared finite-seed evaluator. -/
import P01FiniteCoupling
import Mathlib.Tactic.Ring
namespace P01R
open OrthemologyV2 OrthemologyV3 P01D P01Probability
open scoped BigOperators

theorem seed_weight_app (f x : EExpr) (sf : Seed f) (sx : Seed x) :
    seedWeight (.app f x) (sf,sx) = seedWeight f sf * seedWeight x sx := by
  simp only [seedWeight,Seed,Fintype.card_prod,Nat.cast_mul,one_div_mul_one_div]

theorem seed_weight_mix (p : Weight) (l r : EExpr) (i : Fin p.den) (sl : Seed l) (sr : Seed r) :
    seedWeight (.mix p l r) (i,sl,sr) =
      (1 / (p.den : ℚ)) * seedWeight l sl * seedWeight r sr := by
  simp only [seedWeight,Seed,Fintype.card_prod,Fintype.card_fin,Nat.cast_mul,one_div_mul_one_div]
  rw [mul_assoc]

theorem output_mass_pure (p : Poly) (θ : P01D.Env) (t : Term) :
    outputMass (.pure p) θ t = if eval p θ = t then 1 else 0 := by
  simp [outputMass,pushMass,run,Seed,seedWeight]

/-- Application samples its two syntactic children independently. -/
theorem output_mass_application (f x : EExpr) (θ : P01D.Env) (t : Term) :
    outputMass (.app f x) θ t =
      ∑ sf : Seed f, ∑ sx : Seed x,
        if Term.app (run f θ sf) (run x θ sx) = t then seedWeight f sf * seedWeight x sx else 0 := by
  change (∑s : Seed f × Seed x, if run (.app f x) θ s = t then seedWeight (.app f x) s else 0) = _
  rw [Fintype.sum_prod_type]
  apply Finset.sum_congr rfl
  intro sf hf
  apply Finset.sum_congr rfl
  intro sx hx
  simp only [run,seed_weight_app]

theorem coin_left_count (p : Weight) :
    (Finset.univ.filter (fun i : Fin p.den => i.val < p.num)).card = p.num := by
  let e : {i : Fin p.den // i.val < p.num} ≃ Fin p.num :=
    { toFun := fun i => ⟨i.val.val,i.property⟩
      invFun := fun i => ⟨⟨i.val,Nat.lt_of_lt_of_le i.isLt p.bounded⟩,i.isLt⟩
      left_inv := by intro i; apply Subtype.ext; rfl
      right_inv := by intro i; rfl }
  rw [← Fintype.card_subtype]
  exact (Fintype.card_congr e).trans (Fintype.card_fin p.num)

theorem coin_right_count (p : Weight) :
    (Finset.univ.filter (fun i : Fin p.den => ¬ i.val < p.num)).card = p.den - p.num := by
  have h := Finset.filter_card_add_filter_neg_card_eq_card
    (s := (Finset.univ : Finset (Fin p.den))) (fun i => i.val < p.num)
  rw [coin_left_count,Finset.card_univ,Fintype.card_fin] at h
  omega

theorem coin_sum (p : Weight) (a b : ℚ) :
    (∑i : Fin p.den, if i.val < p.num then a else b) =
      (p.num : ℚ) * a + ((p.den - p.num : Nat) : ℚ) * b := by
  rw [Finset.sum_ite]
  simp only [Finset.sum_const,coin_left_count,coin_right_count,nsmul_eq_mul]

/-- Unused branch coordinates integrate to one; they do not change mixture mass. -/
theorem output_mass_mixture_seed (p : Weight) (l r : EExpr) (θ : P01D.Env) (t : Term) :
    outputMass (.mix p l r) θ t =
      ∑i : Fin p.den, if i.val < p.num
        then (1 / (p.den : ℚ)) * outputMass l θ t
        else (1 / (p.den : ℚ)) * outputMass r θ t := by
  change (∑s : Fin p.den × Seed l × Seed r,
    if run (.mix p l r) θ s = t then seedWeight (.mix p l r) s else 0) = _
  rw [Fintype.sum_prod_type]
  apply Finset.sum_congr rfl
  intro i hi
  rw [Fintype.sum_prod_type]
  by_cases h : i.val < p.num
  · simp only [run,if_pos h,seed_weight_mix,outputMass,pushMass]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro sl hl
    by_cases ht : run l θ sl = t
    · simp only [ht,if_true]
      rw [← Finset.mul_sum,seed_weight_total,mul_one]
    · simp only [ht,if_false,Finset.sum_const_zero,mul_zero]
  · simp only [run,if_neg h,seed_weight_mix,outputMass,pushMass]
    rw [Finset.sum_comm,Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro sr hr
    by_cases ht : run r θ sr = t
    · simp only [ht,if_true]
      simp_rw [mul_assoc, mul_comm (seedWeight l _) (seedWeight r sr), ← mul_assoc]
      rw [← Finset.mul_sum,seed_weight_total,mul_one]
    · simp only [ht,if_false,Finset.sum_const_zero,mul_zero]

/-- The exact rational weight in the unchanged Weight record is respected. -/
theorem output_mass_mixture (p : Weight) (l r : EExpr) (θ : P01D.Env) (t : Term) :
    outputMass (.mix p l r) θ t =
      ((p.num : ℚ) / (p.den : ℚ)) * outputMass l θ t +
      (((p.den - p.num : Nat) : ℚ) / (p.den : ℚ)) * outputMass r θ t := by
  rw [output_mass_mixture_seed,coin_sum]
  ring

end P01R
