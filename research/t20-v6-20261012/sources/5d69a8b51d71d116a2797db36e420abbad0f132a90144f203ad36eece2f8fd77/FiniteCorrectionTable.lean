import PolynomialTestBoundary
import ProofUniquenessControls

namespace FiniteSidecar
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive P01AC.RestrictedIdentity
open P01AC.PolynomialTestBoundary (predPR predPR_denote)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Finite lookup in the already compiled PR basis; the default is explicit. -/
def lookupPR {r : Nat} (query : PR r) : List (PR r) → PR r → PR r
  | [], fallback => fallback
  | value :: rest, fallback => ternary choosePR query value
      (lookupPR (.comp predPR (fun _ => query)) rest fallback)

def lookupValue (values : List Nat) (fallback : Nat) (n : Nat) : Nat :=
  values[n]?.getD fallback

theorem lookupPR_denote {r : Nat} (values : List (PR r)) (query fallback : PR r)
    (v : Nat → Nat) :
    (lookupPR query values fallback).denote v =
      lookupValue (values.map (fun p => p.denote v)) (fallback.denote v) (query.denote v) := by
  induction values generalizing query with
  | nil => rfl
  | cons value rest ih =>
    simp [lookupPR, ternary, PR.denote, choosePR_denote, ih, predPR_denote]
    cases hq : query.denote v <;> simp [lookupValue, hq]

/-- Two-dimensional finite table. Coordinate 0 is coarse value, 1 is local tag. -/
def tablePR (rows : List (List Nat)) (fallback : Nat := 0) : PR 2 :=
  lookupPR (.proj ⟨0, by decide⟩)
    (rows.map (fun row => lookupPR (.proj ⟨1, by decide⟩)
      (row.map (constantPR 2)) (constantPR 2 fallback)))
    (constantPR 2 fallback)

def tableValue (rows : List (List Nat)) (fallback coarse tag : Nat) : Nat :=
  lookupValue ((rows[coarse]?.getD []).map id) fallback tag

theorem tablePR_denote (rows : List (List Nat)) (fallback : Nat) (v : Nat → Nat) :
    (tablePR rows fallback).denote v = tableValue rows fallback (v 0) (v 1) := by
  simp only [tablePR, lookupPR_denote, List.map_map, Function.comp_def,
    constantPR_denote, PR.denote]
  induction rows generalizing v with
  | nil => simp [lookupValue, tableValue]
  | cons row rows ih =>
    cases h : v 0 with
    | zero => simp [lookupValue, tableValue, h]
    | succ n =>
      have hi := ih (cons n (fun i => v (i+1)))
      simpa [lookupValue, tableValue, h, cons] using hi

/-- Exact finite rows can contain arbitrary next-state, label, cost or branch codes. -/
def tabulate (coarseCount tagCount : Nat) (value : Nat → Nat → Nat) : List (List Nat) :=
  (List.range coarseCount).map (fun z => (List.range tagCount).map (value z))

theorem tabulate_value {coarseCount tagCount z k : Nat} (value : Nat → Nat → Nat)
    (hz : z < coarseCount) (hk : k < tagCount) (fallback : Nat) :
    tableValue (tabulate coarseCount tagCount value) fallback z k = value z k := by
  simp [tableValue, tabulate, lookupValue, hz, hk]

/-- The finite description produces an actual source derivation, no alternative typing. -/
theorem table_typed (rows : List (List Nat)) (fallback : Nat) :
    Has (NatCtx 2) (tablePR rows fallback).compile N := (tablePR rows fallback).compile_has

theorem table_observes (rows : List (List Nat)) (fallback : Nat)
    (η : Env) (v : Nat → Nat) (hη : EnvNat 2 η v) :
    NatObs (eval (tablePR rows fallback).compile η)
      (tableValue rows fallback (v 0) (v 1)) := by
  simpa only [tablePR_denote] using (tablePR rows fallback).compile_obs η v hη

#print axioms table_typed
#print axioms table_observes
#print axioms tabulate_value
end FiniteSidecar
