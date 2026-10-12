import SerialCertListImageRule
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000
attribute [local irreducible] Nat.pair

theorem SerialCertList_bounds (c : Nat) (h : ∃ a : JointCertificates.SerialCertList, encode a = c) :
    ∀ d ∈ localChildren serialCertListDescription c, d.2 < c := by
  obtain ⟨a, rfl⟩ := h
  cases a <;> simp [localChildren, serialCertListDescription, dependencies, fieldCode, List.range_succ]
  all_goals repeat' apply And.intro
  all_goals apply field_lt_pack; simp

end CertificateCodeValidity
