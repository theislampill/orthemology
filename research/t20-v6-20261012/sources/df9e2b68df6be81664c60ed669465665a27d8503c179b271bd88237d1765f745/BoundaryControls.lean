import EventualCausalRestoration
import BinaryConstructiveRepair

open MeasureTheory Set Filter
open scoped Topology
namespace CausalQueryAudit
open Orthemology.Tranche2 Orthemology.Tranche2.FiniteQuery

-- The exact center succeeds even at endpoint norms, with weak improvement.
theorem exact_center_good (a e : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) :
    BinaryGood a e (1/2+a*e) := by
  have h := mul_nonneg (mul_nonneg ha0 (sub_nonneg.mpr ha1)) (sq_nonneg e)
  constructor <;> dsimp [BinaryGood] <;> nlinarith

theorem zero_disturbance_all_norms (a : ℝ) : BinaryGood a 0 (1/2) := by
  constructor <;> dsimp [BinaryGood] <;> nlinarith

theorem fixed_disturbance_interval (a : ℝ) (ha : 1/4 ≤ a) (hb : a ≤ 5/16) :
    BinaryGood a (1/4) (9/16) := by
  constructor <;> dsimp [BinaryGood] <;> nlinarith

theorem decoder_necessary_not_sufficient :
    |((21/32 : ℝ)-1/2)/(1/4)-1/2| ≤ (1/4)/2 ∧
    ¬ BinaryGood (1/2) (1/4) (21/32) := by norm_num [BinaryGood, abs_of_pos (by norm_num : (0:ℝ)<1/8)]

theorem endpoint_zero_no_strict (q : ℝ) :
    ¬ (q^2 < (1/2:ℝ)^2 ∧ (1-q)^2 < (1/2:ℝ)^2) := by
  rintro ⟨h0,h1⟩
  nlinarith [sq_nonneg (q-1/2)]

theorem endpoint_one_no_strict (e q : ℝ) (he0 : 0 ≤ e) (he1 : e ≤ 1/4) :
    ¬ (q^2 < (1/2+e)^2 ∧ (1-q)^2 < (1/2-e)^2) := by
  rintro ⟨h0,h1⟩
  have hleft := mul_pos (by linarith : 0 < (1/2:ℝ)-e) (sub_pos.mpr h0)
  have hright := mul_pos (by linarith : 0 < (1/2:ℝ)+e) (sub_pos.mpr h1)
  nlinarith [sq_nonneg (q-(1/2+e))]

theorem outside_probability_domain_strict_endpoint :
    (1:ℝ)^2 < (1/2+1)^2 ∧ (1-1:ℝ)^2 < (1/2-1)^2 := by norm_num

-- No-probe is an actual information boundary: the oracle is absent from the update.
theorem never_ask_run {S : Type*} (next : S → Bool → S)
    (o : Oracle) (s : S) (n : ℕ) :
    (run (fun _ => false) next o s n).2 = 0 := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [run,advance] using ih

theorem never_ask_oracle_independence {S : Type*} (next : S → Bool → S)
    (o p : Oracle) (s : S) :
    run (fun _ => false) next o s = run (fun _ => false) next p s := by
  apply funext
  exact bounded_prefix_locality _ _ o p s 0 (by omega)
    (fun n => (never_ask_run next o s n).le)

theorem zero_prefix_locality {S : Type*} (ask : S → Bool) (next : S → Bool → S)
    (o p : Oracle) (s : S) (hb : Bounded ask next o s 0) :
    run ask next o s = run ask next p s :=
  funext (bounded_prefix_locality ask next o p s 0 (by omega) hb)

theorem raw_oracles_differ_but_observed_traces_equal :
    (fun _ : ℕ => false) ≠ (fun _ : ℕ => true) ∧
    run (fun _ : Unit => false) (fun s _ => s) (fun _ => false) () =
      run (fun _ : Unit => false) (fun s _ => s) (fun _ => true) () := by
  constructor
  · intro h
    have := congrFun h 0
    contradiction
  · exact never_ask_oracle_independence _ _ _ _

