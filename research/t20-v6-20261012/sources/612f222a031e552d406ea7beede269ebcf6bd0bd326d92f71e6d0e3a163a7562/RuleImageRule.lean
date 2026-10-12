import CertificateGrammar
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 200000
attribute [local irreducible] Nat.pair

theorem rule_complete_0 (a0 : P01AC.Tel) :
    localShape ruleDescription (encode (Rule.CtxJ_ctxBase a0)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.CtxJ_ctxBase a0)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_0 (c : Nat) (heq : tag c = 0)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨a0, h0⟩
  refine ⟨Rule.CtxJ_ctxBase a0, ?_⟩
  simpa [h0] using hs.symm

theorem rule_complete_1  :
    localShape ruleDescription (encode (Rule.CtxJ_nil)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.CtxJ_nil)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_1 (c : Nat) (heq : tag c = 1)
    (hs : localShape ruleDescription c = true)
    (_hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  refine ⟨Rule.CtxJ_nil, ?_⟩
  simpa [] using hs.symm

theorem rule_complete_2 (a0 : P01AC.Tel) (a1 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.CtxJ_ext a0 a1)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.CtxJ_ext a0 a1)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_2 (c : Nat) (heq : tag c = 2)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
  refine ⟨Rule.CtxJ_ext a0 a1, ?_⟩
  simpa [h0, h1] using hs.symm

theorem rule_complete_3 (a0 : P01AC.Tel) (a1 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.FormJ_formBase a0 a1)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_formBase a0 a1)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_3 (c : Nat) (heq : tag c = 3)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
  refine ⟨Rule.FormJ_formBase a0 a1, ?_⟩
  simpa [h0, h1] using hs.symm

theorem rule_complete_4 (a0 : P01AC.Tel) (a1 : Nat) :
    localShape ruleDescription (encode (Rule.FormJ_param a0 a1)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_param a0 a1)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_4 (c : Nat) (heq : tag c = 4)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨a0, h0⟩
  refine ⟨Rule.FormJ_param a0 (rest (slot c 1)), ?_⟩
  simpa [h0] using hs.symm

theorem rule_complete_5 (a0 : P01AC.Tel) :
    localShape ruleDescription (encode (Rule.FormJ_bottom a0)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_bottom a0)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_5 (c : Nat) (heq : tag c = 5)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨a0, h0⟩
  refine ⟨Rule.FormJ_bottom a0, ?_⟩
  simpa [h0] using hs.symm

theorem rule_complete_6 (a0 : P01AC.Tel) (a1 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.FormJ_all a0 a1)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_all a0 a1)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_6 (c : Nat) (heq : tag c = 6)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
  refine ⟨Rule.FormJ_all a0 a1, ?_⟩
  simpa [h0, h1] using hs.symm

theorem rule_complete_7 (a0 : P01AC.Tel) :
    localShape ruleDescription (encode (Rule.FormJ_raw a0)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_raw a0)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_7 (c : Nat) (heq : tag c = 7)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨a0, h0⟩
  refine ⟨Rule.FormJ_raw a0, ?_⟩
  simpa [h0] using hs.symm

theorem rule_complete_8 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.FormJ_pi a0 a1 a2)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_pi a0 a1 a2)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_8 (c : Nat) (heq : tag c = 8)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
  refine ⟨Rule.FormJ_pi a0 a1 a2, ?_⟩
  simpa [h0, h1, h2] using hs.symm

theorem rule_complete_9 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.FormJ_sigma a0 a1 a2)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_sigma a0 a1 a2)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_9 (c : Nat) (heq : tag c = 9)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
  refine ⟨Rule.FormJ_sigma a0 a1 a2, ?_⟩
  simpa [h0, h1, h2] using hs.symm

theorem rule_complete_10 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.FormJ_identity a0 a1 a2 a3)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormJ_identity a0 a1 a2 a3)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_10 (c : Nat) (heq : tag c = 10)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
  refine ⟨Rule.FormJ_identity a0 a1 a2 a3, ?_⟩
  simpa [h0, h1, h2, h3] using hs.symm

theorem rule_complete_11 (a0 : P01AC.Tel) (a1 : P01D.Poly) (a2 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.HasJ_hasBase a0 a1 a2)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_hasBase a0 a1 a2)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_11 (c : Nat) (heq : tag c = 11)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
  refine ⟨Rule.HasJ_hasBase a0 a1 a2, ?_⟩
  simpa [h0, h1, h2] using hs.symm

theorem rule_complete_12 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : Nat) (a3 : AuxiliaryCertificates.LookupCert) :
    localShape ruleDescription (encode (Rule.HasJ_var a0 a1 a2 a3)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_var a0 a1 a2 a3)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_12 (c : Nat) (heq : tag c = 12)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a3, h3⟩⟩
  refine ⟨Rule.HasJ_var a0 a1 (rest (slot c 2)) a3, ?_⟩
  simpa [h0, h1, h3] using hs.symm

