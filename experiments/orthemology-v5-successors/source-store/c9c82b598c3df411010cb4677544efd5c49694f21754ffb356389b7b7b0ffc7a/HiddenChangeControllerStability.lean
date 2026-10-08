import HiddenChangeControllerDynamics
import HiddenChangeControllerGraphs

set_option maxHeartbeats 800000
open Filter
namespace HiddenChange
open HiddenParity HiddenParity.Sufficiency HiddenParity.PhaseArithmetic
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
variable {n k : ℕ}

@[simp] theorem prepare_retained_of_some (c : PositiveBody n k) (s : State n)
    (m : ControllerMemory n k) (E : PairSet n k) (he : m.retained = some E) :
    prepare c s m = m := by simp [prepare, he]

theorem run_known_retained_no_exit (I : Input n k) (hI : Admissible I)
    (c : PositiveBody n k) (hc : BodyValid I c) (s : State n)
    (H : ℕ → PublicHistory n k) (t : ℕ)
    (hs : RegionValid c (observedState s (H t)) (runMemory I c s H t))
    (hk : (runMemory I c s H t).known1 = true)
    (hpos : 0 < I.row 1 (runPair I hI c s H t) (observedState s (H (t+1)))) :
    leaves (runMemory I c s H t) (observedState s (H (t+1))) = false := by
  cases he : (runMemory I c s H t).retained with
  | none => simp [leaves, he]
  | some E =>
      have hm := (currentMemory_valid I c hc s (H t)) E he
      have hcpt : ComponentValid I c (runMemory I c s H t) E := hm.1
      have hg : E ⊆ c.D1 ∧ KnownGood I E := by
        simpa only [ComponentValid, hk, ↓reduceIte] using hcpt
      have ha : runPair I hI c s H t ∈ E := by
        have h := compiled_action_active I hI c hc s (H t) hs
        change runPair I hI c s H t ∈ activePairs c (runMemory I c s H t) at h
        simpa [activePairs,he] using h
      have hy := hg.2.1.closed _ ha (Finset.mem_filter.mpr ⟨Finset.mem_univ _,hpos⟩)
      simp [leaves, he, hy]

theorem run_retention_persists (I : Input n k) (hI : Admissible I)
    (c : PositiveBody n k) (hc : BodyValid I c) (s : State n)
    (H : ℕ → PublicHistory n k) (hf : Follows I hI c s H) (t : ℕ)
    (hs : RegionValid c (observedState s (H t)) (runMemory I c s H t))
    (hpos : (runMemory I c s H t).known1 = true →
      0 < I.row 1 (runPair I hI c s H t) (observedState s (H (t+1))))
    (hphase : (runMemory I c s H (t+1)).phase = (runMemory I c s H t).phase)
    (hknown : (runMemory I c s H (t+1)).known1 = (runMemory I c s H t).known1)
    (E : PairSet n k) (he : (runMemory I c s H t).retained = some E) :
    (runMemory I c s H (t+1)).retained = some E := by
  let m := runMemory I c s H t
  let e := runPair I hI c s H t
  let y := observedState s (H (t+1))
  let b := rejectHistory I m.phase (augmentHistory s (H (t+1)))
  have hn : runMemory I c s H (t+1) = prepare c y (advance I e y m b) :=
    runMemory_succ I hI c s H hf t
  by_cases hk : m.known1 = true
  · have hl := run_known_retained_no_exit I hI c hc s H t hs hk (hpos hk)
    have ha : advance I e y m b = m := by
      change leaves m y = false at hl
      unfold advance
      rw [if_pos hk]
      simp only [hl, Bool.false_eq_true, ↓reduceIte]
    rw [hn, ha, prepare_retained_of_some c y m E he]
    exact he
  · by_cases hz : I.row 0 e y = 0
    · have hh : (runMemory I c s H (t+1)).known1 = true := by
        rw [hn, prepare_known1, advance_known1_iff]; exact Or.inr hz
      exact (hk (hknown ▸ hh)).elim
    · by_cases hb : (b || leaves m y) = true
      · have hh : (runMemory I c s H (t+1)).phase = m.phase + 1 := by
          rw [hn, prepare_phase]
          simp [advance,hk,hz,hb]
        have hbad : m.phase + 1 = m.phase := hh.symm.trans hphase
        omega
      · have ha : advance I e y m b = m := by simp [advance,hk,hz,hb]
        rw [hn, ha, prepare_retained_of_some c y m E he]
        exact he

theorem run_layer_stabilizes (I : Input n k) (hI : Admissible I)
    (c : PositiveBody n k) (s : State n) (H : ℕ → PublicHistory n k)
    (hf : Follows I hI c s H) :
    ∃ b : Bool, ∀ᶠ t in atTop, (runMemory I c s H t).known1 = b := by
  by_cases h : ∃ t, (runMemory I c s H t).known1 = true
  · obtain ⟨T,hT⟩ := h
    refine ⟨true, eventually_atTop.mpr ⟨T, ?_⟩⟩
    intro t ht
    induction t,ht using Nat.le_induction with
    | base => exact hT
    | succ t _ ih => exact run_known1_persists I hI c s H hf t ih
  · exact ⟨false, Filter.Eventually.of_forall (fun t => Bool.eq_false_of_not_eq_true
      (fun ht => h ⟨t,ht⟩))⟩

