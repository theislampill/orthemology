import CodecVarint

/-!
# Sentinel-prefixed, big-endian base-256 numeric indices

Source: recovered P02 `prcodec.py`, `encode` and the byte-conversion/sentinel
part of `decode`. `encodeNumeric payload` is exactly the natural number whose
big-endian bytes are `0x01` followed by the supplied bytes. `decodeNumeric`
recovers the minimal big-endian expansion and checks its first byte is `0x01`.
Zero and non-sentinel-leading integers are rejected.

The complete program parser, magic bytes, AST serializer, arity checks, and
universal evaluator are deliberately not part of this theorem. The public
roundtrip assumes every payload member is <256, exactly Python's bytes domain.
The algorithms here are total executable Lean definitions; no `Primrec` or
`Computable` theorem about their numeric representations is asserted.
-/

namespace P02.Codec

/-- Big-endian accumulation, matching `int.from_bytes(_, 'big')`. -/
def fromBytes (bs : List Nat) : Nat := bs.foldl (fun acc b => 256 * acc + b) 0

/-- A leading `1` sentinel preserves even zero-leading or empty payloads. -/
def encodeNumeric (bs : List Nat) : Nat := fromBytes (1 :: bs)

/-- Minimal big-endian expansion. The expansion of zero is empty, matching
`index.to_bytes((index.bit_length()+7)//8, 'big')` before the explicit zero guard. -/
def toBytes (n : Nat) : List Nat :=
  if n = 0 then [] else toBytes (n / 256) ++ [n % 256]
termination_by n
decreasing_by exact Nat.div_lt_self (by omega) (by omega)

/-- Decode the sentinel-only numeric envelope, before the program-byte parser. -/
def decodeNumeric (n : Nat) : Option (List Nat) :=
  if n = 0 then none
  else match toBytes n with
    | 1 :: bs => some bs
    | _ => none

@[simp] theorem fromBytes_nil : fromBytes [] = 0 := rfl

@[simp] theorem fromBytes_append_byte (bs : List Nat) (b : Nat) :
    fromBytes (bs ++ [b]) = 256 * fromBytes bs + b := by
  simp [fromBytes, List.foldl_append]

@[simp] theorem encodeNumeric_nil : encodeNumeric [] = 1 := rfl

@[simp] theorem encodeNumeric_append_byte (bs : List Nat) (b : Nat) :
    encodeNumeric (bs ++ [b]) = 256 * encodeNumeric bs + b := by
  change fromBytes ((1 :: bs) ++ [b]) = _
  exact fromBytes_append_byte (1 :: bs) b

theorem encodeNumeric_pos (bs : List Nat) : 0 < encodeNumeric bs := by
  induction bs using List.reverseRecOn with
  | nil => simp
  | append_singleton bs b ih => rw [encodeNumeric_append_byte]; omega

@[simp] theorem toBytes_zero : toBytes 0 = [] := by rw [toBytes, if_pos rfl]

@[simp] theorem toBytes_one : toBytes 1 = [1] := by
  rw [toBytes, if_neg (by omega)]
  norm_num

/-- Long division peels the final byte of any nonzero big-endian prefix. -/
theorem toBytes_step (n b : Nat) (hn : 0 < n) (hb : b < 256) :
    toBytes (256 * n + b) = toBytes n ++ [b] := by
  have hpos : 256 * n + b ≠ 0 := by omega
  have hd : (256 * n + b) / 256 = n := by omega
  have hm : (256 * n + b) % 256 = b := by omega
  rw [toBytes, if_neg hpos, hd, hm]

/-- The minimal expansion of the numeric encoding is exactly sentinel + payload. -/
theorem toBytes_encodeNumeric (bs : List Nat) (hbs : Bytes bs) :
    toBytes (encodeNumeric bs) = 1 :: bs := by
  induction bs using List.reverseRecOn with
  | nil => simp
  | append_singleton bs b ih =>
    have hb : b < 256 := hbs b (by simp)
    have hprefix : Bytes bs := fun x hx => hbs x (by simp [hx])
    rw [encodeNumeric_append_byte, toBytes_step _ _ (encodeNumeric_pos bs) hb, ih hprefix]
    rfl

