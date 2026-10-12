import FiniteTable

namespace GuardedTree.Executable.Controls
open Executable

/-- Ambient evidence is infinite, but this grammar uses no token. -/
def cycle : Grammar Unit Nat Unit where
  arity := fun _ => 1
  head := fun _ => ()
  premise := fun _ _ => ()
  localSupport := fun _ => ∅
  price := fun _ => 0
  guard := fun _ _ => True
instance : ∀ r s, Decidable (cycle.guard r s) := fun _ _ => isTrue trivial

/-- A nullary seed, and a zero-cost unary cycle. -/
def seeded : Grammar Unit Nat Bool where
  arity := fun r => if r then 1 else 0
  head := fun _ => ()
  premise := fun _ _ => ()
  localSupport := fun _ => ∅
  price := fun _ => 0
  guard := fun _ _ => True
instance : ∀ r s, Decidable (seeded.guard r s) := fun _ _ => isTrue trivial

def blocked : Grammar Unit Nat Unit where
  arity := fun _ => 0
  head := fun _ => ()
  premise := fun _ _ => ()
  localSupport := fun _ => ∅
  price := fun _ => 0
  guard := fun _ _ => False
instance : ∀ r s, Decidable (blocked.guard r s) := fun _ _ => isFalse id

/-- Three nullary A states include a free empty support. B needs supports
[{0},{1}] in this order. C needs two occurrences of [{0}]. -/
def ordered : Grammar (Fin 3) Nat (Fin 5) where
  arity := fun r => if r.val < 3 then 0 else 2
  head := fun r => if r.val < 3 then 0 else if r.val = 3 then 1 else 2
  premise := fun _ _ => 0
  localSupport := fun r => if r.val = 0 then {0} else if r.val = 1 then {1} else ∅
  price := fun r => if r.val = 0 then 1/2 else if r.val = 1 then 1/3
    else if r.val = 2 then 0 else 1/6
  guard := fun r s =>
    if h : r.val < 3 then True else
      if r.val = 3 then
        s ⟨0, by simp [h]⟩ = {0} ∧ s ⟨1, by simp [h]⟩ = {1}
      else s ⟨0, by simp [h]⟩ = {0} ∧ s ⟨1, by simp [h]⟩ = {0}
instance : ∀ r s, Decidable (ordered.guard r s) := by
  intro r s
  unfold ordered
  infer_instance

/-- Same keys at rounds 1 and 2, but an old price falls from 10 to 1. -/
def priceDrop : Grammar (Fin 2) Nat (Fin 3) where
  arity := fun r => if r.val = 2 then 1 else 0
  head := fun r => if r.val = 0 then 0 else 1
  premise := fun _ _ => 0
  localSupport := fun _ => ∅
  price := fun r => if r.val = 1 then 10 else if r.val = 2 then 1 else 0
  guard := fun _ _ => True
instance : ∀ r s, Decidable (priceDrop.guard r s) := fun _ _ => isTrue trivial

/-- A negative unary price demonstrates why global stopping needs nonnegativity. -/
def decreasing : Grammar Unit Nat Bool where
  arity := fun r => if r then 1 else 0
  head := fun _ => ()
  premise := fun _ _ => ()
  localSupport := fun _ => ∅
  price := fun r => if r then -1 else 0
  guard := fun _ _ => True
instance : ∀ r s, Decidable (decreasing.guard r s) := fun _ _ => isTrue trivial

#eval read (compileRounds cycle 4) () ∅
#eval read (compile seeded) () ∅
#eval read (compile blocked) () ∅
#eval read (compileRounds ordered 2) 1 {0,1}
#eval read (compileRounds ordered 2) 2 {0}
#eval read (compileRounds ordered 2) 1 ∅
#eval read (compileRounds priceDrop 1) 1 ∅
#eval read (compileRounds priceDrop 2) 1 ∅

/-- Check results at runtime without turning the evaluator into a proof oracle. -/
def check (label : String) (actual expected : Option ℚ) : IO Unit := do
  unless actual == expected do
    throw (IO.userError s!"{label}: got {actual}, expected {expected}")
  IO.println s!"PASS {label}: {actual}"

def runChecks : IO Unit := do
  check "unsupported cycle" (read (compileRounds cycle 4) () ∅) none
  check "nullary plus zero cycle" (read (compile seeded) () ∅) (some 0)
  check "blocked nullary" (read (compile blocked) () ∅) none
  check "ordered exact supports" (read (compileRounds ordered 2) 1 {0,1}) (some 1)
  check "repeated occurrences" (read (compileRounds ordered 2) 2 {0}) (some (7/6))
  check "cannot shrink guarded support" (read (compileRounds ordered 2) 1 ∅) none
  check "old price" (read (compileRounds priceDrop 1) 1 ∅) (some 10)
  check "improved price" (read (compileRounds priceDrop 2) 1 ∅) (some 1)
  let good : Fin (ordered.arity 3) → Finset Nat := fun i => if i.val = 0 then {0} else {1}
  let reversed : Fin (ordered.arity 3) → Finset Nat := fun i => if i.val = 0 then {1} else {0}
  unless decide (ordered.guard 3 good) do throw (IO.userError "correct order rejected")
  if decide (ordered.guard 3 reversed) then throw (IO.userError "reversed order accepted")
  IO.println "PASS position-sensitive guard: true / false"
  unless compileRounds priceDrop 1 != compileRounds priceDrop 2 do
    throw (IO.userError "price improvement lost")
  unless (compileRounds priceDrop 1).image Prod.fst == (compileRounds priceDrop 2).image Prod.fst do
    throw (IO.userError "price-drop control keys unexpectedly changed")
  IO.println "PASS same keys, different full tables"
  unless compileRounds ordered (grammarBound ordered + 1) == compile ordered do
    throw (IO.userError "post-bound table differs")
  IO.println "PASS post-bound full-table equality"
  check "negative price round one" (read (compileRounds decreasing 1) () ∅) (some 0)
  check "negative price round two" (read (compileRounds decreasing 2) () ∅) (some (-1))
  check "external unused token" (read (compileRounds ordered 2) 0 {999}) none
  check "retain cheap empty state" (read (compileRounds ordered 2) 0 ∅) (some 0)
  check "retain dearer exact state" (read (compileRounds ordered 2) 0 {0}) (some (1/2))


#eval runChecks

end GuardedTree.Executable.Controls
