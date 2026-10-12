import GlobalParitySufficiency
noncomputable section
namespace IndependentHiddenIdenticalOracle
open HiddenParity HiddenParity.Necessity
set_option maxRecDepth 100000
set_option maxHeartbeats 12000000
def kernel : RationalKernel (Fin 2) (Fin 1 × Fin 3) (Fin 1) where
  row := fun _ _ _ => 1
  nonnegative := by intros; norm_num
  normalized := by intros; simp
def priority0 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 2 else if e.2 = 1 then 3 else 1) else (if e.2 = 0 then 3 else if e.2 = 1 then 2 else 1)
def menu0 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1}
theorem hidden_oracle_case_0 : winningRegion kernel menu0 priority0 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_0
def priority1 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 2 else if e.2 = 1 then 1 else 1) else (if e.2 = 0 then 1 else if e.2 = 1 then 2 else 1)
def menu1 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1}
theorem hidden_oracle_case_1 : winningRegion kernel menu1 priority1 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_1
def priority2 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 5 else if e.2 = 1 then 3 else 2) else (if e.2 = 0 then 5 else if e.2 = 1 then 4 else 5)
def menu2 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {1,2}
theorem hidden_oracle_case_2 : winningRegion kernel menu2 priority2 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_2
def priority3 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 5 else if e.2 = 1 then 1 else 2) else (if e.2 = 0 then 0 else if e.2 = 1 then 4 else 1)
def menu3 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,2}
theorem hidden_oracle_case_3 : winningRegion kernel menu3 priority3 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_3
def priority4 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 0 else if e.2 = 1 then 5 else 1) else (if e.2 = 0 then 1 else if e.2 = 1 then 5 else 3)
def menu4 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0}
theorem hidden_oracle_case_4 : winningRegion kernel menu4 priority4 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_4
def priority5 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 5 else if e.2 = 1 then 0 else 4) else (if e.2 = 0 then 4 else if e.2 = 1 then 0 else 4)
def menu5 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {1,2}
theorem hidden_oracle_case_5 : winningRegion kernel menu5 priority5 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_5
def priority6 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 5 else if e.2 = 1 then 3 else 1) else (if e.2 = 0 then 4 else if e.2 = 1 then 1 else 2)
def menu6 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := ∅
theorem hidden_oracle_case_6 : winningRegion kernel menu6 priority6 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_6
def priority7 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 2 else if e.2 = 1 then 0 else 1) else (if e.2 = 0 then 5 else if e.2 = 1 then 4 else 2)
def menu7 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1}
theorem hidden_oracle_case_7 : winningRegion kernel menu7 priority7 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_7
def priority8 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 3 else if e.2 = 1 then 0 else 2) else (if e.2 = 0 then 2 else if e.2 = 1 then 4 else 2)
def menu8 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1,2}
theorem hidden_oracle_case_8 : winningRegion kernel menu8 priority8 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_8
def priority9 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 3 else if e.2 = 1 then 2 else 2) else (if e.2 = 0 then 1 else if e.2 = 1 then 2 else 1)
def menu9 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0}
theorem hidden_oracle_case_9 : winningRegion kernel menu9 priority9 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_9
def priority10 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 2 else if e.2 = 1 then 5 else 1) else (if e.2 = 0 then 3 else if e.2 = 1 then 2 else 2)
def menu10 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {2}
theorem hidden_oracle_case_10 : winningRegion kernel menu10 priority10 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_10
def priority11 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 0 else if e.2 = 1 then 3 else 3) else (if e.2 = 0 then 2 else if e.2 = 1 then 0 else 3)
def menu11 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {2}
theorem hidden_oracle_case_11 : winningRegion kernel menu11 priority11 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_11
def priority12 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 4 else if e.2 = 1 then 0 else 5) else (if e.2 = 0 then 0 else if e.2 = 1 then 5 else 2)
def menu12 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {1,2}
theorem hidden_oracle_case_12 : winningRegion kernel menu12 priority12 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_12
def priority13 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 0 else if e.2 = 1 then 1 else 4) else (if e.2 = 0 then 1 else if e.2 = 1 then 0 else 4)
def menu13 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,2}
theorem hidden_oracle_case_13 : winningRegion kernel menu13 priority13 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_13
def priority14 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 4 else if e.2 = 1 then 3 else 4) else (if e.2 = 0 then 0 else if e.2 = 1 then 4 else 4)
def menu14 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0}
theorem hidden_oracle_case_14 : winningRegion kernel menu14 priority14 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_14
def priority15 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 1 else if e.2 = 1 then 1 else 5) else (if e.2 = 0 then 1 else if e.2 = 1 then 5 else 5)
def menu15 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1}
theorem hidden_oracle_case_15 : winningRegion kernel menu15 priority15 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_15
def priority16 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 4 else if e.2 = 1 then 3 else 2) else (if e.2 = 0 then 1 else if e.2 = 1 then 4 else 1)
def menu16 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1,2}
theorem hidden_oracle_case_16 : winningRegion kernel menu16 priority16 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_16
def priority17 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 3 else if e.2 = 1 then 1 else 5) else (if e.2 = 0 then 1 else if e.2 = 1 then 2 else 4)
def menu17 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {2}
theorem hidden_oracle_case_17 : winningRegion kernel menu17 priority17 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_17
def priority18 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 2 else if e.2 = 1 then 5 else 5) else (if e.2 = 0 then 1 else if e.2 = 1 then 4 else 3)
def menu18 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {1,2}
theorem hidden_oracle_case_18 : winningRegion kernel menu18 priority18 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_18
def priority19 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 1 else if e.2 = 1 then 3 else 2) else (if e.2 = 0 then 4 else if e.2 = 1 then 3 else 0)
def menu19 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0}
theorem hidden_oracle_case_19 : winningRegion kernel menu19 priority19 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_19
def priority20 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 0 else if e.2 = 1 then 3 else 2) else (if e.2 = 0 then 2 else if e.2 = 1 then 2 else 2)
def menu20 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {1}
theorem hidden_oracle_case_20 : winningRegion kernel menu20 priority20 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_20
def priority21 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 5 else if e.2 = 1 then 5 else 1) else (if e.2 = 0 then 0 else if e.2 = 1 then 3 else 1)
def menu21 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1,2}
theorem hidden_oracle_case_21 : winningRegion kernel menu21 priority21 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_21
def priority22 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 1 else if e.2 = 1 then 2 else 3) else (if e.2 = 0 then 5 else if e.2 = 1 then 1 else 5)
def menu22 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {2}
theorem hidden_oracle_case_22 : winningRegion kernel menu22 priority22 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_22
def priority23 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 3 else if e.2 = 1 then 3 else 5) else (if e.2 = 0 then 1 else if e.2 = 1 then 5 else 1)
def menu23 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {1}
theorem hidden_oracle_case_23 : winningRegion kernel menu23 priority23 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_23
def priority24 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 4 else if e.2 = 1 then 1 else 4) else (if e.2 = 0 then 0 else if e.2 = 1 then 4 else 3)
def menu24 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1}
theorem hidden_oracle_case_24 : winningRegion kernel menu24 priority24 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_24
def priority25 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 5 else if e.2 = 1 then 5 else 4) else (if e.2 = 0 then 3 else if e.2 = 1 then 0 else 1)
def menu25 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := ∅
theorem hidden_oracle_case_25 : winningRegion kernel menu25 priority25 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_25
def priority26 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 5 else if e.2 = 1 then 5 else 2) else (if e.2 = 0 then 3 else if e.2 = 1 then 0 else 4)
def menu26 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1,2}
theorem hidden_oracle_case_26 : winningRegion kernel menu26 priority26 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_26
def priority27 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 0 else if e.2 = 1 then 2 else 0) else (if e.2 = 0 then 0 else if e.2 = 1 then 2 else 5)
def menu27 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1}
theorem hidden_oracle_case_27 : winningRegion kernel menu27 priority27 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_27
def priority28 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 4 else if e.2 = 1 then 4 else 3) else (if e.2 = 0 then 5 else if e.2 = 1 then 2 else 3)
def menu28 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {1,2}
theorem hidden_oracle_case_28 : winningRegion kernel menu28 priority28 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_28
def priority29 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 3 else if e.2 = 1 then 3 else 2) else (if e.2 = 0 then 3 else if e.2 = 1 then 1 else 2)
def menu29 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1}
theorem hidden_oracle_case_29 : winningRegion kernel menu29 priority29 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_29
def priority30 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 4 else if e.2 = 1 then 1 else 1) else (if e.2 = 0 then 3 else if e.2 = 1 then 2 else 3)
def menu30 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1,2}
theorem hidden_oracle_case_30 : winningRegion kernel menu30 priority30 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_30
def priority31 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 5 else if e.2 = 1 then 1 else 0) else (if e.2 = 0 then 5 else if e.2 = 1 then 1 else 4)
def menu31 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0}
theorem hidden_oracle_case_31 : winningRegion kernel menu31 priority31 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_31
def priority32 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 5 else if e.2 = 1 then 4 else 1) else (if e.2 = 0 then 1 else if e.2 = 1 then 1 else 4)
def menu32 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {2}
theorem hidden_oracle_case_32 : winningRegion kernel menu32 priority32 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_32
def priority33 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 2 else if e.2 = 1 then 1 else 3) else (if e.2 = 0 then 2 else if e.2 = 1 then 1 else 5)
def menu33 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {1,2}
theorem hidden_oracle_case_33 : winningRegion kernel menu33 priority33 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_33
def priority34 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 3 else if e.2 = 1 then 2 else 3) else (if e.2 = 0 then 1 else if e.2 = 1 then 2 else 0)
def menu34 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0}
theorem hidden_oracle_case_34 : winningRegion kernel menu34 priority34 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_34
def priority35 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 2 else if e.2 = 1 then 2 else 2) else (if e.2 = 0 then 4 else if e.2 = 1 then 1 else 3)
def menu35 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := ∅
theorem hidden_oracle_case_35 : winningRegion kernel menu35 priority35 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_35
def priority36 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 1 else if e.2 = 1 then 1 else 4) else (if e.2 = 0 then 4 else if e.2 = 1 then 0 else 4)
def menu36 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0}
theorem hidden_oracle_case_36 : winningRegion kernel menu36 priority36 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_36
def priority37 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 3 else if e.2 = 1 then 3 else 2) else (if e.2 = 0 then 3 else if e.2 = 1 then 4 else 5)
def menu37 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := ∅
theorem hidden_oracle_case_37 : winningRegion kernel menu37 priority37 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_37
def priority38 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 1 else if e.2 = 1 then 3 else 1) else (if e.2 = 0 then 0 else if e.2 = 1 then 5 else 1)
def menu38 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1,2}
theorem hidden_oracle_case_38 : winningRegion kernel menu38 priority38 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_38
def priority39 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 5 else if e.2 = 1 then 1 else 2) else (if e.2 = 0 then 1 else if e.2 = 1 then 2 else 0)
def menu39 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {1}
theorem hidden_oracle_case_39 : winningRegion kernel menu39 priority39 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_39
def priority40 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 2 else if e.2 = 1 then 2 else 5) else (if e.2 = 0 then 3 else if e.2 = 1 then 4 else 1)
def menu40 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,2}
theorem hidden_oracle_case_40 : winningRegion kernel menu40 priority40 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_40
def priority41 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 4 else if e.2 = 1 then 5 else 1) else (if e.2 = 0 then 1 else if e.2 = 1 then 3 else 3)
def menu41 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := ∅
theorem hidden_oracle_case_41 : winningRegion kernel menu41 priority41 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_41
def priority42 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 4 else if e.2 = 1 then 2 else 4) else (if e.2 = 0 then 5 else if e.2 = 1 then 0 else 2)
def menu42 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {1}
theorem hidden_oracle_case_42 : winningRegion kernel menu42 priority42 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_42
def priority43 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 3 else if e.2 = 1 then 0 else 2) else (if e.2 = 0 then 4 else if e.2 = 1 then 0 else 2)
def menu43 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,2}
theorem hidden_oracle_case_43 : winningRegion kernel menu43 priority43 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_43
def priority44 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 1 else if e.2 = 1 then 4 else 5) else (if e.2 = 0 then 2 else if e.2 = 1 then 2 else 0)
def menu44 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {1,2}
theorem hidden_oracle_case_44 : winningRegion kernel menu44 priority44 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_44
def priority45 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 1 else if e.2 = 1 then 0 else 2) else (if e.2 = 0 then 5 else if e.2 = 1 then 2 else 2)
def menu45 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1}
theorem hidden_oracle_case_45 : winningRegion kernel menu45 priority45 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_45
def priority46 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 3 else if e.2 = 1 then 4 else 2) else (if e.2 = 0 then 1 else if e.2 = 1 then 3 else 3)
def menu46 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,2}
theorem hidden_oracle_case_46 : winningRegion kernel menu46 priority46 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_46
def priority47 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 4 else if e.2 = 1 then 0 else 2) else (if e.2 = 0 then 2 else if e.2 = 1 then 1 else 5)
def menu47 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1}
theorem hidden_oracle_case_47 : winningRegion kernel menu47 priority47 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_47
def priority48 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 3 else if e.2 = 1 then 5 else 5) else (if e.2 = 0 then 3 else if e.2 = 1 then 3 else 0)
def menu48 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {1,2}
theorem hidden_oracle_case_48 : winningRegion kernel menu48 priority48 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_48
def priority49 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 2 else if e.2 = 1 then 2 else 0) else (if e.2 = 0 then 2 else if e.2 = 1 then 2 else 0)
def menu49 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {1}
theorem hidden_oracle_case_49 : winningRegion kernel menu49 priority49 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_49
def priority50 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 1 else if e.2 = 1 then 4 else 1) else (if e.2 = 0 then 1 else if e.2 = 1 then 4 else 2)
def menu50 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := ∅
theorem hidden_oracle_case_50 : winningRegion kernel menu50 priority50 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_50
def priority51 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 3 else if e.2 = 1 then 0 else 2) else (if e.2 = 0 then 3 else if e.2 = 1 then 5 else 1)
def menu51 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1,2}
theorem hidden_oracle_case_51 : winningRegion kernel menu51 priority51 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_51
def priority52 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 2 else if e.2 = 1 then 4 else 1) else (if e.2 = 0 then 3 else if e.2 = 1 then 4 else 1)
def menu52 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1}
theorem hidden_oracle_case_52 : winningRegion kernel menu52 priority52 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_52
def priority53 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 1 else if e.2 = 1 then 2 else 0) else (if e.2 = 0 then 5 else if e.2 = 1 then 3 else 3)
def menu53 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {1}
theorem hidden_oracle_case_53 : winningRegion kernel menu53 priority53 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_53
def priority54 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 2 else if e.2 = 1 then 2 else 4) else (if e.2 = 0 then 1 else if e.2 = 1 then 2 else 4)
def menu54 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := ∅
theorem hidden_oracle_case_54 : winningRegion kernel menu54 priority54 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_54
def priority55 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 5 else if e.2 = 1 then 5 else 2) else (if e.2 = 0 then 4 else if e.2 = 1 then 5 else 1)
def menu55 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {2}
theorem hidden_oracle_case_55 : winningRegion kernel menu55 priority55 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_55
def priority56 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 2 else if e.2 = 1 then 1 else 2) else (if e.2 = 0 then 5 else if e.2 = 1 then 0 else 2)
def menu56 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1,2}
theorem hidden_oracle_case_56 : winningRegion kernel menu56 priority56 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_56
def priority57 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 5 else if e.2 = 1 then 3 else 3) else (if e.2 = 0 then 2 else if e.2 = 1 then 5 else 4)
def menu57 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,2}
theorem hidden_oracle_case_57 : winningRegion kernel menu57 priority57 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_57
def priority58 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 1 else if e.2 = 1 then 0 else 5) else (if e.2 = 0 then 0 else if e.2 = 1 then 2 else 0)
def menu58 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {2}
theorem hidden_oracle_case_58 : winningRegion kernel menu58 priority58 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_58
def priority59 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 2 else if e.2 = 1 then 3 else 5) else (if e.2 = 0 then 0 else if e.2 = 1 then 0 else 4)
def menu59 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,2}
theorem hidden_oracle_case_59 : winningRegion kernel menu59 priority59 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_59
def priority60 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 0 else if e.2 = 1 then 0 else 3) else (if e.2 = 0 then 5 else if e.2 = 1 then 0 else 5)
def menu60 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,2}
theorem hidden_oracle_case_60 : winningRegion kernel menu60 priority60 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_60
def priority61 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 2 else if e.2 = 1 then 1 else 0) else (if e.2 = 0 then 3 else if e.2 = 1 then 1 else 5)
def menu61 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0}
theorem hidden_oracle_case_61 : winningRegion kernel menu61 priority61 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_61
def priority62 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 4 else if e.2 = 1 then 3 else 4) else (if e.2 = 0 then 4 else if e.2 = 1 then 5 else 5)
def menu62 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,2}
theorem hidden_oracle_case_62 : winningRegion kernel menu62 priority62 Finset.univ = (Finset.univ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_62
def priority63 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 1 else if e.2 = 1 then 1 else 3) else (if e.2 = 0 then 3 else if e.2 = 1 then 4 else 5)
def menu63 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0}
theorem hidden_oracle_case_63 : winningRegion kernel menu63 priority63 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_63
def priority64 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 0 else if e.2 = 1 then 0 else 4) else (if e.2 = 0 then 0 else if e.2 = 1 then 1 else 5)
def menu64 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {1,2}
theorem hidden_oracle_case_64 : winningRegion kernel menu64 priority64 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_64
def priority65 (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then (if e.2 = 0 then 0 else if e.2 = 1 then 5 else 4) else (if e.2 = 0 then 1 else if e.2 = 1 then 5 else 1)
def menu65 (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {0,1,2}
theorem hidden_oracle_case_65 : winningRegion kernel menu65 priority65 Finset.univ = (∅ : Finset (Fin 1)) := by decide
#print axioms hidden_oracle_case_65
end IndependentHiddenIdenticalOracle
