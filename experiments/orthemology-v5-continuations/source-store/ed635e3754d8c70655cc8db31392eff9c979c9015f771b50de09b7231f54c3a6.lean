import Mathlib.Data.Nat.Bitwise
import Mathlib.Tactic

/-!
# Exact unsigned LEB128 component of the recovered P02 Python codec

Source: `user-checkpoints/extracted/P02/code/prcodec.py`, `_uv` and `Reader.uv`.
Natural-number lists represent bytes; the reader rejects elements outside 0..255.
The serializer emits exactly the Python continuation byte `(n % 128) | 128`.
The reader uses the same bit mask, left shift, OR accumulator, stopping rule,
and final re-encoding check as `Reader.uv`, with a finite input list replacing
Python's mutable cursor. `uvRead` returns the unread suffix.

This file qualifies only unsigned varints. It does not verify expression,
statement, program, exception/resource, or universal-evaluation semantics.
All definitions are executable total Lean functions. No claim that a numeric
code for this implementation is primitive recursive is made here.
-/

namespace P02.Codec

/-- Every member is a byte value, as for a Python `bytes` object. -/
def Bytes (xs : List Nat) : Prop := ∀ b ∈ xs, b < 256

/-- Exact mathematical translation of Python `_uv`. -/
def uv (n : Nat) : List Nat :=
  if h : n < 128 then [n]
  else ((n % 128) ||| 128) :: uv (n / 128)
termination_by n
decreasing_by exact Nat.div_lt_self (by omega) (by omega)

/-- The high continuation bit is disjoint from the seven-bit payload. -/
theorem continuation_byte (n : Nat) : (n % 128 ||| 128) = n % 128 + 128 := by
  have h := Nat.two_pow_add_eq_or_of_lt (i := 7)
    (b := n % 128) (by have := Nat.mod_lt n (by omega : 0 < 128); simpa using this) 1
  simpa [Nat.or_comm, Nat.add_comm] using h.symm

/-- `b & 127` is precisely the low seven bits. -/
theorem payload_eq_mod (b : Nat) : (b &&& 127) = b % 128 := by
  simpa using Nat.and_two_pow_sub_one_eq_mod b 7

/-- Disjoint low accumulator and shifted payload combine by addition. -/
theorem accumulator_or {acc shift payload : Nat} (h : acc < 2 ^ shift) :
    (acc ||| (payload <<< shift)) = acc + 2 ^ shift * payload := by
  have ht := Nat.two_pow_add_eq_or_of_lt h payload
  simpa [Nat.shiftLeft_eq, Nat.mul_comm, Nat.or_comm, Nat.add_comm] using ht.symm

theorem uv_nonempty (n : Nat) : uv n ≠ [] := by
  rw [uv]
  split <;> simp

theorem uv_bytes (n : Nat) : Bytes (uv n) := by
  induction n using Nat.strong_induction_on with
  | h n ih =>
    rw [uv]
    split_ifs with hn
    · intro b hb
      have hbn : b = n := List.mem_singleton.mp hb
      omega
    · rw [continuation_byte]
      intro b hb
      rcases List.mem_cons.mp hb with hb | hb
      · subst b
        have := Nat.mod_lt n (by omega : 0 < 128)
        omega
      · exact ih (n / 128) (Nat.div_lt_self (by omega) (by omega)) b hb

/-- Result = decoded value, consumed bytes in order, unread bytes. -/
abbrev ReadResult := Nat × List Nat × List Nat

/-- Exact bitwise accumulation of `Reader.uv` before the canonicality check.
`usedRev` represents the consumed slice in reverse order. Truncation and
non-byte list elements give `none` rather than Python's `InvalidCode`. -/
def readAccum : List Nat → Nat → Nat → List Nat → Option ReadResult
  | [], _, _, _ => none
  | b :: bs, acc, shift, usedRev =>
    if b < 256 then
      let next := acc ||| ((b &&& 127) <<< shift)
      if b < 128 then some (next, (b :: usedRev).reverse, bs)
      else readAccum bs next (shift + 7) (b :: usedRev)
    else none

/-- Canonical unsigned-varint reader, returning the value and unread suffix. -/
def uvRead (bs : List Nat) : Option (Nat × List Nat) := do
  let (n, used, rest) ← readAccum bs 0 0 []
  if used = uv n then some (n, rest) else none