theorem rule_complete_13 (a0 : P01AC.Tel) (a1 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.HasJ_i a0 a1)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_i a0 a1)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_13 (c : Nat) (heq : tag c = 13)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
  refine ⟨Rule.HasJ_i a0 a1, ?_⟩
  simpa [h0, h1] using hs.symm

theorem rule_complete_14 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.HasJ_k a0 a1 a2)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_k a0 a1 a2)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_14 (c : Nat) (heq : tag c = 14)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
  refine ⟨Rule.HasJ_k a0 a1 a2, ?_⟩
  simpa [h0, h1, h2] using hs.symm

theorem rule_complete_15 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.HasJ_s a0 a1 a2 a3)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_s a0 a1 a2 a3)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_15 (c : Nat) (heq : tag c = 15)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
  refine ⟨Rule.HasJ_s a0 a1 a2 a3, ?_⟩
  simpa [h0, h1, h2, h3] using hs.symm

theorem rule_complete_16 (a0 : OrthemologyV2.TypeCode) (a1 : P01AC.Tel) (a2 : OrthemologyV2.Term) (a3 : List P01AC.Ty) (a4 : AuxiliaryCertificates.FiniteCert) :
    localShape ruleDescription (encode (Rule.HasJ_finite a0 a1 a2 a3 a4)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_finite a0 a1 a2 a3 a4)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_16 (c : Nat) (heq : tag c = 16)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
  refine ⟨Rule.HasJ_finite a0 a1 a2 a3 a4, ?_⟩
  simpa [h0, h1, h2, h3, h4] using hs.symm

theorem rule_complete_17 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasJ_allIntro a0 a1 a2)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_allIntro a0 a1 a2)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_17 (c : Nat) (heq : tag c = 17)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
  refine ⟨Rule.HasJ_allIntro a0 a1 a2, ?_⟩
  simpa [h0, h1, h2] using hs.symm

theorem rule_complete_18 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasJ_allElim a0 a1 a2 a3)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_allElim a0 a1 a2 a3)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_18 (c : Nat) (heq : tag c = 18)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
  refine ⟨Rule.HasJ_allElim a0 a1 a2 a3, ?_⟩
  simpa [h0, h1, h2, h3] using hs.symm

theorem rule_complete_19 (a0 : P01AC.Tel) (a1 : OrthemologyV2.Term) :
    localShape ruleDescription (encode (Rule.HasJ_rawAtom a0 a1)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_rawAtom a0 a1)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_19 (c : Nat) (heq : tag c = 19)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
  refine ⟨Rule.HasJ_rawAtom a0 a1, ?_⟩
  simpa [h0, h1] using hs.symm

theorem rule_complete_20 (a0 : P01AC.Tel) (a1 : P01D.Poly) (a2 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasJ_rawApp a0 a1 a2)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_rawApp a0 a1 a2)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_20 (c : Nat) (heq : tag c = 20)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
  refine ⟨Rule.HasJ_rawApp a0 a1 a2, ?_⟩
  simpa [h0, h1, h2] using hs.symm

theorem rule_complete_21 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasJ_piIntro a0 a1 a2 a3)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_piIntro a0 a1 a2 a3)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_21 (c : Nat) (heq : tag c = 21)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
  refine ⟨Rule.HasJ_piIntro a0 a1 a2 a3, ?_⟩
  simpa [h0, h1, h2, h3] using hs.symm

theorem rule_complete_22 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasJ_piElim a0 a1 a2 a3 a4)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_piElim a0 a1 a2 a3 a4)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_22 (c : Nat) (heq : tag c = 22)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
  refine ⟨Rule.HasJ_piElim a0 a1 a2 a3 a4, ?_⟩
  simpa [h0, h1, h2, h3, h4] using hs.symm

theorem rule_complete_23 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasJ_sigmaIntro a0 a1 a2 a3 a4)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_sigmaIntro a0 a1 a2 a3 a4)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_23 (c : Nat) (heq : tag c = 23)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
  refine ⟨Rule.HasJ_sigmaIntro a0 a1 a2 a3 a4, ?_⟩
  simpa [h0, h1, h2, h3, h4] using hs.symm

theorem rule_complete_24 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasJ_sigmaFst a0 a1 a2 a3)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_sigmaFst a0 a1 a2 a3)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_24 (c : Nat) (heq : tag c = 24)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
  refine ⟨Rule.HasJ_sigmaFst a0 a1 a2 a3, ?_⟩
  simpa [h0, h1, h2, h3] using hs.symm

