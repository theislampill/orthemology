import FourBitFraming
set_option maxRecDepth 20000
set_option maxHeartbeats 5000000
namespace Orthemology.RuntimeBridge.Fixture
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02.Codec Orthemology.CertifiedObserver
def table0 : Mealy (Fin 36) where
  next q b := match q.val with
    | 0 => if b then 2 else 1
    | 1 => if b then 3 else 3
    | 2 => if b then 4 else 4
    | 3 => if b then 5 else 5
    | 4 => if b then 6 else 6
    | 5 => if b then 7 else 7
    | 6 => if b then 8 else 8
    | 7 => if b then 9 else 9
    | 8 => if b then 11 else 10
    | 9 => if b then 12 else 12
    | 10 => if b then 13 else 13
    | 11 => if b then 14 else 14
    | 12 => if b then 15 else 15
    | 13 => if b then 16 else 16
    | 14 => if b then 17 else 17
    | 15 => if b then 0 else 0
    | 16 => if b then 18 else 18
    | 17 => if b then 0 else 0
    | 18 => if b then 20 else 19
    | 19 => if b then 21 else 21
    | 20 => if b then 22 else 22
    | 21 => if b then 23 else 23
    | 22 => if b then 24 else 24
    | 23 => if b then 25 else 25
    | 24 => if b then 26 else 26
    | 25 => if b then 28 else 27
    | 26 => if b then 29 else 28
    | 27 => if b then 30 else 30
    | 28 => if b then 31 else 31
    | 29 => if b then 32 else 32
    | 30 => if b then 33 else 33
    | 31 => if b then 34 else 34
    | 32 => if b then 35 else 35
    | 33 => if b then 0 else 0
    | 34 => if b then 18 else 18
    | 35 => if b then 18 else 18
    | _ => 0
  out q b := match q.val with
    | 0 => if b then false else false
    | 1 => if b then false else false
    | 2 => if b then false else false
    | 3 => if b then false else false
    | 4 => if b then false else false
    | 5 => if b then false else false
    | 6 => if b then false else false
    | 7 => if b then true else true
    | 8 => if b then false else true
    | 9 => if b then false else false
    | 10 => if b then false else false
    | 11 => if b then false else false
    | 12 => if b then false else false
    | 13 => if b then false else false
    | 14 => if b then false else false
    | 15 => if b then false else false
    | 16 => if b then true else true
    | 17 => if b then false else false
    | 18 => if b then false else false
    | 19 => if b then true else true
    | 20 => if b then true else true
    | 21 => if b then true else true
    | 22 => if b then true else true
    | 23 => if b then false else false
    | 24 => if b then false else false
    | 25 => if b then true else true
    | 26 => if b then false else true
    | 27 => if b then true else true
    | 28 => if b then true else true
    | 29 => if b then true else true
    | 30 => if b then true else true
    | 31 => if b then true else true
    | 32 => if b then true else true
    | 33 => if b then false else false
    | 34 => if b then true else true
    | 35 => if b then false else false
    | _ => false
def index0 : ℕ := index table0 0
theorem runtime0_exact : Indexed.runtimeOutput index0 = output table0 0 := compiled_runtime_output _ _
#eval IO.println ("[" ++ String.intercalate "," ((encodeBytes (compiled table0 0)).map toString) ++ "]")
#eval index0
def boundary0 : Fin 6 → Fin 36 := ![0,7,8,18,25,26]
def coreNext0 (q : Fin 6) (b : Bool) : Fin 6 := (![![1,2],![0,0],![3,0],![4,5],![0,3],![3,3]] : Fin 6 → Fin 2 → Fin 6) q (if b then 1 else 0)
def coreObserve0 (q : Fin 6) (b : Bool) : Fin 4 → Bool := (![![![false,false,false,false],![false,false,false,false]],![![true,false,false,false],![true,false,false,false]],![![true,false,false,true],![false,false,false,false]],![![false,true,true,false],![false,true,true,false]],![![true,true,true,false],![true,true,true,true]],![![true,true,true,true],![false,true,true,false]]] : Fin 6 → Fin 2 → Fin 4 → Bool) q (if b then 1 else 0)
theorem frame0_exact : ∀ q : Fin 6, ∀ w : Fin 4 → Bool,
    (table0).finalState (boundary0 q) (List.ofFn w) = boundary0 (coreNext0 q (w 0)) ∧
    (table0).outputWord (boundary0 q) (List.ofFn w) = List.ofFn (coreObserve0 q (w 0)) := by
  intro q w
  have hw : w = ![w 0,w 1,w 2,w 3] := by funext i; fin_cases i <;> rfl
  rw [hw]
  generalize w 0 = b0
  generalize w 1 = b1
  generalize w 2 = b2
  generalize w 3 = b3
  cases b0 <;> cases b1 <;> cases b2 <;> cases b3 <;> fin_cases q <;> exact ⟨rfl,rfl⟩
