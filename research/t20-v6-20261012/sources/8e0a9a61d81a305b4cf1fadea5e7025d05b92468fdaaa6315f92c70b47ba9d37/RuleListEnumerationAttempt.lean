import CertificateGrammar
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000
attribute [local irreducible] Nat.pair

theorem Rule_rule (c : Nat) : (∃ a : JointCertificates.Rule, encode a = c) ↔
    localShape ruleDescription c = true ∧ ∀ d ∈ localChildren ruleDescription c, CertCanonical d := by
  constructor
  · rintro ⟨a, rfl⟩
    cases a <;> simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]
  · rintro ⟨hs, hc⟩
    unfold localShape at hs
    split_ifs at hs with htag
    have hlt : tag c < 63 := by simpa [ruleDescription] using htag
    have heq : tag c = 0 ∨ tag c = 1 ∨ tag c = 2 ∨ tag c = 3 ∨ tag c = 4 ∨ tag c = 5 ∨ tag c = 6 ∨ tag c = 7 ∨ tag c = 8 ∨ tag c = 9 ∨ tag c = 10 ∨ tag c = 11 ∨ tag c = 12 ∨ tag c = 13 ∨ tag c = 14 ∨ tag c = 15 ∨ tag c = 16 ∨ tag c = 17 ∨ tag c = 18 ∨ tag c = 19 ∨ tag c = 20 ∨ tag c = 21 ∨ tag c = 22 ∨ tag c = 23 ∨ tag c = 24 ∨ tag c = 25 ∨ tag c = 26 ∨ tag c = 27 ∨ tag c = 28 ∨ tag c = 29 ∨ tag c = 30 ∨ tag c = 31 ∨ tag c = 32 ∨ tag c = 33 ∨ tag c = 34 ∨ tag c = 35 ∨ tag c = 36 ∨ tag c = 37 ∨ tag c = 38 ∨ tag c = 39 ∨ tag c = 40 ∨ tag c = 41 ∨ tag c = 42 ∨ tag c = 43 ∨ tag c = 44 ∨ tag c = 45 ∨ tag c = 46 ∨ tag c = 47 ∨ tag c = 48 ∨ tag c = 49 ∨ tag c = 50 ∨ tag c = 51 ∨ tag c = 52 ∨ tag c = 53 ∨ tag c = 54 ∨ tag c = 55 ∨ tag c = 56 ∨ tag c = 57 ∨ tag c = 58 ∨ tag c = 59 ∨ tag c = 60 ∨ tag c = 61 ∨ tag c = 62 := by simpa [List.range_succ, or_assoc, eq_comm] using (List.mem_range.mpr hlt)
    rcases heq with heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨a0, h0⟩
      refine ⟨JointCertificates.Rule.CtxJ_ctxBase a0, ?_⟩
      simpa [h0] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      refine ⟨JointCertificates.Rule.CtxJ_nil, ?_⟩
      simpa [] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨JointCertificates.Rule.CtxJ_ext a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨JointCertificates.Rule.FormJ_formBase a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨a0, h0⟩
      refine ⟨JointCertificates.Rule.FormJ_param a0 (rest (slot c 1)), ?_⟩
      simpa [h0] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨a0, h0⟩
      refine ⟨JointCertificates.Rule.FormJ_bottom a0, ?_⟩
      simpa [h0] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨JointCertificates.Rule.FormJ_all a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨a0, h0⟩
      refine ⟨JointCertificates.Rule.FormJ_raw a0, ?_⟩
      simpa [h0] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨JointCertificates.Rule.FormJ_pi a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨JointCertificates.Rule.FormJ_sigma a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨JointCertificates.Rule.FormJ_identity a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_hasBase a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a3, h3⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_var a0 a1 (rest (slot c 2)) a3, ?_⟩
      simpa [h0, h1, h3] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_i a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_k a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_s a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_finite a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_allIntro a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_allElim a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_rawAtom a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_rawApp a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_piIntro a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_piElim a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_sigmaIntro a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_sigmaFst a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_sigmaSnd a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_identityIntro a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_proofErase a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩, ⟨a5, h5⟩, ⟨a6, h6⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_j a0 a1 a2 a3 a4 a5 a6, ?_⟩
      simpa [h0, h1, h2, h3, h4, h5, h6] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_conv a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩, ⟨a5, h5⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_piExt a0 a1 a2 a3 a4 a5, ?_⟩
      simpa [h0, h1, h2, h3, h4, h5] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_allExt a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩, ⟨a5, h5⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_sigmaElim a0 a1 a2 a3 a4 a5, ?_⟩
      simpa [h0, h1, h2, h3, h4, h5] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨JointCertificates.Rule.HasJ_natInduction a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      refine ⟨JointCertificates.Rule.CtxE_nil, ?_⟩
      simpa [] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨JointCertificates.Rule.CtxE_ext a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨a0, h0⟩
      refine ⟨JointCertificates.Rule.FormE_param a0 (rest (slot c 1)), ?_⟩
      simpa [h0] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨a0, h0⟩
      refine ⟨JointCertificates.Rule.FormE_bottom a0, ?_⟩
      simpa [h0] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨JointCertificates.Rule.FormE_all a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨a0, h0⟩
      refine ⟨JointCertificates.Rule.FormE_raw a0, ?_⟩
      simpa [h0] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨JointCertificates.Rule.FormE_pi a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨JointCertificates.Rule.FormE_sigma a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨JointCertificates.Rule.FormE_identity a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a3, h3⟩⟩
      refine ⟨JointCertificates.Rule.HasE_var a0 a1 (rest (slot c 2)) a3, ?_⟩
      simpa [h0, h1, h3] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨JointCertificates.Rule.HasE_i a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨JointCertificates.Rule.HasE_k a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨JointCertificates.Rule.HasE_s a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨JointCertificates.Rule.HasE_finite a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨JointCertificates.Rule.HasE_allIntro a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨JointCertificates.Rule.HasE_allElim a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
      refine ⟨JointCertificates.Rule.HasE_rawAtom a0 a1, ?_⟩
      simpa [h0, h1] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
      refine ⟨JointCertificates.Rule.HasE_rawApp a0 a1 a2, ?_⟩
      simpa [h0, h1, h2] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨JointCertificates.Rule.HasE_piIntro a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨JointCertificates.Rule.HasE_piElim a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨JointCertificates.Rule.HasE_sigmaIntro a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨JointCertificates.Rule.HasE_sigmaFst a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
      refine ⟨JointCertificates.Rule.HasE_sigmaSnd a0 a1 a2 a3, ?_⟩
      simpa [h0, h1, h2, h3] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨JointCertificates.Rule.HasE_identityIntro a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨JointCertificates.Rule.HasE_proofErase a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩, ⟨a5, h5⟩, ⟨a6, h6⟩⟩
      refine ⟨JointCertificates.Rule.HasE_j a0 a1 a2 a3 a4 a5 a6, ?_⟩
      simpa [h0, h1, h2, h3, h4, h5, h6] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨JointCertificates.Rule.HasE_conv a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩, ⟨a5, h5⟩⟩
      refine ⟨JointCertificates.Rule.HasE_piExt a0 a1 a2 a3 a4 a5, ?_⟩
      simpa [h0, h1, h2, h3, h4, h5] using hs.symm
    · simp [ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
      simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
      rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
      refine ⟨JointCertificates.Rule.HasE_allExt a0 a1 a2 a3 a4, ?_⟩
      simpa [h0, h1, h2, h3, h4] using hs.symm

end CertificateCodeValidity