/-- Sentinel-prefixed numeric byte lists roundtrip exactly. -/
@[simp] theorem decodeNumeric_encodeNumeric (bs : List Nat) (hbs : Bytes bs) :
    decodeNumeric (encodeNumeric bs) = some bs := by
  unfold decodeNumeric
  rw [if_neg (Nat.ne_of_gt (encodeNumeric_pos bs)), toBytes_encodeNumeric bs hbs]

/-- The sentinel numeric encoding is injective on genuine byte lists. -/
theorem encodeNumeric_injective {xs ys : List Nat} (hx : Bytes xs) (hy : Bytes ys)
    (h : encodeNumeric xs = encodeNumeric ys) : xs = ys := by
  have hh := congrArg decodeNumeric h
  simpa [decodeNumeric_encodeNumeric xs hx, decodeNumeric_encodeNumeric ys hy] using hh

/-- Long division always produces genuine bytes. -/
theorem toBytes_bytes (n : Nat) : Bytes (toBytes n) := by
  induction n using Nat.strong_induction_on with
  | h n ih =>
    rw [toBytes]
    split_ifs with hn
    · simp [Bytes]
    · intro b hb
      rcases List.mem_append.mp hb with hb | hb
      · exact ih (n / 256) (Nat.div_lt_self (by omega) (by omega)) b hb
      · have hbn := List.mem_singleton.mp hb
        subst b
        exact Nat.mod_lt n (by omega)

/-- Numeric conversion is inverse to its minimal-byte expansion. -/
@[simp] theorem fromBytes_toBytes (n : Nat) : fromBytes (toBytes n) = n := by
  induction n using Nat.strong_induction_on with
  | h n ih =>
    rw [toBytes]
    split_ifs with hn
    · subst n
      rfl
    · rw [fromBytes_append_byte,
        ih (n / 256) (Nat.div_lt_self (by omega) (by omega))]
      exact Nat.div_add_mod n 256

/-- Successful decoding returns precisely the original integer and valid bytes. -/
theorem decodeNumeric_sound {n : Nat} {bs : List Nat}
    (h : decodeNumeric n = some bs) : Bytes bs ∧ encodeNumeric bs = n := by
  unfold decodeNumeric at h
  split_ifs at h with hn
  split at h
  next tail ht =>
    cases h
    constructor
    · have hb := toBytes_bytes n
      rw [ht] at hb
      intro b hmem
      exact hb b (by simp [hmem])
    · have hv := fromBytes_toBytes n
      rw [ht] at hv
      exact hv
  next => simp at h

/-- Exact range characterization for the sentinel envelope. -/
theorem decodeNumeric_eq_some_iff (n : Nat) (bs : List Nat) :
    decodeNumeric n = some bs ↔ Bytes bs ∧ encodeNumeric bs = n := by
  constructor
  · exact decodeNumeric_sound
  · rintro ⟨hbs, rfl⟩
    exact decodeNumeric_encodeNumeric bs hbs

/-- The complete numeric envelope is reversible on encoded varints. -/
theorem numeric_uv_roundtrip (n : Nat) :
    (decodeNumeric (encodeNumeric (uv n))).bind uvRead = some (n, []) := by
  rw [decodeNumeric_encodeNumeric (uv n) (uv_bytes n), Option.some_bind, uvRead_uv]

/-- Natural-number lists outside the byte domain are intentionally excluded. -/
example : encodeNumeric [0, 256] = encodeNumeric [1, 0] := by decide

/-- Kernel-computed Python-compatible envelope vectors. -/
example : encodeNumeric [] = 1 := rfl
example : encodeNumeric [0] = 256 := by decide
example : encodeNumeric [255] = 511 := by decide
example : encodeNumeric [0, 255] = 65791 := by decide
example : decodeNumeric 0 = none := by decide
example : decodeNumeric 2 = none := by
  have ht : toBytes 2 = [2] := by rw [toBytes]; norm_num
  simp [decodeNumeric, ht]
example : decodeNumeric 256 = some [0] := by
  exact decodeNumeric_encodeNumeric [0] (by simp [Bytes])

end P02.Codec
