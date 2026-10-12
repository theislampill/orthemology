import CertificateGrammar
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000
attribute [local irreducible] Nat.pair

theorem Claim_rule (c : Nat) : (∃ a : JointCertificates.Claim, encode a = c) ↔
    localShape claimDescription c = true ∧ ∀ d ∈ localChildren claimDescription c, CertCanonical d := by
  constructor
  · rintro ⟨a, rfl⟩
    cases a <;> simp [claimDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]
  · rintro ⟨hs, hc⟩
    unfold localShape at hs
    split_ifs at hs with htag
    have hlt : tag c < 6 := by simpa [claimDescription] using htag
    have heq : tag c = 0 ∨ tag c = 1 ∨ tag c = 2 ∨ tag c = 3 ∨ tag c = 4 ∨ tag c = 5 := by simpa [List.range_succ, or_assoc, eq_comm] using (List.mem_range.mpr hlt)
    rcases heq with heq | heq | heq | heq | heq | heq
    · simp [claimDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, claimDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨a0, h0⟩
      refine ⟨JointCertificates.Claim.ctxJ a0, ?_⟩
      simpa [h0] using hs.symm
    · simp [claimDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, claimDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨JointCertificates.Claim.formJ a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm
    · simp [claimDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, claimDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨JointCertificates.Claim.hasJ a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm
    · simp [claimDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, claimDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨a0, h0⟩
      refine ⟨JointCertificates.Claim.ctxE a0, ?_⟩
      simpa [h0] using hs.symm
    · simp [claimDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, claimDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨JointCertificates.Claim.formE a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm
    · simp [claimDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, claimDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨JointCertificates.Claim.hasE a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm

end CertificateCodeValidity
