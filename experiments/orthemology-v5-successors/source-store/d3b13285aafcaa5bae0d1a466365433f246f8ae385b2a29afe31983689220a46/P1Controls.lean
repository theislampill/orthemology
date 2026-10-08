import PythonExprBounds
open P02.PythonExpr

-- Guarded arithmetic and operand orientation.
example : expression [] (.binary .sub (.constant 2) (.constant 5)) ⟨none,none,0⟩ =
    .ok (0,⟨none,none,4⟩) := by rfl
example : expression [] (.binary .div (.constant 7) (.constant 2)) ⟨none,none,0⟩ =
    .ok (3,⟨none,none,4⟩) := by rfl
example : expression [] (.binary .div (.constant 9) (.constant 0)) ⟨none,none,0⟩ =
    .ok (0,⟨none,none,4⟩) := by rfl
example : expression [] (.binary .mod (.constant 9) (.constant 0)) ⟨none,none,0⟩ =
    .ok (9,⟨none,none,4⟩) := by rfl
example : expression [] (.binary .le (.constant 5) (.constant 2)) ⟨none,none,0⟩ =
    .ok (0,⟨none,none,4⟩) := by rfl
example : expression [] (.binary .eq (.constant 2) (.constant 2)) ⟨none,none,0⟩ =
    .ok (1,⟨none,none,4⟩) := by rfl

-- Register reads are intentionally unchecked, including missing=0.
example : expression [(0,2^100)] (.reg 0) ⟨some 1,some 0,0⟩ =
    .ok (2^100,⟨some 1,some 0,1⟩) := by rfl
example : expression [] (.reg 99) ⟨some 1,some 0,0⟩ =
    .ok (0,⟨some 1,some 0,1⟩) := by rfl
example : neededBits [(0,2^100)] (.reg 0) = 0 := rfl

-- Tick failure wins over tag-specific width failure; failing tick is counted.
example : expression [] (.constant 8) ⟨some 0,some 0,0⟩ =
    .error ⟨.stepLimit,1⟩ := by rfl
example : expression [] (.constant 8) ⟨none,some 3,0⟩ =
    .error ⟨.integerStorage,1⟩ := by norm_num [expression_eq_reference, reference, tick, check, power, binaryValue, Nat.size_le, dictionaryRead]
example : expression [] (.pow2 (.constant 3)) ⟨none,some 3,0⟩ =
    .error ⟨.exponentStorage,3⟩ := by norm_num [expression_eq_reference, reference, tick, check, power, binaryValue, Nat.size_le, dictionaryRead]
example : expression [] (.pow2 (.constant 3)) ⟨some 2,some 3,0⟩ =
    .error ⟨.stepLimit,3⟩ := by norm_num [expression_eq_reference, reference, tick, check, power, binaryValue, Nat.size_le, dictionaryRead]
example : expression [] (.pow2 (.constant 3)) ⟨some 3,some 4,0⟩ =
    .ok (8,⟨some 3,some 4,3⟩) := by norm_num [expression_eq_reference, reference, tick, check, power, binaryValue, Nat.size_le, dictionaryRead]
example : expression [] (.binary .add (.constant 8) (.constant 0)) ⟨none,some 3,0⟩ =
    .error ⟨.integerStorage,2⟩ := by norm_num [expression_eq_reference, reference, tick, check, power, binaryValue, Nat.size_le, dictionaryRead]

-- Shared starting count, arbitrary pending work, and dictionary overwrite.
example : expression [] (.binary .add (.constant 2) (.constant 3)) ⟨some 11,none,7⟩ =
    .ok (5,⟨some 11,none,11⟩) := by rfl
example : expression [] (.binary .add (.constant 2) (.constant 3)) ⟨some 10,none,7⟩ =
    .error ⟨.stepLimit,11⟩ := by rfl
example : dictionaryRead (dictionaryWrite [(1,4),(2,8)] 1 7) 1 = 7 := by rfl
example : dictionaryRead (dictionaryWrite [(1,4),(2,8)] 1 7) 2 = 8 := by rfl
example : runSteps [] 4 ⟨[(.binary .div (.constant 7) (.constant 2),false),
      (.constant 88,false)],[99],⟨none,none,0⟩⟩ =
    .ok ⟨[(.constant 88,false)],[3,99],⟨none,none,4⟩⟩ := by rfl

-- Only malformed ready states can cause underflow; distinct final invariant kind.
example : step [] ⟨[(.pow2 (.constant 0),true)],[],⟨none,none,0⟩⟩ =
    .error ⟨.valueStackUnderflow,1⟩ := by rfl
