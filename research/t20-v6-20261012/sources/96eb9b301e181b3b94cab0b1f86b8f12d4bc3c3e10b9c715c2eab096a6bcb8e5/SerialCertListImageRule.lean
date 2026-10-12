import CertificateGrammar
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000
attribute [local irreducible] Nat.pair

theorem SerialCertList_rule (c : Nat) : (∃ a : JointCertificates.SerialCertList, encode a = c) ↔
    localShape serialCertListDescription c = true ∧ ∀ d ∈ localChildren serialCertListDescription c, CertCanonical d := by
  constructor
  · rintro ⟨a, rfl⟩
    cases a <;> simp [serialCertListDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]
  · rintro ⟨hs, hc⟩
    unfold localShape at hs
    split_ifs at hs with htag
    have hlt : tag c < 2 := by simpa [serialCertListDescription] using htag
    have heq : tag c = 0 ∨ tag c = 1 := by simpa [List.range_succ, or_assoc, eq_comm] using (List.mem_range.mpr hlt)
    rcases heq with heq | heq
    · simp [serialCertListDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, serialCertListDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      refine ⟨JointCertificates.SerialCertList.nil, ?_⟩
      simpa [] using hs.symm
    · simp [serialCertListDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, serialCertListDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨JointCertificates.SerialCertList.cons a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm

end CertificateCodeValidity
