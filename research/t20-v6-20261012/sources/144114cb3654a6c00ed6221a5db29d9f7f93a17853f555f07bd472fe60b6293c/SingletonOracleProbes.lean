import GlobalParitySufficiency
noncomputable section
namespace IndependentSingletonOracle
open HiddenParity HiddenParity.Necessity
set_option maxRecDepth 100000
set_option maxHeartbeats 12000000
def half : ℚ := ⟨1,2,by decide,by decide⟩
theorem half_value : half = 1/2 := by norm_num [half,Rat.mk'_eq_divInt,Rat.divInt_eq_div]
def weight0 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 0) else (if e.2 = 0 then 0 else half)
def complement0 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 1) else (if e.2 = 0 then 1 else half)
def kernel0 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight0 e else complement0 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight0,complement0,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight0,complement0,half_value]
def priority0 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 6 else 1) else (if e.2 = 0 then 2 else 3)
def menu0 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then ∅ else {0}
theorem oracle_case_0 : winningRegion kernel0 menu0 priority0 Finset.univ = ({1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_0
def weight1 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 1) else (if e.2 = 0 then 0 else 0)
def complement1 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 0) else (if e.2 = 0 then 1 else 1)
def kernel1 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight1 e else complement1 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight1,complement1,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight1,complement1,half_value]
def priority1 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 3 else 5) else (if e.2 = 0 then 3 else 4)
def menu1 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else {0,1}
theorem oracle_case_1 : winningRegion kernel1 menu1 priority1 Finset.univ = ({1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_1
def weight2 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 0) else (if e.2 = 0 then 1 else 1)
def complement2 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 1) else (if e.2 = 0 then 0 else 0)
def kernel2 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight2 e else complement2 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight2,complement2,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight2,complement2,half_value]
def priority2 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 3 else 4) else (if e.2 = 0 then 7 else 7)
def menu2 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0} else {1}
theorem oracle_case_2 : winningRegion kernel2 menu2 priority2 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_2
def weight3 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else half) else (if e.2 = 0 then half else half)
def complement3 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else half) else (if e.2 = 0 then half else half)
def kernel3 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight3 e else complement3 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight3,complement3,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight3,complement3,half_value]
def priority3 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 0 else 7) else (if e.2 = 0 then 6 else 7)
def menu3 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then ∅ else ∅
theorem oracle_case_3 : winningRegion kernel3 menu3 priority3 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_3
def weight4 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 0) else (if e.2 = 0 then 0 else 1)
def complement4 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 1) else (if e.2 = 0 then 1 else 0)
def kernel4 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight4 e else complement4 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight4,complement4,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight4,complement4,half_value]
def priority4 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 6 else 2) else (if e.2 = 0 then 4 else 0)
def menu4 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0,1} else {0,1}
theorem oracle_case_4 : winningRegion kernel4 menu4 priority4 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_4
def weight5 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else half) else (if e.2 = 0 then half else 1)
def complement5 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else half) else (if e.2 = 0 then half else 0)
def kernel5 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight5 e else complement5 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight5,complement5,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight5,complement5,half_value]
def priority5 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 7 else 7) else (if e.2 = 0 then 2 else 7)
def menu5 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else {0}
theorem oracle_case_5 : winningRegion kernel5 menu5 priority5 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_5
def weight6 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 1) else (if e.2 = 0 then 1 else 1)
def complement6 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 0) else (if e.2 = 0 then 0 else 0)
def kernel6 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight6 e else complement6 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight6,complement6,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight6,complement6,half_value]
def priority6 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 3 else 0) else (if e.2 = 0 then 5 else 3)
def menu6 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0,1} else ∅
theorem oracle_case_6 : winningRegion kernel6 menu6 priority6 Finset.univ = ({0} : Finset (Fin 2)) := by decide
#print axioms oracle_case_6
def weight7 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 0) else (if e.2 = 0 then half else half)
def complement7 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 1) else (if e.2 = 0 then half else half)
def kernel7 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight7 e else complement7 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight7,complement7,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight7,complement7,half_value]
def priority7 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 1 else 2) else (if e.2 = 0 then 7 else 7)
def menu7 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0,1} else {1}
theorem oracle_case_7 : winningRegion kernel7 menu7 priority7 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_7
def weight8 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 0) else (if e.2 = 0 then half else half)
def complement8 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 1) else (if e.2 = 0 then half else half)
def kernel8 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight8 e else complement8 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight8,complement8,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight8,complement8,half_value]
def priority8 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 2 else 3) else (if e.2 = 0 then 5 else 7)
def menu8 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then ∅ else {0,1}
theorem oracle_case_8 : winningRegion kernel8 menu8 priority8 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_8
def weight9 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 1) else (if e.2 = 0 then half else 1)
def complement9 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 0) else (if e.2 = 0 then half else 0)
def kernel9 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight9 e else complement9 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight9,complement9,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight9,complement9,half_value]
def priority9 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 6 else 7) else (if e.2 = 0 then 2 else 1)
def menu9 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0} else {0}
theorem oracle_case_9 : winningRegion kernel9 menu9 priority9 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_9
def weight10 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else half) else (if e.2 = 0 then half else half)
def complement10 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else half) else (if e.2 = 0 then half else half)
def kernel10 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight10 e else complement10 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight10,complement10,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight10,complement10,half_value]
def priority10 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 4 else 3) else (if e.2 = 0 then 2 else 3)
def menu10 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else {1}
theorem oracle_case_10 : winningRegion kernel10 menu10 priority10 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_10
def weight11 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else half) else (if e.2 = 0 then half else half)
def complement11 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else half) else (if e.2 = 0 then half else half)
def kernel11 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight11 e else complement11 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight11,complement11,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight11,complement11,half_value]
def priority11 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 3 else 2) else (if e.2 = 0 then 4 else 2)
def menu11 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then ∅ else {0,1}
theorem oracle_case_11 : winningRegion kernel11 menu11 priority11 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_11
def weight12 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 1) else (if e.2 = 0 then 1 else half)
def complement12 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 0) else (if e.2 = 0 then 0 else half)
def kernel12 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight12 e else complement12 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight12,complement12,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight12,complement12,half_value]
def priority12 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 2 else 2) else (if e.2 = 0 then 5 else 6)
def menu12 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else ∅
theorem oracle_case_12 : winningRegion kernel12 menu12 priority12 Finset.univ = ({0} : Finset (Fin 2)) := by decide
#print axioms oracle_case_12
def weight13 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else half) else (if e.2 = 0 then 1 else 1)
def complement13 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else half) else (if e.2 = 0 then 0 else 0)
def kernel13 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight13 e else complement13 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight13,complement13,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight13,complement13,half_value]
def priority13 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 0 else 6) else (if e.2 = 0 then 0 else 3)
def menu13 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0} else {0,1}
theorem oracle_case_13 : winningRegion kernel13 menu13 priority13 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_13
def weight14 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else half) else (if e.2 = 0 then 0 else 1)
def complement14 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else half) else (if e.2 = 0 then 1 else 0)
def kernel14 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight14 e else complement14 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight14,complement14,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight14,complement14,half_value]
def priority14 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 5 else 5) else (if e.2 = 0 then 7 else 4)
def menu14 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else {0,1}
theorem oracle_case_14 : winningRegion kernel14 menu14 priority14 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_14
def weight15 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 0) else (if e.2 = 0 then half else 1)
def complement15 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 1) else (if e.2 = 0 then half else 0)
def kernel15 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight15 e else complement15 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight15,complement15,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight15,complement15,half_value]
def priority15 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 5 else 0) else (if e.2 = 0 then 5 else 3)
def menu15 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0,1} else ∅
theorem oracle_case_15 : winningRegion kernel15 menu15 priority15 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_15
def weight16 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 0) else (if e.2 = 0 then half else 0)
def complement16 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 1) else (if e.2 = 0 then half else 1)
def kernel16 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight16 e else complement16 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight16,complement16,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight16,complement16,half_value]
def priority16 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 2 else 5) else (if e.2 = 0 then 5 else 2)
def menu16 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0} else {1}
theorem oracle_case_16 : winningRegion kernel16 menu16 priority16 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_16
def weight17 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else half) else (if e.2 = 0 then 1 else 1)
def complement17 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else half) else (if e.2 = 0 then 0 else 0)
def kernel17 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight17 e else complement17 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight17,complement17,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight17,complement17,half_value]
def priority17 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 6 else 2) else (if e.2 = 0 then 1 else 2)
def menu17 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else {1}
theorem oracle_case_17 : winningRegion kernel17 menu17 priority17 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_17
def weight18 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 1) else (if e.2 = 0 then 1 else 1)
def complement18 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 0) else (if e.2 = 0 then 0 else 0)
def kernel18 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight18 e else complement18 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight18,complement18,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight18,complement18,half_value]
def priority18 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 7 else 1) else (if e.2 = 0 then 2 else 2)
def menu18 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else {1}
theorem oracle_case_18 : winningRegion kernel18 menu18 priority18 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_18
def weight19 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 1) else (if e.2 = 0 then half else 0)
def complement19 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 0) else (if e.2 = 0 then half else 1)
def kernel19 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight19 e else complement19 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight19,complement19,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight19,complement19,half_value]
def priority19 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 2 else 4) else (if e.2 = 0 then 6 else 0)
def menu19 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0} else {0}
theorem oracle_case_19 : winningRegion kernel19 menu19 priority19 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_19
def weight20 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 0) else (if e.2 = 0 then 0 else half)
def complement20 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 1) else (if e.2 = 0 then 1 else half)
def kernel20 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight20 e else complement20 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight20,complement20,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight20,complement20,half_value]
def priority20 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 7 else 2) else (if e.2 = 0 then 0 else 7)
def menu20 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0} else ∅
theorem oracle_case_20 : winningRegion kernel20 menu20 priority20 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_20
def weight21 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 1) else (if e.2 = 0 then 1 else half)
def complement21 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 0) else (if e.2 = 0 then 0 else half)
def kernel21 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight21 e else complement21 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight21,complement21,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight21,complement21,half_value]
def priority21 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 0 else 2) else (if e.2 = 0 then 0 else 7)
def menu21 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0,1} else {0}
theorem oracle_case_21 : winningRegion kernel21 menu21 priority21 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_21
def weight22 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else half) else (if e.2 = 0 then 0 else half)
def complement22 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else half) else (if e.2 = 0 then 1 else half)
def kernel22 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight22 e else complement22 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight22,complement22,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight22,complement22,half_value]
def priority22 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 3 else 3) else (if e.2 = 0 then 0 else 5)
def menu22 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then ∅ else {0,1}
theorem oracle_case_22 : winningRegion kernel22 menu22 priority22 Finset.univ = ({1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_22
def weight23 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 1) else (if e.2 = 0 then half else 1)
def complement23 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 0) else (if e.2 = 0 then half else 0)
def kernel23 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight23 e else complement23 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight23,complement23,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight23,complement23,half_value]
def priority23 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 5 else 2) else (if e.2 = 0 then 6 else 7)
def menu23 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0,1} else {0}
theorem oracle_case_23 : winningRegion kernel23 menu23 priority23 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_23
def weight24 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 0) else (if e.2 = 0 then 0 else 0)
def complement24 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 1) else (if e.2 = 0 then 1 else 1)
def kernel24 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight24 e else complement24 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight24,complement24,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight24,complement24,half_value]
def priority24 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 4 else 1) else (if e.2 = 0 then 1 else 5)
def menu24 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0,1} else ∅
theorem oracle_case_24 : winningRegion kernel24 menu24 priority24 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_24
def weight25 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 0) else (if e.2 = 0 then half else 1)
def complement25 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 1) else (if e.2 = 0 then half else 0)
def kernel25 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight25 e else complement25 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight25,complement25,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight25,complement25,half_value]
def priority25 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 1 else 4) else (if e.2 = 0 then 4 else 1)
def menu25 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0,1} else ∅
theorem oracle_case_25 : winningRegion kernel25 menu25 priority25 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_25
def weight26 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else half) else (if e.2 = 0 then 1 else 0)
def complement26 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else half) else (if e.2 = 0 then 0 else 1)
def kernel26 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight26 e else complement26 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight26,complement26,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight26,complement26,half_value]
def priority26 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 7 else 2) else (if e.2 = 0 then 1 else 5)
def menu26 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else {0}
theorem oracle_case_26 : winningRegion kernel26 menu26 priority26 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_26
def weight27 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 1) else (if e.2 = 0 then 1 else 0)
def complement27 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 0) else (if e.2 = 0 then 0 else 1)
def kernel27 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight27 e else complement27 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight27,complement27,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight27,complement27,half_value]
def priority27 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 1 else 5) else (if e.2 = 0 then 2 else 1)
def menu27 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else {0,1}
theorem oracle_case_27 : winningRegion kernel27 menu27 priority27 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_27
def weight28 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 0) else (if e.2 = 0 then 0 else half)
def complement28 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 1) else (if e.2 = 0 then 1 else half)
def kernel28 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight28 e else complement28 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight28,complement28,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight28,complement28,half_value]
def priority28 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 7 else 2) else (if e.2 = 0 then 4 else 2)
def menu28 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then ∅ else {0,1}
theorem oracle_case_28 : winningRegion kernel28 menu28 priority28 Finset.univ = ({1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_28
def weight29 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 1) else (if e.2 = 0 then half else 0)
def complement29 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 0) else (if e.2 = 0 then half else 1)
def kernel29 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight29 e else complement29 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight29,complement29,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight29,complement29,half_value]
def priority29 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 2 else 3) else (if e.2 = 0 then 1 else 5)
def menu29 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0} else {1}
theorem oracle_case_29 : winningRegion kernel29 menu29 priority29 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_29
def weight30 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 0) else (if e.2 = 0 then half else half)
def complement30 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 1) else (if e.2 = 0 then half else half)
def kernel30 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight30 e else complement30 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight30,complement30,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight30,complement30,half_value]
def priority30 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 5 else 0) else (if e.2 = 0 then 5 else 1)
def menu30 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else {1}
theorem oracle_case_30 : winningRegion kernel30 menu30 priority30 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_30
def weight31 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 0) else (if e.2 = 0 then 0 else 0)
def complement31 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 1) else (if e.2 = 0 then 1 else 1)
def kernel31 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight31 e else complement31 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight31,complement31,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight31,complement31,half_value]
def priority31 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 6 else 0) else (if e.2 = 0 then 2 else 5)
def menu31 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else {0,1}
theorem oracle_case_31 : winningRegion kernel31 menu31 priority31 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_31
def weight32 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 1) else (if e.2 = 0 then 1 else half)
def complement32 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 0) else (if e.2 = 0 then 0 else half)
def kernel32 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight32 e else complement32 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight32,complement32,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight32,complement32,half_value]
def priority32 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 4 else 2) else (if e.2 = 0 then 7 else 1)
def menu32 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else ∅
theorem oracle_case_32 : winningRegion kernel32 menu32 priority32 Finset.univ = ({0} : Finset (Fin 2)) := by decide
#print axioms oracle_case_32
def weight33 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 0) else (if e.2 = 0 then half else 0)
def complement33 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 1) else (if e.2 = 0 then half else 1)
def kernel33 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight33 e else complement33 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight33,complement33,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight33,complement33,half_value]
def priority33 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 3 else 4) else (if e.2 = 0 then 0 else 7)
def menu33 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else {0}
theorem oracle_case_33 : winningRegion kernel33 menu33 priority33 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_33
def weight34 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else half) else (if e.2 = 0 then 1 else 0)
def complement34 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else half) else (if e.2 = 0 then 0 else 1)
def kernel34 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight34 e else complement34 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight34,complement34,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight34,complement34,half_value]
def priority34 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 3 else 2) else (if e.2 = 0 then 6 else 0)
def menu34 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then ∅ else ∅
theorem oracle_case_34 : winningRegion kernel34 menu34 priority34 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_34
def weight35 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 0) else (if e.2 = 0 then 1 else 0)
def complement35 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 1) else (if e.2 = 0 then 0 else 1)
def kernel35 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight35 e else complement35 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight35,complement35,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight35,complement35,half_value]
def priority35 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 5 else 2) else (if e.2 = 0 then 2 else 0)
def menu35 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else {0}
theorem oracle_case_35 : winningRegion kernel35 menu35 priority35 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_35
def weight36 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 0) else (if e.2 = 0 then 0 else 0)
def complement36 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 1) else (if e.2 = 0 then 1 else 1)
def kernel36 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight36 e else complement36 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight36,complement36,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight36,complement36,half_value]
def priority36 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 7 else 5) else (if e.2 = 0 then 0 else 5)
def menu36 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0} else {0,1}
theorem oracle_case_36 : winningRegion kernel36 menu36 priority36 Finset.univ = ({1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_36
def weight37 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else half) else (if e.2 = 0 then half else 0)
def complement37 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else half) else (if e.2 = 0 then half else 1)
def kernel37 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight37 e else complement37 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight37,complement37,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight37,complement37,half_value]
def priority37 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 5 else 7) else (if e.2 = 0 then 1 else 2)
def menu37 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0} else ∅
theorem oracle_case_37 : winningRegion kernel37 menu37 priority37 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_37
def weight38 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else half) else (if e.2 = 0 then 1 else half)
def complement38 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else half) else (if e.2 = 0 then 0 else half)
def kernel38 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight38 e else complement38 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight38,complement38,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight38,complement38,half_value]
def priority38 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 5 else 0) else (if e.2 = 0 then 2 else 6)
def menu38 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then ∅ else {0,1}
theorem oracle_case_38 : winningRegion kernel38 menu38 priority38 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_38
def weight39 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 0) else (if e.2 = 0 then 1 else 0)
def complement39 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 1) else (if e.2 = 0 then 0 else 1)
def kernel39 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight39 e else complement39 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight39,complement39,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight39,complement39,half_value]
def priority39 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 2 else 6) else (if e.2 = 0 then 3 else 0)
def menu39 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0} else {0}
theorem oracle_case_39 : winningRegion kernel39 menu39 priority39 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_39
def weight40 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 0) else (if e.2 = 0 then 1 else 0)
def complement40 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 1) else (if e.2 = 0 then 0 else 1)
def kernel40 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight40 e else complement40 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight40,complement40,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight40,complement40,half_value]
def priority40 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 6 else 4) else (if e.2 = 0 then 6 else 0)
def menu40 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else {0,1}
theorem oracle_case_40 : winningRegion kernel40 menu40 priority40 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_40
def weight41 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else half) else (if e.2 = 0 then 1 else 0)
def complement41 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else half) else (if e.2 = 0 then 0 else 1)
def kernel41 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight41 e else complement41 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight41,complement41,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight41,complement41,half_value]
def priority41 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 5 else 3) else (if e.2 = 0 then 1 else 2)
def menu41 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0,1} else {0,1}
theorem oracle_case_41 : winningRegion kernel41 menu41 priority41 Finset.univ = ({0,1} : Finset (Fin 2)) := by decide
#print axioms oracle_case_41
def weight42 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 1) else (if e.2 = 0 then half else 1)
def complement42 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 0) else (if e.2 = 0 then half else 0)
def kernel42 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight42 e else complement42 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight42,complement42,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight42,complement42,half_value]
def priority42 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 1 else 5) else (if e.2 = 0 then 5 else 1)
def menu42 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else {0,1}
theorem oracle_case_42 : winningRegion kernel42 menu42 priority42 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_42
def weight43 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else half) else (if e.2 = 0 then 0 else half)
def complement43 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else half) else (if e.2 = 0 then 1 else half)
def kernel43 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight43 e else complement43 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight43,complement43,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight43,complement43,half_value]
def priority43 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 0 else 5) else (if e.2 = 0 then 0 else 4)
def menu43 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then ∅ else {1}
theorem oracle_case_43 : winningRegion kernel43 menu43 priority43 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_43
def weight44 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 1) else (if e.2 = 0 then half else 1)
def complement44 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else 0) else (if e.2 = 0 then half else 0)
def kernel44 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight44 e else complement44 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight44,complement44,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight44,complement44,half_value]
def priority44 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 1 else 3) else (if e.2 = 0 then 2 else 0)
def menu44 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {1} else {1}
theorem oracle_case_44 : winningRegion kernel44 menu44 priority44 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_44
def weight45 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else half) else (if e.2 = 0 then half else half)
def complement45 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else half) else (if e.2 = 0 then half else half)
def kernel45 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight45 e else complement45 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight45,complement45,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight45,complement45,half_value]
def priority45 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 4 else 3) else (if e.2 = 0 then 7 else 2)
def menu45 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then ∅ else ∅
theorem oracle_case_45 : winningRegion kernel45 menu45 priority45 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_45
def weight46 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else half) else (if e.2 = 0 then 0 else half)
def complement46 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then half else half) else (if e.2 = 0 then 1 else half)
def kernel46 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight46 e else complement46 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight46,complement46,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight46,complement46,half_value]
def priority46 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 5 else 4) else (if e.2 = 0 then 3 else 1)
def menu46 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0} else ∅
theorem oracle_case_46 : winningRegion kernel46 menu46 priority46 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_46
def weight47 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 0 else 1) else (if e.2 = 0 then 0 else 0)
def complement47 (e : Fin 2 × Fin 2) : ℚ := if e.1 = 0 then (if e.2 = 0 then 1 else 0) else (if e.2 = 0 then 1 else 1)
def kernel47 : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where
  row := fun _ e y => if y = 0 then weight47 e else complement47 e
  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight47,complement47,half_value]
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight47,complement47,half_value]
def priority47 (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := if e.1 = 0 then (if e.2 = 0 then 5 else 1) else (if e.2 = 0 then 5 else 3)
def menu47 (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {0} else {1}
theorem oracle_case_47 : winningRegion kernel47 menu47 priority47 Finset.univ = (∅ : Finset (Fin 2)) := by decide
#print axioms oracle_case_47
end IndependentSingletonOracle