theorem rule_complete_25 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasJ_sigmaSnd a0 a1 a2 a3)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_sigmaSnd a0 a1 a2 a3)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_25 (c : Nat) (heq : tag c = 25)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
  refine ⟨Rule.HasJ_sigmaSnd a0 a1 a2 a3, ?_⟩
  simpa [h0, h1, h2, h3] using hs.symm

theorem rule_complete_26 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : AuxiliaryCertificates.PolyCert) :
    localShape ruleDescription (encode (Rule.HasJ_identityIntro a0 a1 a2 a3 a4)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_identityIntro a0 a1 a2 a3 a4)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_26 (c : Nat) (heq : tag c = 26)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
  refine ⟨Rule.HasJ_identityIntro a0 a1 a2 a3 a4, ?_⟩
  simpa [h0, h1, h2, h3, h4] using hs.symm

theorem rule_complete_27 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasJ_proofErase a0 a1 a2 a3 a4)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_proofErase a0 a1 a2 a3 a4)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_27 (c : Nat) (heq : tag c = 27)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
  refine ⟨Rule.HasJ_proofErase a0 a1 a2 a3 a4, ?_⟩
  simpa [h0, h1, h2, h3, h4] using hs.symm

theorem rule_complete_28 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01AC.Ty) (a4 : P01D.Poly) (a5 : P01D.Poly) (a6 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasJ_j a0 a1 a2 a3 a4 a5 a6)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_j a0 a1 a2 a3 a4 a5 a6)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_28 (c : Nat) (heq : tag c = 28)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩, ⟨a5, h5⟩, ⟨a6, h6⟩⟩
  refine ⟨Rule.HasJ_j a0 a1 a2 a3 a4 a5 a6, ?_⟩
  simpa [h0, h1, h2, h3, h4, h5, h6] using hs.symm

theorem rule_complete_29 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : AuxiliaryCertificates.PolyCert) :
    localShape ruleDescription (encode (Rule.HasJ_conv a0 a1 a2 a3 a4)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_conv a0 a1 a2 a3 a4)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_29 (c : Nat) (heq : tag c = 29)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
  refine ⟨Rule.HasJ_conv a0 a1 a2 a3 a4, ?_⟩
  simpa [h0, h1, h2, h3, h4] using hs.symm

theorem rule_complete_30 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) (a5 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasJ_piExt a0 a1 a2 a3 a4 a5)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_piExt a0 a1 a2 a3 a4 a5)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_30 (c : Nat) (heq : tag c = 30)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩, ⟨a5, h5⟩⟩
  refine ⟨Rule.HasJ_piExt a0 a1 a2 a3 a4 a5, ?_⟩
  simpa [h0, h1, h2, h3, h4, h5] using hs.symm

theorem rule_complete_31 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasJ_allExt a0 a1 a2 a3 a4)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_allExt a0 a1 a2 a3 a4)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_31 (c : Nat) (heq : tag c = 31)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
  refine ⟨Rule.HasJ_allExt a0 a1 a2 a3 a4, ?_⟩
  simpa [h0, h1, h2, h3, h4] using hs.symm

theorem rule_complete_32 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01AC.Ty) (a4 : P01D.Poly) (a5 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasJ_sigmaElim a0 a1 a2 a3 a4 a5)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_sigmaElim a0 a1 a2 a3 a4 a5)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_32 (c : Nat) (heq : tag c = 32)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩, ⟨a5, h5⟩⟩
  refine ⟨Rule.HasJ_sigmaElim a0 a1 a2 a3 a4 a5, ?_⟩
  simpa [h0, h1, h2, h3, h4, h5] using hs.symm

theorem rule_complete_33 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasJ_natInduction a0 a1 a2 a3)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasJ_natInduction a0 a1 a2 a3)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_33 (c : Nat) (heq : tag c = 33)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
  refine ⟨Rule.HasJ_natInduction a0 a1 a2 a3, ?_⟩
  simpa [h0, h1, h2, h3] using hs.symm

theorem rule_complete_34  :
    localShape ruleDescription (encode (Rule.CtxE_nil)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.CtxE_nil)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_34 (c : Nat) (heq : tag c = 34)
    (hs : localShape ruleDescription c = true)
    (_hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  refine ⟨Rule.CtxE_nil, ?_⟩
  simpa [] using hs.symm

theorem rule_complete_35 (a0 : P01AC.Tel) (a1 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.CtxE_ext a0 a1)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.CtxE_ext a0 a1)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_35 (c : Nat) (heq : tag c = 35)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
  refine ⟨Rule.CtxE_ext a0 a1, ?_⟩
  simpa [h0, h1] using hs.symm

