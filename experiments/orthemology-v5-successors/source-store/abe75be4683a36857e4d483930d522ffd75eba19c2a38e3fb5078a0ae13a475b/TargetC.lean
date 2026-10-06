import FixedFamilies
open AttributionKernel
example {α : Type*} [Fintype α] [DecidableEq α] (B c : ℕ)
    (hB : 1 ≤ B) (hc : 1 ≤ c) (hcm : c ≤ Fintype.card α)
    (hBn : B < Fintype.card α-c+1) :
    (∃ F G : Set (Finset α), FixedFamilyContract B c F G) ↔
      3*(B+c-1)+1 ≤ Fintype.card α :=
  fixed_family_feasible_iff B c hB hc hcm hBn
