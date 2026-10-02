import SemanticSafeActions

noncomputable section
open MeasureTheory ProbabilityTheory Filter Set
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Necessity
open HiddenParity.Stochastic HiddenParity.Stage HiddenParity.Adaptive
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

theorem stack_history_succ (π : R → History (State × Action) State → State × Action)
    (z : R × FlatStack (State × Action) State) (n : ℕ) :
    stackHistoryTrajectory π z (n+1) =
      (stackActionTrajectory π z n, stackReceipt π z n) :: stackHistoryTrajectory π z n := by
  simp [stackHistoryTrajectory, observedHistory, feedback, stackActionTrajectory, stackReceipt, countBefore]

theorem stack_history_compatible (π : R → History (State × Action) State → State × Action)
    (z : R × FlatStack (State × Action) State) (n : ℕ) :
    ActionCompatible π z.1 (stackHistoryTrajectory π z n) := by
  induction n with
  | zero => exact True.intro
  | succ n ih =>
      rw [stack_history_succ]
      exact ⟨ih, rfl⟩

/-- The observable unchanged-support prefix is exactly enough to keep the actual
full acquired history's live-model set equal to the stage support. -/
theorem stack_liveHistory_of_same_prefix
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (s₀ : State) (π : R → History Action State → Action)
    (z : R × FlatStack (State × Action) State) (n : ℕ)
    (hPrefix : SameSupportPrefix P B (stackActionTrajectory (pairPolicy s₀ π) z) n) :
    liveHistory P B (stackHistoryTrajectory (pairPolicy s₀ π) z n) = B := by
  induction n with
  | zero => exact liveHistory_nil P B
  | succ n ih =>
      have hn : SameSupportPrefix P B (stackActionTrajectory (pairPolicy s₀ π) z) n :=
        fun k hk => hPrefix k (Nat.lt_succ_of_lt hk)
      rw [stack_history_succ, liveHistory_cons, ih hn, ← stack_pair_source_next]
      exact hPrefix n (Nat.lt_succ_self n)

theorem sameSupportPrefix_measurable
    (P : RationalKernel Model (State × Action) State) (B : Finset Model) (n : ℕ) :
    MeasurableSet {x : ℕ → State × Action | SameSupportPrefix P B x n} := by
  simp only [SameSupportPrefix, Set.setOf_forall]
  apply MeasurableSet.iInter
  intro k
  by_cases hk : k < n
  · have hc : Measurable (fun x : ℕ → State × Action => (x k, x (k+1))) :=
      (measurable_pi_apply k).prodMk (measurable_pi_apply (k+1))
    have hm := (Set.toFinite {z : (State × Action) × (State × Action) |
      liveUpdate P B z.1 z.2.1 = B}).measurableSet.preimage hc
    simpa only [hk, Set.iInter_true] using hm
  · simp [hk]

theorem allowed_until_exit_measurable
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (allowed : Finset (State × Action)) :
    MeasurableSet {x : ℕ → State × Action | ∀ n, SameSupportPrefix P B x n → x n ∈ allowed} := by
  simp only [Set.setOf_forall]
  apply MeasurableSet.iInter
  intro n
  have h1 := (sameSupportPrefix_measurable P B n).compl
  have hCoord : Measurable (fun x : ℕ → State × Action => x n) := measurable_pi_apply n
  have h2 := allowed.measurableSet.preimage hCoord
  convert h1.union h2 using 1
  ext x
  change (SameSupportPrefix P B x n → x n ∈ allowed) ↔ (¬ SameSupportPrefix P B x n ∨ x n ∈ allowed)
  tauto