def onceAsk : Option Bool → Bool | none => true | some _ => false
def onceNext (s : Option Bool) (b : Bool) : Option Bool :=
  match s with | none => some b | some v => some v

theorem one_query_run (o : Oracle) :
    ∀ n, run onceAsk onceNext o none (n+1) = (some (o 0),1) := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih => rw [run,ih]; rfl

theorem one_query_bounded (o : Oracle) : Bounded onceAsk onceNext o none 1 := by
  intro n
  cases n with
  | zero => simp [run]
  | succ n => simp [one_query_run]

theorem first_queried_bit_matters :
    run onceAsk onceNext (fun _ => false) none 1 ≠
      run onceAsk onceNext (fun _ => true) none 1 := by decide

theorem always_ask_count {S : Type*} (next : S → Bool → S)
    (o : Oracle) (s : S) (n : ℕ) :
    (run (fun _ => true) next o s n).2 = n := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [run,advance] using congrArg Nat.succ ih

theorem always_ask_not_bounded (o : Oracle) :
    ¬ ∃ N, Bounded (fun _ : Unit => true) (fun s _ => s) o () N := by
  rintro ⟨N,hN⟩
  have := hN (N+1)
  simp only [always_ask_count] at this
  omega

-- An alpha-coded initial state can repair every norm without any queries.
-- This is exactly why its distribution may not vary arbitrarily with alpha.
theorem parameter_coded_seed_succeeds (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (e : ℕ → ℝ) (o : Oracle) :
    ∀ᶠ n in atTop,
      (fun _ : ℝ => false) (run (fun _ => false) (fun s _ => s) o a n).1 = false ∧
      BinaryGood a (e n) (1/2+(run (fun _ => false) (fun s _ => s) o a n).1*e n) := by
  have hr : ∀ n, run (fun _ : ℝ => false) (fun s _ => s) o a n = (a,0) := by
    intro n
    induction n with
    | zero => rfl
    | succ n ih => simp [run,advance,ih]
  apply Eventually.of_forall
  intro n
  rw [hr]
  exact ⟨rfl, exact_center_good a (e n) ha0 ha1⟩

-- A fixed known norm also succeeds; countability never means failure for every norm.
theorem fixed_norm_no_query_success (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (e : ℕ → ℝ) (o : Oracle) :
    ∀ᶠ n in atTop,
      (fun _ : Unit => false) (run (fun _ => false) (fun s _ => s) o () n).1 = false ∧
      BinaryGood a (e n) (1/2+a*e n) :=
  Eventually.of_forall (fun n => ⟨rfl,exact_center_good a (e n) ha0 ha1⟩)

-- Compile-time type guard: no hdom, no assumed exact decoder and one literal event.
example {S : Type*} [MeasurableSpace S]
    (ask : S → Bool) (next : S → Bool → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b))
    (ρ : Measure S) [IsProbabilityMeasure ρ]
    (inputLaw : ℝ → Measure (S × Oracle)) [∀ a, IsProbabilityMeasure (inputLaw a)]
    (hseed : ∀ a, (inputLaw a).map Prod.fst = ρ)
    (e : ℕ → ℝ) (he0 : ∀ n, 0 < e n) (he1 : ∀ n, e n ≤ 1/4)
    (he : Tendsto e atTop (𝓝 0))
    (score : ℕ → S → ℝ) (hscore : ∀ n, Measurable (score n)) :
    Set.Countable {a : ℝ | a ∈ Icc 0 1 ∧
      0 < inputLaw a {z | ∀ᶠ n in atTop,
        ask (run ask next z.2 z.1 n).1 = false ∧
        BinaryGood a (e n) (score n (run ask next z.2 z.1 n).1)}} :=
  countable_positive_eventual_causal_restoration ask next ha hn ρ inputLaw hseed e he0 he1 he score hscore

end CausalQueryAudit
