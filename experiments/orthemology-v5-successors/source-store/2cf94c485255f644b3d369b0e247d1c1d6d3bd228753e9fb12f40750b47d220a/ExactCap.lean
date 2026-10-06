import CanonicalReplies
import LabelTransport

namespace CoveringKernel
open Finset
variable {α : Type*} [Fintype α] [DecidableEq α]

/-- Existence of a fixed prepared uniform family and a history-dependent policy
that hits an intact path within N attempts in every canonical maximal world.
Canonical observations include a truthful effect receipt and homogeneous full
control replies, so the lower bound remains valid when receipts are available. -/
def HasOpaqueCap (q k N : ℕ) : Prop :=
  ∃ F : Finset (Finset α), Uniform q F ∧
    ∃ π : Policy F (MacroReply Unit), ∀ T : Finset α, T.card = k →
      SuccessWithin π (canonicalObserve (fun _ _ => ()) true) T N

theorem exact_opaque_cap_iff (q k N : ℕ) (hq : q ≤ Fintype.card α)
    (hk : k ≤ Fintype.card α-q) :
    HasOpaqueCap (α := α) q k N ↔ C (Fintype.card α) (Fintype.card α-q) k ≤ N := by
  rw [← coveringNumber_eq_C]
  constructor
  · rintro ⟨F, hu, π, hcap⟩
    exact deterministic_cap_lower_bound π _ _ q k N hu
      (canonical_opaque (fun _ _ => ()) true k) hcap
  · intro hN
    obtain ⟨F, hu, π, hcap⟩ := deterministic_cap_attained q k hq hk (MacroReply Unit)
    refine ⟨F, hu, π, ?_⟩
    intro T hT
    obtain ⟨i, hi, hgood⟩ := hcap (canonicalObserve (fun _ _ => ()) true) T hT
    exact ⟨i, lt_of_lt_of_le hi hN, hgood⟩

theorem minimum_labels_cap_iff (k N : ℕ) (hm : Fintype.card α = 3*k+1) :
    HasOpaqueCap (α := α) (2*k+1) k N ↔ (3*k+1).choose k ≤ N := by
  rw [exact_opaque_cap_iff _ _ _ (by omega) (by omega), ← coveringNumber_eq_C,
    minimum_labels_exact_cap k hm]

#print axioms exact_opaque_cap_iff
#print axioms minimum_labels_cap_iff
end CoveringKernel
