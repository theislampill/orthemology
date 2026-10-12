import CheckerStateObservation

namespace PDChecker
noncomputable section
open scoped ENNReal

variable {m : ℕ} {Q Γ : Type*} [DecidableEq Γ]

/-- Every checker updates exactly its own coordinate of the same complete tape.
This is a one-step invariant, not a formal ATM language or strategy reduction. -/
theorem honest_running_step (M : Machine Q Γ) (tape : Fin m → Γ) (q q' : Q)
    (h h' : Fin m) (choice branch : Bool)
    (hin : checkedHead m ((h:ℕ)+(M.step q (tape h) branch).shift)=some h')
    (hnext : (M.step q (tape h) branch).next=.running q') (i : Fin m) :
    advance M (initialAt tape q h i) (tape h,choice) branch=
      initialAt (Function.update tape h (M.step q (tape h) branch).write) q' h' i := by
  rw [initialAt,advance_running M i (tape i) q h h' (tape h,choice) branch q'
    (by intro hi;subst i;rfl) hin hnext]
  simp [initialAt,Function.update_apply,eq_comm]

/-- A truthful step's public receipt is checker-independent, including terminal merging. -/
theorem honest_branch_receipt (M : Machine Q Γ) (tape : Fin m → Γ) (q : Q)
    (h : Fin m) (choice branch : Bool) (i j : Fin m) :
    (branchOutput M (initialAt tape q h i) (tape h,choice) branch).1=
      (branchOutput M (initialAt tape q h j) (tape h,choice) branch).1 := by
  have hi : ¬(i=h ∧ tape i≠tape h) := by rintro ⟨rfl,hh⟩;exact hh rfl
  have hj : ¬(j=h ∧ tape j≠tape h) := by rintro ⟨rfl,hh⟩;exact hh rfl
  simp only [branchOutput,initialAt,isUniversal,advance,hi,hj,if_false,Prod.fst]
  cases hh : checkedHead m ((h:ℕ)+(M.step q (tape h) branch).shift) with
  | none => simp [hh,emit]
  | some h' =>
    cases hc : (M.step q (tape h) branch).next <;> simp [hh,hc,emit]

/-- Equality of actual receipt PMFs follows from the constructed fair/point-mass rows. -/
theorem honest_receipt_law (M : Machine Q Γ) (tape : Fin m → Γ) (q : Q)
    (h : Fin m) (choice : Bool) (i j : Fin m) :
    PMF.map Prod.fst (kernel M (initialAt tape q h i) (tape h,choice))=
      PMF.map Prod.fst (kernel M (initialAt tape q h j) (tape h,choice)) := by
  simp only [kernel,initialAt,isUniversal]
  split
  · rw [PMF.map_comp,PMF.map_comp]
    congr 1
    funext branch
    exact honest_branch_receipt M tape q h choice branch i j
  · rw [PMF.pure_map,PMF.pure_map]
    congr 1
    exact honest_branch_receipt M tape q h choice choice i j

end
end PDChecker
