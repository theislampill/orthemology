import HiddenChangeControllerSafety
import HiddenChangePhaseArithmetic
import PhaseStabilization

set_option maxHeartbeats 800000

open Filter
namespace HiddenChange
open HiddenParity HiddenParity.Sufficiency
open Orthemology.Tranche2.PolicyEmbedding
variable {n k : ℕ}

def runPair (I : Input n k) (hI : Admissible I) (c : PositiveBody n k)
    (s₀ : State n) (H : ℕ → PublicHistory n k) (t : ℕ) : Pair n k :=
  (observedState s₀ (H t), compile I hI s₀ c () (H t))

def runMemory (I : Input n k) (c : PositiveBody n k) (s₀ : State n)
    (H : ℕ → PublicHistory n k) (t : ℕ) : ControllerMemory n k :=
  currentMemory I c s₀ (H t)

/-- Structural recursion only; this contains no recurrence, fairness, stopping,
row-regularity, or success field. It will be discharged on actual-law traces. -/
def Follows (I : Input n k) (hI : Admissible I) (c : PositiveBody n k)
    (s₀ : State n) (H : ℕ → PublicHistory n k) : Prop :=
  H 0 = [] ∧ ∀ t, H (t+1) =
    (compile I hI s₀ c () (H t), observedState s₀ (H (t+1))) :: H t

theorem runMemory_succ (I : Input n k) (hI : Admissible I) (c : PositiveBody n k)
    (s₀ : State n) (H : ℕ → PublicHistory n k) (hf : Follows I hI c s₀ H) (t : ℕ) :
    runMemory I c s₀ H (t+1) =
      prepare c (observedState s₀ (H (t+1)))
        (advance I (runPair I hI c s₀ H t) (observedState s₀ (H (t+1)))
          (runMemory I c s₀ H t)
          (rejectHistory I (runMemory I c s₀ H t).phase (augmentHistory s₀ (H (t+1))))) := by
  conv_lhs => unfold runMemory currentMemory; rw [hf.2 t]
  simp only [memory, observedState]
  conv_rhs => rw [hf.2 t]
  rfl

theorem run_phase_increment (I : Input n k) (hI : Admissible I) (c : PositiveBody n k)
    (s₀ : State n) (H : ℕ → PublicHistory n k) (hf : Follows I hI c s₀ H) (t : ℕ) :
    (runMemory I c s₀ H (t+1)).phase = (runMemory I c s₀ H t).phase ∨
      (runMemory I c s₀ H (t+1)).phase = (runMemory I c s₀ H t).phase + 1 := by
  rw [runMemory_succ I hI c s₀ H hf t, prepare_phase]
  exact advance_uncertain_increment _ _ _ _ _

theorem run_known1_persists (I : Input n k) (hI : Admissible I) (c : PositiveBody n k)
    (s₀ : State n) (H : ℕ → PublicHistory n k) (hf : Follows I hI c s₀ H) (t : ℕ)
    (hk : (runMemory I c s₀ H t).known1 = true) :
    (runMemory I c s₀ H (t+1)).known1 = true := by
  rw [runMemory_succ I hI c s₀ H hf t, prepare_known1]
  exact advance_known1_persists _ _ _ _ _ hk

theorem run_invariant (I : Input n k) (hI : Admissible I)
    (c : PositiveBody n k) (hc : BodyValid I c) (s₀ : State n) (hs₀ : s₀ ∈ c.W)
    (H : ℕ → PublicHistory n k) (hf : Follows I hI c s₀ H)
    (mode : ℕ → Mode) (hpersist : ∀ t, mode t = 1 → mode (t+1) = 1)
    (hsupport : ∀ t, 0 < I.row (mode t) (runPair I hI c s₀ H t) (observedState s₀ (H (t+1)))) :
    ∀ t, RegionValid c (observedState s₀ (H t)) (runMemory I c s₀ H t) ∧
      ((runMemory I c s₀ H t).known1 = true → mode t = 1) := by
  intro t
  induction t with
  | zero => simp [runMemory, currentMemory, hf.1, memory, RegionValid, observedState, hs₀]
  | succ t ih =>
      let m := runMemory I c s₀ H t
      let e := runPair I hI c s₀ H t
      let y := observedState s₀ (H (t+1))
      have he : e ∈ (if m.known1 then c.D1 else c.D) := compiled_action_safe I hI c hc s₀ (H t) ih.1
      have hpos : 0 < I.row (mode t) e y := hsupport t
      have hnext : (runMemory I c s₀ H (t+1)).known1 =
          (advance I e y m (rejectHistory I m.phase (augmentHistory s₀ (H (t+1))))).known1 := by
        rw [runMemory_succ I hI c s₀ H hf t, prepare_known1]
      by_cases hk : m.known1 = true
      · have hm1 := ih.2 hk
        have hD : e ∈ c.D1 := by simpa [hk] using he
        have hy : y ∈ c.K := ((mem_knownAllowed I _ _).mp (hc.1 hD)).2.2 y (hm1 ▸ hpos)
        have hnext1 : (runMemory I c s₀ H (t+1)).known1 = true := run_known1_persists I hI c s₀ H hf t hk
        exact ⟨by simpa [RegionValid, hnext1] using hy, fun _ => hpersist t hm1⟩
      · have hD : e ∈ c.D := by simpa [hk] using he
        have hsafe := (mem_uncertainAllowed I _ _ _).mp (hc.2.1 hD)
        by_cases hz : I.row 0 e y = 0
        · have hm1 : mode t = 1 := by
            have hv := (mode t).isLt
            have hne : mode t ≠ 0 := by intro h0; rw [h0,hz] at hpos; exact (lt_irrefl _ hpos)
            apply Fin.ext
            have hval : (mode t).val ≠ 0 := fun hh => hne (Fin.ext hh)
            omega
          have hy := hsafe.2.2.2 y (hm1 ▸ hpos) hz
          have hnext1 : (runMemory I c s₀ H (t+1)).known1 = true := by
            rw [hnext, advance_known1_iff]; exact Or.inr hz
          exact ⟨by simpa [RegionValid, hnext1] using hy, fun _ => hpersist t hm1⟩
        · have hP0 : 0 < I.row 0 e y := lt_of_le_of_ne (hI.1.2.2.1 0 e y) (Ne.symm hz)
          have hy := hsafe.2.2.1 y hP0
          have hnext0 : (runMemory I c s₀ H (t+1)).known1 = false := by
            apply Bool.eq_false_of_not_eq_true
            rw [hnext, advance_known1_iff]
            exact fun h => h.elim hk hz
          exact ⟨by simpa [RegionValid, hnext0] using hy, by simp [hnext0]⟩

