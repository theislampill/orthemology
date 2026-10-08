import RootImage
open AttributionKernel
example {α : Type*} [Fintype α] [DecidableEq α] (B c : ℕ)
    (hB : 1 ≤ B) (hc : 1 ≤ c) (hcm : c ≤ Fintype.card α)
    (P R : Finset α) : Robust B c P R ↔ B+c ≤ (P ∩ R).card :=
  robust_iff B c hB hc hcm P R
