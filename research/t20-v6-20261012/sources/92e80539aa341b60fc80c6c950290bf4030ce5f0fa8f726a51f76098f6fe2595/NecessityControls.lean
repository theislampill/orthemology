import SeededPolicyNecessity

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset Set
open scoped ENNReal BigOperators
open Orthemology.Tranche2 Orthemology.Tranche2.PolicyEmbedding
namespace NecessityAudit

local instance : MeasurableSpace Bool := ⊤
local instance : MeasurableSingletonClass Bool := ⟨fun _ => trivial⟩

def coin (_a _y : Bool) : ℝ := 1/2
lemma coin_pos : ∀ a y, 0 < coin a y := by intros; norm_num [coin]
lemma coin_nonneg : ∀ a y, 0 ≤ coin a y := fun a y => (coin_pos a y).le
lemma coin_norm : ∀ a, ∑ y, coin a y = 1 := by intro a; norm_num [coin,Fintype.sum_bool]

theorem repeated_inside_keys :
    feedbackKeys ({true} : Finset Bool) ([(true,false),(true,true)] : History Bool Bool) =
      [Sum.inl (true,1),Sum.inl (true,0)] := by
  simp [feedbackKeys,feedbackKey,actionCount]

theorem different_outside_actions_use_new_rows :
    feedbackKeys (∅ : Finset Bool) ([(true,false),(false,true)] : History Bool Bool) =
      [Sum.inr 1,Sum.inr 0] := by
  simp [feedbackKeys,feedbackKey,outsideCount]

theorem actual_request_slots_are_distinct (U : Finset Bool) (h : History Bool Bool) :
    Function.Injective (requestKey U h) := requestKey_injective U h

theorem empty_feedback_fiber :
    feedbackLaw coin coin coin_nonneg coin_norm coin_nonneg coin_norm
      {ω | FeedbackCompatible ({true} : Finset Bool) (fun a n => ω.1 (a,n)) ω.2 ([] : History Bool Bool)} = 1 := by
  rw [feedbackCompatible_probability _ _ _ _ _ _ _ _ (fun _ _ => rfl)]
  simp

theorem independent_two_samples_quarter :
    feedbackLaw coin coin coin_nonneg coin_norm coin_nonneg coin_norm
      {ω | FeedbackCompatible ({true} : Finset Bool) (fun a n => ω.1 (a,n)) ω.2
        ([(true,false),(true,false)] : History Bool Bool)} = 1/4 := by
  rw [feedbackCompatible_probability _ _ _ _ _ _ _ _ (fun _ _ => rfl)]
  norm_num [Fin.prod_univ_two,coin,ENNReal.ofReal_div_of_pos]
  rw [← ENNReal.inv_pow]
  norm_num

theorem copied_one_sample_half :
    feedbackLaw coin coin coin_nonneg coin_norm coin_nonneg coin_norm
      {ω | ω.1 (true,0) = false ∧ ω.1 (true,0) = false} = 1/2 := by
  simp only [and_self]
  rw [feedbackLaw_left_marginal]
  norm_num [coin,ENNReal.ofReal_div_of_pos]

def alwaysTrue (_r : Unit) (_h : History Bool Bool) : Bool := true
def initial : EvalState Unit Bool Bool := ((),((fun _ _ => false),[]))
def zeros (_n : ℕ) (_a : Bool) := false

theorem action_is_before_feedback :
    traceAction alwaysTrue (FiniteAlphabetQuery.run (query ∅ alwaysTrue) (step ∅ alwaysTrue) zeros initial) 0 = true := rfl

theorem unshifted_empty_history_wrong :
    ((historyReadout (FiniteAlphabetQuery.run (query ∅ alwaysTrue) (step ∅ alwaysTrue) zeros initial) 0).headD (false,false)).1 = false := rfl

theorem shifted_history_is_current_action :
    historyAction false (historyReadout (FiniteAlphabetQuery.run (query ∅ alwaysTrue) (step ∅ alwaysTrue) zeros initial)) 0 = true := rfl

