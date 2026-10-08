import HiddenChangeControllerDynamics
import HiddenChangeContamination
import HiddenChangeFixedIndex

set_option maxHeartbeats 800000

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open HiddenParity.Stochastic HiddenParity.Empirical HiddenParity.Sufficiency HiddenParity.Adaptive
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenChange
variable {n k : ℕ} [NeZero n] [NeZero k]

def publicTrace (H : TaggedTrace n k) : ℕ → PublicHistory n k :=
  fun t => erasePairSources (eraseMode (H t))

def FixedStep (I : Input n k) (κ : ChangeIndex) (s : State n) (π : Policy Unit n k)
    (t : ℕ) (h h' : TaggedHistory n k) : Prop :=
  eraseMode h' = (pairPolicy s π () (eraseMode h), currentState s (eraseMode h')) :: eraseMode h ∧
  0 < I.row (fixedMode κ t) (pairPolicy s π () (eraseMode h)) (currentState s (eraseMode h'))

/-- Causal public recursion and governing-row support on the actual fixed law.
This theorem applies to arbitrary deterministic history policies. -/
theorem fixed_law_steps (I : Input n k) (hI : I.Valid) (κ : ChangeIndex)
    (s : State n) (π : Policy Unit n k)
    (hπ : Measurable (fun z : Unit × PublicHistory n k => π z.1 z.2)) :
    ∀ᵐ H ∂fixedLaw I hI κ s (Measure.dirac ()) π,
      H 0 = [] ∧ ∀ t, FixedStep I κ s π t (H t) (H (t+1)) := by
  rw [fixedLaw_eq_stack I hI κ s (Measure.dirac ()) π hπ]
  have hm : MeasurableSet {H : TaggedTrace n k | H 0 = [] ∧
      ∀ t, FixedStep I κ s π t (H t) (H (t+1))} := by
    change MeasurableSet ({H : TaggedTrace n k | H 0 = []} ∩
      {H | ∀ t, FixedStep I κ s π t (H t) (H (t+1))})
    apply MeasurableSet.inter
    · exact (measurableSet_singleton []).preimage (measurable_pi_apply 0)
    · simp only [Set.setOf_forall]
      apply MeasurableSet.iInter
      intro t
      change MeasurableSet ((fun H : TaggedTrace n k => (H t,H (t+1))) ⁻¹'
        {p | FixedStep I κ s π t p.1 p.2})
      exact (Set.to_countable {p : TaggedHistory n k × TaggedHistory n k |
        FixedStep I κ s π t p.1 p.2}).measurableSet.preimage
        ((measurable_pi_apply t).prodMk (measurable_pi_apply (t+1)))
  apply (ae_map_iff (stackHistoryTrajectory_measurable _
    (fixedPolicy_measurable κ s π hπ)).aemeasurable hm).mpr
  filter_upwards [seeded_all_tapes_supported (Measure.dirac ()) (taggedRows I)
    (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)] with z hz
  refine ⟨rfl, ?_⟩
  intro t
  let pol := fixedPolicy κ s π
  let H := stackHistoryTrajectory pol z
  have hrec : eraseMode (H (t+1)) = ((stackActionTrajectory pol z t).2,
      stackReceipt pol z t) :: eraseMode (H t) := by
    dsimp only [H]
    rw [stackHistoryTrajectory_succ_receipt, eraseMode_cons]
  have hcur : currentState s (eraseMode (H (t+1))) = stackReceipt pol z t := by rw [hrec]; rfl
  have hact : (stackActionTrajectory pol z t).2 = pairPolicy s π () (eraseMode (H t)) := by
    cases z.1
    rfl
  refine ⟨?_, ?_⟩
  · change eraseMode (H (t+1)) = (pairPolicy s π () (eraseMode (H t)),
      currentState s (eraseMode (H (t+1)))) :: eraseMode (H t)
    rw [hcur, ← hact]
    exact hrec
  · have hp := hz (stackActionTrajectory pol z t) (countBefore pol z (stackActionTrajectory pol z t) t)
    change 0 < taggedRows I (stackActionTrajectory pol z t) (stackReceipt pol z t) at hp
    have htag := fixed_stack_tag κ s π z t
    change 0 < (I.row (stackActionTrajectory pol z t).1 (stackActionTrajectory pol z t).2
      (stackReceipt pol z t) : ℝ) at hp
    change 0 < I.row (fixedMode κ t) (pairPolicy s π () (eraseMode (H t)))
      (currentState s (eraseMode (H (t+1))))
    rw [hcur, ← hact]
    rw [htag] at hp
    exact_mod_cast hp

theorem fixed_steps_follows (I : Input n k) (hI : Admissible I) (κ : ChangeIndex)
    (c : PositiveBody n k) (s : State n) (H : TaggedTrace n k)
    (h0 : H 0 = [])
    (hstep : ∀ t, FixedStep I κ s (compile I hI s c) t (H t) (H (t+1))) :
    Follows I hI c s (publicTrace H) := by
  refine ⟨by simp [publicTrace, h0, erasePairSources], ?_⟩
  intro t
  have he := congrArg erasePairSources (hstep t).1
  change erasePairSources (eraseMode (H (t+1))) = _
  simp only [publicTrace, observedState_erase]
  simpa only [erasePairSources, List.map_cons, pairPolicy] using he

theorem fixed_steps_augment (I : Input n k) (hI : Admissible I) (κ : ChangeIndex)
    (c : PositiveBody n k) (s : State n) (H : TaggedTrace n k)
    (h0 : H 0 = [])
    (hstep : ∀ t, FixedStep I κ s (compile I hI s c) t (H t) (H (t+1))) :
    ∀ t, augmentHistory s (publicTrace H t) = eraseMode (H t) := by
  intro t
  induction t with
  | zero => simp [publicTrace, h0, erasePairSources, augmentHistory]
  | succ t ih =>
      rw [(fixed_steps_follows I hI κ c s H h0 hstep).2 t]
      simp only [augmentHistory]
      rw [ih]
      simp only [publicTrace, observedState_erase]
      exact (hstep t).1.symm

theorem fixed_steps_supported (I : Input n k) (hI : Admissible I) (κ : ChangeIndex)
    (c : PositiveBody n k) (s : State n) (H : TaggedTrace n k)
    (hstep : ∀ t, FixedStep I κ s (compile I hI s c) t (H t) (H (t+1))) :
    ∀ t, 0 < I.row (fixedMode κ t) (runPair I hI c s (publicTrace H) t)
      (observedState s (publicTrace H (t+1))) := by
  intro t
  simpa only [runPair, publicTrace, observedState_erase, pairPolicy] using (hstep t).2

/-- Actual-law region safety and phase stabilization for the literal compiler.
All support and empirical hypotheses are discharged by constructed law modules.
This endpoint does not yet assert complete component recurrence or parity. -/
theorem compiled_fixed_safety_and_phase (I : Input n k) (hI : Admissible I)
    (c : PositiveBody n k) (s : State n) (hc : positiveCheck I s c = true)
    (κ : ChangeIndex) :
    ∀ᵐ H ∂fixedLaw I hI.1 κ s (Measure.dirac ()) (compile I hI s c),
      (∀ t, RegionValid c (observedState s (publicTrace H t)) (runMemory I c s (publicTrace H) t)) ∧
      ∃ r, ∀ᶠ t in atTop, (runMemory I c s (publicTrace H) t).phase = r := by
  letI : NeZero n := ⟨by intro h; subst n; exact Fin.elim0 s⟩
  letI : NeZero k := ⟨by
    intro h
    obtain ⟨a,_⟩ := hI.2 s
    subst k
    exact Fin.elim0 a⟩
  have hb := ((positiveCheck_iff I s c).mp hc).2.1
  have hs := ((positiveCheck_iff I s c).mp hc).2.2
  filter_upwards [fixed_law_steps I hI.1 κ s (compile I hI s c) (compiled_measurable I hI s c),
    fixed_law_rational_true_gate I hI.1 κ s (Measure.dirac ()) (compile I hI s c)
      (compiled_measurable I hI s c)] with H hsteps hgate
  have hf := fixed_steps_follows I hI κ c s H hsteps.1 hsteps.2
  have hsupport := fixed_steps_supported I hI κ c s H hsteps.2
  have hinv := run_invariant I hI c hb s hs (publicTrace H) hf (fixedMode κ)
    (fixedMode_persistent κ) hsupport
  refine ⟨fun t => (hinv t).1, ?_⟩
  obtain ⟨N,hN⟩ := fixed_eventually_final κ
  obtain ⟨K,hK⟩ := hgate
  apply run_phase_stabilizes I hI c hb s (publicTrace H) hf (finalMode κ) N K
    (fun t => (hinv t).1)
  · intro t ht
    simpa only [hN t ht] using hsupport t
  · intro r hr t
    rw [fixed_steps_augment I hI κ c s H hsteps.1 hsteps.2 t]
    exact hK r hr t

#print axioms fixed_law_steps
#print axioms compiled_fixed_safety_and_phase
end HiddenChange