theorem rule_complete_36 (a0 : P01AC.Tel) (a1 : Nat) :
    localShape ruleDescription (encode (Rule.FormE_param a0 a1)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormE_param a0 a1)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_36 (c : Nat) (heq : tag c = 36)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨a0, h0⟩
  refine ⟨Rule.FormE_param a0 (rest (slot c 1)), ?_⟩
  simpa [h0] using hs.symm

theorem rule_complete_37 (a0 : P01AC.Tel) :
    localShape ruleDescription (encode (Rule.FormE_bottom a0)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormE_bottom a0)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_37 (c : Nat) (heq : tag c = 37)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨a0, h0⟩
  refine ⟨Rule.FormE_bottom a0, ?_⟩
  simpa [h0] using hs.symm

theorem rule_complete_38 (a0 : P01AC.Tel) (a1 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.FormE_all a0 a1)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormE_all a0 a1)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_38 (c : Nat) (heq : tag c = 38)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
  refine ⟨Rule.FormE_all a0 a1, ?_⟩
  simpa [h0, h1] using hs.symm

theorem rule_complete_39 (a0 : P01AC.Tel) :
    localShape ruleDescription (encode (Rule.FormE_raw a0)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormE_raw a0)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_39 (c : Nat) (heq : tag c = 39)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨a0, h0⟩
  refine ⟨Rule.FormE_raw a0, ?_⟩
  simpa [h0] using hs.symm

theorem rule_complete_40 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.FormE_pi a0 a1 a2)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormE_pi a0 a1 a2)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_40 (c : Nat) (heq : tag c = 40)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
  refine ⟨Rule.FormE_pi a0 a1 a2, ?_⟩
  simpa [h0, h1, h2] using hs.symm

theorem rule_complete_41 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.FormE_sigma a0 a1 a2)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormE_sigma a0 a1 a2)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_41 (c : Nat) (heq : tag c = 41)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
  refine ⟨Rule.FormE_sigma a0 a1 a2, ?_⟩
  simpa [h0, h1, h2] using hs.symm

theorem rule_complete_42 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.FormE_identity a0 a1 a2 a3)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.FormE_identity a0 a1 a2 a3)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_42 (c : Nat) (heq : tag c = 42)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
  refine ⟨Rule.FormE_identity a0 a1 a2 a3, ?_⟩
  simpa [h0, h1, h2, h3] using hs.symm

theorem rule_complete_43 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : Nat) (a3 : AuxiliaryCertificates.LookupCert) :
    localShape ruleDescription (encode (Rule.HasE_var a0 a1 a2 a3)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_var a0 a1 a2 a3)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_43 (c : Nat) (heq : tag c = 43)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a3, h3⟩⟩
  refine ⟨Rule.HasE_var a0 a1 (rest (slot c 2)) a3, ?_⟩
  simpa [h0, h1, h3] using hs.symm

theorem rule_complete_44 (a0 : P01AC.Tel) (a1 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.HasE_i a0 a1)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_i a0 a1)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_44 (c : Nat) (heq : tag c = 44)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
  refine ⟨Rule.HasE_i a0 a1, ?_⟩
  simpa [h0, h1] using hs.symm

theorem rule_complete_45 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.HasE_k a0 a1 a2)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_k a0 a1 a2)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_45 (c : Nat) (heq : tag c = 45)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
  refine ⟨Rule.HasE_k a0 a1 a2, ?_⟩
  simpa [h0, h1, h2] using hs.symm

theorem rule_complete_46 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01AC.Ty) :
    localShape ruleDescription (encode (Rule.HasE_s a0 a1 a2 a3)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_s a0 a1 a2 a3)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_46 (c : Nat) (heq : tag c = 46)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
  refine ⟨Rule.HasE_s a0 a1 a2 a3, ?_⟩
  simpa [h0, h1, h2, h3] using hs.symm

theorem rule_complete_47 (a0 : OrthemologyV2.TypeCode) (a1 : P01AC.Tel) (a2 : OrthemologyV2.Term) (a3 : List P01AC.Ty) (a4 : AuxiliaryCertificates.FiniteCert) :
    localShape ruleDescription (encode (Rule.HasE_finite a0 a1 a2 a3 a4)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_finite a0 a1 a2 a3 a4)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_47 (c : Nat) (heq : tag c = 47)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
  refine ⟨Rule.HasE_finite a0 a1 a2 a3 a4, ?_⟩
  simpa [h0, h1, h2, h3, h4] using hs.symm

theorem rule_complete_48 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasE_allIntro a0 a1 a2)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_allIntro a0 a1 a2)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_48 (c : Nat) (heq : tag c = 48)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
  refine ⟨Rule.HasE_allIntro a0 a1 a2, ?_⟩
  simpa [h0, h1, h2] using hs.symm

