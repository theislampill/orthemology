import Availability
open AttributionKernel
example {α : Type*} [Fintype α] [DecidableEq α] (B c : ℕ)
    (hB : 1 ≤ B) (hc : 1 ≤ c) (hcm : c ≤ Fintype.card α)
    (hk : B+c-1 ≤ Fintype.card α) (F : Set (Finset α)) :
    Available B c F ↔ LabelAvailable (B+c-1) F :=
  available_iff B c hB hc hcm hk F