/-- The all-branch safe-action premise of the stage theorem is now derived from
a genuine lawful winning policy and actual positive-history restarts. It is not
assumed as a controller certificate. -/
theorem winningPolicy_safe_until_exit
    {P : RationalKernel Model (State × Action) State}
    {menu : Finset Model → State → Finset Action} {priority : Model → (State × Action) → ℕ}
    {d : State × Action} {B : Finset Model} {s₀ : State}
    (w : WinningPolicy (R := R) P menu priority d B s₀) (θ : Model) :
    ∀ᵐ x ∂markovPairLaw P θ s₀ w.policy w.seedLaw d,
      ∀ n, SameSupportPrefix P B x n → x n ∈ semanticAllowed (R := R) P menu priority d B := by
  letI := w.probability
  have hAllHist : ∀ᵐ r ∂w.seedLaw, ∀ h : History (State × Action) State,
      liveHistory P B h = B → ActionCompatible (pairPolicy s₀ w.policy) r h →
        pairPolicy s₀ w.policy r h ∈ semanticAllowed (R := R) P menu priority d B := by
    apply ae_all_iff.mpr
    intro h
    by_cases hh : liveHistory P B h = B
    · exact (winning_policy_safe_at_same_support_history w h hh).mono (fun _ hsafe _ => hsafe)
    · exact ae_of_all _ (fun _ hEq => (hh hEq).elim)
  have hJoint : ∀ᵐ z ∂w.seedLaw.prod (stackMeasure (realRows P θ) (realRows_nonnegative P θ) (realRows_normalized P θ)),
      ∀ h : History (State × Action) State, liveHistory P B h = B →
        ActionCompatible (pairPolicy s₀ w.policy) z.1 h →
          pairPolicy s₀ w.policy z.1 h ∈ semanticAllowed (R := R) P menu priority d B := by
    have hfst : Measurable (Prod.fst : R × FlatStack (State × Action) State → R) := measurable_fst
    have hMapped : ∀ᵐ r ∂(w.seedLaw.prod (stackMeasure (realRows P θ) (realRows_nonnegative P θ)
        (realRows_normalized P θ))).map Prod.fst,
        ∀ h : History (State × Action) State, liveHistory P B h = B →
          ActionCompatible (pairPolicy s₀ w.policy) r h →
            pairPolicy s₀ w.policy r h ∈ semanticAllowed (R := R) P menu priority d B := by
      simpa only [Measure.map_fst_prod, measure_univ, one_smul] using hAllHist
    exact ae_of_ae_map hfst.aemeasurable hMapped
  apply actionLaw_ae_of_stack (pairPolicy s₀ w.policy) (pairPolicy_measurable s₀ w.policy w.measurable)
    w.seedLaw (realRows P θ) (realRows_nonnegative P θ) (realRows_normalized P θ) d _
    (allowed_until_exit_measurable P B (semanticAllowed (R := R) P menu priority d B))
  filter_upwards [hJoint] with z hz
  intro n hPrefix
  exact hz (stackHistoryTrajectory (pairPolicy s₀ w.policy) z n)
    (stack_liveHistory_of_same_prefix P B s₀ w.policy z n hPrefix)
    (stack_history_compatible (pairPolicy s₀ w.policy) z n)

/-- Genuine semantic winning implies the target-or-proper-exit stage condition,
with all-branch licensing derived from positive common continuations. -/
theorem semantic_winning_target_or_exit
    {P : RationalKernel Model (State × Action) State}
    {menu : Finset Model → State → Finset Action} {priority : Model → (State × Action) → ℕ}
    {d : State × Action} {B : Finset Model} {s₀ : State}
    (w : WinningPolicy (R := R) P menu priority d B s₀) (θ : Model) (hθ : θ ∈ B) :
    ReachableExit P B θ (semanticAllowed (R := R) P menu priority d B) s₀ ∨
      ∃ t ∈ markovTargetStates P Prod.fst B priority θ (semanticAllowed (R := R) P menu priority d B),
        Reach Prod.fst (internalSuccessors P B) (semanticAllowed (R := R) P menu priority d B) s₀ t := by
  letI := w.probability
  exact winning_policy_target_or_exit P B priority θ hθ
    (semanticAllowed (R := R) P menu priority d B) s₀ w.policy w.measurable w.seedLaw d
    (winningPolicy_pair_parity w) (winningPolicy_safe_until_exit w θ)

end HiddenParity.Necessity
