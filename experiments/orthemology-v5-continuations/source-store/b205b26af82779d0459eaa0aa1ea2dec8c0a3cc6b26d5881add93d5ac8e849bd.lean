import RationalFixture
import SingletonControllerSpecialization

namespace Orthemology.RuntimeBridge.Fixture
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Orthemology.CertifiedObserver

/-- Source state; no phase, bit value, model or time is given to the selector. -/
def source (q : Fin 6) : Bool := decide (3 ≤ q.val)
def selector (s : Bool) : Bool := s

def phase (q : Fin 6) : ℕ := q.val % 3
def proposal (q : Fin 6) (b : Bool) : ℕ := 2*(phase q-1) + bitNat b

def accepts (q : Fin 6) (b : Bool) : Bool :=
  decide (phase q ≠ 0 ∧ proposal q b < 3)

def receipt (σ : Bool) (q : Fin 6) (b : Bool) : Bool :=
  decide ((if selector (source q) = σ then 2 else 1) ≤ proposal q b)

def specifiedNext (σ : Bool) (q : Fin 6) (b : Bool) : Fin 6 :=
  if phase q = 0 then ⟨(q.val+1+bitNat b)%6,Nat.mod_lt _ (by decide)⟩
  else if accepts q b then if receipt σ q b then 3 else 0
  else if source q then 3 else 0

def specifiedObserve (σ : Bool) (q : Fin 6) (b : Bool) : Fin 4 → Bool :=
  ![accepts q b,source q,selector (source q),accepts q b && receipt σ q b]

theorem core0_next_spec : coreNext0 = specifiedNext false := by
  funext q b
  fin_cases q <;> cases b <;> rfl

theorem core1_next_spec : coreNext1 = specifiedNext true := by
  funext q b
  fin_cases q <;> cases b <;> rfl

theorem core0_observe_spec : coreObserve0 = specifiedObserve false := by
  funext q b
  fin_cases q <;> cases b <;> rfl

theorem core1_observe_spec : coreObserve1 = specifiedObserve true := by
  funext q b
  fin_cases q <;> cases b <;> rfl

/-- All physical ticks, one real Boolean P02 index, and the exact frame decoder. -/
theorem runtime0_frames (x : Cantor) (n : ℕ) (j : Fin 4) :
    Indexed.runtimeOutput index0 x (4*n+j) =
      specifiedObserve false (state (coreMachine (specifiedNext false)) 0 (decimateFour x) n)
        (x (4*n)) j := by
  rw [runtime0_exact]
  have hf := four_frame_output table0 coreNext0 coreObserve0 boundary0 frame0_exact 0 x n j
  simpa only [core0_next_spec, core0_observe_spec, boundary0, Matrix.cons_val_zero] using hf

theorem runtime1_frames (x : Cantor) (n : ℕ) (j : Fin 4) :
    Indexed.runtimeOutput index1 x (4*n+j) =
      specifiedObserve true (state (coreMachine (specifiedNext true)) 0 (decimateFour x) n)
        (x (4*n)) j := by
  rw [runtime1_exact]
  have hf := four_frame_output table1 coreNext1 coreObserve1 boundary1 frame1_exact 0 x n j
  simpa only [core1_next_spec, core1_observe_spec, boundary1, Matrix.cons_val_zero] using hf

/-- The acceptance bit never re-labels its source/action with the new receipt. -/
theorem reported_action_is_old (σ : Bool) (q : Fin 6) (b : Bool) :
    specifiedObserve σ q b 2 = selector (source q) := rfl

/-- Waiting fillers are not receipts. -/
theorem wait_filler (σ : Bool) (q : Fin 6) (b : Bool) (h : accepts q b = false) :
    specifiedObserve σ q b 0 = false ∧ specifiedObserve σ q b 3 = false := by
  simp [specifiedObserve, h]

/-- Exact 1/3 acceptance interval multiplicities at the first two-bit proposal. -/
theorem initial_row0_counts :
    (Finset.univ.filter (fun w : Fin 2 → Bool =>
      accepts (specifiedNext false 0 (w 0)) (w 1) && receipt false (specifiedNext false 0 (w 0)) (w 1))).card = 1 ∧
    (Finset.univ.filter (fun w : Fin 2 → Bool =>
      accepts (specifiedNext false 0 (w 0)) (w 1))).card = 3 := by decide

theorem initial_row1_counts :
    (Finset.univ.filter (fun w : Fin 2 → Bool =>
      accepts (specifiedNext true 0 (w 0)) (w 1) && receipt true (specifiedNext true 0 (w 0)) (w 1))).card = 2 ∧
    (Finset.univ.filter (fun w : Fin 2 → Bool =>
      accepts (specifiedNext true 0 (w 0)) (w 1))).card = 3 := by decide

end Orthemology.RuntimeBridge.Fixture