theorem default_irrelevant_on_actual_run {R : Type*} (U : Finset Bool)
    (π : R → History Bool Bool → Bool) (oracle : ℕ → Bool → Bool)
    (s : EvalState R Bool Bool) (d e : Bool) :
    historyAction d (historyReadout (FiniteAlphabetQuery.run (query U π) (step U π) oracle s)) =
    historyAction e (historyReadout (FiniteAlphabetQuery.run (query U π) (step U π) oracle s)) :=
  (action_readout_on_run U π oracle s d).symm.trans (action_readout_on_run U π oracle s e)

def malformedTrace (n : ℕ) : EvalState Unit Bool Bool × ℕ := (initial,n)

theorem malformed_trace_in_action_tail :
    malformedTrace ∈ RecurrentSupport.tailEvent (traceAction alwaysTrue) {true} 0 := by
  constructor
  · change RecurrentSupport.recurrentSet (fun _ => true) = {true}
    ext a
    simp [RecurrentSupport.mem_recurrentSet,RecurrentSupport.Recurs,eq_comm]
  · intro n _
    simp [traceAction,selected,alwaysTrue]

theorem malformed_trace_not_finite_query :
    malformedTrace ∉ FiniteAlphabetQuery.finiteQueryTrace := by
  intro h
  obtain ⟨N,hN⟩ := Set.mem_iUnion.mp h
  have hn := hN (N+1)
  change N+1 ≤ N at hn
  omega

theorem incompatible_action_history :
    ¬ ActionCompatible alwaysTrue () ([(false,false)] : History Bool Bool) := by
  simp [ActionCompatible,alwaysTrue]

theorem model_indexed_constant_selector (θ : Bool)
    (tr : FiniteAlphabetQuery.Trace (EvalState Unit Bool Bool)) (n : ℕ) :
    traceAction (fun (_r : Unit) (_h : History Bool Bool) => θ) tr n = θ := rfl

/-- Even arbitrary measurable private randomization cannot supply the model's
answer when the same observation laws and the SAME policy must serve both. -/
theorem no_shared_blind_policy {R : Type*} [MeasurableSpace R]
    (π : R → History Bool Bool → Bool)
    (hπ : Measurable (fun z : R × History Bool Bool => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : Bool) :
    ¬ (∀ θ : Bool, ∀ᵐ x ∂actionLaw π ρ coin coin_nonneg coin_norm d,
      ∀ᶠ n in atTop, x n ∈ ({θ} : Finset Bool)) := by
  intro hg
  have hs := seeded_policy_self_verifying_necessity (fun (_θ : Bool) => coin)
    (fun θ => ({θ} : Finset Bool)) (fun _ => coin_pos) (fun _ => coin_norm) π hπ ρ d hg false
  obtain ⟨U,hU,hself⟩ := hs
  obtain ⟨a,ha⟩ := hU
  have hf : a = false := by simpa using hself.1 ha
  have ht : a = true := by simpa using hself.2 true (fun _ _ => rfl) ha
  cases hf.symm.trans ht

-- A zero-support costly-revelation model has no self-verifying good support.
inductive Act | r0 | r1 | probe deriving DecidableEq, Fintype
open Act

def revealing (θ : Bool) (a : Act) (y : Bool) : ℝ :=
  if a = probe then (if y = θ then 1 else 0) else (if y then 0 else 1)
def repairTarget (θ : Bool) : Finset Act := {if θ then r1 else r0}

theorem repairs_indistinguishable (a : Act) (ha : a ∈ repairTarget false) :
    revealing false a = revealing true a := by
  have he : a = r0 := by simpa [repairTarget] using ha
  subst a
  funext y
  simp [revealing]

theorem no_zero_support_good_certificate :
    ¬ ∃ U : Finset Act, U.Nonempty ∧ SelfVerifying repairTarget
      (fun η ζ a => revealing η a = revealing ζ a) false U := by
  rintro ⟨U,hU,hself⟩
  obtain ⟨a,ha⟩ := hU
  have h0 : a = r0 := by simpa [repairTarget] using hself.1 ha
  have h1 : a = r1 := by
    simpa [repairTarget] using hself.2 true (fun b hb => repairs_indistinguishable b (hself.1 hb)) ha
  cases h0.symm.trans h1

theorem probe_reveals_exactly (θ : Bool) : revealing θ probe θ = 1 ∧ revealing θ probe (!θ) = 0 := by
  cases θ <;> simp [revealing]

end NecessityAudit
