import GrammarExactness
namespace ExactSyntaxValidity
open Encodable SourceFamilyComputability CodedScope OrthemologyV2 P01D P01AC
set_option maxRecDepth 8192
set_option maxHeartbeats 16000000

@[simp] theorem unary_lt (t a : Nat) : a < unary t a :=
  lt_of_lt_of_le (left_lt_node _ _) (right_le_node _ _)
@[simp] theorem binary_left_lt (t a b : Nat) : a < binary t a b :=
  lt_of_lt_of_le (left_lt_node _ _) (right_le_node _ _)
@[simp] theorem binary_right_lt (t a b : Nat) : b < binary t a b :=
  lt_of_lt_of_le (left_lt_node _ _) (le_trans (right_le_node _ _) (right_le_node _ _))
@[simp] theorem ternary_first_lt (t a b d : Nat) : a < ternary t a b d :=
  lt_of_lt_of_le (left_lt_node _ _) (right_le_node _ _)
@[simp] theorem ternary_second_lt (t a b d : Nat) : b < ternary t a b d :=
  lt_of_lt_of_le (left_lt_node _ _) (le_trans (right_le_node _ _) (right_le_node _ _))
@[simp] theorem ternary_third_lt (t a b d : Nat) : d < ternary t a b d :=
  lt_of_lt_of_le (left_lt_node _ _)
    (le_trans (right_le_node _ _) (le_trans (right_le_node _ _) (right_le_node _ _)))
theorem le_leaf (n : Nat) : n ≤ leaf n := Nat.right_le_pair _ _
@[simp] theorem unary_external_lt (t a : Nat) : a < unary t (leaf a) :=
  lt_of_le_of_lt (le_leaf a) (unary_lt t (leaf a))
@[simp] theorem ternary_second_external_lt (t a b d : Nat) : b < ternary t a (leaf b) d :=
  lt_of_le_of_lt (le_leaf b) (ternary_second_lt t a (leaf b) d)
@[simp] theorem ternary_third_external_lt (t a b d : Nat) : d < ternary t a b (leaf d) :=
  lt_of_le_of_lt (le_leaf d) (ternary_third_lt t a b (leaf d))

theorem canonical_bounds (b : Nat × Nat) (hb : Canonical b) :
    ∀ d ∈ children b, d.2 < b.2 := by
  obtain ⟨s, c⟩ := b
  by_cases h0 : s = 0
  · subst s
    obtain ⟨a, rfl⟩ := (show ∃ a : Term, encode a = c by simpa [Canonical] using hb)
    cases a <;> simp [children, termChildren]
  by_cases h1 : s = 1
  · subst s
    obtain ⟨a, rfl⟩ := (show ∃ a : TypeCode, encode a = c by simpa [Canonical] using hb)
    cases a <;> simp [children, typeChildren]
  by_cases h2 : s = 2
  · subst s
    obtain ⟨a, rfl⟩ := (show ∃ a : Poly, encode a = c by simpa [Canonical] using hb)
    cases a <;> simp [children, polyChildren]
  by_cases h3 : s = 3
  · subst s
    obtain ⟨a, rfl⟩ := (show ∃ a : Ty, encode a = c by simpa [Canonical] using hb)
    cases a <;> simp [children, tyChildren]
  · simp [Canonical, h0, h1, h2, h3] at hb

/-- Only genuine objects need satisfy dependency bounds. On invalid inputs the
    total evaluator itself checks every bound, so oversized children cannot be skipped. -/
theorem evaluate_exact_of_image {shape : Nat × Nat → Bool}
    {children : Nat × Nat → List (Nat × Nat)} {P : Nat × Nat → Prop}
    (rule : ∀ b, P b ↔ shape b = true ∧ ∀ d ∈ children b, P d)
    (bounds : ∀ b, P b → ∀ d ∈ children b, d.2 < b.2)
    (b : Nat × Nat) : evaluate shape children b = true ↔ P b := by
  induction h : b.2 using Nat.strong_induction_on generalizing b with
  | h n ih =>
    constructor
    · intro he
      rw [evaluate] at he
      simp only [Bool.and_eq_true] at he
      obtain ⟨hs, hc⟩ := he
      apply (rule b).mpr
      refine ⟨hs, ?_⟩
      intro d hd
      have hr := List.all_eq_true.mp hc d hd
      split_ifs at hr with hlt
      exact (ih d.2 (by omega) d rfl).mp hr
    · intro hp
      obtain ⟨hs, hc⟩ := (rule b).mp hp
      rw [evaluate]
      simp only [Bool.and_eq_true]
      refine ⟨hs, List.all_eq_true.mpr ?_⟩
      intro d hd
      have hlt := bounds b hp d hd
      simp only [hlt, ↓reduceDIte]
      exact (ih d.2 (by omega) d rfl).mpr (hc d hd)

theorem valid_exact (s c : Nat) : valid s c = true ↔ Canonical (s, c) :=
  evaluate_exact_of_image canonical_rule canonical_bounds (s, c)

theorem valid_term (c : Nat) : valid 0 c = true ↔ ∃ a : Term, encode a = c := by
  simpa [Canonical] using valid_exact 0 c
theorem valid_typeCode (c : Nat) : valid 1 c = true ↔ ∃ a : TypeCode, encode a = c := by
  simpa [Canonical] using valid_exact 1 c
theorem valid_poly (c : Nat) : valid 2 c = true ↔ ∃ a : Poly, encode a = c := by
  simpa [Canonical] using valid_exact 2 c
theorem valid_ty (c : Nat) : valid 3 c = true ↔ ∃ a : Ty, encode a = c := by
  simpa [Canonical] using valid_exact 3 c

end ExactSyntaxValidity