theorem run_true_candidate_no_increment (I : Input n k) (hI : Admissible I)
    (c : PositiveBody n k) (hc : BodyValid I c) (s₀ : State n)
    (H : ℕ → PublicHistory n k) (hf : Follows I hI c s₀ H) (t : ℕ) (σ : Mode)
    (hcand : candidate (runMemory I c s₀ H t).phase = σ)
    (hpos : 0 < I.row σ (runPair I hI c s₀ H t) (observedState s₀ (H (t+1))))
    (hs : RegionValid c (observedState s₀ (H t)) (runMemory I c s₀ H t))
    (htest : rejectHistory I (runMemory I c s₀ H t).phase (augmentHistory s₀ (H (t+1))) = false) :
    (runMemory I c s₀ H (t+1)).phase = (runMemory I c s₀ H t).phase := by
  let m := runMemory I c s₀ H t
  let e := runPair I hI c s₀ H t
  let y := observedState s₀ (H (t+1))
  rw [runMemory_succ I hI c s₀ H hf t, prepare_phase]
  change (advance I e y m _).phase = m.phase
  by_cases hk : m.known1 = true
  · simp [advance, hk]
  · by_cases hz : I.row 0 e y = 0
    · simp [advance, hk, hz]
    · have hl : leaves m y = false := by
        cases hr : m.retained with
        | none => simp [leaves, hr]
        | some E =>
            have hv := (currentMemory_valid I c hc s₀ (H t)) E hr
            have hcomp : ComponentValid I c m E := hv.1
            have hg : UncertainGood I (candidate m.phase) E := by
              simp only [ComponentValid, hk, ↓reduceIte] at hcomp
              exact hcomp.2
            have heE : e ∈ E := by
              have heA : e ∈ activePairs c m := compiled_action_active I hI c hc s₀ (H t) hs
              simpa [activePairs, hr] using heA
            have hy : y ∈ usedStates Prod.fst E := hg.1.closed e heE (by
              apply Finset.mem_filter.mpr
              refine ⟨Finset.mem_univ _, ?_⟩
              simpa only [m, e, y, hcand] using hpos)
            simp [leaves,hr,hy]
      simp [advance, hk, hz, hl, htest]

/-- Only tail support is used at the true-candidate barrier. The finite old
history remains inside the actual strict test, with no support reinterpretation. -/
theorem run_phase_stabilizes (I : Input n k) (hI : Admissible I)
    (c : PositiveBody n k) (hc : BodyValid I c) (s₀ : State n)
    (H : ℕ → PublicHistory n k) (hf : Follows I hI c s₀ H) (σ : Mode) (N K : ℕ)
    (hregion : ∀ t, RegionValid c (observedState s₀ (H t)) (runMemory I c s₀ H t))
    (htail : ∀ t, N ≤ t → 0 < I.row σ (runPair I hI c s₀ H t) (observedState s₀ (H (t+1))))
    (htrue : ∀ r, K ≤ r → ∀ t, OrthemicCertificate.Direct.rationalReject I
      (OrthemicCertificate.Direct.tolerance I Finset.univ) σ r (augmentHistory s₀ (H t)) = false) :
    ∃ r, ∀ᶠ t in atTop, (runMemory I c s₀ H t).phase = r := by
  apply phase_mod_two_eventually_constant (fun t => (runMemory I c s₀ H t).phase) N K σ
  · intro t _; exact run_phase_increment I hI c s₀ H hf t
  · intro t ht hK hcan
    have hcand : candidate (runMemory I c s₀ H t).phase = σ := Fin.ext hcan
    apply run_true_candidate_no_increment I hI c hc s₀ H hf t σ hcand (htail t ht) (hregion t)
    simpa only [rejectHistory,hcand] using htrue _ hK (t+1)

end HiddenChange
