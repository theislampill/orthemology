import SelectorCallDomains
set_option autoImplicit false

/-! Exact semantic transport under supplied finite-selector normalization.
Executed and decoding policies remain separate. Agreement is required only on
encoded finite acquired histories, not arbitrary raw natural component inputs.
No byte identity, finite-fuel budget, Python-resource or wall-time claim occurs. -/
namespace Orthemology.Ninth.SelectorTransport
open HiddenParity HiddenParity.Sufficiency
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.RuntimeBridge.PhaseUpdate
open Orthemology.RuntimeBridge.PhaseUpdate.FullController
open Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.RationalLaw.CanonicalBinding
open Orthemology.CertifiedObserver
open Orthemology.Frontier.MealyMeasure
open Orthemology.Ninth.SelectorExtraction
open P02A2.PRProgram
open MeasureTheory

/-- Research-only normalization of selector representation; all other supplied
configuration fields are retained definitionally. -/
def normalizeConfig (c : Config) : Config := { c with selectors := normalizeData c.selectors }

theorem normalizeConfig_certificate (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority) :
    Certificate (normalizeConfig c) menu priority :=
  ⟨(normalized_certificate_iff c.selectors c.kernel menu priority).mpr hc.selectors,
    hc.toleranceDenominator_pos, hc.rowDenominator_pos, hc.row_exact⟩

theorem normalizeConfig_idempotent (c : Config) : normalizeConfig (normalizeConfig c) = normalizeConfig c := by
  cases c
  simp only [normalizeConfig, normalizeData_idempotent]

theorem normalizeConfig_policy (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) :
    policy (normalizeConfig c) menu priority = policy c menu priority := rfl

theorem normalizeConfig_rep (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) :
    rep (normalizeConfig c) menu priority = rep c menu priority := rfl

theorem normalizeConfig_computed_commute (c : Config) :
    withComputedTolerance (normalizeConfig c) = normalizeConfig (withComputedTolerance c) := rfl

/-- This uses the exact initialized/stepped finite-history representation, whose
actual call-domain derivation is exposed in SelectorCallDomains. -/
theorem normalized_raw_policy_history (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) :
    denote (rawPolicyProgram (normalizeConfig c)) ![encodeHistory h] =
      denote (rawPolicyProgram c) ![encodeHistory h] := by
  rw [raw_policy_source_exact (normalizeConfig c) menu priority
      (normalizeConfig_certificate c menu priority hc), raw_policy_source_exact c menu priority hc]
  rfl

theorem normalized_policyProgram_history (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) :
    denote (policyProgram (normalizeConfig c)) ![encodeHistory h] =
      denote (policyProgram c) ![encodeHistory h] := by
  rw [policy_program_retained_exact (normalizeConfig c) menu priority
      (normalizeConfig_certificate c menu priority hc), policy_program_retained_exact c menu priority hc]
  rfl

theorem normalized_source_history (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) :
    sourcePolicy (normalizeConfig c) (encodeHistory h) = sourcePolicy c (encodeHistory h) := by
  rw [source_policy_retained_exact (normalizeConfig c) menu priority
      (normalizeConfig_certificate c menu priority hc), source_policy_retained_exact c menu priority hc]
  rfl

theorem normalized_historyPolicy (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority) :
    historyPolicy (sourcePolicy (normalizeConfig c)) = historyPolicy (sourcePolicy c) := by
  funext u h
  exact normalized_source_history c menu priority hc h

/-- Acquired-history agreement is enough for the actual history transition. -/
theorem historyStep_of_historyPolicy_eq (a b : ℕ → Bool) (hab : historyPolicy a = historyPolicy b)
    (σ : Bool) : historyStep σ a = historyStep σ b := by
  funext q bit
  simp only [historyStep, hab]

theorem historyObservation_of_historyPolicy_eq (a b : ℕ → Bool) (hab : historyPolicy a = historyPolicy b)
    (σ : Bool) : historyObservation σ a = historyObservation σ b := by
  funext q bit
  simp only [historyObservation, hab]

/-- Generic source-wrapper congruence. The programs may disagree on malformed
raw inputs: the accepted runtime always calls them on encoded acquired histories.
No Config kernel or initial-state correctness claim is inferred here. -/
theorem runtime_frames_of_historyPolicy_eq (p q : Program 1) (a b : ℕ → Bool)
    (hp : PolicyImplements p a) (hq : PolicyImplements q b)
    (hab : historyPolicy a = historyPolicy b) (σ : Bool) (x : Cantor) (n : ℕ) (j : Fin 4) :
    Indexed.runtimeOutput (runtimeIndex p σ) x (4*n+j) =
      Indexed.runtimeOutput (runtimeIndex q σ) x (4*n+j) := by
  have h := runtime_observed_history_frames p a hp σ x n j
  rw [historyStep_of_historyPolicy_eq a b hab σ,
    historyObservation_of_historyPolicy_eq a b hab σ] at h
  exact h.trans (runtime_observed_history_frames q b hq σ x n j).symm