def table1 : Mealy (Fin 36) where
  next q b := match q.val with
    | 0 => if b then 2 else 1
    | 1 => if b then 3 else 3
    | 2 => if b then 4 else 4
    | 3 => if b then 5 else 5
    | 4 => if b then 6 else 6
    | 5 => if b then 7 else 7
    | 6 => if b then 8 else 8
    | 7 => if b then 10 else 9
    | 8 => if b then 11 else 10
    | 9 => if b then 12 else 12
    | 10 => if b then 13 else 13
    | 11 => if b then 14 else 14
    | 12 => if b then 15 else 15
    | 13 => if b then 16 else 16
    | 14 => if b then 17 else 17
    | 15 => if b then 0 else 0
    | 16 => if b then 18 else 18
    | 17 => if b then 0 else 0
    | 18 => if b then 20 else 19
    | 19 => if b then 21 else 21
    | 20 => if b then 22 else 22
    | 21 => if b then 23 else 23
    | 22 => if b then 24 else 24
    | 23 => if b then 25 else 25
    | 24 => if b then 26 else 26
    | 25 => if b then 27 else 27
    | 26 => if b then 29 else 28
    | 27 => if b then 30 else 30
    | 28 => if b then 31 else 31
    | 29 => if b then 32 else 32
    | 30 => if b then 33 else 33
    | 31 => if b then 34 else 34
    | 32 => if b then 35 else 35
    | 33 => if b then 0 else 0
    | 34 => if b then 18 else 18
    | 35 => if b then 18 else 18
    | _ => 0
  out q b := match q.val with
    | 0 => if b then false else false
    | 1 => if b then false else false
    | 2 => if b then false else false
    | 3 => if b then false else false
    | 4 => if b then false else false
    | 5 => if b then false else false
    | 6 => if b then false else false
    | 7 => if b then true else true
    | 8 => if b then false else true
    | 9 => if b then false else false
    | 10 => if b then false else false
    | 11 => if b then false else false
    | 12 => if b then false else false
    | 13 => if b then false else false
    | 14 => if b then false else false
    | 15 => if b then false else false
    | 16 => if b then true else true
    | 17 => if b then false else false
    | 18 => if b then false else false
    | 19 => if b then true else true
    | 20 => if b then true else true
    | 21 => if b then true else true
    | 22 => if b then true else true
    | 23 => if b then false else false
    | 24 => if b then false else false
    | 25 => if b then true else true
    | 26 => if b then false else true
    | 27 => if b then true else true
    | 28 => if b then true else true
    | 29 => if b then true else true
    | 30 => if b then true else true
    | 31 => if b then true else true
    | 32 => if b then true else true
    | 33 => if b then false else false
    | 34 => if b then true else true
    | 35 => if b then false else false
    | _ => false
def index1 : ℕ := index table1 0
theorem runtime1_exact : Indexed.runtimeOutput index1 = output table1 0 := compiled_runtime_output _ _
#eval IO.println ("[" ++ String.intercalate "," ((encodeBytes (compiled table1 0)).map toString) ++ "]")
#eval index1
def boundary1 : Fin 6 → Fin 36 := ![0,7,8,18,25,26]
def coreNext1 (q : Fin 6) (b : Bool) : Fin 6 := (![![1,2],![0,3],![3,0],![4,5],![0,0],![3,3]] : Fin 6 → Fin 2 → Fin 6) q (if b then 1 else 0)
def coreObserve1 (q : Fin 6) (b : Bool) : Fin 4 → Bool := (![![![false,false,false,false],![false,false,false,false]],![![true,false,false,false],![true,false,false,true]],![![true,false,false,true],![false,false,false,false]],![![false,true,true,false],![false,true,true,false]],![![true,true,true,false],![true,true,true,false]],![![true,true,true,true],![false,true,true,false]]] : Fin 6 → Fin 2 → Fin 4 → Bool) q (if b then 1 else 0)
theorem frame1_exact : ∀ q : Fin 6, ∀ w : Fin 4 → Bool,
    (table1).finalState (boundary1 q) (List.ofFn w) = boundary1 (coreNext1 q (w 0)) ∧
    (table1).outputWord (boundary1 q) (List.ofFn w) = List.ofFn (coreObserve1 q (w 0)) := by
  intro q w
  have hw : w = ![w 0,w 1,w 2,w 3] := by funext i; fin_cases i <;> rfl
  rw [hw]
  generalize w 0 = b0
  generalize w 1 = b1
  generalize w 2 = b2
  generalize w 3 = b3
  cases b0 <;> cases b1 <;> cases b2 <;> cases b3 <;> fin_cases q <;> exact ⟨rfl,rfl⟩
end Orthemology.RuntimeBridge.Fixture
