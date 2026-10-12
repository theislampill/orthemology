import ResetContinuation

open ResetContinuation

-- These signatures force uniform quantification rather than checked finite samples.
example {n : Nat} {O A : Type} (h : State (Fin n) → O)
    (T : A → State (Fin n) → State (Fin n)) (x y : State (Fin n)) :
    ContinuationEq h T x y ↔ ∀ i, (∃ d, Stage h T d i) → x i = y i := by
  rw [fin_continuation_iff_agreement]
  constructor
  · intro ha i hi
    exact ha i ((closure_iff_stage h T i).mpr hi)
  · intro ha i hi
    exact ha i ((closure_iff_stage h T i).mp hi)

example {n : Nat} {O A S : Type} (h : State (Fin n) → O)
    (T : A → State (Fin n) → State (Fin n)) (M : Summary h T S) :
    ∃ recover : S → ProjectionState h T, ∀ x, recover (M.encode x) = project h T x := by
  apply summary_factors_projection (List.ofFn (fun i : Fin n => i)) _ h T M
  intro i
  exact List.mem_ofFn.mpr ⟨i, rfl⟩

-- Edge: constant outputs retain no coordinates, regardless of total coupled actions.
theorem constant_closure_empty {I O A : Type} (o : O)
    (T : A → State I → State I) (i : I) : ¬ Closure (fun _ => o) T i := by
  intro hi
  induction hi with
  | output he =>
      obtain ⟨x, y, _, hne⟩ := he
      exact hne rfl
  | dependency a hj he ih => exact ih

-- Edge: dimension zero has one state, for arbitrary declared outputs and actions.
example {O A : Type} (h : State (Fin 0) → O)
    (T : A → State (Fin 0) → State (Fin 0)) (x y : State (Fin 0)) :
    ContinuationEq h T x y := by
  apply (fin_continuation_iff_agreement h T x y).mpr
  intro i
  exact Fin.elim0 i

namespace GuardControl

def output (x : State Bool) : Bool := x false

def guarded (_ : Unit) (x : State Bool) : State Bool :=
  fun j => if j = false then x false && !x true else x true

def left : State Bool := fun j => !j

def right : State Bool := fun _ => true

theorem same_present : output left = output right := rfl

theorem guard_not_output_essential : ¬ Essential output true := by
  rintro ⟨x, y, hother, hne⟩
  exact hne (hother false (by decide))

theorem output_essential : Essential output false := by
  refine ⟨left, (fun _ => false), ?_, ?_⟩
  · intro j hj
    cases j with
    | false => exact False.elim (hj rfl)
    | true => rfl
  · decide

theorem guard_essential : Essential (fun x => guarded () x false) true := by
  refine ⟨left, right, ?_, ?_⟩
  · intro j hj
    cases j with
    | false => rfl
    | true => exact False.elim (hj rfl)
  · decide

theorem guard_in_closure : Closure output guarded true :=
  Closure.dependency () (Closure.output output_essential) guard_essential

theorem one_step_distinguishes :
    output (run guarded [Action.coupled ()] left) ≠
      output (run guarded [Action.coupled ()] right) := by decide

theorem same_present_but_not_continuation : ¬ ContinuationEq output guarded left right := by
  intro hc
  exact one_step_distinguishes (hc [Action.coupled ()])

end GuardControl

#print axioms GuardControl.guard_in_closure
#print axioms constant_closure_empty
