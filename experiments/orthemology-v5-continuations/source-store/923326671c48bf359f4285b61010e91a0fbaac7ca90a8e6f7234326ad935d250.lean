import ObservationChannels

namespace Orthemology.RuntimeBridge
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Orthemology.CertifiedObserver
variable {S Q : Type*}

def coreMachine (next : Q → Bool → Q) : Mealy Q where
  next := next
  out _ _ := false

def decimateFour (x : Cantor) : Cantor := fun n => x (4*n)

/-- A local four-acquisition frame certificate yields exact state simulation
for every infinite physical tape, including ignored bits and null stalled tapes. -/
theorem four_frame_state (M : Mealy S) (next : Q → Bool → Q)
    (obs : Q → Bool → Fin 4 → Bool) (boundary : Q → S)
    (frame : ∀ (q : Q) (w : Fin 4 → Bool), M.finalState (boundary q) (List.ofFn w) = boundary (next q (w 0)) ∧
      M.outputWord (boundary q) (List.ofFn w) = List.ofFn (obs q (w 0)))
    (q : Q) (x : Cantor) (n : ℕ) :
    state M (boundary q) x (4*n) =
      boundary (state (coreMachine next) q (decimateFour x) n) := by
  induction n with
  | zero => rfl
  | succ n ih =>
      rw [Nat.mul_add, Nat.mul_one, state_add, ih, ← state_prefix]
      have hf := (frame (state (coreMachine next) q (decimateFour x) n)
        (fun j : Fin 4 => x (4*n+j))).1
      simpa only [pref, shift, Fin.val_zero, Nat.add_zero, state, coreMachine, decimateFour] using hf

/-- Exact ordered data/ack frame, not independent coordinate marginal laws.
Only the first bit of each four-bit input frame is passed to the core. -/
theorem four_frame_output (M : Mealy S) (next : Q → Bool → Q)
    (obs : Q → Bool → Fin 4 → Bool) (boundary : Q → S)
    (frame : ∀ (q : Q) (w : Fin 4 → Bool), M.finalState (boundary q) (List.ofFn w) = boundary (next q (w 0)) ∧
      M.outputWord (boundary q) (List.ofFn w) = List.ofFn (obs q (w 0)))
    (q : Q) (x : Cantor) (n : ℕ) (j : Fin 4) :
    output M (boundary q) x (4*n+j) =
      obs (state (coreMachine next) q (decimateFour x) n) (x (4*n)) j := by
  have hf := (frame (state (coreMachine next) q (decimateFour x) n)
    (fun j : Fin 4 => x (4*n+j))).2
  change M.outputWord (boundary (state (coreMachine next) q (decimateFour x) n))
    (pref 4 (shift (4*n) x)) = _ at hf
  rw [output_prefix, ← four_frame_state M next obs boundary frame q x n, ← output_shift] at hf
  exact congrFun (List.ofFn_inj.mp hf) j

end Orthemology.RuntimeBridge
