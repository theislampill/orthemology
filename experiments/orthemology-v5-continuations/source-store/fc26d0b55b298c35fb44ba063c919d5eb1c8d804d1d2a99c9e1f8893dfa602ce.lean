import LossDecoder

open Set MeasureTheory Filter
namespace OrthemologyMeasure
variable {Ω : Type*} [MeasurableSpace Ω]
variable {Q : ℕ → Type*} [∀ n, MeasurableSpace (Q n)]
  [∀ n, MeasurableSingletonClass (Q n)]
variable (μ ν : Measure Ω) [IsFiniteMeasure μ] [IsFiniteMeasure ν]

noncomputable def historyFamily (Y : ∀ n, Ω → Q n) : Option ℕ → Set Ω
  | none => P02A2.Observation.fullEvent μ Y
  | some n => P02A2.Observation.event μ Y n

noncomputable def commonHistoryFamily (Y : ∀ n, Ω → Q n) : Option ℕ → Set Ω
  | none => commonObservedSupport μ ν (P02A2.Observation.history Y)
  | some n => commonObservedSupport μ ν (Y n)

noncomputable def historyPattern (Y : ∀ n, Ω → Q n) :=
  membershipPattern (historyFamily μ Y)

noncomputable def historyClass (Y : ∀ n, Ω → Q n) :=
  lossClass ∘ historyPattern μ Y

theorem historyPattern_measurable {Y : ∀ n, Ω → Q n}
    (hY : ∀ n, Measurable (Y n)) : Measurable (historyPattern μ Y) := by
  apply membershipPattern_measurable
  intro i
  cases i with
  | none => exact P02A2.Observation.fullEvent_measurable μ hY
  | some n => exact P02A2.Observation.event_measurable μ hY n

theorem historyClass_measurable {Y : ∀ n, Ω → Q n}
    (hY : ∀ n, Measurable (Y n)) : Measurable (historyClass μ Y) :=
  lossClass_measurable.comp (historyPattern_measurable μ hY)

theorem historyPattern_eventTV_bound {Y : ∀ n, Ω → Q n}
    (hY : ∀ n, Measurable (Y n)) :
    eventTV (μ.map (historyPattern μ Y)) (ν.map (historyPattern ν Y)) ≤ eventTV μ ν := by
  let C := membershipPattern (commonHistoryFamily μ ν Y)
  have hμ : historyPattern μ Y =ᵐ[μ] C := by
    apply membershipPattern_ae
    intro i
    cases i with
    | none => exact observedSupport_ae_common_left μ ν (P02A2.Observation.history_measurable hY)
    | some n => exact observedSupport_ae_common_left μ ν (hY n)
  have hν : historyPattern ν Y =ᵐ[ν] C := by
    apply membershipPattern_ae
    intro i
    cases i with
    | none => exact observedSupport_ae_common_right μ ν (P02A2.Observation.history_measurable hY)
    | some n => exact observedSupport_ae_common_right μ ν (hY n)
  have hC : Measurable C := by
    apply membershipPattern_measurable
    intro i
    cases i with
    | none => exact commonObservedSupport_measurable μ ν (P02A2.Observation.history_measurable hY)
    | some n => exact commonObservedSupport_measurable μ ν (hY n)
  rw [Measure.map_congr hμ, Measure.map_congr hν]
  exact eventTV_map_le μ ν hC

/-- The entire law of retained atom, first finite loss, and infinite residual
is jointly one-Lipschitz, even though its classifier depends on the input law. -/
theorem historyClass_eventTV_bound {Y : ∀ n, Ω → Q n}
    (hY : ∀ n, Measurable (Y n)) :
    eventTV (μ.map (historyClass μ Y)) (ν.map (historyClass ν Y)) ≤ eventTV μ ν := by
  unfold historyClass
  rw [← Measure.map_map lossClass_measurable (historyPattern_measurable μ hY),
      ← Measure.map_map lossClass_measurable (historyPattern_measurable ν hY)]
  exact (eventTV_map_le _ _ lossClass_measurable).trans (historyPattern_eventTV_bound μ ν hY)

