import PolicyTranscriptFiber
import PolicyRowLaw

namespace Orthemology.Tranche2.PolicyEmbeddingAudit
open Orthemology.Tranche2.PolicyEmbedding

theorem selected_ignores_stack {R A Y : Type*}
    (π : R → History A Y → A) (r : R) (h : History A Y) (X Z : Stack A Y) :
    selected π (r,(X,h)) = selected π (r,(Z,h)) := rfl

/-- Stored outside-U stacks do not affect the actual observed history. This
does not assert equality of the full traces, which retain the whole stack. -/
theorem observedHistory_stack_noninterference
    {R A Y : Type*} [DecidableEq A] [Inhabited Y]
    (U : Finset A) (π : R → History A Y → A) (oracle : ℕ → A → Y)
    (r : R) (X Z : Stack A Y) (hXZ : ∀ a ∈ U, ∀ n, X a n = Z a n) (n : ℕ) :
    observedHistory U π oracle r X n = observedHistory U π oracle r Z n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [observedHistory, ih]
    by_cases h : π r (observedHistory U π oracle r Z n) ∈ U
    · simp [feedback, h, hXZ _ h]
    · simp [feedback, h]

def Xzero : Stack Bool Bool := fun _ _ => false
def Xoutside : Stack Bool Bool := fun a _ => a
def zeroOracle : ℕ → Bool → Bool := fun _ _ => false
def alwaysFalse : Unit → History Bool Bool → Bool := fun _ _ => false
def goodU : Finset Bool := {false}

theorem unused_stack_same_observations (n : ℕ) :
    observedHistory goodU alwaysFalse zeroOracle () Xzero n =
      observedHistory goodU alwaysFalse zeroOracle () Xoutside n := by
  apply observedHistory_stack_noninterference
  intro a ha k
  have ha' : a = false := by simpa [goodU] using ha
  simp [Xzero,Xoutside,ha']

/-- The generic full-state trace still exposes the unused stack in its initial
state. Therefore model-specific unused-stack laws cannot be substituted into
the theorem's one common initial-law parameter. -/
theorem unused_stack_different_full_traces :
    policyRun goodU alwaysFalse zeroOracle () Xzero ≠
      policyRun goodU alwaysFalse zeroOracle () Xoutside := by
  intro h
  have bad := congrArg (fun t => (t 0).1.2.1 true 0) h
  cases bad

def leakingSelector (s : EvalState Unit Bool Bool) : Bool := s.2.1 true 0

/-- A selector that reads an unobserved stack entry cannot be represented by
the packet's seed/history-only policy interface. -/
theorem leaked_stack_not_representable :
    ¬ ∃ π : Unit → History Bool Bool → Bool,
      ∀ X : Stack Bool Bool, selected π ((),(X,[])) = leakingSelector ((),(X,[])) := by
  rintro ⟨π,hπ⟩
  have h0 := hπ Xzero
  have h1 := hπ Xoutside
  have bad : false = true := h0.symm.trans h1
  cases bad

theorem three_inside_actions_zero_queries :
    (policyRun goodU alwaysFalse zeroOracle () Xzero 3).2 = 0 := by decide

theorem three_outside_actions_three_queries :
    (policyRun (∅ : Finset Bool) alwaysFalse zeroOracle () Xzero 3).2 = 3 := by decide

theorem pre_action_counter_initially_zero :
    (policyRun (∅ : Finset Bool) alwaysFalse zeroOracle () Xzero 0).2 = 0 := rfl

#print axioms selected_ignores_stack
#print axioms observedHistory_stack_noninterference
#print axioms unused_stack_same_observations
#print axioms unused_stack_different_full_traces
#print axioms leaked_stack_not_representable
#print axioms three_inside_actions_zero_queries
#print axioms three_outside_actions_three_queries
#print axioms pre_action_counter_initially_zero

end Orthemology.Tranche2.PolicyEmbeddingAudit