theorem runtime_output_of_historyPolicy_eq (p q : Program 1) (a b : ℕ → Bool)
    (hp : PolicyImplements p a) (hq : PolicyImplements q b)
    (hab : historyPolicy a = historyPolicy b) (σ : Bool) :
    Indexed.runtimeOutput (runtimeIndex p σ) = Indexed.runtimeOutput (runtimeIndex q σ) := by
  funext x k
  let j : Fin 4 := ⟨k%4, Nat.mod_lt _ (by decide)⟩
  have hk : 4*(k/4)+j.val = k := by dsimp [j]; omega
  have h := runtime_frames_of_historyPolicy_eq p q a b hp hq hab σ x (k/4) j
  simpa only [hk] using h

theorem normalized_runtime_frames (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (σ : Bool) (x : Cantor) (n : ℕ) (j : Fin 4) :
    Indexed.runtimeOutput (runtimeIndex (policyProgram (normalizeConfig c)) σ) x (4*n+j) =
      Indexed.runtimeOutput (runtimeIndex (policyProgram c) σ) x (4*n+j) :=
  runtime_frames_of_historyPolicy_eq _ _ _ _ (policy_program_implements (normalizeConfig c))
    (policy_program_implements c) (normalized_historyPolicy c menu priority hc) σ x n j

theorem normalized_runtime_output (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority) (σ : Bool) :
    Indexed.runtimeOutput (runtimeIndex (policyProgram (normalizeConfig c)) σ) =
      Indexed.runtimeOutput (runtimeIndex (policyProgram c) σ) :=
  runtime_output_of_historyPolicy_eq _ _ _ _ (policy_program_implements (normalizeConfig c))
    (policy_program_implements c) (normalized_historyPolicy c menu priority hc) σ

/-- Decoder congruence is independent of which program supplied the receipts. -/
theorem pairSelector_of_historyPolicy_eq (a b : ℕ → Bool) (hab : historyPolicy a = historyPolicy b) :
    pairSelector a = pairSelector b := by
  unfold pairSelector
  rw [hab]

theorem pairUpdate_of_historyPolicy_eq (a b : ℕ → Bool) (hab : historyPolicy a = historyPolicy b) :
    pairUpdate a = pairUpdate b := by
  funext h y
  simp only [pairUpdate, pairSelector_of_historyPolicy_eq a b hab]

theorem generatedHistory_of_historyPolicy_eq (a b : ℕ → Bool) (hab : historyPolicy a = historyPolicy b) :
    generatedHistory a = generatedHistory b := by
  unfold generatedHistory
  rw [pairUpdate_of_historyPolicy_eq a b hab]

theorem canonicalHistoryDecoder_of_historyPolicy_eq (a b : ℕ → Bool)
    (hab : historyPolicy a = historyPolicy b) : canonicalHistoryDecoder a = canonicalHistoryDecoder b := by
  funext z n
  simp only [canonicalHistoryDecoder, generatedHistory_of_historyPolicy_eq a b hab]

/-- The executed policies and decoder policies are deliberately separate.
Agreement within each pair suffices for exact same-tape mixed-readout transport. -/
theorem mixed_decodedHistory_of_historyPolicy_eq
    (p q : Program 1) (executedA executedB decoderA decoderB : ℕ → Bool)
    (hp : PolicyImplements p executedA) (hq : PolicyImplements q executedB)
    (he : historyPolicy executedA = historyPolicy executedB)
    (hd : historyPolicy decoderA = historyPolicy decoderB) (σ : Bool) :
    decodedHistory p decoderA σ = decodedHistory q decoderB σ := by
  change (canonicalHistoryDecoder decoderA) ∘ Indexed.runtimeOutput (runtimeIndex p σ) =
    (canonicalHistoryDecoder decoderB) ∘ Indexed.runtimeOutput (runtimeIndex q σ)
  rw [canonicalHistoryDecoder_of_historyPolicy_eq decoderA decoderB hd,
    runtime_output_of_historyPolicy_eq p q executedA executedB hp hq he σ]

/-- Two independently certified configurations may use different tolerances,
kernels, menus or priorities. Their roles are not conflated. -/
theorem normalized_mixed_decodedHistory
    (executed decoder : Config)
    (executedMenu decoderMenu : Finset Bool → Bool → Finset Bool)
    (executedPriority decoderPriority : Bool → (Bool × Bool) → ℕ)
    (he : Certificate executed executedMenu executedPriority)
    (hd : Certificate decoder decoderMenu decoderPriority) (σ : Bool) :
    decodedHistory (policyProgram (normalizeConfig executed))
      (sourcePolicy (normalizeConfig decoder)) σ =
    decodedHistory (policyProgram executed) (sourcePolicy decoder) σ :=
  mixed_decodedHistory_of_historyPolicy_eq _ _ _ _ _ _
    (policy_program_implements (normalizeConfig executed)) (policy_program_implements executed)
    (normalized_historyPolicy executed executedMenu executedPriority he)
    (normalized_historyPolicy decoder decoderMenu decoderPriority hd) σ

/-- Exact transport of the inherited old-execution/computed-decoder pairing. -/
theorem normalized_old_computed_decodedHistory (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (σ : Bool) :
    decodedHistory (policyProgram (normalizeConfig c))
      (sourcePolicy (withComputedTolerance (normalizeConfig c))) σ =
    decodedHistory (policyProgram c) (sourcePolicy (withComputedTolerance c)) σ := by
  rw [normalizeConfig_computed_commute]
  exact normalized_mixed_decodedHistory c (withComputedTolerance c) menu menu priority priority hc
    (computed_tolerance_certificate c menu priority hc) σ

/-- Pointwise transport yields the same decoded law under every input measure.
This theorem does not need or assume an implementation resource bound. -/
theorem normalized_mixed_decoded_law
    (executed decoder : Config)
    (executedMenu decoderMenu : Finset Bool → Bool → Finset Bool)
    (executedPriority decoderPriority : Bool → (Bool × Bool) → ℕ)
    (he : Certificate executed executedMenu executedPriority)
    (hd : Certificate decoder decoderMenu decoderPriority) (σ : Bool) (μ : Measure Cantor) :
    μ.map (decodedHistory (policyProgram (normalizeConfig executed))
      (sourcePolicy (normalizeConfig decoder)) σ) =
    μ.map (decodedHistory (policyProgram executed) (sourcePolicy decoder) σ) := by
  rw [normalized_mixed_decodedHistory executed decoder executedMenu decoderMenu
    executedPriority decoderPriority he hd σ]

/-- Every event of the inherited mixed decoded history is unchanged, including
its positive-measure failure event. No event measurability premise is needed
for equality obtained by literal function rewriting. -/
theorem normalized_old_computed_event (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (σ : Bool)
    (E : Set (ℕ → PairHistory)) :
    {x : Cantor | decodedHistory (policyProgram (normalizeConfig c))
      (sourcePolicy (withComputedTolerance (normalizeConfig c))) σ x ∈ E} =
    {x : Cantor | decodedHistory (policyProgram c) (sourcePolicy (withComputedTolerance c)) σ x ∈ E} := by
  rw [normalized_old_computed_decodedHistory c menu priority hc σ]


/-- Explicitly retain the domain derivation alongside the exact semantic result.
Both compiled configurations are initialized from encoded histories internally. -/
theorem normalization_with_derived_domains (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) :
    CompiledCallDomains c ∧ CompiledCallDomains (normalizeConfig c) ∧
    (∀ h : HistoryFold.History,
      sourcePolicy (normalizeConfig c) (encodeHistory h) = sourcePolicy c (encodeHistory h)) ∧
    (∀ σ : Bool, Indexed.runtimeOutput (runtimeIndex (policyProgram (normalizeConfig c)) σ) =
      Indexed.runtimeOutput (runtimeIndex (policyProgram c) σ)) :=
  ⟨compiled_call_domains c menu priority hc,
    compiled_call_domains (normalizeConfig c) menu priority (normalizeConfig_certificate c menu priority hc),
    normalized_source_history c menu priority hc,
    normalized_runtime_output c menu priority hc⟩

/-- The exact parity-failure event of the inherited mixed pairing is preserved. -/
theorem normalized_old_computed_failure_event (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (σ : Bool) (d : Bool × Bool) :
    {x : Cantor | ¬HiddenParity.Stochastic.ParitySuccess (priority σ) (historyAction d
      (decodedHistory (policyProgram (normalizeConfig c))
        (sourcePolicy (withComputedTolerance (normalizeConfig c))) σ x))} =
    {x : Cantor | ¬HiddenParity.Stochastic.ParitySuccess (priority σ) (historyAction d
      (decodedHistory (policyProgram c) (sourcePolicy (withComputedTolerance c)) σ x))} := by
  rw [normalized_old_computed_decodedHistory c menu priority hc σ]

theorem normalized_old_computed_positive_failure_iff (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (σ : Bool) (d : Bool × Bool) (μ : Measure Cantor) :
    (0 < μ {x : Cantor | ¬HiddenParity.Stochastic.ParitySuccess (priority σ) (historyAction d
      (decodedHistory (policyProgram (normalizeConfig c))
        (sourcePolicy (withComputedTolerance (normalizeConfig c))) σ x))}) ↔
    (0 < μ {x : Cantor | ¬HiddenParity.Stochastic.ParitySuccess (priority σ) (historyAction d
      (decodedHistory (policyProgram c) (sourcePolicy (withComputedTolerance c)) σ x))}) := by
  rw [normalized_old_computed_failure_event c menu priority hc σ d]

end Orthemology.Ninth.SelectorTransport
