import ActionDisclosure

/-! A stipulated finite repair semantics. This binds the code theorem to its
    announced action contract; it does not authenticate that contract in a
    physical or metaphysical subject. -/
namespace Orthemology.ActionDisclosure

inductive RepairState where
  | pending | restored | ruined
  deriving DecidableEq

variable {R M : Type*} [DecidableEq R] [Fintype M]

def destructiveStep (corrupt : Finset R) (root : R) : RepairState → RepairState
  | .ruined => .ruined
  | _ => if root ∈ corrupt then .ruined else .restored

theorem repair_success_iff (corrupt : Finset R) (root : R) :
    destructiveStep corrupt root .pending = .restored ↔ root ∉ corrupt := by
  simp [destructiveStep]

omit [Fintype M] in
theorem repair_message_contract_iff (decode : M → R) (budget : ℕ) :
    (∀ corrupt : Finset R, corrupt.card ≤ budget →
      ∃ message, destructiveStep corrupt (decode message) .pending = .restored) ↔
      safeDecoder decode budget := by
  simp only [safeDecoder, repair_success_iff]

theorem successful_repair_message_lower_bound (decode : M → R) (budget : ℕ)
    (h : ∀ corrupt : Finset R, corrupt.card ≤ budget →
      ∃ message, destructiveStep corrupt (decode message) .pending = .restored) :
    budget < Fintype.card M :=
  safeDecoder_message_lower_bound decode budget
    ((repair_message_contract_iff decode budget).mp h)

theorem corrupt_action_irreversible (corrupt : Finset R) (bad next : R)
    (hbad : bad ∈ corrupt) :
    destructiveStep corrupt next (destructiveStep corrupt bad .pending) = .ruined := by
  simp [destructiveStep, hbad]

/-- Under the stipulated action semantics, a corrupt act cannot reach the target. -/
theorem corrupt_action_not_restorative (corrupt : Finset R) (bad : R)
    (hbad : bad ∈ corrupt) : destructiveStep corrupt bad .pending ≠ .restored := by
  simp [destructiveStep, hbad]

#print axioms repair_success_iff
#print axioms repair_message_contract_iff
#print axioms successful_repair_message_lower_bound
#print axioms corrupt_action_irreversible
#print axioms corrupt_action_not_restorative
end Orthemology.ActionDisclosure
