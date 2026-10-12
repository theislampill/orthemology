import CertificateGrammar
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000
attribute [local irreducible] Nat.pair

theorem FiniteCert_rule (c : Nat) : (∃ a : AuxiliaryCertificates.FiniteCert, encode a = c) ↔
    localShape finiteCertDescription c = true ∧ ∀ d ∈ localChildren finiteCertDescription c, CertCanonical d := by
  constructor
  · rintro ⟨a, rfl⟩
    cases a <;> simp [finiteCertDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]
  · rintro ⟨hs, hc⟩
    unfold localShape at hs
    split_ifs at hs with htag
    have hlt : tag c < 7 := by simpa [finiteCertDescription] using htag
    have heq : tag c = 0 ∨ tag c = 1 ∨ tag c = 2 ∨ tag c = 3 ∨ tag c = 4 ∨ tag c = 5 ∨ tag c = 6 := by simpa [List.range_succ, or_assoc, eq_comm] using (List.mem_range.mpr hlt)
    rcases heq with heq | heq | heq | heq | heq | heq | heq
    · simp [finiteCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, finiteCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨a0, h0⟩
      refine ⟨AuxiliaryCertificates.FiniteCert.i a0, ?_⟩
      simpa [h0] using hs.symm
    · simp [finiteCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, finiteCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨AuxiliaryCertificates.FiniteCert.k a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm
    · simp [finiteCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, finiteCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨AuxiliaryCertificates.FiniteCert.s a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm
    · simp [finiteCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, finiteCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩, ⟨a5, h5⟩⟩
      refine ⟨AuxiliaryCertificates.FiniteCert.app a0 a1 a2 a3 a4 a5, ?_⟩
      simpa [h0, h1, h2, h3, h4, h5] using hs.symm
    · simp [finiteCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, finiteCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨AuxiliaryCertificates.FiniteCert.allI a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm
    · simp [finiteCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, finiteCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨AuxiliaryCertificates.FiniteCert.allE a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm
    · simp [finiteCertDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, finiteCertDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨AuxiliaryCertificates.FiniteCert.reduce a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm

end CertificateCodeValidity