/-- General accumulator invariant, including the exact consumed byte slice. -/
theorem readAccum_uv (n : Nat) (suffix : List Nat) (acc shift : Nat)
    (usedRev : List Nat) (hacc : acc < 2 ^ shift) :
    readAccum (uv n ++ suffix) acc shift usedRev =
      some (acc + 2 ^ shift * n, usedRev.reverse ++ uv n, suffix) := by
  induction n using Nat.strong_induction_on generalizing acc shift usedRev with
  | h n ih =>
    rw [uv]
    split_ifs with hn
    · have hn256 : n < 256 := by omega
      have hmask : n &&& 127 = n := by rw [payload_eq_mod, Nat.mod_eq_of_lt hn]
      simp only [List.singleton_append, readAccum, hn256, ↓reduceIte, hn,
        hmask, accumulator_or hacc, List.reverse_cons]
    · let low := n % 128
      have hlow : low < 128 := Nat.mod_lt n (by omega)
      have hnpos : 0 < n := by omega
      have hd : n / 128 < n := Nat.div_lt_self hnpos (by omega)
      have hb : n % 128 ||| 128 = low + 128 := continuation_byte n
      have hb256 : low + 128 < 256 := by omega
      have hb128 : ¬ low + 128 < 128 := by omega
      have hmask : (low + 128) &&& 127 = low := by
        rw [payload_eq_mod]
        omega
      have hp : 2 ^ (shift + 7) = 2 ^ shift * 128 := by rw [pow_add]; norm_num
      have hpos : 0 < 2 ^ shift := by positivity
      have hnext : acc + 2 ^ shift * low < 2 ^ (shift + 7) := by
        rw [hp]
        nlinarith
      rw [hb]
      simp only [List.cons_append, readAccum, hb256, ↓reduceIte, hb128,
        hmask, accumulator_or hacc]
      rw [ih (n / 128) hd (acc + 2 ^ shift * low) (shift + 7) ((low + 128) :: usedRev) hnext]
      have harith : acc + 2 ^ shift * low + 2 ^ (shift + 7) * (n / 128) =
          acc + 2 ^ shift * n := by
        rw [hp]
        have hreconstruct : low + 128 * (n / 128) = n := Nat.mod_add_div n 128
        calc
          _ = acc + 2 ^ shift * (low + 128 * (n / 128)) := by ring
          _ = _ := by rw [hreconstruct]
      rw [harith]
      simp only [List.reverse_cons, List.append_assoc, List.singleton_append]

/-- Canonical varints roundtrip in any surrounding input stream. -/
theorem uvRead_append (n : Nat) (suffix : List Nat) :
    uvRead (uv n ++ suffix) = some (n, suffix) := by
  unfold uvRead
  rw [readAccum_uv n suffix 0 0 [] (by norm_num)]
  simp

@[simp] theorem uvRead_uv (n : Nat) : uvRead (uv n) = some (n, []) := by
  simpa using uvRead_append n []

/-- The exact serializer is injective. -/
theorem uv_injective : Function.Injective uv := by
  intro n m h
  have hr := congrArg uvRead h
  simpa using hr

/-- Every successful raw parse splits the original stream at the returned cursor. -/
theorem readAccum_split {bs : List Nat} {acc shift : Nat} {usedRev : List Nat}
    {n : Nat} {used rest : List Nat}
    (h : readAccum bs acc shift usedRev = some (n, used, rest)) :
    usedRev.reverse ++ bs = used ++ rest := by
  induction bs generalizing acc shift usedRev with
  | nil => simp [readAccum] at h
  | cons b bs ih =>
    simp only [readAccum] at h
    split_ifs at h with hb ht
    · cases h
      simp
    · have hr := ih h
      simpa [List.reverse_cons, List.append_assoc] using hr

/-- Exact acceptance characterization: no noncanonical varint prefix is accepted. -/
theorem uvRead_eq_some_iff (bs : List Nat) (n : Nat) (rest : List Nat) :
    uvRead bs = some (n, rest) ↔ bs = uv n ++ rest := by
  constructor
  · intro h
    cases hr : readAccum bs 0 0 [] with
    | none => simp [uvRead, hr] at h
    | some r =>
      rcases r with ⟨k, used, tail⟩
      simp only [uvRead, hr, bind, Option.some_bind] at h
      split_ifs at h with hcan
      · have heq : k = n ∧ tail = rest := by simpa using h
        rcases heq with ⟨rfl, rfl⟩
        have hs := readAccum_split hr
        simpa [hcan] using hs
  · intro h
    rw [h]
    exact uvRead_append n rest

/-- Kernel-computed vectors from the recovered Python format. -/
theorem uv_zero : uv 0 = [0] := by rw [uv]; norm_num
theorem uv_one : uv 1 = [1] := by rw [uv]; norm_num
theorem uv_127 : uv 127 = [127] := by rw [uv]; norm_num
theorem uv_128 : uv 128 = [128, 1] := by
  rw [uv]
  norm_num
  rw [uv]
  norm_num
theorem uv_16384 : uv 16384 = [128, 128, 1] := by
  rw [uv]
  norm_num
  rw [uv_128]
theorem uv_624485 : uv 624485 = [229, 142, 38] := by
  rw [uv]
  simp only [continuation_byte]
  norm_num
  rw [uv]
  simp only [continuation_byte]
  norm_num
  rw [uv]
  norm_num
theorem uvRead_reject_overlong_zero : uvRead [128, 0] = none := by norm_num [uvRead, readAccum, payload_eq_mod, uv_zero, uv_one]
theorem uvRead_reject_overlong_one : uvRead [129, 0] = none := by norm_num [uvRead, readAccum, payload_eq_mod, uv_zero, uv_one]
theorem uvRead_reject_truncated : uvRead [128] = none := by decide
theorem uvRead_reject_nonbyte : uvRead [256, 0] = none := by decide

end P02.Codec
