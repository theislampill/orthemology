import CanonicalDecoderBridge

namespace TelescopeCodeValidity
open Encodable ExactSyntaxValidity OrthemologyV2 P01D P01AC
set_option maxRecDepth 8192
set_option maxHeartbeats 1000000

/-- Actual list encoding: zero is nil; successor is a paired head and tail. -/
def telHead (c : Nat) : Nat := (c - 1).unpair.1
def telTail (c : Nat) : Nat := (c - 1).unpair.2

def telShape (b : Nat × Nat) : Bool :=
  if b.2 = 0 then true else valid 3 (telHead b.2)
def telChildren (b : Nat × Nat) : List (Nat × Nat) :=
  if b.2 = 0 then [] else [(0, telTail b.2)]
def validTel (c : Nat) : Bool := evaluate telShape telChildren (0, c)

def TelCanonical (b : Nat × Nat) : Prop := ∃ xs : List Ty, encode xs = b.2

theorem primrec_telHead : Primrec telHead :=
  Primrec.fst.comp (Primrec.unpair.comp Primrec.pred)
theorem primrec_telTail : Primrec telTail :=
  Primrec.snd.comp (Primrec.unpair.comp Primrec.pred)
theorem primrec_telShape : Primrec telShape :=
  Primrec.ite (Primrec.eq.comp Primrec.snd (Primrec.const 0))
    (Primrec.const true)
    (primrec_valid.comp (Primrec.const 3) (primrec_telHead.comp Primrec.snd))
theorem primrec_telChildren : Primrec telChildren :=
  Primrec.ite (Primrec.eq.comp Primrec.snd (Primrec.const 0))
    (Primrec.const [])
    (Primrec.list_cons.comp
      (Primrec.pair (Primrec.const 0) (primrec_telTail.comp Primrec.snd))
      (Primrec.const []))
theorem primrec_validTel : Primrec validTel :=
  (primrec_evaluate primrec_telShape primrec_telChildren).comp
    (Primrec.pair (Primrec.const 0) Primrec.id)

@[simp] theorem telHead_cons (a : Ty) (xs : List Ty) :
    telHead (encode (a :: xs)) = encode a := by
  simp [telHead]
@[simp] theorem telTail_cons (a : Ty) (xs : List Ty) :
    telTail (encode (a :: xs)) = encode xs := by
  simp [telTail]

theorem tel_rule (b : Nat × Nat) : TelCanonical b ↔
    telShape b = true ∧ ∀ d ∈ telChildren b, TelCanonical d := by
  rcases b with ⟨s, c⟩
  cases c with
  | zero =>
    simp only [TelCanonical, telShape, telChildren, ↓reduceIte, List.not_mem_nil,
      IsEmpty.forall_iff, implies_true, and_true]
    exact iff_true_intro ⟨[], rfl⟩
  | succ c =>
    simp only [telShape, telChildren, Nat.succ_ne_zero, ↓reduceIte,
      List.mem_singleton, forall_eq, TelCanonical, telHead, telTail,
      Nat.succ_sub_one, valid_ty]
    constructor
    · rintro ⟨xs, hx⟩
      cases xs with
      | nil => simp at hx
      | cons a xs =>
        have hp : Nat.pair (encode a) (encode xs) = c := by simpa using hx
        have hu := congrArg Nat.unpair hp
        simp only [Nat.unpair_pair, Prod.mk.injEq] at hu
        exact ⟨⟨a, congrArg Prod.fst hu⟩, ⟨xs, congrArg Prod.snd hu⟩⟩
    · rintro ⟨⟨a, ha⟩, ⟨xs, hx⟩⟩
      refine ⟨a :: xs, ?_⟩
      simp [ha, hx, Nat.pair_unpair]

theorem tel_bounds (b : Nat × Nat) (_hb : telShape b = true) :
    ∀ d ∈ telChildren b, d.2 < b.2 := by
  rcases b with ⟨s, c⟩
  cases c with
  | zero => simp [telChildren]
  | succ c =>
    simp only [telChildren, Nat.succ_ne_zero, ↓reduceIte, List.mem_singleton, forall_eq]
    exact Nat.lt_succ_of_le (Nat.unpair_right_le c)

/-- Exact canonical image of the existing `Encodable (List P01AC.Ty)` instance. -/
theorem validTel_exact (c : Nat) :
    validTel c = true ↔ ∃ xs : List Ty, encode xs = c :=
  evaluate_exact tel_rule tel_bounds (0, c)

theorem validTel_encode (xs : Tel) : validTel (encode xs) = true :=
  (validTel_exact _).mpr ⟨xs, rfl⟩

end TelescopeCodeValidity
