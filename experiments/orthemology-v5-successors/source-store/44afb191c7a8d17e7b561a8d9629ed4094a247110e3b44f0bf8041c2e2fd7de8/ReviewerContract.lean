import PythonExprSafety

namespace IndependentPythonReview
open P02.PythonExpr

/-- The local result may be followed by arbitrary further modeled work. -/
theorem continuation_composition (d : Dictionary) (e : PyExpr) (m : Meter)
    (tail : List (PyExpr × Bool)) (vs : List ℕ) (n : ℕ) :
    runSteps d (cost e+n) ⟨(e,false)::tail,vs,m⟩ = (do
      let (v,out) ← reference d e m
      runSteps d n ⟨tail,v::vs,out⟩) := by
  rw [runSteps_add, expression_stack_exact]
  cases reference d e m with
  | error err => rfl
  | ok pair => cases pair; rfl

/-- Failure correspondence does not erase either the fault category or tick. -/
theorem failure_pair_exact (d : Dictionary) (e : PyExpr) (m : Meter)
    (tail : List (PyExpr × Bool)) (vs : List ℕ) (err : Failure)
    (h : reference d e m = .error err) :
    runSteps d (cost e) ⟨(e,false)::tail,vs,m⟩ = .error err := by
  rw [expression_stack_exact, h]
  rfl

/-- Finite-budget completion is available to a consumer without an extra axiom. -/
theorem finite_witness (d : Dictionary) (e : PyExpr) (s : ℕ) :
    ∃ limit bits out, expression d e ⟨some limit,some bits,s⟩ =
      .ok (P02A2.ObserverCore.evalExpr (lower e) (dictionaryRead d),out) := by
  exact ⟨s+cost e,neededBits d e,_,expression_complete_finite d e s⟩

/-- All successful budgets compute the same extensional semantic result. -/
theorem success_uniqueness (d : Dictionary) (e : PyExpr) (m₁ m₂ o₁ o₂ : Meter)
    (v₁ v₂ : ℕ) (h₁ : expression d e m₁ = .ok (v₁,o₁))
    (h₂ : expression d e m₂ = .ok (v₂,o₂)) : v₁=v₂ :=
  (expression_success_sound _ _ _ _ _ h₁).trans
    (expression_success_sound _ _ _ _ _ h₂).symm

example : expression [] (.constant 0) ⟨some 1,some 0,0⟩ =
    .ok (0,⟨some 1,some 0,1⟩) := by norm_num [expression_eq_reference, reference, tick, check, power, binaryValue, Nat.size_le, dictionaryRead]
example : expression [] (.constant 1) ⟨none,some 0,0⟩ =
    .error ⟨.integerStorage,1⟩ := by norm_num [expression_eq_reference, reference, tick, check, power, binaryValue, Nat.size_le, dictionaryRead]
example : expression [] (.constant 1) ⟨some 0,some 0,0⟩ =
    .error ⟨.stepLimit,1⟩ := by rfl
example : expression [(9,1024)] (.reg 9) ⟨none,some 0,7⟩ =
    .ok (1024,⟨none,some 0,8⟩) := by rfl
example : expression [(9,1024)] (.reg 10) ⟨none,some 0,7⟩ =
    .ok (0,⟨none,some 0,8⟩) := by rfl
example : expression [] (.binary .sub (.constant 8) (.constant 3)) ⟨none,none,5⟩ =
    .ok (5,⟨none,none,9⟩) := by rfl
example : expression [] (.binary .sub (.constant 3) (.constant 8)) ⟨none,none,5⟩ =
    .ok (0,⟨none,none,9⟩) := by rfl
example : expression [] (.binary .div (.constant 8) (.constant 3)) ⟨none,none,0⟩ =
    .ok (2,⟨none,none,4⟩) := by rfl
example : expression [] (.binary .div (.constant 8) (.constant 0)) ⟨none,none,0⟩ =
    .ok (0,⟨none,none,4⟩) := by rfl
example : expression [] (.binary .mod (.constant 8) (.constant 0)) ⟨none,none,0⟩ =
    .ok (8,⟨none,none,4⟩) := by rfl
example : expression [] (.binary .le (.constant 8) (.constant 8)) ⟨none,none,0⟩ =
    .ok (1,⟨none,none,4⟩) := by rfl
example : expression [] (.binary .eq (.constant 8) (.constant 9)) ⟨none,none,0⟩ =
    .ok (0,⟨none,none,4⟩) := by rfl
example : expression [(0,8)] (.binary .mul (.reg 0) (.reg 0)) ⟨none,some 3,0⟩ =
    .error ⟨.integerStorage,4⟩ := by norm_num [expression_eq_reference, reference, tick, check, power, binaryValue, Nat.size_le, dictionaryRead]
example : expression [(0,8)] (.binary .add (.reg 0) (.reg 0)) ⟨some 3,some 3,0⟩ =
    .error ⟨.stepLimit,4⟩ := by rfl
example : expression [(0,8)] (.pow2 (.reg 0)) ⟨none,some 8,0⟩ =
    .error ⟨.exponentStorage,3⟩ := by rfl
example : expression [(0,8)] (.pow2 (.reg 0)) ⟨none,some 9,0⟩ =
    .ok (256,⟨none,some 9,3⟩) := by rfl
example : expression [(0,8)] (.pow2 (.reg 0)) ⟨some 2,some 8,0⟩ =
    .error ⟨.stepLimit,3⟩ := by rfl
example : expression [] (.binary .add (.pow2 (.constant 1)) (.constant 8))
    ⟨none,some 1,0⟩ = .error ⟨.exponentStorage,4⟩ := by norm_num [expression_eq_reference, reference, tick, check, power, binaryValue, Nat.size_le, dictionaryRead]
example : expression [] (.binary .add (.constant 8) (.pow2 (.constant 1)))
    ⟨none,some 1,0⟩ = .error ⟨.integerStorage,2⟩ := by norm_num [expression_eq_reference, reference, tick, check, power, binaryValue, Nat.size_le, dictionaryRead]
example : step [] ⟨[(.pow2 (.constant 0),true)],[],⟨some 0,none,0⟩⟩ =
    .error ⟨.stepLimit,1⟩ := by rfl
example : step [] ⟨[(.pow2 (.constant 0),true)],[],⟨none,none,0⟩⟩ =
    .error ⟨.valueStackUnderflow,1⟩ := by rfl
example : step [] ⟨[(.constant 3,true)],[91],⟨none,none,0⟩⟩ =
    .ok ⟨[],[3,91],⟨none,none,1⟩⟩ := by rfl
example : step [] ⟨[],[91],⟨some 0,some 0,12⟩⟩ =
    .ok ⟨[],[91],⟨some 0,some 0,12⟩⟩ := by rfl
example : runSteps [] 1 ⟨[(.constant 0,false),(.pow2 (.constant 0),true)],
    [31,79],⟨none,none,0⟩⟩ =
    .ok ⟨[(.pow2 (.constant 0),true)],[0,31,79],⟨none,none,1⟩⟩ := by rfl
example : dictionaryRead (dictionaryWrite [(3,1),(3,8),(4,9)] 3 6) 3 = 6 := by rfl
example : dictionaryRead (dictionaryWrite [(3,1),(3,8),(4,9)] 3 6) 4 = 9 := by rfl
example : neededBits [(9,1024)] (.reg 9) = 0 := by rfl
example : cost (.binary .sub (.pow2 (.constant 3)) (.constant 2)) = 6 := by rfl

#print axioms continuation_composition
#print axioms failure_pair_exact
#print axioms finite_witness
#print axioms success_uniqueness
end IndependentPythonReview
