import ContinuumAuditRestoration

open scoped BigOperators
open Orthemology.Tranche2
namespace Orthemology.Tranche3
noncomputable section

def centeredTotal (n : ℕ) (a : ℝ) (w : Bits n) : ℝ :=
  (rationalCount n w:ℝ)-n*a

def centeredMoment (n k : ℕ) (a : ℝ) : ℝ :=
  coinExpectation n a (fun w => centeredTotal n a w ^ k)

lemma expectation_add (n : ℕ) (a : ℝ) (f g : Bits n → ℝ) :
    coinExpectation n a (fun w => f w+g w)=coinExpectation n a f+coinExpectation n a g := by
  simp [coinExpectation,mul_add,Finset.sum_add_distrib]
lemma expectation_mul (n : ℕ) (a c : ℝ) (f : Bits n → ℝ) :
    coinExpectation n a (fun w => c*f w)=c*coinExpectation n a f := by
  simp only [coinExpectation,Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro w _
  ring
lemma expectation_const (n : ℕ) (a c : ℝ) : coinExpectation n a (fun _ => c)=c := by
  simp [coinExpectation,←Finset.sum_mul,bernoulliMass_sum]

lemma centeredTotal_step (n : ℕ) (a : ℝ) (b : Bool) (w : Bits n) :
    centeredTotal (n+1) a (b,w)=centeredTotal n a w+(if b then 1 else 0)-a := by
  cases b <;> simp [centeredTotal,rationalCount] <;> ring

lemma centeredMoment_step (n k : ℕ) (a : ℝ) :
    centeredMoment (n+1) k a = coinExpectation n a (fun w =>
      (1-a)*(centeredTotal n a w-a)^k+a*(centeredTotal n a w+1-a)^k) := by
  rw [centeredMoment,coinExpectation_step]
  simp_rw [centeredTotal_step]
  simp only [Bool.false_eq_true,if_false,if_true,add_zero]
  rw [expectation_add,expectation_mul,expectation_mul]

lemma centeredMoment_one_step (n : ℕ) (a : ℝ) :
    centeredMoment (n+1) 1 a=centeredMoment n 1 a := by
  rw [centeredMoment_step]
  congr 1
  funext w
  ring

lemma centeredMoment_two_step (n : ℕ) (a : ℝ) :
    centeredMoment (n+1) 2 a=centeredMoment n 2 a+a*(1-a) := by
  rw [centeredMoment_step]
  have hh : (fun w => (1-a)*(centeredTotal n a w-a)^2+a*(centeredTotal n a w+1-a)^2)=
      (fun w => centeredTotal n a w^2+a*(1-a)) := by funext w; ring
  rw [hh,expectation_add,expectation_const]
  rfl

lemma centeredMoment_four_step (n : ℕ) (a : ℝ) :
    centeredMoment (n+1) 4 a=centeredMoment n 4 a+
      6*a*(1-a)*centeredMoment n 2 a+
      4*a*(1-a)*(1-2*a)*centeredMoment n 1 a+a*(1-a)*(1-3*a*(1-a)) := by
  rw [centeredMoment_step]
  have hh : (fun w => (1-a)*(centeredTotal n a w-a)^4+a*(centeredTotal n a w+1-a)^4)=
      (fun w => centeredTotal n a w^4+6*a*(1-a)*centeredTotal n a w^2+
        4*a*(1-a)*(1-2*a)*centeredTotal n a w^1+a*(1-a)*(1-3*a*(1-a))) := by
    funext w; ring
  rw [hh]
  simp only [expectation_add,expectation_mul,expectation_const,centeredMoment]

/-- Exact moments under the actual finite Bernoulli prefix masses. No
concentration or independence assumption is added to those masses. -/
theorem centered_moments (n : ℕ) (a : ℝ) :
    centeredMoment n 1 a=0 ∧ centeredMoment n 2 a=n*a*(1-a) ∧
      centeredMoment n 4 a=n*a*(1-a)*(1-3*a*(1-a))+
        3*(n:ℝ)*((n:ℝ)-1)*(a*(1-a))^2 := by
  induction n with
  | zero => simp [centeredMoment,coinExpectation,centeredTotal,rationalCount,bernoulliMass]
  | succ n ih =>
    rw [centeredMoment_one_step,centeredMoment_two_step,centeredMoment_four_step,
      ih.1,ih.2.1,ih.2.2]
    push_cast
    constructor
    · rfl
    constructor <;> ring

/-- A deliberately coarse bound suffices for a summable error budget. -/
theorem centered_fourth_le (n : ℕ) (hn : 1≤n) (a : ℝ) (ha0 : 0≤a) (ha1 : a≤1) :
    centeredMoment n 4 a ≤ 4*(n:ℝ)^2 := by
  rw [(centered_moments n a).2.2]
  have hv0 : 0≤a*(1-a) := mul_nonneg ha0 (by linarith)
  have hv1 : a*(1-a)≤1 := by nlinarith [sq_nonneg a]
  have hm : a*(1-a)*(1-3*a*(1-a))≤1 := by nlinarith [sq_nonneg (a*(1-a))]
  have hv2 : (a*(1-a))^2≤1 := by nlinarith
  have hn1 : (1:ℝ)≤n := by exact_mod_cast hn
  have hfirst := mul_le_mul_of_nonneg_left hm (by positivity : (0:ℝ)≤n)
  have hnminus : 0≤(n:ℝ)-1 := by linarith
  have hsecond := mul_le_mul_of_nonneg_left hv2
    (by positivity : (0:ℝ)≤3*(n:ℝ)*((n:ℝ)-1))
  nlinarith


end
end Orthemology.Tranche3
#print axioms Orthemology.Tranche3.centered_moments

#print axioms Orthemology.Tranche3.centered_fourth_le
