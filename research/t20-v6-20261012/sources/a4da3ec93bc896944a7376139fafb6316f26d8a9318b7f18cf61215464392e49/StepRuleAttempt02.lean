import CertificateGrammar
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000
attribute [local irreducible] Nat.pair

theorem StepCert_rule (c : Nat) : (∃ a : AuxiliaryCertificates.StepCert, encode a = c) ↔
    localShape stepCertDescription c = true ∧ ∀ d ∈ localChildren stepCertDescription c, CertCanonical d := by
  constructor
  · rintro ⟨a, rfl⟩
    cases a <;> simp [stepCertDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, slot, iterRest, pack, List.range_succ, CertCanonical]
  · rintro ⟨hs, hc⟩
    unfold localShape at hs
    split_ifs at hs with htag
    have hlt : tag c < 5 := by simpa [stepCertDescription] using htag
    have heq : tag c = 0 ∨ tag c = 1 ∨ tag c = 2 ∨ tag c = 3 ∨ tag c = 4 := by omega
    rcases heq with heq | heq | heq | heq | heq
    · simp [stepCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, stepCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨a0, h0⟩
      refine ⟨AuxiliaryCertificates.StepCert.i a0, ?_⟩
      simpa [h0] using hs.symm
    · simp [stepCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, stepCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨AuxiliaryCertificates.StepCert.k a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm
    · simp [stepCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, stepCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨AuxiliaryCertificates.StepCert.s a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm
    · simp [stepCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, stepCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨AuxiliaryCertificates.StepCert.left a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm
    · simp [stepCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, stepCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨AuxiliaryCertificates.StepCert.right a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm

end CertificateCodeValidity