theorem run_layer_phase_component_stabilizes (I : Input n k) (hI : Admissible I)
    (c : PositiveBody n k) (hc : BodyValid I c) (s : State n)
    (H : ℕ → PublicHistory n k) (hf : Follows I hI c s H)
    (hregion : ∀ t, RegionValid c (observedState s (H t)) (runMemory I c s H t))
    (hknownpos : ∀ t, (runMemory I c s H t).known1 = true →
      0 < I.row 1 (runPair I hI c s H t) (observedState s (H (t+1))))
    (hphase : ∃ r, ∀ᶠ t in atTop, (runMemory I c s H t).phase = r) :
    ∃ b : Bool, ∃ r : ℕ,
      (∀ᶠ t in atTop, (runMemory I c s H t).known1 = b) ∧
      (∀ᶠ t in atTop, (runMemory I c s H t).phase = r) ∧
      ((∀ᶠ t in atTop, (runMemory I c s H t).retained = none) ∨
        ∃ E, ∀ᶠ t in atTop, (runMemory I c s H t).retained = some E) := by
  obtain ⟨b,hb⟩ := run_layer_stabilizes I hI c s H hf
  obtain ⟨N,hN⟩ := eventually_atTop.mp hb
  obtain ⟨r,hr,hret⟩ := eventual_phase_and_mode_stable
    (fun t => (runMemory I c s H t).phase) (fun t => (runMemory I c s H t).retained) N hphase (by
      intro t ht hph E he
      apply run_retention_persists I hI c hc s H hf t (hregion t) (hknownpos t) hph
      · exact (hN (t+1) (by omega)).trans (hN t ht).symm
      · exact he)
  exact ⟨b,r,hb,hr,hret⟩

theorem run_visits (I : Input n k) (hI : Admissible I) (c : PositiveBody n k)
    (s : State n) (H : ℕ → PublicHistory n k) (hf : Follows I hI c s H) (u : State n) :
    ∀ t, historyVisits s u (H t) = visitsBefore (fun j => (runPair I hI c s H j).1) u t := by
  intro t
  induction t with
  | zero => simp [hf.1, historyVisits, visitsBefore]
  | succ t ih =>
      rw [hf.2 t]
      simp only [historyVisits, ih, visitsBefore]
      rfl

theorem run_cycle (I : Input n k) (hI : Admissible I)
    (c : PositiveBody n k) (hc : BodyValid I c) (s : State n)
    (H : ℕ → PublicHistory n k) (hf : Follows I hI c s H) (t : ℕ)
    (hs : RegionValid c (observedState s (H t)) (runMemory I c s H t))
    (fallback : Action k) :
    (runPair I hI c s H t).2 = OrthemicCertificate.Direct.cycleAction
      (retainedActions (activePairs c (runMemory I c s H t)) (runPair I hI c s H t).1)
      fallback (visitsBefore (fun j => (runPair I hI c s H j).1) (runPair I hI c s H t).1 t) := by
  letI : Inhabited (State n) := ⟨s⟩
  have hm := currentMemory_valid I c hc s (H t)
  have hv := valid_activePairs I c hc _ _ hm hs
  have hne := retainedActions_nonempty _ _ hv.2
  change compile I hI s c () (H t) = _
  dsimp only [compile]
  rw [actionMenu_eq I c hc _ _ hm hs, run_visits I hI c s H hf]
  simp only [runPair, runMemory, OrthemicCertificate.Direct.cycleAction, dif_pos hne]

theorem prepare_none_avoids (c : PositiveBody n k) (s : State n) (m : ControllerMemory n k)
    (h : (prepare c s m).retained = none) :
    s ∉ componentTargets (availableComponents c (prepare c s m)) := by
  apply (firstContaining_none_iff _ _).mp
  have ha : availableComponents c (prepare c s m) = availableComponents c m := by
    simp only [availableComponents,prepare_known1,prepare_phase]
  rw [ha]
  cases he : m.retained with
  | none => simpa [prepare,he] using h
  | some E => simp [prepare,he] at h

theorem run_false_no_revelation (I : Input n k) (hI : Admissible I)
    (c : PositiveBody n k) (s : State n) (H : ℕ → PublicHistory n k)
    (hf : Follows I hI c s H) (t : ℕ)
    (hnext : (runMemory I c s H (t+1)).known1 = false) :
    I.row 0 (runPair I hI c s H t) (observedState s (H (t+1))) ≠ 0 := by
  intro hz
  have hh : (runMemory I c s H (t+1)).known1 = true := by
    rw [runMemory_succ I hI c s H hf t, prepare_known1, advance_known1_iff]
    exact Or.inr hz
  rw [hnext] at hh
  contradiction

theorem run_stable_false_not_rejected (I : Input n k) (hI : Admissible I)
    (c : PositiveBody n k) (s : State n) (H : ℕ → PublicHistory n k)
    (hf : Follows I hI c s H) (t : ℕ)
    (hk : (runMemory I c s H t).known1 = false)
    (hnext : (runMemory I c s H (t+1)).known1 = false)
    (hphase : (runMemory I c s H (t+1)).phase = (runMemory I c s H t).phase) :
    rejectHistory I (runMemory I c s H t).phase (augmentHistory s (H (t+1))) = false := by
  have hz := run_false_no_revelation I hI c s H hf t hnext
  apply Bool.eq_false_of_not_eq_true
  intro hb
  have hph : (runMemory I c s H (t+1)).phase = (runMemory I c s H t).phase+1 := by
    rw [runMemory_succ I hI c s H hf t,prepare_phase]
    simp [advance,hk,hz,hb]
  omega

end HiddenChange
