import EncodedPolicyHistory
import FourBitFraming

namespace Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Orthemology.CertifiedObserver
open P02A2.PRProgram

def frameBits (σ : Bool) (a : ℕ → Bool) (q : ℕ) (b : Bool) : Fin 4 → Bool :=
  ![accepts q b,observedState (policyHistory q),a (policyHistory q),accepts q b && receipt σ (a (policyHistory q)) q b]

theorem event_bound (σ : Bool) (a : ℕ → Bool) (q : ℕ) (b : Bool) : eventCode σ a q b < 16 := by
  unfold eventCode
  generalize receipt σ (a (policyHistory q)) q b = r
  generalize accepts q b = acc
  generalize observedState (policyHistory q) = s
  generalize a (policyHistory q) = act
  cases acc <;> cases s <;> cases act <;> cases r <;> decide

theorem event_bits_exact (σ : Bool) (a : ℕ → Bool) (q : ℕ) (b : Bool) (j : Fin 4) :
    decide (eventCode σ a q b / 2^(3-j.val) % 2 = 1) = frameBits σ a q b j := by
  unfold eventCode frameBits
  generalize receipt σ (a (policyHistory q)) q b = r
  generalize accepts q b = acc
  generalize observedState (policyHistory q) = s
  generalize a (policyHistory q) = act
  fin_cases j <;> cases acc <;> cases s <;> cases act <;> cases r <;> rfl

def packFrame (c e j : ℕ) : ℕ := 64*c + 4*e + j

theorem packed_core (c e j : ℕ) (he : e < 16) (hj : j < 4) : packFrame c e j / 64 = c := by
  unfold packFrame
  omega

theorem packed_phase (c e j : ℕ) (hj : j < 4) : framePhase (packFrame c e j) = j := by
  unfold framePhase packFrame
  omega

theorem packed_pending (c e j : ℕ) (he : e < 16) (hj : j < 4) : storedFrame (packFrame c e j) = e := by
  unfold storedFrame packFrame
  omega

theorem boundary_phase (c : ℕ) : framePhase (64*c) = 0 := by simp [framePhase,Nat.mul_mod]

/-- The internal policy is called only at the beginning of a physical frame;
all remaining ticks serialize the already fixed payload. -/
theorem program_waits_skip_policy (p : Program 1) (σ : Bool) (τ : P02A2.ObserverCore.Store)
    (h : framePhase (τ 0) ≠ 0) :
    P02A2.ObserverCore.exec (nextProgram p σ).body τ = P02A2.ObserverCore.exec (nextBody σ) τ ∧
    P02A2.ObserverCore.exec (outputProgram p σ).body τ = P02A2.ObserverCore.exec (outputBody σ) τ := by
  change τ 0 % 4 ≠ 0 at h
  simp [nextProgram,outputProgram,P02A2.ObserverCore.exec,P02A2.ObserverCore.evalExpr,frameExpr,h]

/-- Four physical acquisitions correspond to one core sampling acquisition,
with exact ordered observations and an unbounded encoded-history successor. -/
theorem history_frame_exact (σ : Bool) (a : ℕ → Bool) (c : ℕ) (w : Fin 4 → Bool) :
    (machine σ a).finalState (64*c) (List.ofFn w) = 64*coreNext σ a (64*c) (w 0) ∧
    (machine σ a).outputWord (64*c) (List.ofFn w) = List.ofFn (frameBits σ a (64*c) (w 0)) := by
  let c' := coreNext σ a (64*c) (w 0)
  let e := eventCode σ a (64*c) (w 0)
  have he : e < 16 := event_bound σ a (64*c) (w 0)
  have hn0 : (machine σ a).next (64*c) (w 0) = packFrame c' e 1 := by
    simp [machine,boundary_phase,packFrame,c',e]
  have hn1 : (machine σ a).next (packFrame c' e 1) (w 1) = packFrame c' e 2 := by
    simp only [machine,packed_phase _ _ _ (by decide : 1 < 4)]
    simp [packFrame]
  have hn2 : (machine σ a).next (packFrame c' e 2) (w 2) = packFrame c' e 3 := by
    simp only [machine,packed_phase _ _ _ (by decide : 2 < 4)]
    simp [packFrame]
  have hn3 : (machine σ a).next (packFrame c' e 3) (w 3) = 64*c' := by
    simp [machine,packed_phase _ _ _ (by decide : 3 < 4),packed_core _ _ _ he (by decide : 3 < 4)]
  have ho0 : (machine σ a).out (64*c) (w 0) = frameBits σ a (64*c) (w 0) 0 := by
    simpa [machine,boundary_phase] using event_bits_exact σ a (64*c) (w 0) 0
  have ho1 : (machine σ a).out (packFrame c' e 1) (w 1) = frameBits σ a (64*c) (w 0) 1 := by
    simpa [machine,packed_phase _ _ _ (by decide : 1 < 4),packed_pending _ _ _ he (by decide : 1 < 4),e]
      using event_bits_exact σ a (64*c) (w 0) 1
  have ho2 : (machine σ a).out (packFrame c' e 2) (w 2) = frameBits σ a (64*c) (w 0) 2 := by
    simpa [machine,packed_phase _ _ _ (by decide : 2 < 4),packed_pending _ _ _ he (by decide : 2 < 4),e]
      using event_bits_exact σ a (64*c) (w 0) 2
  have ho3 : (machine σ a).out (packFrame c' e 3) (w 3) = frameBits σ a (64*c) (w 0) 3 := by
    simpa [machine,packed_phase _ _ _ (by decide : 3 < 4),packed_pending _ _ _ he (by decide : 3 < 4),e]
      using event_bits_exact σ a (64*c) (w 0) (⟨3,by decide⟩ : Fin 4)
  have hw : List.ofFn w = [w 0,w 1,w 2,w 3] := by simp [List.ofFn_succ]
  rw [hw]
  simp only [Mealy.finalState,Mealy.outputWord,hn0,hn1,hn2,hn3,ho0,ho1,ho2,ho3]
  constructor
  · rfl
  · simp [List.ofFn_succ]

/-- The actual source/runtime output decodes into the literal unbounded-history
sampler frames. No finite-memory abstraction is supplied or required. -/
theorem actual_history_frames (p : Program 1) (a : ℕ → Bool) (hp : PolicyImplements p a)
    (σ : Bool) (x : Cantor) (n : ℕ) (j : Fin 4) :
    Indexed.runtimeOutput (runtimeIndex p σ) x (4*n+j) =
      frameBits σ a (64 * state (coreMachine (fun c b => coreNext σ a (64*c) b)) 3 (decimateFour x) n)
        (x (4*n)) j := by
  rw [actual_history_runtime p a hp σ]
  exact four_frame_output (machine σ a) (fun c b => coreNext σ a (64*c) b)
    (fun c b => frameBits σ a (64*c) b) (fun c => 64*c) (history_frame_exact σ a) 3 x n j

end Orthemology.RuntimeBridge.HistoryRuntime