theorem historyClass_atom {Y : ∀ n, Ω → Q n} (ω : Ω) :
    historyClass μ Y ω = none ↔ ω ∈ P02A2.Observation.fullEvent μ Y := by
  classical
  simp [historyClass, lossClass, historyPattern, membershipPattern, historyFamily]

theorem historyClass_residual {Y : ∀ n, Ω → Q n} (ω : Ω) :
    historyClass μ Y ω = some none ↔ ω ∈ ownResidual μ Y := by
  classical
  simp [historyClass, lossClass, historyPattern, membershipPattern, historyFamily,
    firstLoss_none, ownResidual, Set.mem_diff, Set.mem_iInter, and_comm]

theorem historyClass_finite {Y : ∀ n, Ω → Q n} (ω : Ω) (n : ℕ) :
    historyClass μ Y ω = some (some n) ↔
      ω ∉ P02A2.Observation.fullEvent μ Y ∧
      ω ∉ P02A2.Observation.event μ Y n ∧
      ∀ k < n, ω ∈ P02A2.Observation.event μ Y k := by
  classical
  simp [historyClass, lossClass, historyPattern, membershipPattern, historyFamily,
    firstLoss_some]

theorem historyClass_initial {Y : ∀ n, Ω → Q n}
    (hY : ∀ n, Measurable (Y n)) (ω : Ω) :
    historyClass μ Y ω = some (some 0) ↔ ω ∉ P02A2.Observation.event μ Y 0 := by
  rw [historyClass_finite]
  constructor
  · exact fun h => h.2.1
  · intro h
    exact ⟨fun hf => h (P02A2.Observation.full_subset_event μ hY 0 hf), h,
      fun k hk => False.elim (Nat.not_lt_zero k hk)⟩

theorem historyClass_step {Y : ∀ n, Ω → Q n}
    (hY : ∀ n, Measurable (Y n))
    (hanti : Antitone (P02A2.Observation.event μ Y)) (ω : Ω) (n : ℕ) :
    historyClass μ Y ω = some (some (n+1)) ↔
      ω ∈ P02A2.Refinement.loss (P02A2.Observation.event μ Y) n := by
  rw [historyClass_finite]
  constructor
  · intro h
    exact ⟨h.2.2 n (Nat.lt_succ_self n), h.2.1⟩
  · intro h
    refine ⟨fun hf => h.2 (P02A2.Observation.full_subset_event μ hY (n+1) hf), h.2, ?_⟩
    intro k hk
    exact hanti (Nat.le_of_lt_succ hk) h.1

theorem historyClass_residual_mass {Y : ∀ n, Ω → Q n}
    (hY : ∀ n, Measurable (Y n)) :
    (μ.map (historyClass μ Y)) {some none} = μ (ownResidual μ Y) := by
  rw [Measure.map_apply (historyClass_measurable μ hY) (by trivial)]
  congr 1
  ext ω
  exact historyClass_residual μ ω

theorem historyClass_initial_mass {Y : ∀ n, Ω → Q n}
    (hY : ∀ n, Measurable (Y n)) :
    (μ.map (historyClass μ Y)) {some (some 0)} = μ (P02A2.Observation.event μ Y 0)ᶜ := by
  rw [Measure.map_apply (historyClass_measurable μ hY) (by trivial)]
  congr 1
  ext ω
  exact historyClass_initial μ hY ω

theorem historyClass_step_mass {Y : ∀ n, Ω → Q n}
    (hY : ∀ n, Measurable (Y n))
    (hanti : Antitone (P02A2.Observation.event μ Y)) (n : ℕ) :
    (μ.map (historyClass μ Y)) {some (some (n+1))} =
      μ (P02A2.Refinement.loss (P02A2.Observation.event μ Y) n) := by
  rw [Measure.map_apply (historyClass_measurable μ hY) (by trivial)]
  congr 1
  ext ω
  exact historyClass_step μ hY hanti ω n

end OrthemologyMeasure
#print axioms OrthemologyMeasure.historyClass_eventTV_bound
#print axioms OrthemologyMeasure.historyClass_atom
#print axioms OrthemologyMeasure.historyClass_residual

#print axioms OrthemologyMeasure.historyClass_finite

#print axioms OrthemologyMeasure.historyClass_step_mass
#print axioms OrthemologyMeasure.historyClass_residual_mass
