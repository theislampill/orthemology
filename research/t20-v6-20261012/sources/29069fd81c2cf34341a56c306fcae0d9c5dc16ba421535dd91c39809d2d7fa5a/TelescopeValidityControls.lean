import TelescopeDecoderBridge
namespace TelescopeCodeValidity
open Encodable ExactSyntaxValidity OrthemologyV2 P01D P01AC
set_option maxRecDepth 8192
set_option maxHeartbeats 1000000

@[simp] theorem validTel_nil : validTel 0 = true := by
  rw [validTel, evaluate]
  rfl

/-- Raw payload equation exposes independent head and recursive-tail checks. -/
theorem validTel_cons_code (h t : Nat) :
    validTel (Nat.pair h t + 1) = (valid 3 h && validTel t) := by
  have ht : t < Nat.pair h t + 1 := Nat.lt_succ_of_le (Nat.right_le_pair h t)
  rw [validTel, evaluate]
  simp [telShape, telChildren, telHead, telTail, ht, validTel]

theorem reject_bad_head (h t : Nat) (hh : valid 3 h = false) :
    validTel (Nat.pair h t + 1) = false := by
  rw [validTel_cons_code, hh]
  rfl

theorem reject_bad_tail (h t : Nat) (ht : validTel t = false) :
    validTel (Nat.pair h t + 1) = false := by
  rw [validTel_cons_code, ht, Bool.and_false]

theorem reject_zero_head (t : Nat) : validTel (Nat.pair 0 t + 1) = false := by
  apply reject_bad_head
  rw [valid, evaluate]
  rfl

/-- List code one is a cons whose head is not a canonical Ty code. -/
@[simp] theorem rejectTelOne : validTel 1 = false := reject_zero_head 0

theorem reject_tail_payload (a : Ty) :
    validTel (Nat.pair (encode a) 1 + 1) = false :=
  reject_bad_tail _ _ rejectTelOne

theorem reject_nested_head (a : Ty) (t : Nat) :
    validTel (Nat.pair (encode a) (Nat.pair 0 t + 1) + 1) = false :=
  reject_bad_tail _ _ (reject_zero_head t)

example (a : Ty) (xs : Tel) : validTel (encode (a :: xs)) = true := validTel_encode _
example : validTel (encode ([] : Tel)) = true := validTel_encode _
example (xs : Tel) : normalizeTel (encode xs) = some (encode xs) := by
  simp [normalizeTel, validTel_encode]

-- Finite runtime controls accompany the all-input image theorem.
#eval [validTel (encode ([] : Tel)), validTel (encode ([Ty.raw] : Tel)),
  validTel (encode ([Ty.param 0, Ty.bottom] : Tel)),
  validTel (encode ([Ty.all .raw, Ty.pi .raw .bottom] : Tel)),
  validTel (encode ([Ty.sigma .raw .raw] : Tel)),
  validTel (encode ([Ty.identity .raw (.var 0) (.atom .one)] : Tel))]
#eval [validTel 1, validTel (Nat.pair (encode Ty.raw) 1 + 1),
  validTel (Nat.pair 0 (encode ([Ty.raw] : Tel)) + 1),
  validTel (Nat.pair (encode Ty.raw) (Nat.pair 0 0 + 1) + 1)]
end TelescopeCodeValidity
