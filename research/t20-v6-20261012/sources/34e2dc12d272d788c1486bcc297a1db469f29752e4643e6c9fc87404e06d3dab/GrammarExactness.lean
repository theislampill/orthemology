import CoreGrammar
namespace ExactSyntaxValidity
open Encodable SourceFamilyComputability CodedScope OrthemologyV2 P01D P01AC
set_option maxRecDepth 8192
set_option maxHeartbeats 16000000

theorem term_rule (c : Nat) : (∃ a : Term, encode a = c) ↔
    termShape c = true ∧ ∀ d ∈ termChildren c, Canonical d := by
  constructor
  · rintro ⟨a, rfl⟩
    cases a <;> simp [termShape, termChildren, Canonical]
  · rintro ⟨hs, hc⟩
    unfold termShape at hs
    split_ifs at hs with hsmall happ
    · have he := of_decide_eq_true hs
      have hcases : tag c = 0 ∨ tag c = 1 ∨ tag c = 2 ∨ tag c = 3 ∨ tag c = 4 := by omega
      rcases hcases with h | h | h | h | h
      · exact ⟨.i, by simpa [h] using he.symm⟩
      · exact ⟨.k, by simpa [h] using he.symm⟩
      · exact ⟨.s, by simpa [h] using he.symm⟩
      · exact ⟨.zero, by simpa [h] using he.symm⟩
      · exact ⟨.one, by simpa [h] using he.symm⟩
    · have he := of_decide_eq_true hs
      have hc' : (∃ p : Term, encode p = arg1 c) ∧ (∃ q : Term, encode q = arg2 c) := by
        simpa [termChildren, happ, Canonical] using hc
      rcases hc' with ⟨⟨p, hp⟩, ⟨q, hq⟩⟩
      exact ⟨.app p q, by simpa [hp, hq] using he.symm⟩

theorem type_rule (c : Nat) : (∃ a : TypeCode, encode a = c) ↔
    typeShape c = true ∧ ∀ d ∈ typeChildren c, Canonical d := by
  constructor
  · rintro ⟨a, rfl⟩
    cases a <;> simp [typeShape, typeChildren, Canonical]
  · rintro ⟨hs, hc⟩
    unfold typeShape at hs
    split_ifs at hs with h0 h1 h2 h3
    · exact ⟨.var (rest (arg1 c)), by simpa using (of_decide_eq_true hs).symm⟩
    · have hc' : (∃ a : TypeCode, encode a = arg1 c) ∧ (∃ b : TypeCode, encode b = arg2 c) := by
        simpa [typeChildren, h1, Canonical] using hc
      rcases hc' with ⟨⟨a, ha⟩, ⟨b, hb⟩⟩
      exact ⟨.arrow a b, by simpa [ha, hb] using (of_decide_eq_true hs).symm⟩
    · have hc' : ∃ a : TypeCode, encode a = arg1 c := by
        simpa [typeChildren, h1, h2, Canonical] using hc
      rcases hc' with ⟨a, ha⟩
      exact ⟨.all a, by simpa [ha] using (of_decide_eq_true hs).symm⟩
    · exact ⟨.bottom, by simpa using (of_decide_eq_true hs).symm⟩

theorem poly_rule (c : Nat) : (∃ a : Poly, encode a = c) ↔
    polyShape c = true ∧ ∀ d ∈ polyChildren c, Canonical d := by
  constructor
  · rintro ⟨a, rfl⟩
    cases a <;> simp [polyShape, polyChildren, Canonical]
  · rintro ⟨hs, hc⟩
    unfold polyShape at hs
    split_ifs at hs with h0 h1 h2
    · exact ⟨.var (rest (arg1 c)), by simpa using (of_decide_eq_true hs).symm⟩
    · have hc' : ∃ a : Term, encode a = rest (arg1 c) := by
        simpa [polyChildren, h1, Canonical] using hc
      rcases hc' with ⟨a, ha⟩
      exact ⟨.atom a, by simpa [ha] using (of_decide_eq_true hs).symm⟩
    · have hc' : (∃ a : Poly, encode a = arg1 c) ∧ (∃ b : Poly, encode b = arg2 c) := by
        simpa [polyChildren, h1, h2, Canonical] using hc
      rcases hc' with ⟨⟨a, ha⟩, ⟨b, hb⟩⟩
      exact ⟨.app a b, by simpa [ha, hb] using (of_decide_eq_true hs).symm⟩

theorem ty_rule (c : Nat) : (∃ a : Ty, encode a = c) ↔
    tyShape c = true ∧ ∀ d ∈ tyChildren c, Canonical d := by
  constructor
  · rintro ⟨a, rfl⟩
    cases a <;> simp [tyShape, tyChildren, Canonical]
  · rintro ⟨hs, hc⟩
    unfold tyShape at hs
    split_ifs at hs with h0 h1 h2 h3 h4 h5 h6
    · exact ⟨.param (rest (arg1 c)), by simpa using (of_decide_eq_true hs).symm⟩
    · exact ⟨.bottom, by simpa using (of_decide_eq_true hs).symm⟩
    · have hc' : ∃ a : Ty, encode a = arg1 c := by
        simpa [tyChildren, h2, Canonical] using hc
      rcases hc' with ⟨a, ha⟩
      exact ⟨.all a, by simpa [ha] using (of_decide_eq_true hs).symm⟩
    · exact ⟨.raw, by simpa using (of_decide_eq_true hs).symm⟩
    · have hc' : (∃ a : Ty, encode a = arg1 c) ∧ (∃ b : Ty, encode b = arg2 c) := by
        simpa [tyChildren, h2, h4, Canonical] using hc
      rcases hc' with ⟨⟨a, ha⟩, ⟨b, hb⟩⟩
      exact ⟨.pi a b, by simpa [ha, hb] using (of_decide_eq_true hs).symm⟩
    · have hc' : (∃ a : Ty, encode a = arg1 c) ∧ (∃ b : Ty, encode b = arg2 c) := by
        simpa [tyChildren, h2, h5, Canonical] using hc
      rcases hc' with ⟨⟨a, ha⟩, ⟨b, hb⟩⟩
      exact ⟨.sigma a b, by simpa [ha, hb] using (of_decide_eq_true hs).symm⟩
    · have hc' : (∃ a : Ty, encode a = arg1 c) ∧
          (∃ p : Poly, encode p = rest (arg2 c)) ∧ (∃ q : Poly, encode q = rest (arg3 c)) := by
        simpa [tyChildren, h2, h4, h5, h6, Canonical] using hc
      rcases hc' with ⟨⟨a, ha⟩, ⟨p, hp⟩, ⟨q, hq⟩⟩
      exact ⟨.identity a p q, by simpa [ha, hp, hq] using (of_decide_eq_true hs).symm⟩

theorem canonical_rule (b : Nat × Nat) :
    Canonical b ↔ shape b = true ∧ ∀ d ∈ children b, Canonical d := by
  by_cases h0 : b.1 = 0
  · simpa [Canonical, shape, children, h0] using term_rule b.2
  by_cases h1 : b.1 = 1
  · simpa [Canonical, shape, children, h0, h1] using type_rule b.2
  by_cases h2 : b.1 = 2
  · simpa [Canonical, shape, children, h0, h1, h2] using poly_rule b.2
  by_cases h3 : b.1 = 3
  · simpa [Canonical, shape, children, h0, h1, h2, h3] using ty_rule b.2
  · simp [Canonical, shape, children, h0, h1, h2, h3]

end ExactSyntaxValidity
