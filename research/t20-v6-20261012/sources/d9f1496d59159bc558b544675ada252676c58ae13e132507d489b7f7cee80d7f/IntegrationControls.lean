import GeneratedBinaryExperiment
import BinaryConstructiveRepair
open MeasureTheory ProbabilityTheory Set Filter
open scoped Topology BigOperators
namespace IntegrationAudit
open Orthemology.Tranche2 Orthemology.Tranche2.IntegratedBinary

lemma history_count_le_length {Θ A : Type*} (support : Θ → Finset A)
    (hist : List Θ) (a : A) : historyCount support hist a ≤ hist.length := by
  classical
  exact List.countP_le_length

lemma history_length {Θ A Y Ω : Type*} [Fintype Θ] [Fintype A]
    (P : Θ → A → Y → ℝ) (support : Θ → Finset A) (X : A → ℕ → Ω → Y)
    (initial : Θ) (n : ℕ) (ω : Ω) :
    (canonicalHistory P support X initial n ω).length = n := by
  rw [canonicalHistory_eq_range_map, List.length_map, List.length_range]

lemma full_history_prefix_local {Θ A Y Ω : Type*} [Fintype Θ] [Fintype A]
    (P : Θ → A → Y → ℝ) (support : Θ → Finset A) (X : A → ℕ → Ω → Y)
    (initial : Θ) (n : ℕ) (ω ω' : Ω)
    (h : ∀ a i, i<n → X a i ω = X a i ω') :
    canonicalHistory P support X initial n ω = canonicalHistory P support X initial n ω' := by
  induction n with
  | zero => rfl
  | succ n ih =>
    have heq := ih (fun a i hi => h a i (Nat.lt_succ_of_lt hi))
    have hcand := candidateFor_prefix_local P support X initial
      (canonicalHistory P support X initial n ω') ω ω' (by
        intro a i hi
        have hl := history_count_le_length support (canonicalHistory P support X initial n ω') a
        rw [history_length] at hl
        exact h a i (Nat.lt_succ_of_lt (lt_of_lt_of_le hi hl)))
    change canonicalHistory P support X initial n ω ++
      [candidateFor P support X initial (canonicalHistory P support X initial n ω) ω] = _
    rw [heq]
    exact congrArg (fun x => canonicalHistory P support X initial n ω' ++ [x]) hcand

lemma selected_prefix_local {Θ A Y Ω : Type*} [Fintype Θ] [Fintype A]
    (P : Θ → A → Y → ℝ) (support : Θ → Finset A) (X : A → ℕ → Ω → Y)
    (initial : Θ) (n : ℕ) (ω ω' : Ω)
    (h : ∀ a i, i<n → X a i ω = X a i ω') :
    canonicalSelected P support X initial ω n = canonicalSelected P support X initial ω' n := by
  unfold canonicalSelected
  rw [full_history_prefix_local P support X initial n ω ω' h]
  apply candidateFor_prefix_local
  intro a i hi
  have hl := history_count_le_length support (canonicalHistory P support X initial n ω') a
  rw [history_length] at hl
  exact h a i (lt_of_lt_of_le hi hl)

lemma selectedRepair_measurable (e : ℝ) (initial : Bool) (n : ℕ) :
    Measurable (fun ω => selectedRepair e initial ω n) := by
  exact (measurable_of_countable (repair e)).comp
    (canonicalSelected_measurable (law e) support observation initial n
      (fun a n => measurable_pi_apply (a,n)))

lemma final_event_measurable (e : ℝ) (θ initial : Bool) :
    MeasurableSet {ω | ∀ᶠ n in atTop, BinaryGood (alpha e θ) e (selectedRepair e initial ω n)} := by
  simp only [eventually_atTop, setOf_exists, setOf_forall]
  apply MeasurableSet.iUnion
  intro N
  apply MeasurableSet.iInter
  intro n
  apply MeasurableSet.iInter
  intro hn
  exact (measurable_binaryGood (alpha e θ) e).preimage (selectedRepair_measurable e initial n)

lemma zero_epsilon_all_labels_good (θ a : Bool) :
    BinaryGood (alpha 0 θ) 0 (repair 0 a) := by
  cases θ <;> cases a <;> norm_num [alpha,repair,BinaryGood]

lemma wrong_label_bad (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ : Bool) :
    ¬ BinaryGood (alpha e θ) e (repair e (!θ)) := by
  rw [good_iff_same e he0 he1]
  cases θ <;> decide

lemma repair_coherent (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (a : Bool) :
    0 < repair e a ∧ repair e a < 1 :=
  binary_good_is_coherent (alpha e a) e (repair e a)
    (alpha_bounds e he0 he1 a).1.le (alpha_bounds e he0 he1 a).2.le he0.le he1
    (exact_action_good e he0 he1 a)

lemma no_common_repair_label (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) :
    ¬ ∃ a : Bool, ∀ θ, BinaryGood (alpha e θ) e (repair e a) := by
  rintro ⟨a,h⟩
  have h0 := (good_iff_same e he0 he1 false a).mp (h false)
  have h1 := (good_iff_same e he0 he1 true a).mp (h true)
  cases a <;> simp_all

lemma target_preserving_actions_are_informative
    (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ : Bool) :
    BinaryGood (alpha e θ) e (repair e θ) ∧ law e false θ ≠ law e true θ := by
  refine ⟨exact_action_good e he0 he1 θ, ?_⟩
  intro h
  have hh := law_identifies e he0 false true θ h
  contradiction

lemma flipped_sensor_eventually_fails
    (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ initial : Bool) :
    ∀ᵐ ω ∂experimentLaw e he0 he1 (!θ), ∀ᶠ n : ℕ in atTop,
      ¬ BinaryGood (alpha e θ) e (selectedRepair e initial ω n) := by
  filter_upwards [generated_experiment_eventually_repairs e he0 he1 (!θ) initial] with ω hω
  apply hω.mono
  intro n hn
  have ha : canonicalSelected (law e) support observation initial ω n = !θ :=
    (good_iff_same e he0 he1 (!θ) _).mp hn
  rw [selectedRepair,ha]
  exact wrong_label_bad e he0 he1 θ

lemma uninformative_support_not_self_verifying
    (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ : Bool) :
    ¬ SelfVerifying (good e) (fun _ _ _ => True) θ (support θ) := by
  intro h
  have hh := h.2 (!θ) (fun _ _ => trivial) (by simp [support] : θ ∈ support θ)
  have heq : θ = !θ := by simpa [good,good_iff_same e he0 he1] using hh
  cases θ <;> contradiction

-- No sensor law, independence, maximization, or target-label premise remains.
example (e : ℝ) (he0 : 0 < e) (he1 : e ≤ 1/4) (θ initial : Bool) :
    ∀ᵐ ω ∂experimentLaw e he0 he1 θ, ∀ᶠ n : ℕ in atTop,
      BinaryGood (alpha e θ) e (selectedRepair e initial ω n) :=
  generated_experiment_eventually_repairs e he0 he1 θ initial
end IntegrationAudit

