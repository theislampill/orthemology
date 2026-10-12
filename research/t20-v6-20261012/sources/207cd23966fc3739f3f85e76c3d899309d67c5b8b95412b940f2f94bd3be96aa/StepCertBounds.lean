import StepCertImageRule
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000
attribute [local irreducible] Nat.pair

theorem StepCert_bounds (c : Nat) (h : ∃ a : AuxiliaryCertificates.StepCert, encode a = c) :
    ∀ d ∈ localChildren stepCertDescription c, d.2 < c := by
  obtain ⟨a, rfl⟩ := h
  cases a <;> simp [localChildren, stepCertDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals first
    | solve | apply field_lt_pack; simp
    | apply lt_of_le_of_lt (le_leaf _); apply field_lt_pack; simp

end CertificateCodeValidity
