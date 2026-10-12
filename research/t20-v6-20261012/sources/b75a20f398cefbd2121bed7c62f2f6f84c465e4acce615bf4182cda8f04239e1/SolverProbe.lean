import MealySolverFixtures

open Orthemology.Frontier Orthemology.Frontier.MealyMeasure

def smallMachine (m : ℕ) (hm : 0 < m) (code : ℕ) : Mealy (Fin m) where
  next q b :=
    let e := (code / (2*m)^(2*q.val + if b then 1 else 0)) % (2*m)
    ⟨e / 2, by have h := Nat.mod_lt (code / (2*m)^(2*q.val + if b then 1 else 0)) (by omega : 0 < 2*m); dsimp [e]; omega⟩
  out q b :=
    let e := (code / (2*m)^(2*q.val + if b then 1 else 0)) % (2*m)
    e % 2 == 1

def main : IO Unit := do
  for code in List.range 4 do
    let d := solveDefect (smallMachine 1 (by decide) code) 0
    IO.println s!"1,{code},{d.num},{d.den}"
  for code in List.range 256 do
    let d := solveDefect (smallMachine 2 (by decide) code) 0
    IO.println s!"2,{code},{d.num},{d.den}"