theorem rule_complete_49 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasE_allElim a0 a1 a2 a3)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_allElim a0 a1 a2 a3)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_49 (c : Nat) (heq : tag c = 49)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
  refine ⟨Rule.HasE_allElim a0 a1 a2 a3, ?_⟩
  simpa [h0, h1, h2, h3] using hs.symm

theorem rule_complete_50 (a0 : P01AC.Tel) (a1 : OrthemologyV2.Term) :
    localShape ruleDescription (encode (Rule.HasE_rawAtom a0 a1)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_rawAtom a0 a1)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_50 (c : Nat) (heq : tag c = 50)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩⟩
  refine ⟨Rule.HasE_rawAtom a0 a1, ?_⟩
  simpa [h0, h1] using hs.symm

theorem rule_complete_51 (a0 : P01AC.Tel) (a1 : P01D.Poly) (a2 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasE_rawApp a0 a1 a2)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_rawApp a0 a1 a2)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_51 (c : Nat) (heq : tag c = 51)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩⟩
  refine ⟨Rule.HasE_rawApp a0 a1 a2, ?_⟩
  simpa [h0, h1, h2] using hs.symm

theorem rule_complete_52 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasE_piIntro a0 a1 a2 a3)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_piIntro a0 a1 a2 a3)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_52 (c : Nat) (heq : tag c = 52)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
  refine ⟨Rule.HasE_piIntro a0 a1 a2 a3, ?_⟩
  simpa [h0, h1, h2, h3] using hs.symm

theorem rule_complete_53 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasE_piElim a0 a1 a2 a3 a4)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_piElim a0 a1 a2 a3 a4)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_53 (c : Nat) (heq : tag c = 53)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
  refine ⟨Rule.HasE_piElim a0 a1 a2 a3 a4, ?_⟩
  simpa [h0, h1, h2, h3, h4] using hs.symm

theorem rule_complete_54 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasE_sigmaIntro a0 a1 a2 a3 a4)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_sigmaIntro a0 a1 a2 a3 a4)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_54 (c : Nat) (heq : tag c = 54)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
  refine ⟨Rule.HasE_sigmaIntro a0 a1 a2 a3 a4, ?_⟩
  simpa [h0, h1, h2, h3, h4] using hs.symm

theorem rule_complete_55 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasE_sigmaFst a0 a1 a2 a3)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_sigmaFst a0 a1 a2 a3)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_55 (c : Nat) (heq : tag c = 55)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
  refine ⟨Rule.HasE_sigmaFst a0 a1 a2 a3, ?_⟩
  simpa [h0, h1, h2, h3] using hs.symm

theorem rule_complete_56 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasE_sigmaSnd a0 a1 a2 a3)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_sigmaSnd a0 a1 a2 a3)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_56 (c : Nat) (heq : tag c = 56)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩⟩
  refine ⟨Rule.HasE_sigmaSnd a0 a1 a2 a3, ?_⟩
  simpa [h0, h1, h2, h3] using hs.symm

theorem rule_complete_57 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : AuxiliaryCertificates.PolyCert) :
    localShape ruleDescription (encode (Rule.HasE_identityIntro a0 a1 a2 a3 a4)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_identityIntro a0 a1 a2 a3 a4)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_57 (c : Nat) (heq : tag c = 57)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
  refine ⟨Rule.HasE_identityIntro a0 a1 a2 a3 a4, ?_⟩
  simpa [h0, h1, h2, h3, h4] using hs.symm

theorem rule_complete_58 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasE_proofErase a0 a1 a2 a3 a4)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_proofErase a0 a1 a2 a3 a4)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_58 (c : Nat) (heq : tag c = 58)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
  refine ⟨Rule.HasE_proofErase a0 a1 a2 a3 a4, ?_⟩
  simpa [h0, h1, h2, h3, h4] using hs.symm

theorem rule_complete_59 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01AC.Ty) (a4 : P01D.Poly) (a5 : P01D.Poly) (a6 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasE_j a0 a1 a2 a3 a4 a5 a6)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_j a0 a1 a2 a3 a4 a5 a6)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_59 (c : Nat) (heq : tag c = 59)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩, ⟨a5, h5⟩, ⟨a6, h6⟩⟩
  refine ⟨Rule.HasE_j a0 a1 a2 a3 a4 a5 a6, ?_⟩
  simpa [h0, h1, h2, h3, h4, h5, h6] using hs.symm

theorem rule_complete_60 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : AuxiliaryCertificates.PolyCert) :
    localShape ruleDescription (encode (Rule.HasE_conv a0 a1 a2 a3 a4)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_conv a0 a1 a2 a3 a4)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_60 (c : Nat) (heq : tag c = 60)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
  refine ⟨Rule.HasE_conv a0 a1 a2 a3 a4, ?_⟩
  simpa [h0, h1, h2, h3, h4] using hs.symm

theorem rule_complete_61 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01AC.Ty) (a3 : P01D.Poly) (a4 : P01D.Poly) (a5 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasE_piExt a0 a1 a2 a3 a4 a5)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_piExt a0 a1 a2 a3 a4 a5)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_61 (c : Nat) (heq : tag c = 61)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩, ⟨a5, h5⟩⟩
  refine ⟨Rule.HasE_piExt a0 a1 a2 a3 a4 a5, ?_⟩
  simpa [h0, h1, h2, h3, h4, h5] using hs.symm

theorem rule_complete_62 (a0 : P01AC.Tel) (a1 : P01AC.Ty) (a2 : P01D.Poly) (a3 : P01D.Poly) (a4 : P01D.Poly) :
    localShape ruleDescription (encode (Rule.HasE_allExt a0 a1 a2 a3 a4)) = true ∧
    ∀ d ∈ localChildren ruleDescription (encode (Rule.HasE_allExt a0 a1 a2 a3 a4)), CertCanonical d := by
  simp [ruleDescription, localShape, localChildren, dependencies, rebuild, rebuildField, fieldCode, List.range_succ, CertCanonical]

theorem rule_sound_62 (c : Nat) (heq : tag c = 62)
    (hs : localShape ruleDescription c = true)
    (hc : ∀ d ∈ localChildren ruleDescription c, CertCanonical d) : ∃ a : Rule, encode a = c := by
  simp [localShape, ruleDescription, heq, rebuild, rebuildField, fieldCode, List.range_succ] at hs
  simp [localChildren, ruleDescription, heq, dependencies, fieldCode, List.range_succ, CertCanonical] at hc
  rcases hc with ⟨⟨a0, h0⟩, ⟨a1, h1⟩, ⟨a2, h2⟩, ⟨a3, h3⟩, ⟨a4, h4⟩⟩
  refine ⟨Rule.HasE_allExt a0 a1 a2 a3 a4, ?_⟩
  simpa [h0, h1, h2, h3, h4] using hs.symm

theorem Rule_rule (c : Nat) : (∃ a : Rule, encode a = c) ↔
    localShape ruleDescription c = true ∧ ∀ d ∈ localChildren ruleDescription c, CertCanonical d := by
  constructor
  · rintro ⟨a, rfl⟩
    cases a with
    | CtxJ_ctxBase a0 => exact rule_complete_0 a0
    | CtxJ_nil  => exact rule_complete_1 
    | CtxJ_ext a0 a1 => exact rule_complete_2 a0 a1
    | FormJ_formBase a0 a1 => exact rule_complete_3 a0 a1
    | FormJ_param a0 a1 => exact rule_complete_4 a0 a1
    | FormJ_bottom a0 => exact rule_complete_5 a0
    | FormJ_all a0 a1 => exact rule_complete_6 a0 a1
    | FormJ_raw a0 => exact rule_complete_7 a0
    | FormJ_pi a0 a1 a2 => exact rule_complete_8 a0 a1 a2
    | FormJ_sigma a0 a1 a2 => exact rule_complete_9 a0 a1 a2
    | FormJ_identity a0 a1 a2 a3 => exact rule_complete_10 a0 a1 a2 a3
    | HasJ_hasBase a0 a1 a2 => exact rule_complete_11 a0 a1 a2
    | HasJ_var a0 a1 a2 a3 => exact rule_complete_12 a0 a1 a2 a3
    | HasJ_i a0 a1 => exact rule_complete_13 a0 a1
    | HasJ_k a0 a1 a2 => exact rule_complete_14 a0 a1 a2
    | HasJ_s a0 a1 a2 a3 => exact rule_complete_15 a0 a1 a2 a3
    | HasJ_finite a0 a1 a2 a3 a4 => exact rule_complete_16 a0 a1 a2 a3 a4
    | HasJ_allIntro a0 a1 a2 => exact rule_complete_17 a0 a1 a2
    | HasJ_allElim a0 a1 a2 a3 => exact rule_complete_18 a0 a1 a2 a3
    | HasJ_rawAtom a0 a1 => exact rule_complete_19 a0 a1
    | HasJ_rawApp a0 a1 a2 => exact rule_complete_20 a0 a1 a2
    | HasJ_piIntro a0 a1 a2 a3 => exact rule_complete_21 a0 a1 a2 a3
    | HasJ_piElim a0 a1 a2 a3 a4 => exact rule_complete_22 a0 a1 a2 a3 a4
    | HasJ_sigmaIntro a0 a1 a2 a3 a4 => exact rule_complete_23 a0 a1 a2 a3 a4
    | HasJ_sigmaFst a0 a1 a2 a3 => exact rule_complete_24 a0 a1 a2 a3
    | HasJ_sigmaSnd a0 a1 a2 a3 => exact rule_complete_25 a0 a1 a2 a3
    | HasJ_identityIntro a0 a1 a2 a3 a4 => exact rule_complete_26 a0 a1 a2 a3 a4
    | HasJ_proofErase a0 a1 a2 a3 a4 => exact rule_complete_27 a0 a1 a2 a3 a4
    | HasJ_j a0 a1 a2 a3 a4 a5 a6 => exact rule_complete_28 a0 a1 a2 a3 a4 a5 a6
    | HasJ_conv a0 a1 a2 a3 a4 => exact rule_complete_29 a0 a1 a2 a3 a4
    | HasJ_piExt a0 a1 a2 a3 a4 a5 => exact rule_complete_30 a0 a1 a2 a3 a4 a5
    | HasJ_allExt a0 a1 a2 a3 a4 => exact rule_complete_31 a0 a1 a2 a3 a4
    | HasJ_sigmaElim a0 a1 a2 a3 a4 a5 => exact rule_complete_32 a0 a1 a2 a3 a4 a5
    | HasJ_natInduction a0 a1 a2 a3 => exact rule_complete_33 a0 a1 a2 a3
    | CtxE_nil  => exact rule_complete_34 
    | CtxE_ext a0 a1 => exact rule_complete_35 a0 a1
    | FormE_param a0 a1 => exact rule_complete_36 a0 a1
    | FormE_bottom a0 => exact rule_complete_37 a0
    | FormE_all a0 a1 => exact rule_complete_38 a0 a1
    | FormE_raw a0 => exact rule_complete_39 a0
    | FormE_pi a0 a1 a2 => exact rule_complete_40 a0 a1 a2
    | FormE_sigma a0 a1 a2 => exact rule_complete_41 a0 a1 a2
    | FormE_identity a0 a1 a2 a3 => exact rule_complete_42 a0 a1 a2 a3
    | HasE_var a0 a1 a2 a3 => exact rule_complete_43 a0 a1 a2 a3
    | HasE_i a0 a1 => exact rule_complete_44 a0 a1
    | HasE_k a0 a1 a2 => exact rule_complete_45 a0 a1 a2
    | HasE_s a0 a1 a2 a3 => exact rule_complete_46 a0 a1 a2 a3
    | HasE_finite a0 a1 a2 a3 a4 => exact rule_complete_47 a0 a1 a2 a3 a4
    | HasE_allIntro a0 a1 a2 => exact rule_complete_48 a0 a1 a2
    | HasE_allElim a0 a1 a2 a3 => exact rule_complete_49 a0 a1 a2 a3
    | HasE_rawAtom a0 a1 => exact rule_complete_50 a0 a1
    | HasE_rawApp a0 a1 a2 => exact rule_complete_51 a0 a1 a2
    | HasE_piIntro a0 a1 a2 a3 => exact rule_complete_52 a0 a1 a2 a3
    | HasE_piElim a0 a1 a2 a3 a4 => exact rule_complete_53 a0 a1 a2 a3 a4
    | HasE_sigmaIntro a0 a1 a2 a3 a4 => exact rule_complete_54 a0 a1 a2 a3 a4
    | HasE_sigmaFst a0 a1 a2 a3 => exact rule_complete_55 a0 a1 a2 a3
    | HasE_sigmaSnd a0 a1 a2 a3 => exact rule_complete_56 a0 a1 a2 a3
    | HasE_identityIntro a0 a1 a2 a3 a4 => exact rule_complete_57 a0 a1 a2 a3 a4
    | HasE_proofErase a0 a1 a2 a3 a4 => exact rule_complete_58 a0 a1 a2 a3 a4
    | HasE_j a0 a1 a2 a3 a4 a5 a6 => exact rule_complete_59 a0 a1 a2 a3 a4 a5 a6
    | HasE_conv a0 a1 a2 a3 a4 => exact rule_complete_60 a0 a1 a2 a3 a4
    | HasE_piExt a0 a1 a2 a3 a4 a5 => exact rule_complete_61 a0 a1 a2 a3 a4 a5
    | HasE_allExt a0 a1 a2 a3 a4 => exact rule_complete_62 a0 a1 a2 a3 a4
  · rintro ⟨hs,hc⟩
    have hlt : tag c < 63 := by
      by_contra h
      simp [localShape, ruleDescription, h] at hs
    have heq : tag c = 0 ∨ tag c = 1 ∨ tag c = 2 ∨ tag c = 3 ∨ tag c = 4 ∨ tag c = 5 ∨ tag c = 6 ∨ tag c = 7 ∨ tag c = 8 ∨ tag c = 9 ∨ tag c = 10 ∨ tag c = 11 ∨ tag c = 12 ∨ tag c = 13 ∨ tag c = 14 ∨ tag c = 15 ∨ tag c = 16 ∨ tag c = 17 ∨ tag c = 18 ∨ tag c = 19 ∨ tag c = 20 ∨ tag c = 21 ∨ tag c = 22 ∨ tag c = 23 ∨ tag c = 24 ∨ tag c = 25 ∨ tag c = 26 ∨ tag c = 27 ∨ tag c = 28 ∨ tag c = 29 ∨ tag c = 30 ∨ tag c = 31 ∨ tag c = 32 ∨ tag c = 33 ∨ tag c = 34 ∨ tag c = 35 ∨ tag c = 36 ∨ tag c = 37 ∨ tag c = 38 ∨ tag c = 39 ∨ tag c = 40 ∨ tag c = 41 ∨ tag c = 42 ∨ tag c = 43 ∨ tag c = 44 ∨ tag c = 45 ∨ tag c = 46 ∨ tag c = 47 ∨ tag c = 48 ∨ tag c = 49 ∨ tag c = 50 ∨ tag c = 51 ∨ tag c = 52 ∨ tag c = 53 ∨ tag c = 54 ∨ tag c = 55 ∨ tag c = 56 ∨ tag c = 57 ∨ tag c = 58 ∨ tag c = 59 ∨ tag c = 60 ∨ tag c = 61 ∨ tag c = 62 := by
      simpa [List.range_succ, or_assoc, eq_comm] using (List.mem_range.mpr hlt)
    rcases heq with heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq | heq
    · exact rule_sound_0 c heq hs hc
    · exact rule_sound_1 c heq hs hc
    · exact rule_sound_2 c heq hs hc
    · exact rule_sound_3 c heq hs hc
    · exact rule_sound_4 c heq hs hc
    · exact rule_sound_5 c heq hs hc
    · exact rule_sound_6 c heq hs hc
    · exact rule_sound_7 c heq hs hc
    · exact rule_sound_8 c heq hs hc
    · exact rule_sound_9 c heq hs hc
    · exact rule_sound_10 c heq hs hc
    · exact rule_sound_11 c heq hs hc
    · exact rule_sound_12 c heq hs hc
    · exact rule_sound_13 c heq hs hc
    · exact rule_sound_14 c heq hs hc
    · exact rule_sound_15 c heq hs hc
    · exact rule_sound_16 c heq hs hc
    · exact rule_sound_17 c heq hs hc
    · exact rule_sound_18 c heq hs hc
    · exact rule_sound_19 c heq hs hc
    · exact rule_sound_20 c heq hs hc
    · exact rule_sound_21 c heq hs hc
    · exact rule_sound_22 c heq hs hc
    · exact rule_sound_23 c heq hs hc
    · exact rule_sound_24 c heq hs hc
    · exact rule_sound_25 c heq hs hc
    · exact rule_sound_26 c heq hs hc
    · exact rule_sound_27 c heq hs hc
    · exact rule_sound_28 c heq hs hc
    · exact rule_sound_29 c heq hs hc
    · exact rule_sound_30 c heq hs hc
    · exact rule_sound_31 c heq hs hc
    · exact rule_sound_32 c heq hs hc
    · exact rule_sound_33 c heq hs hc
    · exact rule_sound_34 c heq hs hc
    · exact rule_sound_35 c heq hs hc
    · exact rule_sound_36 c heq hs hc
    · exact rule_sound_37 c heq hs hc
    · exact rule_sound_38 c heq hs hc
    · exact rule_sound_39 c heq hs hc
    · exact rule_sound_40 c heq hs hc
    · exact rule_sound_41 c heq hs hc
    · exact rule_sound_42 c heq hs hc
    · exact rule_sound_43 c heq hs hc
    · exact rule_sound_44 c heq hs hc
    · exact rule_sound_45 c heq hs hc
    · exact rule_sound_46 c heq hs hc
    · exact rule_sound_47 c heq hs hc
    · exact rule_sound_48 c heq hs hc
    · exact rule_sound_49 c heq hs hc
    · exact rule_sound_50 c heq hs hc
    · exact rule_sound_51 c heq hs hc
    · exact rule_sound_52 c heq hs hc
    · exact rule_sound_53 c heq hs hc
    · exact rule_sound_54 c heq hs hc
    · exact rule_sound_55 c heq hs hc
    · exact rule_sound_56 c heq hs hc
    · exact rule_sound_57 c heq hs hc
    · exact rule_sound_58 c heq hs hc
    · exact rule_sound_59 c heq hs hc
    · exact rule_sound_60 c heq hs hc
    · exact rule_sound_61 c heq hs hc
    · exact rule_sound_62 c heq hs hc

end CertificateCodeValidity
